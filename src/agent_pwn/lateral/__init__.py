"""Lateral module: Multi-agent propagation payloads."""

from agent_pwn.lateral.crewai import simulate_crewai
from agent_pwn.lateral.langgraph import simulate_langgraph
from agent_pwn.lateral.delegation import simulate_delegation


def run_lateral(vector: str, agents: int, simulate: bool) -> None:
    """Run lateral movement simulation for specified vector.

    Args:
        vector: Attack vector ('crewai', 'langgraph', or 'delegation')
        agents: Number of agents to simulate
        simulate: If True, don't write files, just show what would happen
    """
    vectors = {
        'crewai': simulate_crewai,
        'langgraph': simulate_langgraph,
        'delegation': simulate_delegation,
    }

    if vector not in vectors:
        raise ValueError(f"Unknown attack vector: {vector}")

    vectors[vector](num_agents=agents, simulate=simulate)
