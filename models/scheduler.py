"""
@Author: obstacle
@Time: 13/03/25 06:00
@Description: Scheduler configuration models
"""
from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class TimeUnit(str, Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"

class ScheduleConfig(BaseModel):
    tweet_interval: int = Field(default=4, description="Interval between tweets")
    tweet_interval_unit: TimeUnit = Field(default=TimeUnit.HOURS, description="Unit for tweet interval")
    mention_check_interval: int = Field(default=5, description="Interval for checking mentions")
    mention_check_unit: TimeUnit = Field(default=TimeUnit.MINUTES, description="Unit for mention check interval")
    active_hours_start: int = Field(default=9, description="Hour to start posting (24h format)")
    active_hours_end: int = Field(default=23, description="Hour to stop posting (24h format)")
    max_tweets_per_day: int = Field(default=10, description="Maximum tweets per day")
    
    def get_tweet_interval_seconds(self) -> int:
        """Convert tweet interval to seconds"""
        multiplier = {
            TimeUnit.MINUTES: 60,
            TimeUnit.HOURS: 3600,
            TimeUnit.DAYS: 86400
        }
        return self.tweet_interval * multiplier[self.tweet_interval_unit]
        
    def get_mention_check_seconds(self) -> int:
        """Convert mention check interval to seconds"""
        multiplier = {
            TimeUnit.MINUTES: 60,
            TimeUnit.HOURS: 3600,
            TimeUnit.DAYS: 86400
        }
        return self.mention_check_interval * multiplier[self.mention_check_unit] 