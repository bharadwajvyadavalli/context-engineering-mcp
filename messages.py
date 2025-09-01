"""Message protocol for agent communication."""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """Types of messages agents can send."""
    QUERY = "query"
    RESPONSE = "response"
    CRITIQUE = "critique"
    CONTEXT_UPDATE = "context_update"
    ERROR = "error"


class AgentMessage(BaseModel):
    """Standard message format for agent communication."""
    
    sender: str = Field(description="Agent ID of sender")
    recipient: str = Field(description="Agent ID of recipient")
    message_type: MessageType = Field(description="Type of message")
    content: str = Field(description="Main message content")
    context: Dict[str, Any] = Field(default_factory=dict, description="Shared context")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    def to_prompt_context(self) -> str:
        """Convert message to context string for prompts."""
        return f"[{self.sender} -> {self.recipient}]: {self.content}"


class MessageHistory:
    """Manages conversation history between agents."""
    
    def __init__(self):
        self.messages: List[AgentMessage] = []
        
    def add_message(self, message: AgentMessage):
        """Add a message to history."""
        self.messages.append(message)
        
    def get_recent_messages(self, n: int = 5) -> List[AgentMessage]:
        """Get n most recent messages."""
        return self.messages[-n:] if self.messages else []
    
    def get_conversation_context(self) -> str:
        """Get formatted conversation history for prompts."""
        if not self.messages:
            return "No previous conversation."
        
        context = "Previous conversation:\n"
        for msg in self.messages[-10:]:  # Last 10 messages
            context += f"{msg.to_prompt_context()}\n"
        return context
    
    def clear(self):
        """Clear message history."""
        self.messages = []