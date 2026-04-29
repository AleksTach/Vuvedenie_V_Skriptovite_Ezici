from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "venv",
}

BINARY_EXTENSIONS = {
    ".7z",
    ".db",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".pyc",
    ".sqlite",
    ".sqlite3",
    ".webp",
    ".zip",
}


@dataclass
class ProjectDeps:
    project_root: Path
    max_read_chars: int = 25_000


class Finding(BaseModel):
    file_path: str = Field(description="Project-relative file path.")
    severity: Literal["low", "medium", "high"] = Field(
        description="How important the improvement is."
    )
    category: str = Field(description="Area such as security, tests, style, bugs.")
    issue: str = Field(description="What is wrong or risky.")
    recommendation: str = Field(description="Concrete change that would improve it.")


class ReviewReport(BaseModel):
    project_path: str
    summary: str
    strengths: list[str] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)


def _safe_path(root: Path, user_path: str) -> Path:
    root = root.resolve()
    candidate = (root / user_path).resolve()

    if candidate != root and root not in candidate.parents:
        raise ValueError(f"Path escapes project root: {user_path}")

    return candidate


def _relative_path(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def list_dir(ctx: RunContext[ProjectDeps], path: str = ".") -> dict[str, Any]:
    """List files and folders inside the project.

    Args:
        path: Project-relative directory path to inspect.
    """
    directory = _safe_path(ctx.deps.project_root, path)

    if not directory.exists():
        return {"path": path, "error": "Directory does not exist."}
    if not directory.is_dir():
        return {"path": path, "error": "Path is not a directory."}

    entries: list[dict[str, Any]] = []
    for item in sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        if item.name in IGNORED_DIRS:
            continue

        stat = item.stat()
        entries.append(
            {
                "name": item.name,
                "path": _relative_path(ctx.deps.project_root, item),
                "type": "directory" if item.is_dir() else "file",
                "size": stat.st_size,
            }
        )

    return {"path": _relative_path(ctx.deps.project_root, directory), "entries": entries}


def read_file(ctx: RunContext[ProjectDeps], path: str) -> dict[str, Any]:
    """Read a text file from the project.

    Args:
        path: Project-relative file path to read.
    """
    file_path = _safe_path(ctx.deps.project_root, path)

    if not file_path.exists():
        return {"path": path, "error": "File does not exist."}
    if not file_path.is_file():
        return {"path": path, "error": "Path is not a file."}
    if file_path.suffix.lower() in BINARY_EXTENSIONS:
        return {"path": path, "error": "Refusing to read an obvious binary file."}

    text = file_path.read_text(encoding="utf-8", errors="replace")
    truncated = len(text) > ctx.deps.max_read_chars

    if truncated:
        text = text[: ctx.deps.max_read_chars]

    return {
        "path": _relative_path(ctx.deps.project_root, file_path),
        "content": text,
        "truncated": truncated,
    }


def write_file(ctx: RunContext[ProjectDeps], path: str, content: str) -> dict[str, Any]:
    """Write a text file inside the project.

    Args:
        path: Project-relative file path to create or overwrite.
        content: New UTF-8 text content for the file.
    """
    file_path = _safe_path(ctx.deps.project_root, path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

    return {
        "path": _relative_path(ctx.deps.project_root, file_path),
        "bytes_written": len(content.encode("utf-8")),
    }


review_agent = Agent(
    os.getenv("PROJECT_REVIEW_MODEL", "openai:gpt-5.2"),
    deps_type=ProjectDeps,
    output_type=ReviewReport,
    tools=[list_dir, read_file, write_file],
    instructions=(
        "You are a senior code review agent for Python and JavaScript projects. "
        "Use list_dir first, then read_file for relevant source and config files. "
        "Focus on correctness, security, maintainability, tests, dependencies, and project structure. "
        "Ignore virtual environments, caches, build output, dependency folders, databases, and binary files. "
        "Only use write_file when the user explicitly asks you to create or modify a project file. "
        "Return concrete, prioritized recommendations with project-relative file paths."
    ),
)


def review_project(project_root: Path, prompt: str | None = None) -> ReviewReport:
    deps = ProjectDeps(project_root=project_root.resolve())
    user_prompt = prompt or (
        f"Review the project in {deps.project_root}. "
        "Inspect the Python/JavaScript files and return improvement recommendations."
    )
    result = review_agent.run_sync(user_prompt, deps=deps)
    return result.output


def report_to_markdown(report: ReviewReport) -> str:
    lines = [
        f"# Code Review: {report.project_path}",
        "",
        "## Summary",
        report.summary,
        "",
    ]

    if report.strengths:
        lines.extend(["## Strengths"])
        lines.extend(f"- {strength}" for strength in report.strengths)
        lines.append("")

    if report.findings:
        lines.extend(["## Findings"])
        for finding in report.findings:
            lines.extend(
                [
                    f"### {finding.severity.upper()} - {finding.file_path}",
                    f"- Category: {finding.category}",
                    f"- Issue: {finding.issue}",
                    f"- Recommendation: {finding.recommendation}",
                    "",
                ]
            )
    else:
        lines.extend(["## Findings", "No concrete issues found.", ""])

    if report.next_steps:
        lines.extend(["## Next Steps"])
        lines.extend(f"- {step}" for step in report.next_steps)
        lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Review a Python/JavaScript project with a Pydantic AI agent."
    )
    parser.add_argument(
        "project",
        type=Path,
        help="Path to the Python or JavaScript project that should be reviewed.",
    )
    parser.add_argument(
        "--prompt",
        help="Optional custom review instruction for the agent.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional Markdown file where the report should be saved.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = review_project(args.project, args.prompt)
    markdown = report_to_markdown(report)

    if args.output:
        args.output.write_text(markdown, encoding="utf-8")

    print(markdown)


if __name__ == "__main__":
    main()
