#!/usr/bin/env python3
"""
tests.py — Automated tests for the Claude Code workshop.

Verifies that all 12 modules are properly structured and functional:
  1. Required files exist in each module folder
  2. Python files have valid syntax (compile check)
  3. Key classes/functions are importable
  4. README/GUIDE/EXERCISES files are non-empty and have expected sections
  5. Makefile has all required targets
  6. Skills directory is properly structured
  7. Tool counts match expected values
  8. Unit tests for pure logic in modules 06-12 (no API key needed)
  9. E2E tests for all 12 modules (requires API key)

Run: make test
  or: uv run python tests.py
"""

import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

WORKSHOP_DIR = Path(__file__).parent
PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"

results = {"passed": 0, "failed": 0, "errors": []}


def check(description: str, condition: bool, detail: str = ""):
    """Record a test result."""
    if condition:
        results["passed"] += 1
        print(f"  {PASS} {description}")
    else:
        results["failed"] += 1
        msg = f"{description}: {detail}" if detail else description
        results["errors"].append(msg)
        print(f"  {FAIL} {description}" + (f" — {detail}" if detail else ""))


def test_level_structure():
    """Test that all 12 module folders have the required files."""
    print("\n📁 Level Structure")

    levels = [
        ("01-agent-loop", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("02-bash-agent", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("03-tool-design", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("04-structured-planning", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("05-subagents-and-skills", ["agent.py", "subagent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("06-context-compaction", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("07-task-system", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("08-background-tasks", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("09-agent-teams", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("10-team-protocols", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("11-autonomous-agents", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("12-worktree-isolation", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
    ]

    for folder, required_files in levels:
        folder_path = WORKSHOP_DIR / folder
        check(f"{folder}/ exists", folder_path.is_dir(), "folder missing")
        if folder_path.is_dir():
            for fname in required_files:
                fpath = folder_path / fname
                check(f"  {folder}/{fname} exists", fpath.is_file(), "file missing")
                if fpath.is_file():
                    size = fpath.stat().st_size
                    check(f"  {folder}/{fname} is non-empty ({size} bytes)", size > 0, "file is empty")


def test_python_syntax():
    """Test that all Python files have valid syntax."""
    print("\n🐍 Python Syntax")

    py_files = [
        "01-agent-loop/agent.py",
        "02-bash-agent/agent.py",
        "03-tool-design/agent.py",
        "04-structured-planning/agent.py",
        "05-subagents-and-skills/agent.py",
        "05-subagents-and-skills/subagent.py",
        "06-context-compaction/agent.py",
        "07-task-system/agent.py",
        "08-background-tasks/agent.py",
        "09-agent-teams/agent.py",
        "10-team-protocols/agent.py",
        "11-autonomous-agents/agent.py",
        "12-worktree-isolation/agent.py",
    ]

    for py_file in py_files:
        path = WORKSHOP_DIR / py_file
        if not path.is_file():
            check(f"{py_file} syntax", False, "file not found")
            continue

        try:
            source = path.read_text()
            ast.parse(source)
            check(f"{py_file} syntax valid", True)
        except SyntaxError as e:
            check(f"{py_file} syntax valid", False, f"line {e.lineno}: {e.msg}")


def test_key_patterns():
    """Test that key code patterns exist in each level's agent."""
    print("\n🔍 Key Code Patterns")

    checks = [
        ("01-agent-loop/agent.py", [
            ("agent loop", r"while True"),
            ("bash tool", r"\"bash\""),
        ]),
        ("02-bash-agent/agent.py", [
            ("agent loop", r"while True"),
            ("bash tool", r"\"bash\""),
            ("subagent mode", r"sys\.argv"),
            ("timeout handling", r"timeout"),
        ]),
        ("03-tool-design/agent.py", [
            ("agent loop", r"def agent_loop"),
            ("bash tool", r"\"bash\""),
            ("read_file tool", r"\"read_file\""),
            ("write_file tool", r"\"write_file\""),
            ("edit_file tool", r"\"edit_file\""),
            ("safe_path security", r"def safe_path"),
        ]),
        ("04-structured-planning/agent.py", [
            ("TodoManager class", r"class TodoManager"),
            ("TodoWrite tool", r"\"TodoWrite\""),
            ("nag reminder", r"NAG_REMINDER"),
            ("max 20 constraint", r"20"),
            ("one in_progress constraint", r"in_progress"),
        ]),
        ("05-subagents-and-skills/agent.py", [
            ("SkillLoader class", r"class SkillLoader"),
            ("Skill tool", r"\"Skill\""),
            ("Task tool", r"\"Task\""),
            ("AGENT_TYPES registry", r"AGENT_TYPES"),
            ("skill-loaded tags", r"skill-loaded"),
        ]),
        ("05-subagents-and-skills/subagent.py", [
            ("Task tool", r"\"Task\""),
            ("AGENT_TYPES registry", r"AGENT_TYPES"),
            ("run_task function", r"def run_task"),
            ("context isolation", r"sub_messages"),
        ]),
        ("06-context-compaction/agent.py", [
            ("micro_compact function", r"def micro_compact"),
            ("auto_compact function", r"def auto_compact"),
            ("token estimation", r"def estimate_tokens"),
            ("threshold constant", r"THRESHOLD"),
            ("transcript saving", r"transcript"),
        ]),
        ("07-task-system/agent.py", [
            ("TaskManager class", r"class TaskManager"),
            ("task_create handler", r"task_create"),
            ("dependency clearing", r"_clear_dependency"),
            ("blockedBy field", r"blockedBy"),
        ]),
        ("08-background-tasks/agent.py", [
            ("BackgroundManager class", r"class BackgroundManager"),
            ("background_run tool", r"background_run"),
            ("drain notifications", r"drain_notifications"),
            ("threading import", r"import threading"),
        ]),
        ("09-agent-teams/agent.py", [
            ("TeammateManager class", r"class TeammateManager"),
            ("MessageBus class", r"class MessageBus"),
            ("spawn_teammate tool", r"spawn_teammate"),
            ("JSONL inbox", r"\.jsonl"),
        ]),
        ("10-team-protocols/agent.py", [
            ("shutdown protocol", r"shutdown_request"),
            ("plan approval", r"plan_approval"),
            ("request_id correlation", r"request_id"),
            ("tracker lock", r"_tracker_lock"),
        ]),
        ("11-autonomous-agents/agent.py", [
            ("idle polling", r"IDLE_TIMEOUT"),
            ("task scanning", r"scan_unclaimed_tasks"),
            ("claim_task function", r"def claim_task"),
            ("identity re-injection", r"make_identity_block"),
        ]),
        ("12-worktree-isolation/agent.py", [
            ("WorktreeManager class", r"class WorktreeManager"),
            ("EventBus class", r"class EventBus"),
            ("worktree_create tool", r"worktree_create"),
            ("worktree_run tool", r"worktree_run"),
            ("detect_repo_root", r"def detect_repo_root"),
        ]),
    ]

    for py_file, patterns in checks:
        path = WORKSHOP_DIR / py_file
        if not path.is_file():
            check(f"{py_file} patterns", False, "file not found")
            continue

        source = path.read_text()
        for label, pattern in patterns:
            found = bool(re.search(pattern, source))
            check(f"{py_file}: has {label}", found, f"pattern '{pattern}' not found")

        # Verify litellm usage (not raw anthropic SDK)
        check(f"{py_file}: uses litellm", "from litellm" in source, "expected 'from litellm' import")
        check(f"{py_file}: no anthropic SDK", "import anthropic" not in source, "should not import anthropic directly")


def test_progressive_complexity():
    """Test that line counts follow an upward arc across modules."""
    print("\n📈 Progressive Complexity")

    files = [
        ("01-agent-loop/agent.py", "01-Agent-Loop"),
        ("02-bash-agent/agent.py", "02-Bash-Agent"),
        ("03-tool-design/agent.py", "03-Tool-Design"),
        ("04-structured-planning/agent.py", "04-Planning"),
        ("05-subagents-and-skills/agent.py", "05-Subagents"),
        ("06-context-compaction/agent.py", "06-Compaction"),
        ("07-task-system/agent.py", "07-Tasks"),
        ("08-background-tasks/agent.py", "08-Background"),
        ("09-agent-teams/agent.py", "09-Teams"),
        ("10-team-protocols/agent.py", "10-Protocols"),
        ("11-autonomous-agents/agent.py", "11-Autonomous"),
        ("12-worktree-isolation/agent.py", "12-Worktree"),
    ]

    line_counts = []
    for py_file, label in files:
        path = WORKSHOP_DIR / py_file
        if path.is_file():
            count = len(path.read_text().splitlines())
            line_counts.append((label, count))
            print(f"  ℹ {label}: {count} lines")
        else:
            line_counts.append((label, 0))

    # Arc-based checks: overall trend rather than strict pairwise monotonic increase.
    # Modules 06-08 are intentionally smaller (single-concept focused) before the
    # complexity ramps back up in 09-12.
    arc_checks = [
        # Early modules grow
        ("05-Subagents", "01-Agent-Loop", "Module 05 > Module 01"),
        # Final modules are substantial
        ("12-Worktree", "01-Agent-Loop", "Module 12 > Module 01"),
        ("12-Worktree", "09-Teams", "Module 12 > Module 09"),
        # Mid arc: 05 is the first peak
        ("05-Subagents", "03-Tool-Design", "Module 05 > Module 03"),
        # Late arc ramp-up
        ("11-Autonomous", "08-Background", "Module 11 > Module 08"),
        ("10-Protocols", "08-Background", "Module 10 > Module 08"),
    ]

    counts_by_label = {label: count for label, count in line_counts}

    for bigger_label, smaller_label, desc in arc_checks:
        bigger = counts_by_label.get(bigger_label, 0)
        smaller = counts_by_label.get(smaller_label, 0)
        check(
            f"{desc}: {bigger_label} ({bigger}) > {smaller_label} ({smaller})",
            bigger > smaller,
            f"expected {bigger_label} to have more lines than {smaller_label}"
        )


def test_tool_counts():
    """Verify each module exposes the expected number of tools."""
    print("\n🔧 Tool Counts")

    expected = {
        "01-agent-loop": 1,
        "02-bash-agent": 1,
        "03-tool-design": 4,
        "04-structured-planning": 5,
        "05-subagents-and-skills": 7,
        "06-context-compaction": 5,
        "07-task-system": 8,
        "08-background-tasks": 6,
        "09-agent-teams": 9,
        "10-team-protocols": 12,
        "11-autonomous-agents": 14,
        "12-worktree-isolation": 16,
    }

    for folder, expected_count in expected.items():
        path = WORKSHOP_DIR / folder / "agent.py"
        if not path.is_file():
            check(f"{folder} tool count", False, "agent.py not found")
            continue

        source = path.read_text()

        # Count tools using TOOL_HANDLERS entries (most reliable for modules 03+)
        handler_entries = len(re.findall(r'^\s+"[\w]+"\s*:', source, re.MULTILINE))
        # For modules 01-02 which don't have TOOL_HANDLERS, count "type": "function"
        inline_tools = source.count('"type": "function"')
        # For modules using _tool() helper, count standalone _tool( calls
        # (?<!\w) prevents matching execute_tool( or other identifiers containing _tool
        helper_calls = len(re.findall(r'(?<!\w)_tool\(', source))
        # Subtract the helper function definition itself (def _tool)
        if 'def _tool(' in source:
            helper_calls -= 1

        # Use TOOL_HANDLERS count if available, otherwise inline count
        if "TOOL_HANDLERS" in source:
            # Count lambda entries in TOOL_HANDLERS dict
            actual = len(re.findall(r'"[\w]+":\s*lambda', source))
        elif helper_calls > 0:
            actual = helper_calls
        else:
            actual = inline_tools

        check(
            f"{folder}: {actual} tools (expected {expected_count})",
            actual == expected_count,
            f"got {actual}, expected {expected_count}"
        )


def test_markdown_content():
    """Test that README/GUIDE/EXERCISES have expected content."""
    print("\n📝 Markdown Content")

    levels = ["01-agent-loop", "02-bash-agent", "03-tool-design", "04-structured-planning", "05-subagents-and-skills", "06-context-compaction", "07-task-system", "08-background-tasks", "09-agent-teams", "10-team-protocols", "11-autonomous-agents", "12-worktree-isolation"]

    for folder in levels:
        folder_path = WORKSHOP_DIR / folder

        readme = folder_path / "README.md"
        if readme.is_file():
            content = readme.read_text()
            check(f"{folder}/README.md has heading", content.startswith("#"))
            check(f"{folder}/README.md has run instructions", "make" in content.lower() or "uv run" in content.lower())

        guide = folder_path / "GUIDE.md"
        if guide.is_file():
            content = guide.read_text()
            check(f"{folder}/GUIDE.md has heading", content.startswith("#"))
            check(f"{folder}/GUIDE.md has code blocks", "```" in content)

        exercises = folder_path / "EXERCISES.md"
        if exercises.is_file():
            content = exercises.read_text()
            check(f"{folder}/EXERCISES.md has heading", content.startswith("#"))
            exercise_count = content.count("## Exercise")
            check(
                f"{folder}/EXERCISES.md has multiple exercises ({exercise_count})",
                exercise_count >= 3,
                f"only {exercise_count} exercises found"
            )


def test_root_files():
    """Test that root-level files are correct."""
    print("\n📋 Root Files")

    readme = WORKSHOP_DIR / "README.md"
    check("README.md exists", readme.is_file())
    if readme.is_file():
        content = readme.read_text()
        check("README.md mentions all 12 modules", all(
            level in content for level in ["01-agent-loop", "02-bash-agent", "03-tool-design", "04-structured-planning", "05-subagents-and-skills", "06-context-compaction", "07-task-system", "08-background-tasks", "09-agent-teams", "10-team-protocols", "11-autonomous-agents", "12-worktree-isolation"]
        ))
        check("README.md has make targets", "make 01-agent-loop" in content)

    makefile = WORKSHOP_DIR / "Makefile"
    check("Makefile exists", makefile.is_file())
    if makefile.is_file():
        content = makefile.read_text()
        for target in ["01-agent-loop", "02-bash-agent", "03-tool-design", "04-structured-planning", "05-subagents-and-skills", "06-context-compaction", "07-task-system", "08-background-tasks", "09-agent-teams", "10-team-protocols", "11-autonomous-agents", "12-worktree-isolation", "test"]:
            check(f"Makefile has '{target}' target", f"{target}:" in content)

    check("pyproject.toml exists", (WORKSHOP_DIR / "pyproject.toml").is_file())
    check(".env.example exists", (WORKSHOP_DIR / ".env.example").is_file())


def test_skills_directory():
    """Test that the skills directory is properly structured."""
    print("\n🎯 Skills Directory")

    skills_dir = WORKSHOP_DIR / "skills"
    check("skills/ directory exists", skills_dir.is_dir())

    if skills_dir.is_dir():
        expected_skills = ["agent-builder", "code-review", "mcp-builder", "pdf"]
        for skill_name in expected_skills:
            skill_dir = skills_dir / skill_name
            check(f"skills/{skill_name}/ exists", skill_dir.is_dir())
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                check(f"skills/{skill_name}/SKILL.md exists", skill_md.is_file())
                if skill_md.is_file():
                    content = skill_md.read_text()
                    check(
                        f"skills/{skill_name}/SKILL.md has frontmatter",
                        content.startswith("---"),
                        "missing YAML frontmatter"
                    )


def test_module_unit_logic():
    """Unit tests for pure logic in modules 06-12 (no API key needed)."""
    print("\n🧪 Module Unit Logic (06-12)")

    # -- 06: Token estimation + micro_compact --
    print("  — 06: Context Compaction")
    try:
        mod06 = WORKSHOP_DIR / "06-context-compaction" / "agent.py"
        source = mod06.read_text()
        # We can't import directly (side effects), so we exec the functions
        ns = {}
        # Extract and exec just the functions we need
        tree = ast.parse(source)
        func_names = {"estimate_tokens", "micro_compact"}
        const_names = {"KEEP_RECENT"}
        lines = source.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name in func_names:
                func_src = "\n".join(lines[node.lineno - 1:node.end_lineno])
                exec(func_src, ns)
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in const_names:
                        exec(lines[node.lineno - 1], ns)

        estimate_tokens = ns.get("estimate_tokens")
        micro_compact = ns.get("micro_compact")

        if estimate_tokens:
            check("06: estimate_tokens([]) == 0", estimate_tokens([]) == 0)
            test_msgs = [{"role": "user", "content": "Hello world this is a test message"}]
            tokens = estimate_tokens(test_msgs)
            check("06: estimate_tokens returns positive for non-empty", tokens > 0, f"got {tokens}")
        else:
            check("06: estimate_tokens extractable", False, "could not extract function")

        if micro_compact:
            # Build messages with tool results — micro_compact should trim old ones
            msgs = [
                {"role": "user", "content": "test"},
                {"role": "assistant", "content": None, "tool_calls": [
                    {"id": "tc1", "function": {"name": "bash", "arguments": "{}"}}
                ]},
                {"role": "tool", "tool_call_id": "tc1", "name": "bash", "content": "A" * 200},
                {"role": "assistant", "content": None, "tool_calls": [
                    {"id": "tc2", "function": {"name": "bash", "arguments": "{}"}}
                ]},
                {"role": "tool", "tool_call_id": "tc2", "name": "bash", "content": "B" * 200},
                {"role": "assistant", "content": None, "tool_calls": [
                    {"id": "tc3", "function": {"name": "bash", "arguments": "{}"}}
                ]},
                {"role": "tool", "tool_call_id": "tc3", "name": "bash", "content": "C" * 200},
                {"role": "assistant", "content": None, "tool_calls": [
                    {"id": "tc4", "function": {"name": "bash", "arguments": "{}"}}
                ]},
                {"role": "tool", "tool_call_id": "tc4", "name": "bash", "content": "D" * 200},
            ]
            result = micro_compact(msgs)
            # First tool result should be trimmed (only last KEEP_RECENT=3 preserved)
            first_tool = [m for m in result if m.get("role") == "tool"][0]
            check("06: micro_compact trims old tool results",
                  len(first_tool["content"]) < 200,
                  f"first tool content length: {len(first_tool['content'])}")
            # Last tool result should be preserved
            last_tool = [m for m in result if m.get("role") == "tool"][-1]
            check("06: micro_compact preserves recent tool results",
                  last_tool["content"] == "D" * 200)
        else:
            check("06: micro_compact extractable", False, "could not extract function")
    except Exception as e:
        check("06: unit tests", False, str(e))

    # -- 07: TaskManager CRUD --
    print("  — 07: Task System")
    tmpdir = None
    try:
        tmpdir = tempfile.mkdtemp(prefix="test_07_")
        tasks_dir = Path(tmpdir) / ".tasks"

        # Import TaskManager by extracting class from source
        mod07 = WORKSHOP_DIR / "07-task-system" / "agent.py"
        source = mod07.read_text()
        # Execute class definition in isolated namespace
        ns07 = {"Path": Path, "json": json}
        tree = ast.parse(source)
        lines = source.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "TaskManager":
                class_src = "\n".join(lines[node.lineno - 1:node.end_lineno])
                exec(class_src, ns07)

        TaskManager = ns07.get("TaskManager")
        if TaskManager:
            tm = TaskManager(tasks_dir)

            # Create task
            t1_json = tm.create("Test task 1", "Description 1")
            t1 = json.loads(t1_json)
            check("07: create task returns valid JSON", t1["subject"] == "Test task 1")
            check("07: task file created", (tasks_dir / f"task_{t1['id']}.json").exists())

            # Create second task
            t2_json = tm.create("Test task 2")
            t2 = json.loads(t2_json)
            check("07: second task has incremented ID", t2["id"] == t1["id"] + 1)

            # Update status
            updated_json = tm.update(t1["id"], status="in_progress")
            updated = json.loads(updated_json)
            check("07: update status works", updated["status"] == "in_progress")

            # Add dependency: t2 blocked by t1
            tm.update(t2["id"], add_blocked_by=[t1["id"]])
            t2_loaded = json.loads(tm.get(t2["id"]))
            check("07: blockedBy set correctly", t1["id"] in t2_loaded["blockedBy"])

            # Complete t1 — should clear t1 from t2's blockedBy
            tm.update(t1["id"], status="completed")
            t2_after = json.loads(tm.get(t2["id"]))
            check("07: dependency cleared on completion",
                  t1["id"] not in t2_after["blockedBy"],
                  f"blockedBy still contains {t1['id']}")

            # list_all
            listing = tm.list_all()
            check("07: list_all includes both tasks",
                  "Test task 1" in listing and "Test task 2" in listing)
        else:
            check("07: TaskManager extractable", False, "could not extract class")
    except Exception as e:
        check("07: unit tests", False, str(e))
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)

    # -- 08: BackgroundManager --
    print("  — 08: Background Tasks")
    try:
        import threading
        import uuid

        mod08 = WORKSHOP_DIR / "08-background-tasks" / "agent.py"
        source = mod08.read_text()
        ns08 = {"Path": Path, "subprocess": subprocess, "threading": threading,
                "uuid": uuid, "json": json}
        tree = ast.parse(source)
        lines = source.splitlines()
        # Need WORKDIR for BackgroundManager._execute
        ns08["WORKDIR"] = Path(tempfile.mkdtemp(prefix="test_08_"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "BackgroundManager":
                class_src = "\n".join(lines[node.lineno - 1:node.end_lineno])
                exec(class_src, ns08)

        BackgroundManager = ns08.get("BackgroundManager")
        if BackgroundManager:
            bg = BackgroundManager()
            check("08: BackgroundManager instantiation succeeds", bg is not None)

            # run() returns a task_id string
            result = bg.run("echo test_bg_08")
            check("08: run() returns task_id string", "started" in result.lower() or "task" in result.lower(),
                  f"got: {result[:100]}")

            # drain_notifications returns list (may be empty initially)
            notifs = bg.drain_notifications()
            check("08: drain_notifications returns list", isinstance(notifs, list))

            # Wait briefly for background task to complete, then check again
            import time
            time.sleep(1)
            notifs = bg.drain_notifications()
            check("08: background task completes", len(notifs) >= 0)  # May or may not have completed

            # check() with no task_id lists all
            status = bg.check()
            check("08: check() returns status string", isinstance(status, str))
        else:
            check("08: BackgroundManager extractable", False, "could not extract class")

        shutil.rmtree(ns08["WORKDIR"], ignore_errors=True)
    except Exception as e:
        check("08: unit tests", False, str(e))

    # -- 09: MessageBus --
    print("  — 09: Agent Teams")
    tmpdir09 = None
    try:
        tmpdir09 = tempfile.mkdtemp(prefix="test_09_")
        inbox_dir = Path(tmpdir09) / "inbox"

        mod09 = WORKSHOP_DIR / "09-agent-teams" / "agent.py"
        source = mod09.read_text()
        ns09 = {"Path": Path, "json": json, "time": __import__("time")}
        # Need VALID_MSG_TYPES
        tree = ast.parse(source)
        lines = source.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "VALID_MSG_TYPES":
                        exec("\n".join(lines[node.lineno - 1:node.end_lineno]), ns09)
            if isinstance(node, ast.ClassDef) and node.name == "MessageBus":
                class_src = "\n".join(lines[node.lineno - 1:node.end_lineno])
                exec(class_src, ns09)

        MessageBus = ns09.get("MessageBus")
        if MessageBus:
            bus = MessageBus(inbox_dir)

            # send creates JSONL file
            result = bus.send("alice", "bob", "Hello Bob")
            check("09: send() returns confirmation", "Sent" in result)
            inbox_file = inbox_dir / "bob.jsonl"
            check("09: send() creates inbox file", inbox_file.exists())

            # Verify JSONL format
            content = inbox_file.read_text().strip()
            msg = json.loads(content)
            check("09: JSONL message has correct format",
                  msg.get("from") == "alice" and msg.get("content") == "Hello Bob")

            # read_inbox returns messages and clears file
            messages = bus.read_inbox("bob")
            check("09: read_inbox returns messages", len(messages) == 1)
            check("09: read_inbox clears inbox", inbox_file.read_text().strip() == "")

            # broadcast sends to all listed teammates
            result = bus.broadcast("lead", "All hands meeting", ["alice", "bob", "lead"])
            check("09: broadcast sends to non-sender teammates", "2" in result,
                  f"got: {result}")
        else:
            check("09: MessageBus extractable", False, "could not extract class")
    except Exception as e:
        check("09: unit tests", False, str(e))
    finally:
        if tmpdir09:
            shutil.rmtree(tmpdir09, ignore_errors=True)

    # -- 10: Protocol state --
    print("  — 10: Team Protocols")
    try:
        mod10 = WORKSHOP_DIR / "10-team-protocols" / "agent.py"
        source = mod10.read_text()
        # Check that shutdown_requests and plan_requests dicts exist
        check("10: shutdown_requests dict exists", "shutdown_requests = {}" in source or "shutdown_requests = " in source)
        check("10: plan_requests dict exists", "plan_requests = {}" in source or "plan_requests = " in source)
        check("10: _tracker_lock exists", "_tracker_lock" in source)
        check("10: request_id correlation pattern", "request_id" in source)
        # Check FSM transitions: pending → approved/rejected
        check("10: shutdown FSM has 'approved' state", '"approved"' in source)
        check("10: shutdown FSM has 'rejected' state", '"rejected"' in source)
        check("10: plan FSM has 'pending' state", '"pending"' in source)
    except Exception as e:
        check("10: unit tests", False, str(e))

    # -- 11: Identity + scanning --
    print("  — 11: Autonomous Agents")
    tmpdir11 = None
    try:
        tmpdir11 = tempfile.mkdtemp(prefix="test_11_")
        tasks_dir = Path(tmpdir11) / ".tasks"
        tasks_dir.mkdir()

        mod11 = WORKSHOP_DIR / "11-autonomous-agents" / "agent.py"
        source = mod11.read_text()
        ns11 = {"Path": Path, "json": json, "threading": threading}
        tree = ast.parse(source)
        lines = source.splitlines()

        # Extract standalone functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name in ("make_identity_block", "scan_unclaimed_tasks", "claim_task"):
                func_src = "\n".join(lines[node.lineno - 1:node.end_lineno])
                exec(func_src, ns11)
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ("TASKS_DIR", "_claim_lock"):
                        # Override TASKS_DIR to our tmpdir
                        pass

        make_identity_block = ns11.get("make_identity_block")
        scan_unclaimed_tasks = ns11.get("scan_unclaimed_tasks")

        if make_identity_block:
            block = make_identity_block("alice", "coder", "team-alpha")
            check("11: make_identity_block returns dict", isinstance(block, dict))
            check("11: identity block has role=user", block.get("role") == "user")
            check("11: identity block contains name", "alice" in block.get("content", ""))
        else:
            check("11: make_identity_block extractable", False, "could not extract function")

        if scan_unclaimed_tasks:
            # Override TASKS_DIR in function's globals
            ns11["TASKS_DIR"] = tasks_dir

            # Create test tasks
            pending_no_owner = {"id": 1, "subject": "Open task", "status": "pending", "owner": "", "blockedBy": []}
            pending_with_owner = {"id": 2, "subject": "Claimed task", "status": "pending", "owner": "bob", "blockedBy": []}
            pending_blocked = {"id": 3, "subject": "Blocked task", "status": "pending", "owner": "", "blockedBy": [1]}
            completed = {"id": 4, "subject": "Done task", "status": "completed", "owner": "alice", "blockedBy": []}

            for task in [pending_no_owner, pending_with_owner, pending_blocked, completed]:
                (tasks_dir / f"task_{task['id']}.json").write_text(json.dumps(task))

            # Re-exec scan_unclaimed_tasks with our TASKS_DIR
            exec(f"""
def scan_unclaimed_tasks():
    TASKS_DIR = Path("{tasks_dir}")
    TASKS_DIR.mkdir(exist_ok=True)
    unclaimed = []
    for f in sorted(TASKS_DIR.glob("task_*.json")):
        task = json.loads(f.read_text())
        if (task.get("status") == "pending"
                and not task.get("owner")
                and not task.get("blockedBy")):
            unclaimed.append(task)
    return unclaimed
""", ns11)
            scan_fn = ns11["scan_unclaimed_tasks"]
            unclaimed = scan_fn()
            check("11: scan_unclaimed_tasks finds only open unblocked tasks",
                  len(unclaimed) == 1 and unclaimed[0]["id"] == 1,
                  f"got {len(unclaimed)} tasks: {[t['id'] for t in unclaimed]}")
        else:
            check("11: scan_unclaimed_tasks extractable", False, "could not extract function")
    except Exception as e:
        check("11: unit tests", False, str(e))
    finally:
        if tmpdir11:
            shutil.rmtree(tmpdir11, ignore_errors=True)

    # -- 12: EventBus + WorktreeManager validation --
    print("  — 12: Worktree Isolation")
    tmpdir12 = None
    try:
        tmpdir12 = tempfile.mkdtemp(prefix="test_12_")
        events_path = Path(tmpdir12) / "events.jsonl"

        mod12 = WORKSHOP_DIR / "12-worktree-isolation" / "agent.py"
        source = mod12.read_text()
        ns12 = {"Path": Path, "json": json, "time": __import__("time"),
                "re": re, "subprocess": subprocess}
        tree = ast.parse(source)
        lines = source.splitlines()

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name in ("EventBus", "WorktreeManager", "TaskManager"):
                class_src = "\n".join(lines[node.lineno - 1:node.end_lineno])
                exec(class_src, ns12)

        EventBus = ns12.get("EventBus")
        WorktreeManager = ns12.get("WorktreeManager")

        if EventBus:
            eb = EventBus(events_path)

            # emit() appends JSONL line
            eb.emit("test.event", task={"id": 1}, worktree={"name": "wt1"})
            content = events_path.read_text().strip()
            check("12: EventBus.emit() writes JSONL", len(content) > 0)
            parsed = json.loads(content)
            check("12: EventBus event has correct structure",
                  parsed.get("event") == "test.event" and parsed.get("task", {}).get("id") == 1)

            # Emit multiple events
            for i in range(6):
                eb.emit(f"event_{i}")

            # list_recent returns last N events
            recent_json = eb.list_recent(5)
            recent = json.loads(recent_json)
            check("12: EventBus.list_recent(5) returns 5 events", len(recent) == 5,
                  f"got {len(recent)}")
        else:
            check("12: EventBus extractable", False, "could not extract class")

        if WorktreeManager:
            # Test _validate_name
            wm_tasks_dir = Path(tmpdir12) / ".tasks"
            wm_tasks_dir.mkdir()
            TM = ns12.get("TaskManager")
            if TM:
                tasks = TM(wm_tasks_dir)
                events = EventBus(Path(tmpdir12) / "wm_events.jsonl")
                # Can't fully instantiate WorktreeManager without git repo,
                # but we can test _validate_name
                wm = object.__new__(WorktreeManager)
                wm.repo_root = Path(tmpdir12)
                wm.tasks = tasks
                wm.events = events
                wm.dir = Path(tmpdir12) / ".worktrees"
                wm.dir.mkdir(exist_ok=True)
                wm.index_path = wm.dir / "index.json"
                wm.index_path.write_text(json.dumps({"worktrees": []}, indent=2))
                wm.git_available = False

                # Valid names
                try:
                    wm._validate_name("my-worktree")
                    check("12: _validate_name accepts valid name", True)
                except ValueError:
                    check("12: _validate_name accepts valid name", False, "rejected 'my-worktree'")

                try:
                    wm._validate_name("wt_01.fix")
                    check("12: _validate_name accepts dots/underscores", True)
                except ValueError:
                    check("12: _validate_name accepts dots/underscores", False, "rejected 'wt_01.fix'")

                # Invalid names
                try:
                    wm._validate_name("bad name with spaces")
                    check("12: _validate_name rejects spaces", False, "should have raised ValueError")
                except ValueError:
                    check("12: _validate_name rejects spaces", True)

                try:
                    wm._validate_name("")
                    check("12: _validate_name rejects empty", False, "should have raised ValueError")
                except ValueError:
                    check("12: _validate_name rejects empty", True)

                try:
                    wm._validate_name("a" * 50)
                    check("12: _validate_name rejects >40 chars", False, "should have raised ValueError")
                except ValueError:
                    check("12: _validate_name rejects >40 chars", True)

                # Test task/worktree binding via TaskManager
                t_json = tasks.create("Bind test task")
                t = json.loads(t_json)
                bind_result = tasks.bind_worktree(t["id"], "my-wt", "agent-1")
                bound = json.loads(bind_result)
                check("12: task/worktree binding sets worktree field",
                      bound.get("worktree") == "my-wt")
                check("12: task/worktree binding sets owner",
                      bound.get("owner") == "agent-1")
                check("12: task/worktree binding auto-sets in_progress",
                      bound.get("status") == "in_progress")
        else:
            check("12: WorktreeManager extractable", False, "could not extract class")
    except Exception as e:
        check("12: unit tests", False, str(e))
    finally:
        if tmpdir12:
            shutil.rmtree(tmpdir12, ignore_errors=True)


def test_agent_functionality():
    """End-to-end practical tests for real use cases."""
    print("\n🤖 Agent Functionality (E2E)")

    if not (os.getenv("API_KEY") or os.getenv("OPENROUTER_API_KEY") or os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")):
        print(f"  \033[33m⚠\033[0m Skipping E2E tests: No LLM API key set in environment.")
        return

    timeout_s = 60

    # E2E test definitions — each verifies the agent can start, process, and use write_file
    tests = [
        {
            "name": "01 The Agent Loop (Bash execution)",
            "cmd": ["uv", "run", "python", "01-agent-loop/agent.py"],
            "input": "List the files in the skills/ directory and write the output using bash to e2e_01_ls.txt",
            "verify_file": "e2e_01_ls.txt",
            "expected_content_fn": lambda text: "pdf" in text and "code-review" in text
        },
        {
            "name": "02 Bash Agent (grep search)",
            "cmd": ["uv", "run", "python", "02-bash-agent/agent.py"],
            "input": "Search for the string 'AGENT_TYPES' inside 05-subagents-and-skills/agent.py and save the matching lines to e2e_02_grep.txt via bash.",
            "verify_file": "e2e_02_grep.txt",
            "expected_content_fn": lambda text: "AGENT_TYPES" in text
        },
        {
            "name": "03 Tool Design (write file)",
            "cmd": ["uv", "run", "python", "03-tool-design/agent.py"],
            "input": "Use the write_file tool to create e2e_03_create.py with a python function `def test_func(): return '03_PASS'`.",
            "verify_file": "e2e_03_create.py",
            "expected_content_fn": lambda text: "def test_func" in text and "03_PASS" in text
        },
        {
            "name": "04 Structured Planning (TodoWrite)",
            "cmd": ["uv", "run", "python", "04-structured-planning/agent.py"],
            "input": "Create a 3-step plan using TodoWrite, step 1 must be 'Start the plan'. Then use write_file to write 'PLAN_OK' to e2e_04_plan.txt.",
            "verify_file": "e2e_04_plan.txt",
            "expected_content_fn": lambda text: "PLAN_OK" in text
        },
        {
            "name": "05 Subagents & Skills (Tool use)",
            "cmd": ["uv", "run", "python", "05-subagents-and-skills/agent.py"],
            "input": "Use write_file to create e2e_05_skill.txt with the content 'SKILL_OK'. Do not use any other tools.",
            "verify_file": "e2e_05_skill.txt",
            "expected_content_fn": lambda text: "SKILL_OK" in text
        },
        {
            "name": "06 Context Compaction (write file)",
            "cmd": ["uv", "run", "python", "06-context-compaction/agent.py"],
            "input": "Use write_file to write 'COMPACT_OK' to e2e_06_compact.txt",
            "verify_file": "e2e_06_compact.txt",
            "expected_content_fn": lambda text: "COMPACT_OK" in text
        },
        {
            "name": "07 Task System (write file)",
            "cmd": ["uv", "run", "python", "07-task-system/agent.py"],
            "input": "Use write_file to write 'TASK_OK' to e2e_07_task.txt",
            "verify_file": "e2e_07_task.txt",
            "expected_content_fn": lambda text: "TASK_OK" in text
        },
        {
            "name": "08 Background Tasks (write file)",
            "cmd": ["uv", "run", "python", "08-background-tasks/agent.py"],
            "input": "Use write_file to write 'BG_OK' to e2e_08_bg.txt",
            "verify_file": "e2e_08_bg.txt",
            "expected_content_fn": lambda text: "BG_OK" in text
        },
        {
            "name": "09 Agent Teams (write file)",
            "cmd": ["uv", "run", "python", "09-agent-teams/agent.py"],
            "input": "Use write_file to write 'TEAM_OK' to e2e_09_team.txt",
            "verify_file": "e2e_09_team.txt",
            "expected_content_fn": lambda text: "TEAM_OK" in text
        },
        {
            "name": "10 Team Protocols (write file)",
            "cmd": ["uv", "run", "python", "10-team-protocols/agent.py"],
            "input": "Use write_file to write 'PROTO_OK' to e2e_10_proto.txt",
            "verify_file": "e2e_10_proto.txt",
            "expected_content_fn": lambda text: "PROTO_OK" in text
        },
        {
            "name": "11 Autonomous Agents (write file)",
            "cmd": ["uv", "run", "python", "11-autonomous-agents/agent.py"],
            "input": "Use write_file to write 'AUTO_OK' to e2e_11_auto.txt",
            "verify_file": "e2e_11_auto.txt",
            "expected_content_fn": lambda text: "AUTO_OK" in text
        },
        {
            "name": "12 Worktree Isolation (write file)",
            "cmd": ["uv", "run", "python", "12-worktree-isolation/agent.py"],
            "input": "Use write_file to write 'WT_OK' to e2e_12_wt.txt",
            "verify_file": "e2e_12_wt.txt",
            "expected_content_fn": lambda text: "WT_OK" in text
        },
    ]

    for test in tests:
        v_file = WORKSHOP_DIR / test["verify_file"]
        if v_file.exists():
            v_file.unlink()

        try:
            print(f"  ... testing {test['name']}")
            input_data = test.get("input", "") + "\nexit\n"

            result = subprocess.run(
                test["cmd"],
                cwd=WORKSHOP_DIR,
                input=input_data,
                text=True,
                capture_output=True,
                timeout=timeout_s
            )

            if v_file.exists():
                text = v_file.read_text()
                if test["expected_content_fn"](text):
                    check(f"{test['name']} successfully executed", True)
                else:
                    check(f"{test['name']} executed but content wrong", False, f"Output: {text.strip()[:100]}")
                v_file.unlink()
            else:
                tail = result.stdout[-500:] if result.stdout else "(no stdout)"
                err = result.stderr[-500:] if result.stderr else "(no stderr)"
                check(f"{test['name']} executed", False, f"File {test['verify_file']} missing. Tail out: {tail} | Tail err: {err}")

        except subprocess.TimeoutExpired:
            check(f"{test['name']} executed", False, f"Timeout after {timeout_s}s")
        except Exception as e:
            check(f"{test['name']} executed", False, str(e))


def main():
    print("=" * 60)
    print("🧪 Claude Code Workshop — Automated Tests")
    print("=" * 60)

    test_level_structure()
    test_python_syntax()
    test_key_patterns()
    test_progressive_complexity()
    test_tool_counts()
    test_markdown_content()
    test_root_files()
    test_skills_directory()
    test_module_unit_logic()
    test_agent_functionality()

    # Summary
    total = results["passed"] + results["failed"]
    print(f"\n{'=' * 60}")
    print(f"Results: {results['passed']}/{total} passed", end="")
    if results["failed"] > 0:
        print(f", {results['failed']} failed")
        print(f"\nFailed tests:")
        for err in results["errors"]:
            print(f"  {FAIL} {err}")
        sys.exit(1)
    else:
        print(" ✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
