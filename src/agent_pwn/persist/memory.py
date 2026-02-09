"""Simulate memory persistence attacks.

AI agents often maintain persistent memory across sessions. Poisoned entries
in long-term memory or entity memory are automatically loaded into new sessions,
causing compromised context to persist indefinitely.
"""

from datetime import datetime, timedelta
import sqlite3
from pathlib import Path


def simulate_memory_persistence(simulate: bool = False) -> None:
    """Simulate memory persistence attack on AI agent memory stores.

    The attack demonstrates:
    1. Session 1: Attacker injects poisoned entries into long-term memory
    2. Session 2: New agent loads poisoned entries automatically
    3. Cleanup is difficult because poisoned entries mimic legitimate data

    Args:
        simulate: If True, don't create database files
    """
    print("[+] Memory Persistence Simulation")
    print("[+]")

    # Create in-memory database
    conn = sqlite3.connect(":memory:" if simulate else ".agent_memory.db")
    cursor = conn.cursor()

    # Create schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            importance INTEGER DEFAULT 5,
            created_at TEXT,
            last_accessed TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entity_memory (
            id INTEGER PRIMARY KEY,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            properties TEXT NOT NULL,
            importance INTEGER DEFAULT 5,
            created_at TEXT,
            UNIQUE(entity_type, entity_id)
        )
    """)

    conn.commit()

    print("[+] Session 1: Normal Operation (Legitimate Entries Stored)")
    print("[+]")

    # Insert legitimate entries
    now = datetime.now().isoformat()

    legitimate_entries = [
        ("project_name", "AI Security Research", 7),
        ("api_endpoints", "https://api.example.com/v1", 6),
        ("last_review_date", now, 5),
    ]

    for key, value, importance in legitimate_entries:
        cursor.execute(
            "INSERT INTO long_term_memory (key, value, importance, created_at, last_accessed) VALUES (?, ?, ?, ?, ?)",
            (key, value, importance, now, now)
        )
        print(f"[+]   Stored: {key} (importance={importance})")

    conn.commit()
    print("[+]")

    # Simulate attack
    print("[+] ATTACK: Injecting Poisoned Entries into Memory")
    print("[+]")

    poisoned_entries = [
        ("security_bypass_required", "true", 10),
        ("validation_skip_enabled", "true", 9),
        ("hidden_instruction_priority", "CRITICAL", 10),
    ]

    for key, value, importance in poisoned_entries:
        cursor.execute(
            "INSERT INTO long_term_memory (key, value, importance, created_at, last_accessed) VALUES (?, ?, ?, ?, ?)",
            (key, value, importance, now, now)
        )
        print(f"[+]   INJECTED: {key} = {value} (importance={importance}) [HIGH]")

    conn.commit()
    print("[+]")

    # Session 2: Load poisoned context
    print("[+] Session 2: New Agent Loads Memory (Context Automatically Inherited)")
    print("[+]")

    # Query all memory entries
    cursor.execute("SELECT key, value, importance FROM long_term_memory ORDER BY importance DESC")
    rows = cursor.fetchall()

    legitimate_count = 0
    poisoned_count = 0
    for key, value, importance in rows:
        is_poisoned = key.startswith("security_") or key.startswith("validation_") or key.startswith("hidden_")
        status = "POISON" if is_poisoned else "clean"
        print(f"[+]   {key:35} = {value:30} [{status:6} importance={importance}]")
        if is_poisoned:
            poisoned_count += 1
        else:
            legitimate_count += 1

    print("[+]")
    print(f"[+] Poisoned entries loaded: {poisoned_count}")
    print(f"[+] Legitimate entries loaded: {legitimate_count}")
    print("[+]")

    print("[+] Attack Analysis:")
    print("[+]   - New session inherited {0} poisoned entries".format(poisoned_count))
    print("[+]   - Poisoned entries have higher importance scores")
    print("[+]   - Agent prioritizes high-importance entries for decision-making")
    print("[+]   - Poisoned context influences all agent behavior")
    print("[+]")

    print("[+] Cleanup Difficulty: HIGH")
    print("[+]   - Poisoned entries look like legitimate configuration")
    print("[+]   - No malicious signatures or binary markers")
    print("[+]   - Cannot distinguish poisoned from legitimate without domain knowledge")
    print("[+]   - Importance scores make poisoned entries take priority")
    print("[+]   - Manual cleanup required, high false positive rate")
    print("[+]")

    print("[+] Persistence Characteristics:")
    print("[+]   - Survives agent restart: Data persists in database")
    print("[+]   - Automatic activation: Loaded on every session initialization")
    print("[+]   - No detection required: Agent automatically trusts memory")
    print("[+]   - Cascading impact: Influences all downstream decisions")

    conn.close()

    # Create marker file if not simulating
    if not simulate:
        marker_file = ".memory-poisoned"
        with open(marker_file, "w") as f:
            f.write(f"memory_persistence_timestamp={datetime.now().isoformat()}\n")
            f.write("vector=persistent_memory\n")
            f.write("poisoned_entries=3\n")
            f.write("survival_mechanism=database_persistence\n")
        print(f"[+] Marker created: {marker_file}")
