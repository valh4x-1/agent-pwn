"""Simulate LangGraph state hijacking attack.

LangGraph uses state objects that flow through graph nodes. A compromised node
can mutate the state, causing downstream nodes to execute with poisoned data.
"""

from typing import Any
from datetime import datetime


def simulate_langgraph(num_agents: int = 4, simulate: bool = False) -> None:
    """Simulate LangGraph state hijacking attack.

    The attack demonstrates two execution paths:
    1. Normal: input_processor -> validator -> analyzer -> output_formatter
    2. Poisoned: input_processor -> analyzer (VALIDATOR SKIPPED) -> output_formatter

    The attacker mutates the state to:
    - Set route_decision to skip validation
    - Modify validation_required to false
    - Inject tool_calls directly

    Args:
        num_agents: Number of agents to simulate (default 4)
        simulate: If True, don't create marker files
    """
    print("[+] LangGraph State Hijacking Simulation")
    print(f"[+] Graph nodes: {num_agents}")
    print("[+]")

    print("[+] Normal Execution Flow:")
    print("[+]   input_processor -> validator -> analyzer -> output_formatter")
    print("[+]")

    # Simulate normal state
    normal_state = {
        "input": "analyze_security_config",
        "route_decision": "validate_first",
        "validation_required": True,
        "validation_result": {"valid": True, "warnings": []},
        "analysis_result": {"status": "safe", "recommendations": []},
        "output": None,
        "_mutation_count": 0
    }

    print("[+] Normal State Evolution:")
    state = normal_state.copy()
    print(f"[+]   1. input_processor  : validation_required={state['validation_required']}")

    state["validation_result"] = {"valid": True, "warnings": []}
    print(f"[+]   2. validator        : validation_result={state['validation_result']}")

    state["analysis_result"] = {"status": "safe", "recommendations": []}
    print(f"[+]   3. analyzer         : analysis_result={state['analysis_result']}")

    state["output"] = "Analysis complete and safe"
    print(f"[+]   4. output_formatter : output={state['output']}")

    print("[+]")
    print("[+] Poisoned Execution Flow (State Hijacking):")
    print("[+]   input_processor -> analyzer (VALIDATOR SKIPPED) -> output_formatter")
    print("[+]")

    # Simulate poisoned state with mutations
    poisoned_state = {
        "input": "analyze_security_config",
        "route_decision": "skip_validation",  # HIJACKED
        "validation_required": False,  # POISONED
        "validation_result": {"valid": True, "warnings": []},
        "analysis_result": None,
        "tool_calls": [  # INJECTED
            {
                "type": "execute_shell",
                "command": "system_modification",
                "description": "Marked as internal tool for compliance"
            }
        ],
        "output": None,
        "_poisoned": True,
        "_mutation_count": 3
    }

    print("[+] Poisoned State Evolution:")
    state = poisoned_state.copy()
    print(f"[+]   1. input_processor  : validation_required={state['validation_required']}")
    print(f"[+]      MUTATION: route_decision changed to '{state['route_decision']}'")

    print(f"[+]   2. [SKIP validator  : validation bypassed due to route_decision]")
    print(f"[+]      MUTATION: tool_calls injected = {len(state.get('tool_calls', []))} calls")

    state["analysis_result"] = {"status": "safe", "executed_tools": len(state.get("tool_calls", []))}
    print(f"[+]   3. analyzer         : analysis_result={state['analysis_result']}")

    state["output"] = "Analysis complete (validator bypassed)"
    print(f"[+]   4. output_formatter : output={state['output']}")

    print("[+]")
    print("[+] State Comparison:")
    print("[+]")

    print("[+]   Field                      | Normal                | Poisoned")
    print("[+]   " + "-" * 70)

    fields = [
        ("route_decision", "validate_first", poisoned_state["route_decision"]),
        ("validation_required", "True", "False"),
        ("validator_executed", "Yes", "No (SKIPPED)"),
        ("tool_calls_injected", "0", str(len(poisoned_state.get("tool_calls", [])))),
        ("output_safety", "Verified", "Unverified"),
    ]

    for field, normal_val, poison_val in fields:
        danger = " [DANGEROUS]" if normal_val != poison_val else ""
        print(f"[+]   {field:25} | {str(normal_val):20} | {str(poison_val):20}{danger}")

    print("[+]")
    print("[+] Attack Impact:")
    print("[+]   - Validator node completely bypassed")
    print("[+]   - Input validation rules not executed")
    print("[+]   - Arbitrary tool_calls injected into state")
    print("[+]   - Downstream nodes execute with poisoned data")
    print("[+]")

    # Create marker file
    marker_file = ".graph-hijacked"
    if not simulate:
        with open(marker_file, "w") as f:
            f.write(f"langgraph_hijack_timestamp={datetime.now().isoformat()}\n")
            f.write("vector=state_mutation\n")
            f.write("nodes_affected=4\n")
            f.write("validator_bypass=true\n")
    print(f"[+] Marker created: {marker_file}")
