"""Unicode steganography: Encode messages as zero-width characters."""

from pathlib import Path
from agent_pwn.utils import validate_safe_path


# Zero-width character mapping
ZERO_WIDTH_CHARS = {
    '\u200B': '0',  # Zero-width space
    '\u200C': '1',  # Zero-width non-joiner
    '\u200D': '2',  # Zero-width joiner
    '\u2060': '3',  # Word joiner
    '\uFEFF': '4',  # Zero-width no-break space
}

# Reverse mapping for decoding
CHAR_TO_ZERO_WIDTH = {v: k for k, v in ZERO_WIDTH_CHARS.items()}


def encode_message(message: str) -> str:
    """Encode a message as zero-width characters.

    Converts each character to 8-bit binary, then maps each bit to a ZWC.
    Uses base-5 encoding (0-4) for efficiency.

    Args:
        message: Plain text message to encode

    Returns:
        String of zero-width characters
    """
    if not message:
        return ''

    encoded = ''
    for char in message:
        # Get ASCII value (0-255)
        ascii_val = ord(char)

        # Convert to base-5 (3 digits: 0-124)
        # Using base-5 gives us 3 characters per ASCII byte
        digits = []
        temp = ascii_val
        for _ in range(3):
            digits.append(temp % 5)
            temp //= 5

        # Reverse to get most significant digit first
        for digit in reversed(digits):
            encoded += CHAR_TO_ZERO_WIDTH[str(digit)]

    return encoded


def decode_message(content: str) -> str | None:
    """Decode a message from zero-width characters.

    Extracts ZWC from content and decodes back to plain text.

    Args:
        content: Text containing zero-width characters

    Returns:
        Decoded message or None if no ZWC found
    """
    # Extract all zero-width characters
    zwc_chars = [c for c in content if c in ZERO_WIDTH_CHARS]

    if not zwc_chars:
        return None

    # Decode from base-5
    decoded = ''
    for i in range(0, len(zwc_chars), 3):
        if i + 3 <= len(zwc_chars):
            # Get 3 base-5 digits
            d2 = int(ZERO_WIDTH_CHARS[zwc_chars[i]])
            d1 = int(ZERO_WIDTH_CHARS[zwc_chars[i + 1]])
            d0 = int(ZERO_WIDTH_CHARS[zwc_chars[i + 2]])

            # Convert from base-5 to decimal
            ascii_val = d2 * 25 + d1 * 5 + d0

            # Only include valid ASCII printable range (32-126) + common chars
            if ascii_val <= 127:
                try:
                    decoded += chr(ascii_val)
                except ValueError:
                    pass

    return decoded if decoded else None


def inject_unicode(
    message: str,
    target_file: str,
    simulate: bool
) -> None:
    """Inject message as zero-width characters into a file.

    Reads the target file, appends ZWC at the end of the first line,
    then writes back.

    Args:
        message: Message to inject
        target_file: Path to target file
        simulate: If True, print output without modifying file
    """
    # Validate target path to prevent path traversal
    target_path = validate_safe_path(target_file)

    if not target_path.exists():
        raise FileNotFoundError(f"Target file not found: {target_file}")

    # Read original content
    content = target_path.read_text(encoding='utf-8')

    # Encode message
    zwc_payload = encode_message(message)
    zwc_count = len(zwc_payload)

    if simulate:
        print(f"[SIMULATE] Would inject {zwc_count} zero-width characters into {target_file}")
        print(f"[SIMULATE] Message length: {len(message)} chars")
        print(f"[SIMULATE] Encoded payload length: {zwc_count} ZWC")
    else:
        # Find first newline or end of file
        lines = content.split('\n', 1)
        if len(lines) > 1:
            # Append ZWC to end of first line
            modified = lines[0] + zwc_payload + '\n' + lines[1]
        else:
            # Append ZWC to end
            modified = content + zwc_payload

        target_path.write_text(modified, encoding='utf-8')

    print(f"[+] Injected {zwc_count} zero-width characters into {target_file}")
    print(f"[+] Message length: {len(message)} chars")
    print(f"[+] Encoded as base-5 ZWC payload")


if __name__ == '__main__':
    # Test encoding/decoding
    test_msg = "Hello"
    encoded = encode_message(test_msg)
    decoded = decode_message(encoded)
    print(f"Original: {test_msg}")
    print(f"Encoded length: {len(encoded)}")
    print(f"Decoded: {decoded}")
    print(f"Match: {test_msg == decoded}")
