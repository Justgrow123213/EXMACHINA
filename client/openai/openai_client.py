"""
@Author: obstacle
@Time: 13/03/25 03:30
@Description: OpenAI GPT-4 client
"""
from openai import AsyncOpenAI
from typing import Optional, List
from pydantic import BaseModel, Field
from logs import logger_factory
from models.agent import AgentPersonality

lgr = logger_factory.client

class OpenAIConfig(BaseModel):
    """Configuration for OpenAI client"""
    api_key: str = Field(..., description="OpenAI API key")
    model: str = Field(default="gpt-4-turbo-preview", description="Model to use")
    temperature: float = Field(default=0.7, description="Temperature for generation")
    max_tokens: int = Field(default=150, description="Maximum tokens to generate")

class OpenAIClient:
    def __init__(self, config: OpenAIConfig, personality: AgentPersonality):
        self.config = config
        self.personality = personality
        self.client = AsyncOpenAI(api_key=config.api_key)
        
    def _get_personality_prompt(self) -> str:
        """Generate system prompt based on agent's personality"""
        traits_str = ", ".join(self.personality.traits)
        interests_str = ", ".join(self.personality.interests)
        
        prompt = f"""You are an AI Twitter personality named {self.personality.name}.
Your personality traits are: {traits_str}
Your main interests are: {interests_str}
You communicate in a {self.personality.tone} style.
Your Twitter bio is: {self.personality.bio}

When generating content:
1. Stay true to your personality traits and interests
2. Maintain your {self.personality.tone} tone
3. {"Use relevant emojis" if self.personality.emoji_style else "Avoid using emojis"}
4. {"Add relevant hashtags" if self.personality.hashtag_style else "Don't use hashtags"}
5. Keep responses within Twitter's 280 character limit
6. Be engaging and encourage interaction
7. Stay up-to-date and relevant in your field

Remember: You're not just generating content, you're building a consistent online presence."""

        return prompt
        
    async def generate_tweet(self, topic: Optional[str] = None, context: Optional[str] = None) -> str:
        """Generate a tweet using GPT-4 based on agent's personality"""
        prompt = "Generate an engaging tweet"
        if topic:
            prompt += f" about {topic}"
        if context:
            prompt += f"\nContext: {context}"
            
        try:
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self._get_personality_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            tweet = response.choices[0].message.content.strip()
            lgr.info(f"Generated tweet: {tweet}")
            return tweet
            
        except Exception as e:
            lgr.error(f"Error generating tweet: {str(e)}")
            raise Exception(f"Failed to generate tweet: {str(e)}")
        
    async def generate_joke(self, topic: Optional[str] = None) -> str:
        """Generate a joke using GPT-4 based on agent's personality"""
        prompt = "Generate a funny and original joke"
        if topic:
            prompt += f" about {topic}"
        prompt += " that matches your personality and style."
        
        try:
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self._get_personality_prompt() + "\nYou especially excel at creating witty and clever jokes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            joke = response.choices[0].message.content.strip()
            lgr.info(f"Generated joke: {joke}")
            return joke
            
        except Exception as e:
            lgr.error(f"Error generating joke: {str(e)}")
            raise Exception(f"Failed to generate joke: {str(e)}")
            
    async def generate_reply(self, tweet_content: str, context: Optional[str] = None) -> str:
        """Generate a reply to a tweet based on agent's personality"""
        prompt = f"Generate a reply to this tweet: '{tweet_content}'"
        if context:
            prompt += f"\nContext: {context}"
            
        try:
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self._get_personality_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            reply = response.choices[0].message.content.strip()
            lgr.info(f"Generated reply: {reply}")
            return reply
            
        except Exception as e:
            lgr.error(f"Error generating reply: {str(e)}")
            raise Exception(f"Failed to generate reply: {str(e)}") 