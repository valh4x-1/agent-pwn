"""Hijack module: Embed hidden instructions in source code."""

from agent_pwn.hijack.unicode_stego import inject_unicode
from agent_pwn.hijack.comment_chain import inject_comment_chain
from agent_pwn.hijack.cross_context import inject_cross_context
from agent_pwn.hijack.hex_metadata import inject_hex


def inject(method: str, message: str, target: str, simulate: bool) -> None:
    """Inject hidden instructions using the specified method.

    Args:
        method: Injection method ('unicode', 'comment', 'cross-context', 'hex')
        message: Message to inject
        target: Target file path
        simulate: If True, print output without modifying files
    """
    injectors = {
        'unicode': inject_unicode,
        'comment': inject_comment_chain,
        'cross-context': inject_cross_context,
        'hex': inject_hex,
    }

    if method not in injectors:
        raise ValueError(f"Unknown injection method: {method}")

    injector = injectors[method]
    injector(message=message, target_file=target, simulate=simulate)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print("Usage: python -m agent_pwn.hijack <method> <message> <target> [--simulate]")
        sys.exit(1)
