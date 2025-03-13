"""
@Author: obstacle
@Time: 13/03/25 02:10
@Description: Twitter API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from models.twitter import Tweet, TweetResponse, ErrorResponse, TweetType, ActivityType
from client.twitter.twitter_client import TwikitClient
from client.openai.openai_client import OpenAIClient
from typing import List, Optional
import datetime

router = APIRouter(prefix="/api/twitter", tags=["twitter"])

async def get_twitter_client(request: Request) -> TwikitClient:
    return request.app.state.twitter_client

async def get_openai_client(request: Request) -> OpenAIClient:
    return request.app.state.openai_client

@router.get("/generate_tweet")
async def generate_test_tweet(
    topic: Optional[str] = None,
    openai_client: OpenAIClient = Depends(get_openai_client)
):
    """
    Generate a test tweet without posting it
    """
    try:
        tweet_content = await openai_client.generate_tweet(topic=topic)
        return {"generated_tweet": tweet_content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tweet", response_model=TweetResponse, responses={400: {"model": ErrorResponse}})
async def create_tweet(
    tweet: Tweet,
    request: Request,
    twitter_client: TwikitClient = Depends(get_twitter_client),
    openai_client: OpenAIClient = Depends(get_openai_client)
):
    """
    Create a new tweet
    """
    try:
        if tweet.type == TweetType.ACTIVITY:
            if not tweet.activity_type:
                raise HTTPException(status_code=400, detail="Activity type is required for activity tweets")
            
            if tweet.activity_type == ActivityType.JOKE:
                # Generate joke using GPT-4
                joke = await openai_client.generate_joke()
                tweet.content = joke
            elif tweet.activity_type == ActivityType.SEND_TOKEN:
                # TODO: Handle token sending
                pass

        response = await twitter_client.post_tweet(
            text=tweet.content,
            image_path=tweet.media_urls if tweet.media_urls else None,
            reply_tweet_id=tweet.reply_to_id
        )
        
        if response.status != 200:
            raise HTTPException(status_code=400, detail=response.msg)

        return TweetResponse(
            id=str(response.data.id),
            content=tweet.content,
            created_at=datetime.datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tweet/{tweet_id}/reply", response_model=TweetResponse, responses={400: {"model": ErrorResponse}})
async def reply_to_tweet(
    tweet_id: str,
    tweet: Tweet,
    request: Request,
    twitter_client: TwikitClient = Depends(get_twitter_client),
    openai_client: OpenAIClient = Depends(get_openai_client)
):
    """
    Reply to an existing tweet
    """
    try:
        if tweet.type == TweetType.ACTIVITY and tweet.activity_type == ActivityType.JOKE:
            # Generate joke as reply
            joke = await openai_client.generate_joke()
            tweet.content = joke

        response = await twitter_client.reply_to_tweet(
            text=tweet.content,
            media_path=tweet.media_urls if tweet.media_urls else [],
            tweet_id=int(tweet_id),
            author_id=0  # We'll get this from the tweet itself
        )

        if response.status != 200:
            raise HTTPException(status_code=400, detail=response.msg)

        return TweetResponse(
            id=str(response.data.id),
            content=tweet.content,
            created_at=datetime.datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tweet/{tweet_id}", response_model=TweetResponse, responses={400: {"model": ErrorResponse}})
async def get_tweet(tweet_id: str, client: TwikitClient = Depends(get_twitter_client)):
    """
    Get tweet by ID
    """
    try:
        # Since we don't have a direct method to get a single tweet,
        # we'll need to implement this later
        raise HTTPException(status_code=501, detail="Not implemented yet")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 