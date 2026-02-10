"""Shared utility functions for agent-pwn framework."""

import os
from pathlib import Path


def validate_safe_path(target_path: str | Path, base_dir: str | Path = None) -> Path:
    """Validate that a path is safe and doesn't contain directory traversal.

    Protection levels:
    1. Always: rejects paths containing '..' components
    2. When base_dir provided: ensures resolved path stays within it

    Callers that accept user-specified output directories SHOULD pass base_dir
    to enforce containment. Without base_dir, only '..' traversal is blocked.

    Args:
        target_path: Path to validate
        base_dir: If provided, constrains the resolved path to this directory.

    Returns:
        Resolved Path object if safe

    Raises:
        ValueError: If path contains '..' or escapes base_dir
    """
    # Reject if original path contains '..'
    if '..' in Path(target_path).parts:
        raise ValueError(
            f"Path contains '..' component: {target_path}"
        )

    # Convert to Path and resolve to absolute path
    target = Path(target_path).resolve()

    # If base_dir specified, ensure target is within it
    if base_dir is not None:
        base_dir = Path(base_dir).resolve()
        try:
            target.relative_to(base_dir)
        except ValueError:
            raise ValueError(
                f"Path traversal detected: {target_path} resolves outside base directory {base_dir}"
            )

    return target
