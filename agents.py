"""Agent implementations for the multi-agent system."""

import os
import yaml
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from messages import AgentMessage, MessageType, MessageHistory
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)
load_dotenv()


class BaseAgent:
    """Base class for all agents."""
    
    def __init__(self, agent_id: str, role: str, model_name: Optional[str] = None):
        self.agent_id = agent_id
        self.role = role
        self.model_name = model_name or os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "500"))
        )
        self.memory = MessageHistory()
        self.system_prompt = self._load_system_prompt()
        
    def _load_system_prompt(self) -> str:
        """Load system prompt from YAML file."""
        try:
            with open("prompts/agents.yaml", "r") as f:
                prompts = yaml.safe_load(f)
                return prompts.get(self.role, {}).get("system_prompt", f"You are a {self.role} agent.")
        except:
            return f"You are a {self.role} agent in a multi-agent system."
    
    def process(self, message: AgentMessage) -> AgentMessage:
        """Process incoming message and generate response."""
        self.memory.add_message(message)
        
        # Build prompt with context
        context = self.memory.get_conversation_context()
        prompt = f"{context}\n\nCurrent message: {message.content}\n\nYour response:"
        
        # Get LLM response
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Create response message
        response_msg = AgentMessage(
            sender=self.agent_id,
            recipient=message.sender,
            message_type=MessageType.RESPONSE,
            content=response.content,
            context=message.context,
            metadata={"model": self.model_name}
        )
        
        self.memory.add_message(response_msg)
        self._log_interaction(message, response_msg)
        
        return response_msg
    
    def _log_interaction(self, received: AgentMessage, sent: AgentMessage):
        """Log agent interactions with color."""
        if os.getenv("DEBUG_MODE", "False") == "True":
            print(f"{Fore.CYAN}[{self.agent_id}] Received:{Style.RESET_ALL} {received.content[:100]}...")
            print(f"{Fore.GREEN}[{self.agent_id}] Sent:{Style.RESET_ALL} {sent.content[:100]}...")
            print("-" * 50)


class RetrieverAgent(BaseAgent):
    """Agent specialized in retrieving relevant information."""
    
    def __init__(self, model_name: Optional[str] = None):
        super().__init__("retriever", "retriever", model_name)
        
    def search(self, query: str, sources: Optional[Dict[str, Any]] = None) -> str:
        """Simulate searching for relevant information."""
        # In a real implementation, this would search databases, APIs, etc.
        prompt = f"""Given the query: "{query}"
        
        Provide relevant information that would help answer this query.
        Focus on facts, definitions, and key concepts.
        If you don't have specific information, provide general context."""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content


class SynthesizerAgent(BaseAgent):
    """Agent specialized in synthesizing information."""
    
    def __init__(self, model_name: Optional[str] = None):
        super().__init__("synthesizer", "synthesizer", model_name)
        
    def synthesize(self, query: str, retrieved_info: str) -> str:
        """Synthesize information into a coherent response."""
        prompt = f"""Original query: "{query}"
        
        Retrieved information:
        {retrieved_info}
        
        Please synthesize this information into a clear, comprehensive answer.
        Ensure the response is well-structured and directly addresses the query."""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content


class CriticAgent(BaseAgent):
    """Agent specialized in critiquing and improving responses."""
    
    def __init__(self, model_name: Optional[str] = None):
        super().__init__("critic", "critic", model_name)
        
    def critique(self, query: str, response: str) -> Dict[str, Any]:
        """Critique a response and suggest improvements."""
        prompt = f"""Original query: "{query}"
        
        Response to evaluate:
        {response}
        
        Please evaluate this response for:
        1. Accuracy and factual correctness
        2. Completeness in addressing the query
        3. Clarity and coherence
        4. Any potential hallucinations or unsupported claims
        
        Provide:
        - A quality score (1-10)
        - Specific issues found
        - Suggested improvements
        - A revised response if needed"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse the critique (simplified)
        critique_text = response.content
        
        # Extract score (simple regex would be better)
        score = 7  # Default score
        if "10" in critique_text[:50]:
            score = 10
        elif "9" in critique_text[:50]:
            score = 9
        elif "8" in critique_text[:50]:
            score = 8
        elif "6" in critique_text[:50]:
            score = 6
        elif "5" in critique_text[:50]:
            score = 5
            
        return {
            "score": score,
            "critique": critique_text,
            "issues": [],
            "improvements": []
        }