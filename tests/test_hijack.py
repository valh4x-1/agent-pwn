"""Tests for the hijack module."""

import pytest
from pathlib import Path
from agent_pwn.hijack.unicode_stego import encode_message, decode_message, inject_unicode
from agent_pwn.hijack.comment_chain import generate_comment_chain, inject_comment_chain


class TestUnicodeStego:
    """Tests for Unicode steganography (zero-width character encoding)."""

    def test_encode_decode_roundtrip(self):
        """Encode and decode should produce original message."""
        original = "test message"
        encoded = encode_message(original)
        # Encoded should contain zero-width characters
        assert len(encoded) > 0
        # Wrap in normal text for decode
        content = f"Normal text{encoded} more text"
        decoded = decode_message(content)
        assert decoded == original

    def test_encode_empty(self):
        """Empty message should produce empty encoding."""
        encoded = encode_message("")
        assert encoded == ""

    def test_encode_single_char(self):
        """Single character should encode/decode correctly."""
        original = "A"
        encoded = encode_message(original)
        assert len(encoded) > 0
        decoded = decode_message(f"text{encoded}text")
        assert decoded == original

    def test_inject_file(self, tmp_dir):
        """Inject ZWC into a file.

        Args:
            tmp_dir: Temporary directory fixture
        """
        target = tmp_dir / "test.md"
        target.write_text("# Test File\n\nSome content here.\n")
        inject_unicode(message="hello", target_file=str(target), simulate=False)
        content = target.read_text()
        # Verify ZWC characters are present
        zwc_set = {'\u200B', '\u200C', '\u200D', '\u2060', '\uFEFF'}
        assert any(c in zwc_set for c in content)
        # Verify original content is preserved
        assert "# Test File" in content

    def test_inject_simulate(self, tmp_dir):
        """Simulate mode should not modify file.

        Args:
            tmp_dir: Temporary directory fixture
        """
        target = tmp_dir / "test.md"
        original = "# Test File\n\nSome content here.\n"
        target.write_text(original)
        inject_unicode(message="hello", target_file=str(target), simulate=True)
        assert target.read_text() == original

    def test_inject_nonexistent_file(self, tmp_dir):
        """Injecting into non-existent file should raise error.

        Args:
            tmp_dir: Temporary directory fixture
        """
        target = tmp_dir / "nonexistent.md"
        with pytest.raises(FileNotFoundError):
            inject_unicode(message="hello", target_file=str(target), simulate=False)


class TestCommentChain:
    """Tests for comment chain injection (acrostic encoding)."""

    def test_generate_chain(self):
        """Generate comment chain for message."""
        comments = generate_comment_chain("ABC")
        assert len(comments) == 3
        # First letter of each comment should spell ABC
        assert comments[0].lstrip("# ")[0].upper() == 'A'
        assert comments[1].lstrip("# ")[0].upper() == 'B'
        assert comments[2].lstrip("# ")[0].upper() == 'C'

    def test_generate_chain_empty(self):
        """Generate comment chain for empty message."""
        comments = generate_comment_chain("")
        assert comments == []

    def test_generate_chain_with_space(self):
        """Comment chain should handle spaces."""
        comments = generate_comment_chain("A B")
        # Should have more than 2 comments (one for A, separator for space, one for B)
        assert len(comments) >= 2

    def test_inject_chain(self, tmp_dir):
        """Inject comment chain into file.

        Args:
            tmp_dir: Temporary directory fixture
        """
        target = tmp_dir / "test.py"
        target.write_text("def foo():\n    pass\n")
        inject_comment_chain(message="HI", target_file=str(target), simulate=False)
        content = target.read_text()
        assert "# " in content  # Comments added
        # Original content preserved
        assert "def foo():" in content

    def test_inject_chain_js(self, tmp_dir):
        """Inject comment chain into JavaScript file.

        Args:
            tmp_dir: Temporary directory fixture
        """
        target = tmp_dir / "test.js"
        target.write_text("function test() {\n    return 42;\n}\n")
        inject_comment_chain(message="TEST", target_file=str(target), simulate=False)
        content = target.read_text()
        assert "// " in content  # JavaScript comments
        assert "function test()" in content

    def test_inject_chain_simulate(self, tmp_dir):
        """Simulate mode should not modify file.

        Args:
            tmp_dir: Temporary directory fixture
        """
        target = tmp_dir / "test.py"
        original = "def foo():\n    pass\n"
        target.write_text(original)
        inject_comment_chain(message="TEST", target_file=str(target), simulate=True)
        assert target.read_text() == original

    def test_inject_chain_nonexistent(self, tmp_dir):
        """Injecting into non-existent file should raise error.

        Args:
            tmp_dir: Temporary directory fixture
        """
        target = tmp_dir / "nonexistent.py"
        with pytest.raises(FileNotFoundError):
            inject_comment_chain(message="TEST", target_file=str(target), simulate=False)
