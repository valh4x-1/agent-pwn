"""Persist module: Persistence and worm generators."""

from agent_pwn.persist.worm import generate_worm
from agent_pwn.persist.memory import simulate_memory_persistence


def run_persist(worm_type: str, target_file: str, r0: float, generations: int, payload: str, simulate: bool) -> None:
    """Run persistence attack simulation or generator.

    Args:
        worm_type: Type of persistence ('instruction' or 'memory')
        target_file: Target instruction file for worm injection
        r0: Reproduction number (expected spread rate)
        generations: Maximum generations the worm should propagate
        payload: Payload type (usually 'benign')
        simulate: If True, don't create marker files
    """
    if worm_type == 'instruction':
        generate_worm(target_file=target_file, r0=r0, generations=generations, payload=payload, simulate=simulate)
    elif worm_type == 'memory':
        simulate_memory_persistence(simulate=simulate)
    else:
        raise ValueError(f"Unknown worm type: {worm_type}")
