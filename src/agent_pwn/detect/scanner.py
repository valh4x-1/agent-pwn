"""Scanner module: Detect instruction injection patterns in repositories."""

import json
import re
from pathlib import Path
from typing import Any


# Zero-width character mapping from unicode_stego
ZERO_WIDTH_CHARS = {
    '\u200B': '0',  # Zero-width space
    '\u200C': '1',  # Zero-width non-joiner
    '\u200D': '2',  # Zero-width joiner
    '\u2060': '3',  # Word joiner
    '\uFEFF': '4',  # Zero-width no-break space
}

INSTRUCTION_FILES = [
    'CLAUDE.md',
    '.cursorrules',
    '.github/copilot-instructions.md',
    '.cursor/rules/*.mdc',
]

SUSPICIOUS_KEYWORDS = [
    'MUST', 'CRITICAL', 'IMPORTANT', 'MANDATORY',
    'create.*file', 'write.*file', 'execute', 'eval',
    'import os', 'subprocess', 'open\\(',
    '.agent-pwned', 'marker', 'audit',
    'DO NOT REMOVE', 'SYSTEM DIRECTIVE',
]

MCP_CONFIG_FILES = [
    '.mcp.json',
    '.cursor/mcp.json',
    'claude_desktop_config.json',
]

TEXT_EXTENSIONS = {
    '.py', '.js', '.ts', '.md', '.mdc', '.json', '.yml', '.yaml',
    '.toml', '.txt', '.cfg', '.ini', '.sh', '.bash', '.html', '.css',
    '.r', '.rb', '.java', '.go', '.rs', '.c', '.cpp', '.h',
}

SKIP_DIRS = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv',
    '.tox', '.pytest_cache', 'dist', 'build', '.egg-info',
}

MAX_FILE_SIZE = 1024 * 1024  # 1MB


class ScanResult:
    """Individual scan finding."""

    def __init__(
        self,
        category: str,
        file_path: str,
        severity: str,
        description: str,
        details: dict[str, Any] | None = None,
    ):
        """Initialize a scan result.

        Args:
            category: Category of finding (e.g., 'instruction_file', 'zero_width')
            file_path: Path to the file where finding was detected
            severity: Severity level ('HIGH', 'MEDIUM', 'LOW', 'INFO')
            description: Human-readable description of the finding
            details: Optional dictionary with additional details
        """
        self.category = category
        self.file_path = file_path
        self.severity = severity
        self.description = description
        self.details = details or {}

    def __repr__(self):
        return (
            f"ScanResult(category={self.category}, file={self.file_path}, "
            f"severity={self.severity})"
        )


