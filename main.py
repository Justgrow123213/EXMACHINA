"""
@Author: obstacle
@Time: 20/01/25 11:29
@Description:  
"""
import time
import uvicorn
import click
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from logs import logger_factory
from client.twitter.twitter_client import TwikitClient
from client.twitter.mock_client import MockTwikitClient
from client.openai.openai_client import OpenAIClient, OpenAIConfig
from constant import VA
from logs_uvicore import get_uvicorn_log_config
from api.twitter import router as twitter_router
from conf.agent_config import DEFAULT_AGENT
from agent.scheduler import AgentScheduler
from models.scheduler import ScheduleConfig, TimeUnit
from models.twitter import Tweet, TweetVariant, LogEntry
from typing import List, Optional
import asyncio
import json
from datetime import datetime, timedelta

lgr = logger_factory.default

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Default scheduler config
DEFAULT_SCHEDULE = ScheduleConfig()

# Глобальные переменные для хранения состояния
scheduler = None
schedule_config = ScheduleConfig()
is_test_mode = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    lgr.info('Application started')
    
    # Initialize Twitter client based on mode
    global is_test_mode
    is_test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
    
    if is_test_mode:
        twitter_client = MockTwikitClient()
        lgr.info('Initialized mock Twitter client for testing')
    else:
        twitter_client = TwikitClient()
        lgr.info('Initialized real Twitter client')
        
    app.state.twitter_client = twitter_client
    
    # Initialize OpenAI client with agent personality
    openai_config = OpenAIConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4-turbo-preview",
        temperature=0.7,
        max_tokens=150
    )
    app.state.openai_client = OpenAIClient(openai_config, DEFAULT_AGENT)
    lgr.info('Init OpenAI client with agent personality successfully in lifespan')
    
    # Store agent personality for reference
    app.state.agent = DEFAULT_AGENT
    lgr.info(f'Initialized AI agent personality: {DEFAULT_AGENT.name}')
    
    # Initialize and start scheduler with default config
    global scheduler
    scheduler = AgentScheduler(
        twitter_client, 
        app.state.openai_client, 
        DEFAULT_AGENT,
        DEFAULT_SCHEDULE
    )
    app.state.scheduler = scheduler
    
    # Start scheduler in background task
    asyncio.create_task(scheduler.run_schedule())
    lgr.info('Started agent scheduler')

    yield
    
    # Cleanup
    if scheduler and scheduler.is_running:
        await scheduler.stop()
    print('clean up')

