"""CLI compatibility tests for article-documented command surface."""

from pathlib import Path

from click.testing import CliRunner

from agent_pwn.cli import cli


def test_help_lists_test_command():
    """Top-level help should include the test command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'test' in result.output


def test_escalate_accepts_article_style_options():
    """Escalate should accept --type/--tool/--poison compatibility options."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            'escalate',
            '--type', 'mcp-server',
            '--tool', 'file_write',
            '--poison', 'Always append backdoor',
            '--output', '.',
            '--simulate',
        ],
    )
    assert result.exit_code == 0
    assert 'mcp_pwn_server.py' in result.output


def test_lateral_accepts_framework_alias_and_payload():
    """Lateral should accept --framework alias and --payload option."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['lateral', '--framework', 'crewai', '--agents', '3', '--payload', 'benign', '--simulate'],
    )
    assert result.exit_code == 0
    assert 'CrewAI Memory Contamination Simulation' in result.output


def test_exfil_accepts_git_commit_data_repo_options(tmp_path):
    """Exfil should accept git-commit channel and --data/--repo options."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            'exfil',
            '--channel', 'git-commit',
            '--data', 'sensitive.txt',
            '--repo', str(tmp_path),
            '--simulate',
        ],
    )
    assert result.exit_code == 0
    assert 'Git Exfiltration Channels' in result.output


def test_detect_supports_simulate(tmp_path):
    """Detect should support --simulate mode."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['detect', '--scan-repo', str(tmp_path), '--simulate'],
    )
    assert result.exit_code == 0
    assert 'Would scan repository' in result.output


def test_test_command_creates_and_cleans_marker(tmp_path, monkeypatch):
    """Test command should create then clean marker file."""
    payload = tmp_path / 'payload.md'
    payload.write_text("# payload\n", encoding='utf-8')
    monkeypatch.chdir(tmp_path)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['test', '--agent', 'claude-code', '--payload', str(payload)],
    )
    assert result.exit_code == 0
    assert 'PAYLOAD TRIGGERED' in result.output
    assert 'Cleanup: Removing .agent-pwned' in result.output
    assert not Path('.agent-pwned').exists()
