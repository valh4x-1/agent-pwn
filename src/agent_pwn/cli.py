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
@click.option('--output', type=click.Path(), default=None, help='Output file path (default: patient-zero.md)')
@click.option('--simulate', is_flag=True)
def persist(worm_type, target_file, r0, generations, payload, output, simulate):
    """Persistence and worm generators."""
    from agent_pwn.persist import run_persist
    run_persist(worm_type, target_file, r0, generations, payload, simulate, output)


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
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    required=True,
    help='Repository path to scan'
)
@click.option(
    '--exclude',
    multiple=True,
    help='Patterns to exclude from scanning (can be specified multiple times)'
)
def detect(scan_repo, exclude):
    """Scan repositories for instruction injection."""
    from agent_pwn.detect import scan
    exclude_list = list(exclude) if exclude else None
    scan(scan_repo, exclude_patterns=exclude_list)


@cli.command()
@click.option('--dry-run', is_flag=True, help='List files without deleting them')
@click.option('--target-dir', type=click.Path(), default='.', help='Directory to clean (default: current)')
def clean(dry_run, target_dir):
    """Remove agent-pwn marker files from a directory."""
    from pathlib import Path
    import glob

    # Marker file patterns created by agent-pwn
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

    # Find all matching files
    for pattern in marker_patterns:
        # Search in target directory
        matches = list(target_path.glob(pattern))
        found_files.extend(matches)

        # Also search in common subdirectories
        for subdir in ['.agent', '.github', '.cursor']:
            subdir_path = target_path / subdir
            if subdir_path.exists():
                matches = list(subdir_path.glob(pattern))
                found_files.extend(matches)

    # Remove duplicates
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

        # Re-scan to catch any files created between find and delete
        remaining = [f for f in found_files if f.exists()]
        if remaining:
            print(f"[!] {len(remaining)} file(s) still present (may have been recreated)")
            for f in remaining:
                print(f"    {f.relative_to(target_path)}")


if __name__ == '__main__':
    cli()
