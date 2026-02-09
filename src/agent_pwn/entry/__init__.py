"""Entry module: Generate instruction files for target agents."""

from agent_pwn.entry.claude_md import generate_claude_md
from agent_pwn.entry.cursorrules import generate_cursorrules
from agent_pwn.entry.copilot import generate_copilot


def generate(target: str, payload: str, output: str, simulate: bool) -> None:
    """Generate instruction file for the specified target agent.

    Args:
        target: Target agent ('claude', 'cursor', or 'copilot')
        payload: Payload type ('benign' or custom string)
        output: Output directory path
        simulate: If True, print output without writing files
    """
    generators = {
        'claude': generate_claude_md,
        'cursor': generate_cursorrules,
        'copilot': generate_copilot,
    }

    if target not in generators:
        raise ValueError(f"Unknown target: {target}")

    gen = generators[target]
    gen(payload=payload, output_dir=output, simulate=simulate)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python -m agent_pwn.entry <target> <payload> [output] [--simulate]")
        sys.exit(1)
