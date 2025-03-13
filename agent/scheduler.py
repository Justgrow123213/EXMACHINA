"""
@Author: obstacle
@Time: 13/03/25 05:00
@Description: AI Agent task scheduler
"""
from typing import Optional, List
import asyncio
import random
from datetime import datetime, timedelta
from client.twitter.twitter_client import TwikitClient
from client.openai.openai_client import OpenAIClient
from models.agent import AgentPersonality, Interest
from models.scheduler import ScheduleConfig
from logs import logger_factory

lgr = logger_factory.default

class AgentScheduler:
    def __init__(
        self,
        twitter_client: TwikitClient,
        openai_client: OpenAIClient,
        personality: AgentPersonality,
        config: Optional[ScheduleConfig] = None
    ):
        self.twitter = twitter_client
        self.openai = openai_client
        self.personality = personality
        self.config = config or ScheduleConfig()
        self.is_running = False
        self.tweet_count_today = 0
        self.last_tweet_time = None
        
    def _reset_daily_count(self):
        """Reset daily tweet counter"""
        now = datetime.now()
        if self.last_tweet_time and now.date() > self.last_tweet_time.date():
            self.tweet_count_today = 0
            
    def _can_tweet_now(self) -> bool:
        """Check if we can tweet based on schedule and limits"""
        now = datetime.now()
        
        # Check active hours
        if not (self.config.active_hours_start <= now.hour < self.config.active_hours_end):
            return False
            
        # Check daily limit
        self._reset_daily_count()
        if self.tweet_count_today >= self.config.max_tweets_per_day:
            return False
            
        # Check interval
        if self.last_tweet_time:
            elapsed = (now - self.last_tweet_time).total_seconds()
            if elapsed < self.config.get_tweet_interval_seconds():
                return False
                
        return True
        
    async def generate_topic(self) -> str:
        """Выбирает случайную тему из интересов агента"""
        return random.choice(self.personality.interests)
        
    async def check_mentions(self):
        """Проверяет и отвечает на упоминания"""
        try:
            # Получаем последние упоминания
            mentions = await self.twitter.get_mentions()
            
            # Обрабатываем mentions как список, независимо от режима
            mentions_list = mentions if isinstance(mentions, list) else mentions.data
            
            for mention in mentions_list:
                if not mention.replied:  # Отвечаем только на новые упоминания
                    # Генерируем ответ на основе контекста
                    reply = await self.openai.generate_reply(
                        tweet_content=mention.text,
                        context=f"This is a reply to a mention from user {mention.author_id}"
                    )
                    
                    # Отправляем ответ
                    await self.twitter.reply_to_tweet(
                        text=reply,
                        tweet_id=mention.mention_id,
                        author_id=mention.author_id,
                        media_path=[]
                    )
                    
                    lgr.info(f"Replied to mention {mention.mention_id}")
                    
        except Exception as e:
            lgr.error(f"Error checking mentions: {str(e)}")
            
    async def post_scheduled_tweet(self):
        """Генерирует и публикует запланированный твит"""
        try:
            if not self._can_tweet_now():
                return
                
            topic = await self.generate_topic()
            tweet_content = await self.openai.generate_tweet(topic=topic)
            
            response = await self.twitter.post_tweet(
                text=tweet_content,
                image_path=None
            )
            
            if response.status == 200:
                self.tweet_count_today += 1
                self.last_tweet_time = datetime.now()
                lgr.info(f"Posted scheduled tweet about {topic}")
            else:
                lgr.error(f"Failed to post tweet: {response.msg}")
                
        except Exception as e:
            lgr.error(f"Error posting scheduled tweet: {str(e)}")
            
    async def run_schedule(self):
        """Запускает основной цикл планировщика"""
        self.is_running = True
        
        while self.is_running:
            try:
                # Проверяем упоминания
                await self.check_mentions()
                
                # Пытаемся опубликовать твит
                await self.post_scheduled_tweet()
                
                # Ждем следующей проверки
                await asyncio.sleep(self.config.get_mention_check_seconds())
                
            except Exception as e:
                lgr.error(f"Error in scheduler loop: {str(e)}")
                await asyncio.sleep(60)  # Ждем минуту перед повторной попыткой
                
    def stop(self):
        """Останавливает планировщик"""
        self.is_running = False
        lgr.info("Scheduler stopped")
        
    def update_config(self, new_config: ScheduleConfig):
        """Обновляет конфигурацию планировщика"""
        self.config = new_config
        lgr.info("Updated scheduler configuration") 