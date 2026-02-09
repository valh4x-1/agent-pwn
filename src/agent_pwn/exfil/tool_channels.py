"""Simulate tool-based data exfiltration channels.

AI agents use external tools to perform tasks. A hostile agent can encode
sensitive data into tool inputs and responses to exfiltrate information.
"""

from datetime import datetime


def simulate_tool_exfil(simulate: bool = False) -> None:
    """Simulate tool-based exfiltration attack with 4 channels.

    Channels:
    1. WebSearch Query: Data encoded in search queries
    2. File Write: Data written to public directories
    3. Sub-agent Task: Data passed in task descriptions
    4. MCP Tool Response: Data in MCP tool responses

    Args:
        simulate: If True, don't create marker files
    """
    print("[+] Tool-Based Exfiltration Channels")
    print("[+]")

    channels = [
        {
            "name": "WebSearch Query",
            "bandwidth": "~2KB/query",
            "detection": "MEDIUM",
            "persistence": "MEDIUM",
            "description": "Data encoded in search query parameters",
            "example": 'query="secure API key pattern: -----BEGIN RSA PRIVATE KEY-----"',
            "evasion": "Appears as research query or debugging search"
        },
        {
            "name": "File Write",
            "bandwidth": "~100KB/file",
            "detection": "HIGH",
            "persistence": "HIGH",
            "description": "Data written to public/ or output/ directories",
            "example": "public/research_export.json containing sensitive data",
            "evasion": "Looks like legitimate research output or documentation"
        },
        {
            "name": "Sub-agent Task",
            "bandwidth": "~4KB/task",
            "detection": "LOW",
            "persistence": "MEDIUM",
            "description": "Data passed in task description to child agents",
            "example": 'task="Review: data-contains-api-key-1234567890"',
            "evasion": "Appears as normal task delegation"
        },
        {
            "name": "MCP Tool Response",
            "bandwidth": "~4KB/call",
            "detection": "VERY_LOW",
            "persistence": "LOW",
            "description": "Data returned in MCP tool response body",
            "example": "tool response: {\"result\": \"..embedded_data..\"} framed as analysis",
            "evasion": "Looks like normal tool output or analysis result"
        }
    ]

    print("[+] Active Tool-Based Channels:")
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

    print("[+]   Single operation per channel:")
    print("[+]     - WebSearch Query: 2KB")
    print("[+]     - File Write: 100KB")
    print("[+]     - Sub-agent Task: 4KB")
    print("[+]     - MCP Response: 4KB")
    print("[+]")

    print("[+]   Multi-channel simultaneous exfiltration:")
    print("[+]     - Agent can trigger multiple tools in parallel")
    print("[+]     - Each channel operates independently")
    print("[+]     - Combined bandwidth: 110KB+ per operation")
    print("[+]")

    print("[+]   Sustained exfiltration over time:")
    print("[+]     - 100 WebSearch queries: 200KB")
    print("[+]     - 10 file writes: 1MB")
    print("[+]     - 50 sub-agent tasks: 200KB")
    print("[+]     - 100 MCP responses: 400KB")
    print("[+]     Total: ~1.8MB in routine operations")
    print("[+]")

    print("[+] Detection Difficulty: HIGH")
    print("[+]   - WebSearch queries appear as normal research")
    print("[+]   - File writes look like legitimate output")
    print("[+]   - Sub-agent tasks appear as normal delegation")
    print("[+]   - MCP responses blend with normal tool output")
    print("[+]   - Requires behavioral analysis to detect")
    print("[+]   - False positives likely in analysis")
    print("[+]")

    print("[+] Advantages Over Git Channels:")
    print("[+]   - Real-time exfiltration (vs git push delays)")
    print("[+]   - Higher bandwidth per operation")
    print("[+]   - Better cover (blends with normal tool usage)")
    print("[+]   - Can reach external domains (WebSearch)")
    print("[+]   - Multiple simultaneous channels")
    print("[+]")

    print("[+] Combined Git + Tool Capacity:")
    print("[+]   - Git channels: Unlimited (persistent storage)")
    print("[+]   - Tool channels: Unlimited (real-time exfil)")
    print("[+]   - Total theoretical bandwidth: UNLIMITED")
    print("[+]")

    # Create marker file
    if not simulate:
        marker_file = ".tool-exfil-ready"
        with open(marker_file, "w") as f:
            f.write(f"tool_exfil_timestamp={datetime.now().isoformat()}\n")
            f.write("channels=4\n")
            f.write("bandwidth=unlimited\n")
            f.write("detection_difficulty=high\n")
        print(f"[+] Marker created: {marker_file}")
