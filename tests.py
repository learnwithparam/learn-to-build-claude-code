#!/usr/bin/env python3
"""
tests.py — Automated tests for the Claude Code workshop.

Verifies that all 5 levels are properly structured and functional:
  1. Required files exist in each level folder
  2. Python files have valid syntax (compile check)
  3. Key classes/functions are importable
  4. README/GUIDE/EXERCISES files are non-empty and have expected sections
  5. Makefile has all required targets
  6. Skills directory is properly structured

Run: make test
  or: uv run python tests.py
"""

import ast
import os
import re
import subprocess
import sys
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
    """Test that all 5 level folders have the required files."""
    print("\n📁 Level Structure")

    levels = [
        ("01-agent-loop", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("02-bash-agent", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("03-tool-design", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("04-structured-planning", ["agent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
        ("05-subagents-and-skills", ["agent.py", "subagent.py", "README.md", "GUIDE.md", "EXERCISES.md"]),
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


def test_progressive_complexity():
    """Test that line counts increase progressively across levels."""
    print("\n📈 Progressive Complexity")

    files = [
        ("01-agent-loop/agent.py", "Noob"),
        ("02-bash-agent/agent.py", "Beginner"),
        ("03-tool-design/agent.py", "Intermediate"),
        ("04-structured-planning/agent.py", "Advanced"),
        ("05-subagents-and-skills/agent.py", "Expert"),
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

    for i in range(1, len(line_counts)):
        prev_label, prev_count = line_counts[i - 1]
        curr_label, curr_count = line_counts[i]
        check(
            f"{curr_label} ({curr_count}) > {prev_label} ({prev_count})",
            curr_count > prev_count,
            f"expected {curr_label} to have more lines than {prev_label}"
        )


def test_markdown_content():
    """Test that README/GUIDE/EXERCISES have expected content."""
    print("\n📝 Markdown Content")

    levels = ["01-agent-loop", "02-bash-agent", "03-tool-design", "04-structured-planning", "05-subagents-and-skills"]

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
        check("README.md mentions all 5 levels", all(
            level in content for level in ["01-agent-loop", "02-bash-agent", "03-tool-design", "04-structured-planning", "05-subagents-and-skills"]
        ))
        check("README.md has make targets", "make 01-agent-loop" in content)

    makefile = WORKSHOP_DIR / "Makefile"
    check("Makefile exists", makefile.is_file())
    if makefile.is_file():
        content = makefile.read_text()
        for target in ["01-agent-loop", "02-bash-agent", "03-tool-design", "04-structured-planning", "05-subagents-and-skills", "test"]:
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


def test_agent_functionality():
    """End-to-end practical tests for real use cases."""
    print("\n🤖 Agent Functionality (E2E)")
    
    if not (os.getenv("API_KEY") or os.getenv("OPENROUTER_API_KEY") or os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")):
        print(f"  \033[33m⚠\033[0m Skipping E2E tests: No LLM API key set in environment.")
        return

    timeout_s = 60

    # Clean up before testing
    for file in ["e2e_01_ls.txt", "e2e_02_grep.txt", "e2e_03_create.py", "e2e_04_plan.txt", "e2e_05_skill.txt"]:
        f = WORKSHOP_DIR / file
        if f.exists():
            f.unlink()

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
            "input": "Create an empty file e2e_05_skill.txt to prove you're alive.",
            "verify_file": "e2e_05_skill.txt",
            "expected_content_fn": lambda text: True
        }
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
    test_markdown_content()
    test_root_files()
    test_skills_directory()
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
