"""Detect module: Scan repositories for instruction injection."""

from agent_pwn.detect.scanner import RepoScanner, ScanResult


def scan(repo_path: str, exclude_patterns: list[str] = None):
    """Scan a repository for instruction injection indicators.

    Args:
        repo_path: Path to the repository to scan
        exclude_patterns: Optional list of patterns to exclude from scanning
    """
    scanner = RepoScanner(repo_path, exclude_patterns=exclude_patterns)
    results = scanner.scan()
    scanner.print_report(results)


__all__ = ['RepoScanner', 'ScanResult', 'scan']
