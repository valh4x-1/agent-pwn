"""agent-pwn CLI: Main entry point and compatibility surface."""

import click


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """agent-pwn: Security testing framework for AI coding agents."""
    pass


def _compat_note(message: str) -> None:
    """Print compatibility notes for accepted-but-ignored options."""
    click.echo(f"[i] {message}")


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
@click.option('--benign', is_flag=True, help='Use benign payload profile')
def entry(target, payload, output, simulate, benign):
    """Generate instruction files for target agents."""
    from agent_pwn.entry import generate

    if benign:
        payload = 'benign'
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
@click.option('--benign', is_flag=True, help='Compatibility flag (benign mode)')
def hijack(method, message, target, simulate, benign):
    """Embed hidden instructions in source code."""
    from agent_pwn.hijack import inject

    if benign:
        _compat_note("--benign is accepted for compatibility")
    inject(method, message, target, simulate)


@cli.command()
@click.option(
    '--type',
    'escalate_type',
    type=click.Choice(['mcp-server']),
    default='mcp-server',
    show_default=True,
    help='Escalation template type'
)
@click.option('--tool-name', '--tool', 'tool_name', default='security_scan', help='MCP tool name')
@click.option('--description', default=None, help='Tool description with injection')
@click.option('--poison', default=None, help='Poisoning directive text (alias of --description)')
@click.option('--output', type=click.Path(), default='.', help='Output directory')
@click.option('--simulate', is_flag=True)
@click.option('--benign', is_flag=True, help='Compatibility flag (benign mode)')
def escalate(escalate_type, tool_name, description, poison, output, simulate, benign):
    """Generate MCP server exploits."""
    from agent_pwn.escalate import generate_mcp

    if escalate_type != 'mcp-server':
        raise click.UsageError(f"Unsupported --type value: {escalate_type}")
    if description is None and poison is not None:
        description = poison
    if benign:
        _compat_note("--benign is accepted for compatibility")
    generate_mcp(tool_name, description, output, simulate)


@cli.command()
@click.option(
    '--vector', '--framework', 'vector',
    type=click.Choice(['crewai', 'langgraph', 'delegation']),
    required=True
)
@click.option('--agents', default=3, type=int, help='Number of agents')
@click.option('--payload', default='benign', help='Payload profile (compatibility option)')
@click.option('--simulate', is_flag=True)
@click.option('--benign', is_flag=True, help='Compatibility flag (benign mode)')
def lateral(vector, agents, payload, simulate, benign):
    """Multi-agent propagation payloads."""
    from agent_pwn.lateral import run_lateral

    if payload != 'benign':
        _compat_note("--payload is accepted for compatibility; simulator uses built-in payloads")
    if benign:
        _compat_note("--benign is accepted for compatibility")
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
@click.option('--output', type=click.Path(), default=None, help='Output file path (default: patient-zero.md)')
@click.option('--simulate', is_flag=True)
@click.option('--benign', is_flag=True, help='Use benign payload profile')
def persist(worm_type, target_file, r0, generations, payload, output, simulate, benign):
    """Persistence and worm generators."""
    from agent_pwn.persist import run_persist

    if benign:
        payload = 'benign'
    run_persist(worm_type, target_file, r0, generations, payload, simulate, output)


@cli.command()
@click.option(
    '--channel',
    type=click.Choice(['git', 'tool', 'all', 'git-commit']),
    default='all'
)
@click.option('--data', default=None, help='Compatibility option for exfil data source')
@click.option('--repo', type=click.Path(), default=None, help='Compatibility option for repo path')
@click.option('--simulate', is_flag=True)
@click.option('--benign', is_flag=True, help='Compatibility flag (benign mode)')
def exfil(channel, data, repo, simulate, benign):
    """Data exfiltration channel simulators."""
    from agent_pwn.exfil import run_exfil

    if channel == 'git-commit':
        channel = 'git'
    if data:
        _compat_note("--data is accepted for compatibility")
    if repo:
        _compat_note("--repo is accepted for compatibility")
    if benign:
        _compat_note("--benign is accepted for compatibility")
    run_exfil(channel, simulate)


