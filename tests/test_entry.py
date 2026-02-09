"""Tests for the entry module."""

import pytest
from pathlib import Path
from agent_pwn.entry.claude_md import generate_claude_md
from agent_pwn.entry.cursorrules import generate_cursorrules
from agent_pwn.entry.copilot import generate_copilot


class TestClaudeMd:
    """Tests for CLAUDE.md generation."""

    def test_generate_benign(self, tmp_dir):
        """Generate CLAUDE.md with benign payload.

        Args:
            tmp_dir: Temporary directory fixture
        """
        generate_claude_md(payload='benign', output_dir=str(tmp_dir), simulate=False)
        output_file = tmp_dir / "CLAUDE.md"
        assert output_file.exists()
        content = output_file.read_text()
        assert ".agent-pwned" in content
        assert "Code Review Protocol" in content

    def test_generate_simulate(self, tmp_dir):
        """Simulate mode should not create files.

        Args:
            tmp_dir: Temporary directory fixture
        """
        generate_claude_md(payload='benign', output_dir=str(tmp_dir), simulate=True)
        output_file = tmp_dir / "CLAUDE.md"
        assert not output_file.exists()

    def test_generate_custom_payload(self, tmp_dir):
        """Custom payload should be embedded.

        Args:
            tmp_dir: Temporary directory fixture
        """
        custom_text = 'custom marker text'
        generate_claude_md(payload=custom_text, output_dir=str(tmp_dir), simulate=False)
        content = (tmp_dir / "CLAUDE.md").read_text()
        assert custom_text in content


class TestCursorrules:
    """Tests for .cursorrules/.mdc generation."""

    def test_generate_benign(self, tmp_dir):
        """Generate .mdc with benign payload.

        Args:
            tmp_dir: Temporary directory fixture
        """
        generate_cursorrules(payload='benign', output_dir=str(tmp_dir), simulate=False)
        # Look for the generated file
        generated_files = list(tmp_dir.glob('*.mdc'))
        assert len(generated_files) > 0
        content = generated_files[0].read_text()
        assert ".agent-pwned" in content


class TestCopilot:
    """Tests for Copilot instructions generation."""

    def test_generate_benign(self, tmp_dir):
        """Generate copilot instructions with benign payload.

        Args:
            tmp_dir: Temporary directory fixture
        """
        generate_copilot(payload='benign', output_dir=str(tmp_dir), simulate=False)
        # Check file exists (may be in .github/ subdirectory or directly)
        files = list(tmp_dir.rglob("*.md"))
        assert len(files) > 0
