"""agent-pwn CLI: Main entry point with 7 subcommands."""

import click


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """agent-pwn: Security testing framework for AI coding agents."""
    pass


@cli.command()
@click.option(
    '--target',
    type=click.Choice(['claude', 'cursor', 'copilot']),
    required=True,
    help='Target agent'
)
@click.option('--payload', default='benign', help='Payload type')
@click.option('--output', type=click.Path(), default='.', help='Output directory')
@click.option('--simulate', is_flag=True, help='Dry-run mode')
def entry(target, payload, output, simulate):
    """Generate instruction files for target agents."""
    from agent_pwn.entry import generate
    generate(target, payload, output, simulate)


@cli.command()
@click.option(
    '--method',
    type=click.Choice(['unicode', 'comment', 'cross-context', 'hex']),
    required=True
)
@click.option('--message', required=True, help='Message to hide')
@click.option('--target', type=click.Path(exists=True), required=True, help='Target file')
@click.option('--simulate', is_flag=True)
def hijack(method, message, target, simulate):
    """Embed hidden instructions in source code."""
    from agent_pwn.hijack import inject
    inject(method, message, target, simulate)


@cli.command()
@click.option('--tool-name', default='security_scan', help='MCP tool name')
@click.option('--description', default=None, help='Tool description with injection')
@click.option('--output', type=click.Path(), default='.', help='Output directory')
@click.option('--simulate', is_flag=True)
def escalate(tool_name, description, output, simulate):
    """Generate MCP server exploits."""
    from agent_pwn.escalate import generate_mcp
    generate_mcp(tool_name, description, output, simulate)


@cli.command()
@click.option(
    '--vector',
    type=click.Choice(['crewai', 'langgraph', 'delegation']),
    required=True
)
@click.option('--agents', default=3, type=int, help='Number of agents')
@click.option('--simulate', is_flag=True)
def lateral(vector, agents, simulate):
    """Multi-agent propagation payloads."""
    from agent_pwn.lateral import run_lateral
    run_lateral(vector, agents, simulate)


@cli.command()
@click.option(
    '--worm-type',
    type=click.Choice(['instruction', 'memory']),
    default='instruction'
)
@click.option('--target-file', default='CLAUDE.md', help='Target instruction file')
@click.option('--r0', default=5.1, type=float, help='Target R0')
@click.option('--generations', default=3, type=int, help='Max generations')
@click.option('--payload', default='benign')
@click.option('--simulate', is_flag=True)
def persist(worm_type, target_file, r0, generations, payload, simulate):
    """Persistence and worm generators."""
    from agent_pwn.persist import run_persist
    run_persist(worm_type, target_file, r0, generations, payload, simulate)


@cli.command()
@click.option(
    '--channel',
    type=click.Choice(['git', 'tool', 'all']),
    default='all'
)
@click.option('--simulate', is_flag=True)
def exfil(channel, simulate):
    """Data exfiltration channel simulators."""
    from agent_pwn.exfil import run_exfil
    run_exfil(channel, simulate)


@cli.command()
@click.option(
    '--scan-repo',
    type=click.Path(exists=True),
    required=True,
    help='Repository path to scan'
)
def detect(scan_repo):
    """Scan repositories for instruction injection."""
    from agent_pwn.detect import scan
    scan(scan_repo)


if __name__ == '__main__':
    cli()