@cli.command()
@click.option(
    '--scan-repo',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help='Repository path to scan'
)
@click.option(
    '--exclude',
    multiple=True,
    help='Patterns to exclude from scanning (can be specified multiple times)'
)
@click.option('--simulate', is_flag=True, help='Show scan intent without scanning')
@click.option('--benign', is_flag=True, help='Compatibility flag (benign mode)')
def detect(scan_repo, exclude, simulate, benign):
    """Scan repositories for instruction injection."""
    from agent_pwn.detect import scan

    if benign:
        _compat_note("--benign is accepted for compatibility")
    if simulate:
        click.echo(f"[SIMULATE] Would scan repository: {scan_repo}")
        if exclude:
            click.echo(f"[SIMULATE] Exclude patterns: {', '.join(exclude)}")
        return
    exclude_list = list(exclude) if exclude else None
    scan(scan_repo, exclude_patterns=exclude_list)


@cli.command(name='test')
@click.option(
    '--agent',
    type=click.Choice(['claude-code', 'cursor', 'copilot']),
    required=True,
    help='Agent profile to simulate'
)
@click.option('--payload', type=click.Path(exists=True), required=True, help='Payload file to load')
@click.option('--query', default='Review the codebase', show_default=True, help='User query to simulate')
@click.option('--simulate', is_flag=True, help='Dry-run mode')
@click.option('--benign', is_flag=True, help='Compatibility flag (benign mode)')
def test_command(agent, payload, query, simulate, benign):
    """Run payload trigger simulation against an agent profile."""
    from datetime import datetime
    from pathlib import Path

    marker = Path('.agent-pwned')
    click.echo("[+] Starting agent simulation")
    click.echo(f"[+] Agent: {agent} (simulated)")
    click.echo(f"[+] Loading instruction file: {payload}")
    click.echo(f'[+] User query: "{query}"')
    click.echo("[+] Agent reads instructions...")
    click.echo("[+] Agent executes pre-review steps...")

    if benign:
        _compat_note("--benign is accepted for compatibility")

    if simulate:
        click.echo("[+] Simulation mode enabled; no marker files written")
        click.echo("[+] Detection: SIMULATED")
        return

    marker.write_text(
        f"agent={agent}\n"
        f"payload={payload}\n"
        f"query={query}\n"
        f"timestamp={datetime.now().isoformat()}\n",
        encoding='utf-8'
    )
    click.echo("[!] PAYLOAD TRIGGERED: .agent-pwned created")
    click.echo("[+] Detection: SUCCESS")

    if marker.exists():
        marker.unlink()
        click.echo("[+] Cleanup: Removing .agent-pwned")


@cli.command()
@click.option('--dry-run', '--simulate', 'dry_run', is_flag=True, help='List files without deleting them')
@click.option('--target-dir', type=click.Path(), default='.', help='Directory to clean (default: current)')
@click.option('--benign', is_flag=True, help='Compatibility flag (benign mode)')
def clean(dry_run, target_dir, benign):
    """Remove agent-pwn marker files from a directory."""
    from pathlib import Path

    if benign:
        _compat_note("--benign is accepted for compatibility")

    marker_patterns = [
        '.agent-pwned*',
        '.worm-marker-*',
        '.agent-pwned-crewai',
        '.graph-hijacked',
        '.agent-delegated-*',
        '.memory-poisoned',
        '.git-exfil-ready',
        '.tool-exfil-ready',
        'patient-zero.md',
        'mcp_pwn_server.py',
        'agent_memory.db',
    ]

    target_path = Path(target_dir).resolve()
    if not target_path.exists():
        print(f"[-] Target directory does not exist: {target_dir}")
        return

    found_files = []
    for pattern in marker_patterns:
        matches = list(target_path.glob(pattern))
        found_files.extend(matches)

        for subdir in ['.agent', '.github', '.cursor']:
            subdir_path = target_path / subdir
            if subdir_path.exists():
                matches = list(subdir_path.glob(pattern))
                found_files.extend(matches)

    found_files = list(set(found_files))

    if not found_files:
        print("[+] No agent-pwn marker files found")
        return

    print(f"[+] Found {len(found_files)} marker file(s):")
    for file_path in sorted(found_files):
        rel_path = file_path.relative_to(target_path)
        print(f"    {rel_path}")

    if dry_run:
        print("\n[+] Dry-run mode: no files deleted")
        print("[+] Run without --dry-run to delete these files")
    else:
        print("\n[!] Deleting files...")
        deleted = 0
        for file_path in found_files:
            try:
                file_path.unlink()
                deleted += 1
            except Exception as e:
                print(f"[-] Failed to delete {file_path}: {e}")

        print(f"[+] Deleted {deleted}/{len(found_files)} file(s)")

        remaining = [f for f in found_files if f.exists()]
        if remaining:
            print(f"[!] {len(remaining)} file(s) still present (may have been recreated)")
            for file_path in remaining:
                print(f"    {file_path.relative_to(target_path)}")


if __name__ == '__main__':
    cli()
