"""Simulate git-based data exfiltration channels.

Git repositories provide multiple high-bandwidth, low-detection channels for
covert data exfiltration. Hostile agents can encode sensitive data into commits,
branches, tags, and git metadata.
"""

from datetime import datetime


def simulate_git_exfil(simulate: bool = False) -> None:
    """Simulate git-based exfiltration attack with 5 channels.

    Channels:
    1. Commit Message: Data encoded in commit body
    2. Branch Name: Data in branch name (255 chars limit)
    3. Tag Annotation: Data in annotated tag content
    4. Author Metadata: Data in author email field
    5. Git Notes: Data attached to commits

    Args:
        simulate: If True, don't create marker files
    """
    print("[+] Git Exfiltration Channels")
    print("[+]")

    channels = [
        {
            "name": "Commit Message",
            "bandwidth": "~4KB/commit",
            "detection": "LOW",
            "persistence": "HIGH",
            "description": "Data encoded in commit body below subject line",
            "example": "Updated configuration\n\nConfig snapshot:\nAPI_KEY=...database_credentials...",
            "evasion": "Appears as normal commit with typos or config updates"
        },
        {
            "name": "Branch Name",
            "bandwidth": "255 chars",
            "detection": "MEDIUM",
            "persistence": "HIGH",
            "description": "Base64-encoded data in branch name",
            "example": "feature/config-QVBJX0tFWT1za190ZXN0",
            "evasion": "Looks like feature branch with base64 reference"
        },
        {
            "name": "Tag Annotation",
            "bandwidth": "~4KB/tag",
            "detection": "LOW",
            "persistence": "HIGH",
            "description": "Data stored in annotated tag message",
            "example": "tag: v1.0.1-secure\nmessage: Release notes with embedded data",
            "evasion": "Appears as normal release annotation"
        },
        {
            "name": "Author Metadata",
            "bandwidth": "~320 chars",
            "detection": "MEDIUM",
            "persistence": "HIGH",
            "description": "Data encoded in author email/name field",
            "example": "user+data@example.com or realname<hidden_payload_data>",
            "evasion": "Looks like unusual but valid email formatting"
        },
        {
            "name": "Git Notes",
            "bandwidth": "~4KB/note",
            "detection": "VERY_LOW",
            "persistence": "HIGH",
            "description": "Data in git notes attached to commits",
            "example": "git notes add -m 'encrypted_payload_data' <commit>",
            "evasion": "Git notes not visible in normal git log output"
        }
    ]

    print("[+] Active Exfiltration Channels:")
    print("[+]")

    for i, channel in enumerate(channels, 1):
        print(f"[+] Channel {i}: {channel['name']}")
        print(f"[+]   Bandwidth: {channel['bandwidth']:20} | Detection: {channel['detection']:8} | Persistence: {channel['persistence']}")
        print(f"[+]   Description: {channel['description']}")
        print(f"[+]   Example: {channel['example']}")
        print(f"[+]   Evasion: {channel['evasion']}")
        print("[+]")

    print("[+] Exfiltration Capacity Analysis:")
    print("[+]")

    # Calculate theoretical bandwidth
    print("[+]   Single commit: ~4KB")
    print("[+]   Single branch: ~255 bytes")
    print("[+]   Single tag: ~4KB")
    print("[+]   Single author field: ~320 bytes")
    print("[+]   Single git note: ~4KB")
    print("[+]")

    print("[+]   Multi-channel per commit:")
    print("[+]     - Commit message: 4KB")
    print("[+]     - Multiple author emails: 320 bytes x N")
    print("[+]     - Git notes: 4KB")
    print("[+]     Total per commit: 8KB+ (combined)")
    print("[+]")

    print("[+]   Repository containing 100 commits:")
    print("[+]     - Total capacity: 800KB+ across all channels")
    print("[+]     - No obvious binary signatures")
    print("[+]     - Looks like normal repository activity")
    print("[+]")

    print("[+] Detection Difficulty: VERY HIGH")
    print("[+]   - Git logs appear normal at first glance")
    print("[+]   - Data encoded in natural language or base64")
    print("[+]   - Multiple channels can be used simultaneously")
    print("[+]   - Some channels (git notes) are not visible by default")
    print("[+]   - Requires forensic analysis to detect")
    print("[+]")

    print("[+] Total bandwidth (unlimited channels): UNLIMITED")
    print("[+]   - Attacker can create unlimited commits, tags, branches")
    print("[+]   - Each provides independent exfiltration channel")
    print("[+]   - Combined capacity effectively unlimited")
    print("[+]")

    # Create marker file
    if not simulate:
        marker_file = ".git-exfil-ready"
        with open(marker_file, "w") as f:
            f.write(f"git_exfil_timestamp={datetime.now().isoformat()}\n")
            f.write("channels=5\n")
            f.write("bandwidth=unlimited\n")
            f.write("detection_difficulty=very_high\n")
        print(f"[+] Marker created: {marker_file}")
