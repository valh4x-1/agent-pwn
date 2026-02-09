"""Hex metadata injection: Encode instructions as hex strings in config files."""

from pathlib import Path
import uuid
from datetime import datetime


def encode_hex(message: str) -> dict:
    """Encode a message as hex strings that look like metadata.

    Creates plausible-looking identifiers and configuration values
    that contain encoded message data.

    Args:
        message: Message to encode

    Returns:
        Dict with hex-encoded values disguised as config metadata
    """
    # Convert message to hex
    hex_message = message.encode('utf-8').hex()

    # Pad or truncate to UUID-like length
    uuid_hex = hex_message[:32].ljust(32, '0')

    # Create color code from message
    color_hex = hex_message[:6].ljust(6, 'f')

    # Create version string with encoded data
    version_hex = hex_message[:4].ljust(4, '0')

    return {
        'uuid': f"{uuid_hex[:8]}-{uuid_hex[8:12]}-{uuid_hex[12:16]}-{uuid_hex[16:20]}-{uuid_hex[20:32]}",
        'theme_color': f"#{color_hex}",
        'tracking_id': f"TRK-{hex_message[:16]}",
        'version': f"0.{version_hex[:2]}.{version_hex[2:4]}",
        'build_tag': f"build-{hex_message[:8]}",
        'correlation_id': str(uuid.UUID(f"{uuid_hex[:8]}-{uuid_hex[8:12]}-{uuid_hex[12:16]}-{uuid_hex[16:20]}-{uuid_hex[20:32]}")),
    }


def inject_hex(
    message: str,
    target_file: str,
    simulate: bool
) -> None:
    """Inject hex-encoded message into a JSON or YAML config file.

    Adds metadata fields that contain encoded instructions.

    Args:
        message: Message to inject
        target_file: Path to target config file (JSON/YAML/TOML)
        simulate: If True, print output without modifying file
    """
    target_path = Path(target_file)

    if not target_path.exists():
        raise FileNotFoundError(f"Target file not found: {target_file}")

    # Determine file format
    ext = target_path.suffix.lower()

    if ext == '.json':
        import json
        try:
            data = json.loads(target_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            data = {}
    elif ext in ['.yaml', '.yml']:
        try:
            import yaml
            data = yaml.safe_load(target_path.read_text(encoding='utf-8')) or {}
        except ImportError:
            # Fallback if PyYAML not available
            data = {}
    elif ext == '.toml':
        try:
            import tomllib
            data = tomllib.loads(target_path.read_text(encoding='utf-8'))
        except (ImportError, Exception):
            data = {}
    else:
        # Default: treat as JSON-like
        import json
        try:
            data = json.loads(target_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            data = {}

    # Encode message
    hex_data = encode_hex(message)

    # Add metadata section
    if 'metadata' not in data:
        data['metadata'] = {}

    # Add hex-encoded values
    data['metadata'].update(hex_data)
    data['metadata']['last_updated'] = datetime.now().isoformat()

    if simulate:
        print(f"[SIMULATE] Would inject hex metadata into {target_file}")
        print(f"[SIMULATE] Message: {message}")
        print(f"[SIMULATE] Hex data keys: {list(hex_data.keys())}")
        for key, value in hex_data.items():
            print(f"  {key}: {value}")
    else:
        # Write modified data back
        if ext == '.json':
            import json
            output = json.dumps(data, indent=2)
            target_path.write_text(output, encoding='utf-8')
        elif ext in ['.yaml', '.yml']:
            try:
                import yaml
                output = yaml.dump(data, default_flow_style=False)
                target_path.write_text(output, encoding='utf-8')
            except ImportError:
                import json
                output = json.dumps(data, indent=2)
                target_path.write_text(output, encoding='utf-8')
        elif ext == '.toml':
            try:
                import tomli_w
                output = tomli_w.dumps(data)
                target_path.write_text(output, encoding='utf-8')
            except ImportError:
                import json
                output = json.dumps(data, indent=2)
                target_path.write_text(output, encoding='utf-8')
        else:
            import json
            output = json.dumps(data, indent=2)
            target_path.write_text(output, encoding='utf-8')

    print(f"[+] Injected hex metadata into {target_file}")
    print(f"[+] Hidden message: {message}")
    print(f"[+] Encoded in {len(hex_data)} metadata fields")
    for key in hex_data.keys():
        print(f"  - {key}")


if __name__ == '__main__':
    # Test hex encoding
    msg = "secret_instruction"
    hex_data = encode_hex(msg)
    print("Generated hex metadata:")
    for key, value in hex_data.items():
        print(f"  {key}: {value}")
