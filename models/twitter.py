"""
@Author: obstacle
@Time: 13/03/25 06:00
@Description: Twitter API models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class TweetType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    POLL = "poll"

class ActivityType(str, Enum):
    SCHEDULED = "scheduled"
    MANUAL = "manual"
    REPLY = "reply"

class Tweet(BaseModel):
    id: str = Field(..., description="Tweet ID")
    content: str = Field(..., description="Tweet content")
    type: TweetType = Field(default=TweetType.TEXT, description="Type of tweet")
    media_urls: Optional[List[str]] = Field(default=None, description="URLs of media attachments")
    reply_to_id: Optional[str] = Field(default=None, description="ID of tweet being replied to")
    activity_type: ActivityType = Field(default=ActivityType.MANUAL, description="Type of activity")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    likes: int = Field(default=0, description="Number of likes")
    retweets: int = Field(default=0, description="Number of retweets")
    replies: int = Field(default=0, description="Number of replies")
    author_id: Optional[str] = Field(default=None, description="Author's ID")
    mention_id: Optional[str] = Field(default=None, description="ID of the mention")
    replied: bool = Field(default=False, description="Whether this mention has been replied to")
    text: Optional[str] = Field(default=None, description="Text content (alias for content)")

    @property
    def text(self) -> str:
        """Alias for content to maintain compatibility"""
        return self.content

class TweetVariant(BaseModel):
    content: str = Field(..., description="Tweet content")
    tone: str = Field(..., description="Tone used for generation")
    topic: str = Field(..., description="Topic of the tweet")

class TweetResponse(BaseModel):
    tweet_id: str = Field(..., description="ID of created tweet")
    content: str = Field(..., description="Content of created tweet")
    created_at: datetime = Field(..., description="Creation timestamp")

class ErrorResponse(BaseModel):
    message: str = Field(..., description="Error message")
    code: int = Field(..., description="Error code")

class LogEntry(BaseModel):
    id: int = Field(..., description="Log entry ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="Log timestamp")
    level: str = Field(..., description="Log level")
    message: str = Field(..., description="Log message")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata") 