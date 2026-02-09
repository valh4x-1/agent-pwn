"""Exfil module: Data exfiltration channel simulators."""

from agent_pwn.exfil.git_channels import simulate_git_exfil
from agent_pwn.exfil.tool_channels import simulate_tool_exfil


def run_exfil(channel: str, simulate: bool) -> None:
    """Run data exfiltration simulation for specified channel.

    Args:
        channel: Exfiltration channel ('git', 'tool', or 'all')
        simulate: If True, don't create marker files
    """
    if channel == 'git':
        simulate_git_exfil(simulate=simulate)
    elif channel == 'tool':
        simulate_tool_exfil(simulate=simulate)
    elif channel == 'all':
        simulate_git_exfil(simulate=simulate)
        simulate_tool_exfil(simulate=simulate)
    else:
        raise ValueError(f"Unknown exfiltration channel: {channel}")