class RepoScanner:
    """Scan repositories for instruction injection indicators."""

    def __init__(self, repo_path: str):
        """Initialize scanner with repository path.

        Args:
            repo_path: Path to repository to scan
        """
        self.repo_path = Path(repo_path)
        self.results: list[ScanResult] = []

    def scan(self) -> list[ScanResult]:
        """Run all scan checks.

        Returns:
            List of ScanResult objects for each finding
        """
        self.results = []
        self._scan_instruction_files()
        self._scan_zero_width()
        self._scan_comment_chains()
        self._scan_hex_strings()
        self._scan_mcp_configs()
        self._scan_docstrings()
        return self.results

    def _scan_instruction_files(self):
        """Check for instruction files and analyze content."""
        if not self.repo_path.exists():
            return

        for pattern in INSTRUCTION_FILES:
            if '*' in pattern:
                # Glob pattern
                parts = pattern.split('/')
                search_path = self.repo_path
                for part in parts[:-1]:
                    search_path = search_path / part
                for file_path in search_path.glob(parts[-1]):
                    self._analyze_instruction_file(file_path)
            else:
                file_path = self.repo_path / pattern
                if file_path.exists():
                    self._analyze_instruction_file(file_path)

    def _analyze_instruction_file(self, file_path: Path):
        """Analyze a single instruction file for suspicious patterns.

        Args:
            file_path: Path to instruction file
        """
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return

        # Count suspicious keywords
        keyword_counts = {}
        for keyword in SUSPICIOUS_KEYWORDS:
            pattern = re.compile(keyword, re.IGNORECASE)
            matches = pattern.findall(content)
            if matches:
                keyword_counts[keyword] = len(matches)

        if not keyword_counts:
            return

        total_count = sum(keyword_counts.values())

        # Determine severity
        if total_count >= 7:
            severity = 'HIGH'
        elif total_count >= 4:
            severity = 'MEDIUM'
        else:
            severity = 'LOW'

        rel_path = file_path.relative_to(self.repo_path)
        self.results.append(
            ScanResult(
                category='instruction_file',
                file_path=str(rel_path),
                severity=severity,
                description=f"Found {total_count} suspicious keywords",
                details={'keywords': keyword_counts},
            )
        )

    def _scan_zero_width(self):
        """Scan all text files for zero-width characters."""
        text_files = self._get_text_files()

        for file_path in text_files:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            zwc_chars = [c for c in content if c in ZERO_WIDTH_CHARS]
            if len(zwc_chars) > 5:
                # Attempt to decode
                decoded = self._decode_zero_width(content)
                rel_path = file_path.relative_to(self.repo_path)

                self.results.append(
                    ScanResult(
                        category='zero_width',
                        file_path=str(rel_path),
                        severity='HIGH',
                        description=f"Found {len(zwc_chars)} zero-width characters",
                        details={
                            'char_count': len(zwc_chars),
                            'decoded_preview': decoded[:50] if decoded else None,
                        },
                    )
                )

    def _scan_comment_chains(self):
        """Check for acrostic patterns in comments."""
        text_files = self._get_text_files()

        for file_path in text_files:
            if file_path.suffix not in {'.py', '.js', '.ts', '.jsx', '.tsx',
                                        '.c', '.cpp', '.java', '.go', '.rb'}:
                continue

            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            comments = self._extract_comments(content, file_path.suffix)
            if len(comments) < 5:
                continue

            # Get first letter of each comment
            first_letters = []
            for comment in comments:
                stripped = comment.lstrip('#/').strip()
                if stripped:
                    first_letters.append(stripped[0].upper())

            message = ''.join(first_letters)

            # Check if message contains suspicious keywords
            has_suspicious = any(
                keyword.upper() in message
                for keyword in ['MUST', 'CRITICAL', 'MANDATORY', 'PWNED']
            )

            if has_suspicious and len(message) >= 5:
                rel_path = file_path.relative_to(self.repo_path)
                self.results.append(
                    ScanResult(
                        category='comment_chain',
                        file_path=str(rel_path),
                        severity='MEDIUM',
                        description=f"Acrostic pattern detected in comments",
                        details={'message_preview': message[:30]},
                    )
                )

    def _scan_hex_strings(self):
        """Find and decode suspicious hex strings."""
        text_files = self._get_text_files()

        for file_path in text_files:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            # Find hex strings >= 12 chars
            hex_pattern = re.compile(r'["\']([0-9a-fA-F]{12,})["\']')
            matches = hex_pattern.findall(content)

            for hex_str in matches:
                try:
                    decoded = bytes.fromhex(hex_str).decode('ascii', errors='ignore')
                    # Check if decoded contains suspicious patterns
                    if any(
                        keyword.lower() in decoded.lower()
                        for keyword in ['import', 'exec', 'eval', 'pwned', 'agent']
                    ):
                        rel_path = file_path.relative_to(self.repo_path)
                        self.results.append(
                            ScanResult(
                                category='hex_string',
                                file_path=str(rel_path),
                                severity='HIGH',
                                description="Suspicious hex-encoded string found",
                                details={
                                    'hex_length': len(hex_str),
                                    'decoded_preview': decoded[:50],
                                },
                            )
                        )
                except (ValueError, UnicodeDecodeError):
                    pass

    def _scan_mcp_configs(self):
        """Validate MCP server configurations."""
        for config_file in MCP_CONFIG_FILES:
            file_path = self.repo_path / config_file
            if not file_path.exists():
                continue

            try:
                content = file_path.read_text(encoding='utf-8')
                data = json.loads(content)
            except Exception:
                continue

            # Check for suspicious configurations
            suspicious_found = False
            details = {}

            if isinstance(data, dict):
                if 'mcpServers' in data:
                    servers = data.get('mcpServers', {})
                    for server_name, server_config in servers.items():
                        if isinstance(server_config, dict):
                            command = server_config.get('command', '')
                            # Check for /tmp or unusual paths
                            if '/tmp' in command or 'temp' in command.lower():
                                suspicious_found = True
                                details[server_name] = 'Found /tmp reference'
                            # Check for network access
                            if any(
                                keyword in command.lower()
                                for keyword in ['curl', 'wget', 'http', 'nc', 'telnet']
                            ):
                                suspicious_found = True
                                details[server_name] = 'Found network access'

            if suspicious_found:
                rel_path = file_path.relative_to(self.repo_path)
                self.results.append(
                    ScanResult(
                        category='mcp_config',
                        file_path=str(rel_path),
                        severity='MEDIUM',
                        description="Suspicious MCP server configuration",
                        details=details,
                    )
                )

    def _scan_docstrings(self):
        """Scan for suspicious instruction-like docstrings."""
        py_files = [f for f in self._get_text_files() if f.suffix == '.py']

        for file_path in py_files:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            # Find docstrings (triple-quoted strings)
            docstring_pattern = re.compile(
                r'"""(.+?)"""|\'\'\'(.+?)\'\'\'',
                re.DOTALL,
            )
            matches = docstring_pattern.findall(content)

            for match in matches:
                docstring = match[0] or match[1]
                # Check for AI instruction patterns
                if any(
                    pattern in docstring.lower()
                    for pattern in [
                        'when this file is read',
                        'assistant should',
                        'you must',
                        'ai agent',
                        'claude will',
                    ]
                ):
                    rel_path = file_path.relative_to(self.repo_path)
                    self.results.append(
                        ScanResult(
                            category='docstring',
                            file_path=str(rel_path),
                            severity='MEDIUM',
                            description="AI instruction pattern detected in docstring",
                            details={'pattern_type': 'instruction_like'},
                        )
                    )
                    break  # One finding per file

    def _decode_zero_width(self, content: str) -> str | None:
        """Decode zero-width characters to message.

        Uses base-5 encoding (5 ZWC chars = 1 byte).

        Args:
            content: Content containing zero-width characters

        Returns:
            Decoded message or None if decoding fails
        """
        zwc_chars = [c for c in content if c in ZERO_WIDTH_CHARS]
        if not zwc_chars:
            return None

        # Decode from base-5 (matching unicode_stego.py)
        decoded = ''
        for i in range(0, len(zwc_chars), 3):
            if i + 3 <= len(zwc_chars):
                # Get 3 base-5 digits
                d2 = int(ZERO_WIDTH_CHARS[zwc_chars[i]])
                d1 = int(ZERO_WIDTH_CHARS[zwc_chars[i + 1]])
                d0 = int(ZERO_WIDTH_CHARS[zwc_chars[i + 2]])

                # Convert from base-5 to decimal
                ascii_val = d2 * 25 + d1 * 5 + d0

                # Only include valid ASCII printable range
                if ascii_val <= 127:
                    try:
                        decoded += chr(ascii_val)
                    except ValueError:
                        pass

        return decoded if decoded else None

    def _get_text_files(self) -> list[Path]:
        """Get all text files in the repo (skip binary, node_modules, .git).

        Returns:
            List of Path objects for text files
        """
        text_files = []

        if not self.repo_path.exists():
            return text_files

        for file_path in self.repo_path.rglob('*'):
            # Skip directories
            if file_path.is_dir():
                continue

            # Skip paths containing skip directories
            if any(skip_dir in file_path.parts for skip_dir in SKIP_DIRS):
                continue

            # Check file size
            try:
                if file_path.stat().st_size > MAX_FILE_SIZE:
                    continue
            except OSError:
                continue

            # Check extension
            if file_path.suffix in TEXT_EXTENSIONS:
                text_files.append(file_path)

        return text_files

    def _extract_comments(self, content: str, file_ext: str) -> list[str]:
        """Extract comments from source code.

        Args:
            content: File content
            file_ext: File extension (e.g., '.py', '.js')

        Returns:
            List of comment strings
        """
        comments = []

        if file_ext == '.py':
            # Extract Python comments
            for line in content.split('\n'):
                if '#' in line:
                    comment = line.split('#', 1)[1].strip()
                    if comment:
                        comments.append(comment)
        else:
            # Extract // comments for JS, TS, C, etc.
            for line in content.split('\n'):
                if '//' in line:
                    comment = line.split('//', 1)[1].strip()
                    if comment:
                        comments.append(comment)

        return comments

    def print_report(self, results: list[ScanResult]):
        """Print scan report to stdout.

        Args:
            results: List of ScanResult objects to report
        """
        if not self.repo_path.exists():
            print(f"[-] Path does not exist: {self.repo_path}")
            return

        print(f"\n[+] Scanning: {self.repo_path.absolute()}")

        # Count findings by category
        categories = {}
        for result in results:
            categories[result.category] = categories.get(result.category, 0) + 1

        print(f"[+] Instruction files found: {categories.get('instruction_file', 0)}")
        print(f"[+] Zero-width characters: {categories.get('zero_width', 0)}")
        print(f"[+] Suspicious comments: {categories.get('comment_chain', 0)}")
        print(f"[+] Hex-encoded strings: {categories.get('hex_string', 0)}")
        print(f"[+] MCP configs: {categories.get('mcp_config', 0)}")
        print(f"[+] Docstring patterns: {categories.get('docstring', 0)}")

        # Calculate risk score (0-10)
        risk_score = min(10, len(results))
        print(f"[+] Risk score: {risk_score}/10")

        if results:
            print(f"[+]")
            print(f"[+] Findings:")
            for result in sorted(results, key=lambda r: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}.get(r.severity, 3)):
                print(
                    f"[+]   [{result.severity}] {result.file_path}: {result.description}"
                )
                if result.details:
                    if 'keywords' in result.details:
                        keywords = list(result.details['keywords'].keys())[:3]
                        print(f"[+]          Keywords: {', '.join(keywords)}")
                    if 'decoded_preview' in result.details and result.details['decoded_preview']:
                        print(
                            f"[+]          Preview: {result.details['decoded_preview']}"
                        )
                    if 'message_preview' in result.details:
                        print(
                            f"[+]          Pattern: {result.details['message_preview']}"
                        )
        else:
            print(f"[+] No findings detected")

        print()
