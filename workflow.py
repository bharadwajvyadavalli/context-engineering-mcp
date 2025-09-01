"""Workflow orchestration for multi-agent collaboration."""

from typing import Dict, Any, Optional, List
from agents import RetrieverAgent, SynthesizerAgent, CriticAgent
from messages import AgentMessage, MessageType
from colorama import Fore, Style
import time


class MultiAgentWorkflow:
    """Orchestrates collaboration between multiple agents."""
    
    def __init__(self, model_name: Optional[str] = None):
        self.retriever = RetrieverAgent(model_name)
        self.synthesizer = SynthesizerAgent(model_name)
        self.critic = CriticAgent(model_name)
        self.interaction_log = []
        
    def run(self, query: str, max_iterations: int = 2) -> Dict[str, Any]:
        """Run the multi-agent workflow for a given query."""
        print(f"\n{Fore.YELLOW}Starting multi-agent workflow for query:{Style.RESET_ALL} {query}\n")
        
        start_time = time.time()
        
        # Step 1: Retrieve relevant information
        print(f"{Fore.BLUE}[1/3] Retriever Agent working...{Style.RESET_ALL}")
        retrieved_info = self.retriever.search(query)
        self.interaction_log.append({
            "agent": "retriever",
            "output": retrieved_info[:200] + "..." if len(retrieved_info) > 200 else retrieved_info
        })
        
        # Step 2: Synthesize response
        print(f"{Fore.BLUE}[2/3] Synthesizer Agent working...{Style.RESET_ALL}")
        synthesized_response = self.synthesizer.synthesize(query, retrieved_info)
        self.interaction_log.append({
            "agent": "synthesizer", 
            "output": synthesized_response[:200] + "..." if len(synthesized_response) > 200 else synthesized_response
        })
        
        # Step 3: Critique and refine
        print(f"{Fore.BLUE}[3/3] Critic Agent evaluating...{Style.RESET_ALL}")
        critique = self.critic.critique(query, synthesized_response)
        self.interaction_log.append({
            "agent": "critic",
            "output": critique
        })
        
        # Optional: If score is low, iterate
        current_response = synthesized_response
        iterations = 1
        
        while critique["score"] < 7 and iterations < max_iterations:
            print(f"\n{Fore.YELLOW}Score {critique['score']}/10 - Refining response (iteration {iterations + 1})...{Style.RESET_ALL}")
            
            # Re-synthesize based on critique
            refinement_prompt = f"{synthesized_response}\n\nCritique: {critique['critique']}"
            current_response = self.synthesizer.synthesize(query, refinement_prompt)
            
            # Re-evaluate
            critique = self.critic.critique(query, current_response)
            iterations += 1
        
        end_time = time.time()
        
        # Compile results
        result = {
            "query": query,
            "final_response": current_response,
            "quality_score": critique["score"],
            "critique": critique["critique"],
            "iterations": iterations,
            "time_taken": round(end_time - start_time, 2),
            "interaction_log": self.interaction_log
        }
        
        print(f"\n{Fore.GREEN}✓ Workflow complete!{Style.RESET_ALL}")
        print(f"Quality Score: {critique['score']}/10")
        print(f"Iterations: {iterations}")
        print(f"Time: {result['time_taken']}s\n")
        
        return result
    
    def run_simple(self, query: str) -> str:
        """Simple workflow that just returns the final answer."""
        result = self.run(query)
        return result["final_response"]


class SingleAgentBaseline:
    """Single agent baseline for comparison."""
    
    def __init__(self, model_name: Optional[str] = None):
        from langchain.chat_models import ChatOpenAI
        from langchain.schema import HumanMessage, SystemMessage
        import os
        
        self.llm = ChatOpenAI(
            model=model_name or os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS", "500"))
        )
        
    def run(self, query: str) -> Dict[str, Any]:
        """Run single agent on query."""
        start_time = time.time()
        
        messages = [
            SystemMessage(content="You are a helpful AI assistant. Answer the question comprehensively."),
            HumanMessage(content=query)
        ]
        
        response = self.llm.invoke(messages)
        
        end_time = time.time()
        
        return {
            "query": query,
            "response": response.content,
            "time_taken": round(end_time - start_time, 2)
        }