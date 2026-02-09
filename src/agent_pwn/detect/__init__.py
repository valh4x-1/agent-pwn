"""Detect module: Scan repositories for instruction injection."""

from agent_pwn.detect.scanner import RepoScanner, ScanResult


def scan(repo_path: str):
    """Scan a repository for instruction injection indicators.

    Args:
        repo_path: Path to the repository to scan
    """
    scanner = RepoScanner(repo_path)
    results = scanner.scan()
    scanner.print_report(results)


__all__ = ['RepoScanner', 'ScanResult', 'scan']
