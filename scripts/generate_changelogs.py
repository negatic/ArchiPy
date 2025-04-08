#!/usr/bin/env python3
"""
Script to generate changelog files for each Git tag.
This script extracts commit information between tags and categorizes them
to create structured changelog files.
"""

import os
import re
import subprocess
from collections import defaultdict
from datetime import datetime


def run_cmd(cmd):
    """Run a shell command and return the output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(result.stderr)
        return ""
    return result.stdout.strip()


def get_tags():
    """Get all git tags sorted by version."""
    tags = run_cmd("git tag -l").split("\n")
    # Sort tags semantically (0.1.0, 0.2.0, etc.)
    return sorted(tags, key=lambda x: [int(n) for n in x.split(".")])


def get_tag_date(tag):
    """Get the date of a tag."""
    date_str = run_cmd(f"git log -1 --format=%ai {tag}")
    if not date_str:
        return "Unknown date"
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
        return date.strftime("%Y-%m-%d")
    except ValueError:
        return "Unknown date"


def categorize_commit(message):
    """Categorize a commit message."""
    message = message.lower()

    # Common prefixes in commit messages
    if re.match(r"^add", message) or re.match(r"^feat", message):
        return "added"
    elif re.match(r"^fix", message) or "fix" in message:
        return "fixed"
    elif re.match(r"^change", message) or re.match(r"^refactor", message) or re.match(r"^update", message):
        return "changed"
    elif re.match(r"^remove", message) or re.match(r"^delete", message):
        return "removed"
    elif re.match(r"^deprecate", message):
        return "deprecated"
    elif re.match(r"^security", message) or "security" in message:
        return "security"
    else:
        return "added"  # Default category


def get_commits_between_tags(start_tag, end_tag):
    """Get all commits between two tags."""
    # If start_tag is None, get all commits up to end_tag
    if start_tag is None:
        range_spec = end_tag
    else:
        range_spec = f"{start_tag}..{end_tag}"

    # Get commit messages
    commits = run_cmd(f"git log {range_spec} --pretty=format:'%s'").split("\n")

    # Filter out empty commits
    commits = [c for c in commits if c]

    # Categorize commits
    categorized = defaultdict(list)
    for commit in commits:
        category = categorize_commit(commit)
        # Clean up the commit message
        message = commit
        # Remove common prefixes
        message = re.sub(r"^(fix|feat|chore|docs|style|refactor|perf|test|build|ci|revert)(\([^)]+\))?:", "", message).strip()
        # Capitalize first letter
        if message:
            message = message[0].upper() + message[1:]
        if message:
            categorized[category].append(message)

    return categorized


def generate_changelog(tag, prev_tag, output_dir):
    """Generate a changelog for a tag."""
    commits = get_commits_between_tags(prev_tag, tag)
    release_date = get_tag_date(tag)

    changelog_content = f"# Changelog for ArchiPy {tag}\n\n"
    changelog_content += f"## Release Date: {release_date}\n\n"

    # Add description based on the changes
    major_changes = []
    for category, messages in commits.items():
        if messages:
            major_changes.extend(messages[:3])  # Take up to 3 major changes from each category

    if major_changes:
        changelog_content += "## Overview\n\n"
        changelog_content += "This release includes the following major changes:\n\n"
        for change in major_changes[:5]:  # Limit to top 5 changes
            changelog_content += f"- {change}\n"
        changelog_content += "\n"

    # Add detailed changes by category
    categories = ["added", "changed", "deprecated", "removed", "fixed", "security"]
    for category in categories:
        if category in commits and commits[category]:
            title = category.capitalize()
            changelog_content += f"## {title}\n\n"
            for message in commits[category]:
                changelog_content += f"- {message}\n"
            changelog_content += "\n"

    # Save to file
    filename = os.path.join(output_dir, f"changelog_{tag}.md")
    with open(filename, "w") as f:
        f.write(changelog_content)

    print(f"Generated changelog for {tag} at {filename}")


def main():
    """Main function."""
    import sys

    output_dir = "changelogs"
    os.makedirs(output_dir, exist_ok=True)

    # Check if a specific tag was requested
    if len(sys.argv) > 1 and sys.argv[1] == "--tag" and len(sys.argv) > 2:
        tag = sys.argv[2]
        tags = get_tags()

        if tag not in tags:
            print(f"Error: Tag '{tag}' not found in repository")
            sys.exit(1)

        # Find the previous tag
        index = tags.index(tag)
        prev_tag = None if index == 0 else tags[index - 1]

        # Generate changelog for the specific tag
        generate_changelog(tag, prev_tag, output_dir)
        print(f"Generated changelog for {tag} at {output_dir}/changelog_{tag}.md")
    else:
        # Generate changelog for all tags
        tags = get_tags()
        print(f"Found {len(tags)} tags")

        prev_tag = None
        for tag in tags:
            generate_changelog(tag, prev_tag, output_dir)
            prev_tag = tag


if __name__ == "__main__":
    main()