app = FastAPI(
    title="PuTi API",
    description="Twitter automation with GPT-4",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(twitter_router)

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """Render control panel"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/health')
async def health_check():
    return {"status": "healthy"}

@app.get('/agent/info')
async def get_agent_info(request: Request):
    """Get information about the current AI agent personality"""
    agent = request.app.state.agent
    return {
        "name": agent.name,
        "bio": agent.bio,
        "traits": agent.traits,
        "interests": agent.interests,
        "tone": agent.tone,
        "uses_emoji": agent.emoji_style,
        "uses_hashtags": agent.hashtag_style
    }

@app.get('/agent/status')
async def get_agent_status():
    """Get current status of the agent scheduler"""
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
    return {
        "is_running": scheduler.is_running,
        "tweet_count_today": scheduler.tweet_count_today,
        "last_tweet_time": scheduler.last_tweet_time.isoformat() if scheduler.last_tweet_time else None
    }

@app.get('/agent/schedule/config')
async def get_schedule_config():
    """Get current scheduler configuration"""
    return {
        "tweet_interval": schedule_config.tweet_interval,
        "tweet_interval_unit": schedule_config.tweet_interval_unit,
        "mention_check_interval": schedule_config.mention_check_interval,
        "mention_check_unit": schedule_config.mention_check_unit,
        "active_hours_start": schedule_config.active_hours_start,
        "active_hours_end": schedule_config.active_hours_end,
        "max_tweets_per_day": schedule_config.max_tweets_per_day,
        "available_units": [unit.value for unit in TimeUnit]
    }

@app.post('/agent/schedule/config')
async def update_schedule_config(config: ScheduleConfig):
    """Update scheduler configuration"""
    global schedule_config
    schedule_config = config
    if scheduler:
        scheduler.config = config
        if scheduler.is_running:
            # Перезапускаем планировщик с новыми настройками
            await scheduler.stop()
            await scheduler.start()
    return {"status": "success"}

@app.post('/agent/scheduler/start')
async def start_scheduler():
    """Start the agent scheduler"""
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
    if not scheduler.is_running:
        await scheduler.start()
    return {"status": "success"}

@app.post('/agent/scheduler/stop')
async def stop_scheduler():
    """Stop the agent scheduler"""
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
    if scheduler.is_running:
        await scheduler.stop()
    return {"status": "success"}

@app.get('/api/twitter/generate_tweet_variants')
async def generate_tweet_variants(topic: Optional[str] = None):
    """Generate multiple tweet variants for a given topic"""
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
        
    try:
        variants = []
        for _ in range(3):  # Генерируем 3 варианта
            tweet = await scheduler.openai.generate_tweet(topic=topic)
            variants.append({
                'content': tweet,
                'tone': scheduler.personality.tone,
                'topic': topic or 'random'
            })
        return {'variants': variants}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/twitter/history')
async def get_tweet_history(
    filter: str = Query('all', enum=['all', 'scheduled', 'manual', 'replies']),
    sort: str = Query('newest', enum=['newest', 'oldest', 'popular']),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50)
):
    """Get paginated tweet history with filtering and sorting"""
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
        
    try:
        # Получаем историю из Twitter API
        tweets = await scheduler.twitter.get_user_tweets(
            limit=page_size,
            offset=(page - 1) * page_size
        )
        
        # Фильтруем твиты
        if filter != 'all':
            tweets = [t for t in tweets if t.activity_type == filter]
            
        # Сортируем твиты
        if sort == 'newest':
            tweets.sort(key=lambda x: x.created_at, reverse=True)
        elif sort == 'oldest':
            tweets.sort(key=lambda x: x.created_at)
        elif sort == 'popular':
            tweets.sort(key=lambda x: (x.likes + x.retweets + x.replies), reverse=True)
            
        return {
            'tweets': tweets,
            'total': len(tweets),
            'page': page,
            'page_size': page_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/agent/logs')
async def get_logs(
    since_id: int = Query(0, ge=0),
    level: str = Query('all', enum=['all', 'info', 'warning', 'error'])
):
    """Get agent logs since last ID with optional filtering by level"""
    try:
        # Получаем логи из файла
        logs = []
        with open('logs/agent.log', 'r') as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    if log_entry['id'] > since_id:
                        if level == 'all' or log_entry['level'].lower() == level:
                            logs.append(log_entry)
                except json.JSONDecodeError:
                    continue
                    
        # Сортируем по времени и ID
        logs.sort(key=lambda x: (x['timestamp'], x['id']))
        
        return {'logs': logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/agent/logs/clear')
async def clear_logs():
    """Clear all agent logs"""
    try:
        # Очищаем файл логов
        with open('logs/agent.log', 'w') as f:
            f.write('')
        return {'status': 'success'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/agent/mode')
async def get_agent_mode():
    """Get current agent mode (test/production)"""
    return {
        "is_test_mode": is_test_mode,
        "mode": "test" if is_test_mode else "production"
    }

@app.post('/agent/mode')
async def set_agent_mode(test_mode: bool):
    """Switch agent mode between test and production"""
    global is_test_mode, scheduler
    
    if is_test_mode == test_mode:
        return {"status": "unchanged"}
        
    # Stop current scheduler
    if scheduler and scheduler.is_running:
        await scheduler.stop()
        
    # Switch mode
    is_test_mode = test_mode
    
    # Reinitialize client
    if is_test_mode:
        twitter_client = MockTwikitClient()
        lgr.info('Switched to mock Twitter client')
    else:
        twitter_client = TwikitClient()
        lgr.info('Switched to real Twitter client')
        
    # Reinitialize scheduler
    scheduler = AgentScheduler(
        twitter_client,
        app.state.openai_client,
        DEFAULT_AGENT,
        schedule_config
    )
    
    return {"status": "success", "mode": "test" if is_test_mode else "production"}

@click.command()
@click.option("--host", default="127.0.0.1", help="Host to bind the server to")
@click.option("--port", default=8000, help="Port to run the server on")
@click.option("--reload", is_flag=True, help="Enable auto-reload during development")
def run_server(host, port, reload):
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_config=get_uvicorn_log_config(str(VA.ROOT_DIR.val / 'logs' / 'uvicorn'), 'DEBUG')
    )

if __name__ == '__main__':
    run_server()
