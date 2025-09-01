"""Evaluation script for comparing multi-agent vs single-agent performance."""

import json
import time
from typing import List, Dict, Any
from workflow import MultiAgentWorkflow, SingleAgentBaseline
from tabulate import tabulate
from colorama import Fore, Style, init
import os

init(autoreset=True)


# Sample evaluation tasks
EVALUATION_TASKS = [
    {
        "id": "task_1",
        "query": "Explain the difference between supervised and unsupervised learning in machine learning.",
        "type": "explanation"
    },
    {
        "id": "task_2", 
        "query": "What are the main advantages and disadvantages of electric vehicles compared to gasoline cars?",
        "type": "comparison"
    },
    {
        "id": "task_3",
        "query": "Create a step-by-step plan for someone who wants to learn web development from scratch.",
        "type": "planning"
    },
    {
        "id": "task_4",
        "query": "Explain how photosynthesis works and why it's important for life on Earth.",
        "type": "explanation"
    },
    {
        "id": "task_5",
        "query": "What are the key considerations when choosing between SQL and NoSQL databases for a new project?",
        "type": "analysis"
    }
]


def evaluate_response_length(response: str) -> int:
    """Calculate response length in words."""
    return len(response.split())


def evaluate_response_completeness(response: str, query: str) -> float:
    """Simple heuristic for response completeness (0-1)."""
    # Check if response addresses key terms from query
    query_terms = set(query.lower().split())
    response_terms = set(response.lower().split())
    
    overlap = len(query_terms.intersection(response_terms))
    return min(overlap / len(query_terms), 1.0) if query_terms else 0


def run_evaluation(tasks: List[Dict[str, Any]] = None, save_results: bool = True):
    """Run evaluation comparing multi-agent and single-agent approaches."""
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Starting Evaluation: Multi-Agent vs Single-Agent{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    tasks = tasks or EVALUATION_TASKS
    
    # Initialize systems
    multi_agent = MultiAgentWorkflow()
    single_agent = SingleAgentBaseline()
    
    results = {
        "multi_agent": [],
        "single_agent": [],
        "summary": {}
    }
    
    # Run evaluations
    for i, task in enumerate(tasks, 1):
        print(f"\n{Fore.YELLOW}Task {i}/{len(tasks)}: {task['type'].upper()}{Style.RESET_ALL}")
        print(f"Query: {task['query'][:100]}...\n")
        
        # Multi-agent evaluation
        print(f"{Fore.BLUE}Running multi-agent workflow...{Style.RESET_ALL}")
        ma_result = multi_agent.run(task["query"])
        results["multi_agent"].append({
            "task_id": task["id"],
            "query": task["query"],
            "response": ma_result["final_response"],
            "score": ma_result["quality_score"],
            "time": ma_result["time_taken"],
            "iterations": ma_result["iterations"],
            "word_count": evaluate_response_length(ma_result["final_response"]),
            "completeness": evaluate_response_completeness(ma_result["final_response"], task["query"])
        })
        
        # Single-agent evaluation
        print(f"\n{Fore.BLUE}Running single-agent baseline...{Style.RESET_ALL}")
        sa_result = single_agent.run(task["query"])
        results["single_agent"].append({
            "task_id": task["id"],
            "query": task["query"],
            "response": sa_result["response"],
            "time": sa_result["time_taken"],
            "word_count": evaluate_response_length(sa_result["response"]),
            "completeness": evaluate_response_completeness(sa_result["response"], task["query"])
        })
        
        # Brief pause to avoid rate limits
        time.sleep(1)
    
    # Calculate summary statistics
    ma_avg_score = sum(r["score"] for r in results["multi_agent"]) / len(results["multi_agent"])
    ma_avg_time = sum(r["time"] for r in results["multi_agent"]) / len(results["multi_agent"])
    ma_avg_words = sum(r["word_count"] for r in results["multi_agent"]) / len(results["multi_agent"])
    ma_avg_complete = sum(r["completeness"] for r in results["multi_agent"]) / len(results["multi_agent"])
    
    sa_avg_time = sum(r["time"] for r in results["single_agent"]) / len(results["single_agent"])
    sa_avg_words = sum(r["word_count"] for r in results["single_agent"]) / len(results["single_agent"])
    sa_avg_complete = sum(r["completeness"] for r in results["single_agent"]) / len(results["single_agent"])
    
    results["summary"] = {
        "multi_agent": {
            "avg_quality_score": round(ma_avg_score, 2),
            "avg_time": round(ma_avg_time, 2),
            "avg_word_count": round(ma_avg_words),
            "avg_completeness": round(ma_avg_complete, 2)
        },
        "single_agent": {
            "avg_time": round(sa_avg_time, 2),
            "avg_word_count": round(sa_avg_words),
            "avg_completeness": round(sa_avg_complete, 2)
        },
        "comparison": {
            "time_overhead": f"{round(((ma_avg_time / sa_avg_time) - 1) * 100, 1)}%",
            "response_length_diff": f"{round(((ma_avg_words / sa_avg_words) - 1) * 100, 1)}%",
            "completeness_improvement": f"{round(((ma_avg_complete / sa_avg_complete) - 1) * 100, 1)}%"
        }
    }
    
    # Display results
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}EVALUATION RESULTS{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
    
    # Create comparison table
    table_data = []
    for i, task in enumerate(tasks):
        ma = results["multi_agent"][i]
        sa = results["single_agent"][i]
        table_data.append([
            task["type"],
            f"{ma['score']}/10",
            f"{ma['time']}s",
            f"{sa['time']}s",
            ma["word_count"],
            sa["word_count"]
        ])
    
    headers = ["Task Type", "MA Score", "MA Time", "SA Time", "MA Words", "SA Words"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Summary statistics
    print(f"\n{Fore.CYAN}Summary Statistics:{Style.RESET_ALL}")
    print(f"Multi-Agent Average Quality Score: {results['summary']['multi_agent']['avg_quality_score']}/10")
    print(f"Time Overhead: {results['summary']['comparison']['time_overhead']}")
    print(f"Response Length Difference: {results['summary']['comparison']['response_length_diff']}")
    print(f"Completeness Improvement: {results['summary']['comparison']['completeness_improvement']}")
    
    # Save results
    if save_results:
        output_file = f"examples/outputs/evaluation_{int(time.time())}.json"
        os.makedirs("examples/outputs", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n{Fore.GREEN}Results saved to: {output_file}{Style.RESET_ALL}")
    
    return results


if __name__ == "__main__":
    # Run evaluation
    results = run_evaluation()
    
    # Print sample responses for comparison
    print(f"\n{Fore.CYAN}Sample Response Comparison (Task 1):{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Multi-Agent Response:{Style.RESET_ALL}")
    print(results["multi_agent"][0]["response"][:500] + "...")
    print(f"\n{Fore.YELLOW}Single-Agent Response:{Style.RESET_ALL}")
    print(results["single_agent"][0]["response"][:500] + "...")