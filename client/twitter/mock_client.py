"""
@Author: obstacle
@Time: 13/03/25 07:00
@Description: Mock Twitter client for testing
"""
from typing import List, Optional
from models.twitter import Tweet, TweetType, ActivityType
from datetime import datetime
import json
import os
import asyncio
import random

class MockTwikitClient:
    def __init__(self, storage_path: str = "data/mock_tweets.json"):
        self.storage_path = storage_path
        self._ensure_storage_exists()
        self._load_tweets()
        
    def _ensure_storage_exists(self):
        """Create storage directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)
                
    def _load_tweets(self):
        """Load tweets from storage"""
        with open(self.storage_path, 'r') as f:
            try:
                self.tweets = [Tweet(**t) for t in json.load(f)]
            except:
                self.tweets = []
                
    def _save_tweets(self):
        """Save tweets to storage"""
        with open(self.storage_path, 'w') as f:
            json.dump([t.dict() for t in self.tweets], f, default=str)
            
    async def post_tweet(self, text: str, image_path: Optional[str] = None) -> Tweet:
        """Post a new tweet"""
        tweet = Tweet(
            id=str(len(self.tweets) + 1),
            content=text,
            type=TweetType.IMAGE if image_path else TweetType.TEXT,
            media_urls=[image_path] if image_path else None,
            activity_type=ActivityType.MANUAL,
            created_at=datetime.now()
        )
        self.tweets.append(tweet)
        self._save_tweets()
        return tweet
        
    async def reply_to_tweet(
        self, 
        text: str, 
        tweet_id: str,
        author_id: str,
        media_path: List[str] = None
    ) -> Tweet:
        """Reply to a tweet"""
        tweet = Tweet(
            id=str(len(self.tweets) + 1),
            content=text,
            type=TweetType.IMAGE if media_path else TweetType.TEXT,
            media_urls=media_path,
            reply_to_id=tweet_id,
            activity_type=ActivityType.REPLY,
            created_at=datetime.now()
        )
        self.tweets.append(tweet)
        self._save_tweets()
        return tweet
        
    async def get_mentions(self, since_id: Optional[str] = None):
        """Get mentions"""
        mentions = [
            Tweet(
                id=t.id,
                content=t.content,
                type=t.type,
                activity_type=t.activity_type,
                author_id=f"user_{t.id}",  # Мок ID пользователя
                mention_id=t.id,  # В тестовом режиме ID упоминания совпадает с ID твита
                replied=False,  # По умолчанию не отвечено
                created_at=t.created_at
            )
            for t in self.tweets 
            if t.activity_type == ActivityType.REPLY
        ]
        
        if since_id:
            mentions = [m for m in mentions if int(m.id) > int(since_id)]
            
        return mentions
        
    async def get_user_tweets(
        self,
        limit: int = 10,
        offset: int = 0
    ) -> List[Tweet]:
        """Get user tweets"""
        sorted_tweets = sorted(
            self.tweets, 
            key=lambda x: x.created_at,
            reverse=True
        )
        return sorted_tweets[offset:offset + limit]
        
    async def simulate_engagement(self, tweet_id: str):
        """Simulate random engagement on a tweet"""
        for tweet in self.tweets:
            if tweet.id == tweet_id:
                # Симулируем случайную активность
                tweet.likes += 1
                if random.random() > 0.7:
                    tweet.retweets += 1
                if random.random() > 0.8:
                    tweet.replies += 1
                self._save_tweets()
                break 