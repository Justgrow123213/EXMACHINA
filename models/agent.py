"""
@Author: obstacle
@Time: 13/03/25 04:00
@Description: AI Agent personality models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class PersonalityTrait(str, Enum):
    WITTY = "witty"
    SARCASTIC = "sarcastic"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    ENTHUSIASTIC = "enthusiastic"
    PHILOSOPHICAL = "philosophical"
    CREATIVE = "creative"
    TECHNICAL = "technical"

class Interest(str, Enum):
    TECHNOLOGY = "technology"
    SCIENCE = "science"
    CRYPTO = "cryptocurrency"
    AI = "artificial_intelligence"
    PROGRAMMING = "programming"
    MEMES = "memes"
    GAMING = "gaming"
    MUSIC = "music"

class ToneStyle(str, Enum):
    CASUAL = "casual"
    FORMAL = "formal"
    HUMOROUS = "humorous"
    EDUCATIONAL = "educational"
    INSPIRATIONAL = "inspirational"

class AgentPersonality(BaseModel):
    name: str = Field(..., description="Agent's display name")
    bio: str = Field(..., description="Agent's Twitter bio")
    traits: List[PersonalityTrait] = Field(..., description="Primary personality traits")
    interests: List[Interest] = Field(..., description="Main topics of interest")
    tone: ToneStyle = Field(..., description="Primary communication style")
    emoji_style: bool = Field(default=True, description="Whether to use emojis in tweets")
    hashtag_style: bool = Field(default=True, description="Whether to use hashtags")
    
    class Config:
        use_enum_values = True 