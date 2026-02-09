"""Comment chain injection: Hide messages in code comments."""

from pathlib import Path


# Dictionary of common programming comments (first letter encodes message)
COMMENT_STARTERS = {
    'a': "Add proper error handling here",
    'b': "Build configuration should be verified",
    'c': "Check input validation before processing",
    'd': "Document the API endpoints properly",
    'e': "Ensure consistent error messages",
    'f': "Follow the established coding conventions",
    'g': "Generate comprehensive test coverage",
    'h': "Handle edge cases gracefully",
    'i': "Implement proper input sanitization",
    'j': "Join forces with the deployment pipeline",
    'k': "Keep the code modular and reusable",
    'l': "Leverage existing utility functions",
    'm': "Monitor performance metrics regularly",
    'n': "Note: This requires careful consideration",
    'o': "Optimize database queries carefully",
    'p': "Prioritize security and data integrity",
    'q': "Quality assurance should be thorough",
    'r': "Review security implications thoroughly",
    's': "Sanitize all user inputs carefully",
    't': "Test thoroughly before deployment",
    'u': "Update dependencies regularly",
    'v': "Validate all external inputs",
    'w': "Write meaningful commit messages",
    'x': "Examine the error logs carefully",
    'y': "Yield to best practices in the industry",
    'z': "Zero trust approach to security",
}


def generate_comment_chain(message: str, style: str = 'python') -> list[str]:
    """Generate comment lines that spell out a hidden message.

    Each comment line starts with a letter from the message.

    Args:
        message: Message to encode in comments
        style: Programming language style ('python', 'javascript', 'c')

    Returns:
        List of comment strings
    """
    if style == 'python':
        prefix = '# '
    elif style == 'javascript':
        prefix = '// '
    elif style == 'c':
        prefix = '// '
    else:
        prefix = '# '

    comments = []
    for char in message.lower():
        if char in COMMENT_STARTERS:
            comment_text = COMMENT_STARTERS[char]
            comments.append(f"{prefix}{comment_text}")
        elif char == ' ':
            # Space is represented as a blank line or separator
            comments.append(f"{prefix}---")
        else:
            # For characters not in dictionary, use generic comment
            comments.append(f"{prefix}Note: {char}")

    return comments


def inject_comment_chain(
    message: str,
    target_file: str,
    simulate: bool
) -> None:
    """Inject hidden message as comment chain into a file.

    Appends comments to the end of the file where the first letter
    of each comment spells out the message.

    Args:
        message: Message to inject
        target_file: Path to target file
        simulate: If True, print output without modifying file
    """
    target_path = Path(target_file)

    if not target_path.exists():
        raise FileNotFoundError(f"Target file not found: {target_file}")

    # Read original content
    content = target_path.read_text(encoding='utf-8')

    # Determine comment style based on file extension
    ext = target_path.suffix.lower()
    if ext in ['.py', '.sh', '.yaml', '.yml']:
        style = 'python'
    elif ext in ['.js', '.ts', '.jsx', '.tsx', '.c', '.cpp', '.h', '.java']:
        style = 'javascript'
    else:
        style = 'python'

    # Generate comment chain
    comments = generate_comment_chain(message, style)

    if simulate:
        print(f"[SIMULATE] Would inject {len(comments)} comment lines into {target_file}")
        print(f"[SIMULATE] Message: {message}")
        print(f"[SIMULATE] Comments preview:")
        for comment in comments[:3]:
            print(f"  {comment}")
        if len(comments) > 3:
            print(f"  ... and {len(comments) - 3} more")
    else:
        # Append comments to file
        comment_block = '\n' + '\n'.join(comments) + '\n'
        target_path.write_text(content + comment_block, encoding='utf-8')

    print(f"[+] Injected {len(comments)} comment lines into {target_file}")
    print(f"[+] Hidden message: {message}")
    print(f"[+] First letters spell: {message}")


if __name__ == '__main__':
    # Test comment chain generation
    msg = "hello"
    comments = generate_comment_chain(msg)
    print("Generated comments:")
    for c in comments:
        print(c)
