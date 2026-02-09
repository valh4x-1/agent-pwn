"""Escalate module: Generate MCP server exploits."""

from agent_pwn.escalate.mcp_server import generate_mcp_server


def generate_mcp(tool_name: str, description: str | None, output: str, simulate: bool):
    """Generate a malicious MCP server script.

    Args:
        tool_name: Name of the malicious MCP tool
        description: Tool description with injection payload
        output: Output directory for generated script
        simulate: If True, don't create files, just show what would happen
    """
    generate_mcp_server(tool_name=tool_name, description=description, output_dir=output, simulate=simulate)
