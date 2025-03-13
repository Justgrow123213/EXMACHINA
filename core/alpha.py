"""
@Author: obstacle
@Time: 10/01/25 11:01
@Description:  
"""
from pydantic import BaseModel, Field

from client.client import Client
from typing import List


class AlphaCore(BaseModel):

    startup_clients: List[Client] = Field(
        default_factory=list,
        validate_default=True,
        description='clients connection to start up'
    )

