"""Basic tests for the multi-agent system."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from messages import AgentMessage, MessageType, MessageHistory
from agents import BaseAgent, RetrieverAgent, SynthesizerAgent, CriticAgent
from workflow import MultiAgentWorkflow, SingleAgentBaseline


def test_message_creation():
    """Test message creation and serialization."""
    msg = AgentMessage(
        sender="agent1",
        recipient="agent2",
        message_type=MessageType.QUERY,
        content="Test message"
    )
    
    assert msg.sender == "agent1"
    assert msg.recipient == "agent2"
    assert msg.message_type == MessageType.QUERY
    assert msg.content == "Test message"
    assert msg.to_prompt_context() == "[agent1 -> agent2]: Test message"


def test_message_history():
    """Test message history management."""
    history = MessageHistory()
    
    # Add messages
    msg1 = AgentMessage(sender="a1", recipient="a2", message_type=MessageType.QUERY, content="Query 1")
    msg2 = AgentMessage(sender="a2", recipient="a1", message_type=MessageType.RESPONSE, content="Response 1")
    
    history.add_message(msg1)
    history.add_message(msg2)
    
    assert len(history.messages) == 2
    assert history.get_recent_messages(1)[0] == msg2
    
    # Test context generation
    context = history.get_conversation_context()
    assert "Query 1" in context
    assert "Response 1" in context
    
    # Test clear
    history.clear()
    assert len(history.messages) == 0


def test_base_agent_initialization():
    """Test base agent initialization."""
    agent = BaseAgent("test_agent", "test_role")
    
    assert agent.agent_id == "test_agent"
    assert agent.role == "test_role"
    assert agent.llm is not None
    assert isinstance(agent.memory, MessageHistory)


def test_retriever_agent():
    """Test retriever agent functionality."""
    retriever = RetrieverAgent()
    
    assert retriever.agent_id == "retriever"
    assert retriever.role == "retriever"
    
    # Test search method exists
    assert hasattr(retriever, 'search')
    assert callable(retriever.search)


def test_synthesizer_agent():
    """Test synthesizer agent functionality."""
    synthesizer = SynthesizerAgent()
    
    assert synthesizer.agent_id == "synthesizer"
    assert synthesizer.role == "synthesizer"
    
    # Test synthesize method exists
    assert hasattr(synthesizer, 'synthesize')
    assert callable(synthesizer.synthesize)


def test_critic_agent():
    """Test critic agent functionality."""
    critic = CriticAgent()
    
    assert critic.agent_id == "critic"
    assert critic.role == "critic"
    
    # Test critique method exists
    assert hasattr(critic, 'critique')
    assert callable(critic.critique)


def test_workflow_initialization():
    """Test workflow initialization."""
    workflow = MultiAgentWorkflow()
    
    assert workflow.retriever is not None
    assert workflow.synthesizer is not None
    assert workflow.critic is not None
    assert isinstance(workflow.interaction_log, list)


def test_single_agent_baseline():
    """Test single agent baseline initialization."""
    baseline = SingleAgentBaseline()
    
    assert baseline.llm is not None
    assert hasattr(baseline, 'run')
    assert callable(baseline.run)


@pytest.mark.skip(reason="Requires API key")
def test_simple_workflow_execution():
    """Test simple workflow execution (requires API key)."""
    workflow = MultiAgentWorkflow()
    result = workflow.run_simple("What is Python?")
    
    assert isinstance(result, str)
    assert len(result) > 0


if __name__ == "__main__":
    # Run basic tests without pytest
    print("Running basic tests...")
    
    test_message_creation()
    print("✓ Message creation test passed")
    
    test_message_history()
    print("✓ Message history test passed")
    
    test_base_agent_initialization()
    print("✓ Base agent initialization test passed")
    
    test_retriever_agent()
    print("✓ Retriever agent test passed")
    
    test_synthesizer_agent()
    print("✓ Synthesizer agent test passed")
    
    test_critic_agent()
    print("✓ Critic agent test passed")
    
    test_workflow_initialization()
    print("✓ Workflow initialization test passed")
    
    test_single_agent_baseline()
    print("✓ Single agent baseline test passed")
    
    print("\nAll basic tests passed! ✨")