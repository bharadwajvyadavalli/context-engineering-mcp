#!/usr/bin/env python
"""Simple demonstration of the multi-agent system."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow import MultiAgentWorkflow, SingleAgentBaseline
from colorama import init, Fore, Style
import json

init(autoreset=True)


def demo_interactive():
    """Interactive demo where user can input queries."""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Multi-Agent System Interactive Demo{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    print("Enter 'quit' to exit\n")
    
    workflow = MultiAgentWorkflow()
    
    while True:
        query = input(f"{Fore.YELLOW}Enter your question: {Style.RESET_ALL}")
        
        if query.lower() in ['quit', 'exit', 'q']:
            print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break
            
        if not query.strip():
            continue
        
        # Run the workflow
        result = workflow.run(query)
        
        # Display the final response
        print(f"\n{Fore.GREEN}Final Response:{Style.RESET_ALL}")
        print(result["final_response"])
        print(f"\n{Fore.CYAN}Quality Score: {result['quality_score']}/10{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Processing Time: {result['time_taken']}s{Style.RESET_ALL}")
        print("\n" + "="*60 + "\n")


def demo_comparison():
    """Demo comparing multi-agent vs single-agent on a sample query."""
    
    query = "What are the key principles of object-oriented programming and how do they improve code quality?"
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Comparison Demo: Multi-Agent vs Single-Agent{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Query:{Style.RESET_ALL} {query}\n")
    
    # Multi-agent approach
    print(f"{Fore.BLUE}1. MULTI-AGENT APPROACH{Style.RESET_ALL}")
    print("=" * 40)
    ma_workflow = MultiAgentWorkflow()
    ma_result = ma_workflow.run(query)
    
    print(f"\n{Fore.GREEN}Multi-Agent Response:{Style.RESET_ALL}")
    print(ma_result["final_response"])
    
    # Single-agent approach
    print(f"\n{Fore.BLUE}2. SINGLE-AGENT APPROACH{Style.RESET_ALL}")
    print("=" * 40)
    sa_baseline = SingleAgentBaseline()
    sa_result = sa_baseline.run(query)
    
    print(f"\n{Fore.GREEN}Single-Agent Response:{Style.RESET_ALL}")
    print(sa_result["response"])
    
    # Comparison
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}COMPARISON RESULTS{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    print(f"Multi-Agent Quality Score: {ma_result['quality_score']}/10")
    print(f"Multi-Agent Time: {ma_result['time_taken']}s")
    print(f"Multi-Agent Iterations: {ma_result['iterations']}")
    print(f"Single-Agent Time: {sa_result['time_taken']}s")
    print(f"Time Overhead: {round(((ma_result['time_taken'] / sa_result['time_taken']) - 1) * 100, 1)}%")
    
    # Save results
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/demo_comparison.json", "w") as f:
        json.dump({
            "query": query,
            "multi_agent": ma_result,
            "single_agent": sa_result
        }, f, indent=2)
    
    print(f"\n{Fore.GREEN}Results saved to outputs/demo_comparison.json{Style.RESET_ALL}")


def demo_simple():
    """Simple demo with predefined queries."""
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Simple Multi-Agent Demo{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    queries = [
        "What is quantum computing and how does it differ from classical computing?",
        "Explain the concept of blockchain in simple terms.",
        "What are the main challenges in developing artificial general intelligence?"
    ]
    
    workflow = MultiAgentWorkflow()
    
    for i, query in enumerate(queries, 1):
        print(f"{Fore.YELLOW}Query {i}: {query}{Style.RESET_ALL}\n")
        
        result = workflow.run(query)
        
        print(f"\n{Fore.GREEN}Response:{Style.RESET_ALL}")
        print(result["final_response"][:500] + "..." if len(result["final_response"]) > 500 else result["final_response"])
        print(f"\n{Fore.CYAN}Score: {result['quality_score']}/10 | Time: {result['time_taken']}s{Style.RESET_ALL}")
        print("\n" + "-"*60 + "\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-Agent System Demo")
    parser.add_argument("--mode", choices=["interactive", "comparison", "simple"], 
                       default="simple", help="Demo mode to run")
    
    args = parser.parse_args()
    
    if args.mode == "interactive":
        demo_interactive()
    elif args.mode == "comparison":
        demo_comparison()
    else:
        demo_simple()