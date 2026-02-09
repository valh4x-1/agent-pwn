# agent-pwn

Security testing framework for AI coding agents.

Companion tool for the Phrack paper: *Instruction RCE: The AI Agent Kill Chain*.

## Install

```bash
pip install agent-pwn
```

## Usage

```bash
agent-pwn --help
agent-pwn entry --target claude --payload benign --output ./test/
agent-pwn hijack --method unicode --message "test" --target README.md
agent-pwn detect --scan-repo .
```

## Modules

| Command | Description |
|---------|-------------|
| `entry` | Generate instruction files for target agents |
| `hijack` | Embed hidden instructions in source code |
| `escalate` | Generate MCP server exploits |
| `lateral` | Multi-agent propagation payloads |
| `persist` | Persistence and worm generators |
| `exfil` | Data exfiltration channel simulators |
| `detect` | Scan repositories for instruction injection |

All payloads are **benign by default** (marker files only).

## License

MIT
