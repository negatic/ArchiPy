#!/usr/bin/env python3
import argparse
import subprocess
import sys
from typing import Optional, Tuple


class LibVersionBumper:
    def __init__(self) -> None:
        self.valid_bump_types = ['major', 'minor', 'patch']
        self._sync_with_remote()

    def get_current_version(self) -> Tuple[str, Tuple[int, int, int], bool]:
        """Get the current version from git tags."""
        try:
            result = subprocess.run(
                ['git', 'describe', '--tags', '--abbrev=0'],
                capture_output=True,
                text=True,
                check=True,
            )
            current_version = result.stdout.strip().lstrip('v')

            # Check if current version is an RC
            is_rc = current_version.endswith('rc')
            if is_rc:
                current_version = current_version[:-2]  # Remove 'rc' suffix

            major, minor, patch = map(int, current_version.split('.'))
            return current_version, (major, minor, patch), is_rc
        except subprocess.CalledProcessError:
            print("No existing tags found. Starting from v0.0.0")
            return "0.0.0", (0, 0, 0), False
        except ValueError as e:
            print(f"Error parsing version: {e}")
            sys.exit(1)

    def calculate_new_version(
        self,
        current_version: Tuple[int, int, int],
        current_is_rc: bool,
        bump_type: str,
        is_rc: bool,
    ) -> str:
        """Calculate the new version based on bump type and RC flag."""
        major, minor, patch = current_version

        # If current version is RC and we're not creating a new RC, just remove the RC suffix
        if current_is_rc and not is_rc:
            version_str = f"{'.'.join(map(str, current_version))}"
        else:
            # Otherwise, bump version according to bump_type
            if bump_type == 'major':
                new_version = (major + 1, 0, 0)
            elif bump_type == 'minor':
                new_version = (major, minor + 1, 0)
            elif bump_type == 'patch':
                new_version = (major, minor, patch + 1)
            else:
                raise ValueError(f"Invalid bump type: {bump_type}")

            version_str = f"{'.'.join(map(str, new_version))}"

        if is_rc:
            version_str += 'rc'

        return version_str

    def create_and_push_tag(self, new_version: str, message: Optional[str] = None) -> None:
        """Create and push a new git tag."""
        try:
            # Check if tag already exists (on remote)
            self._sync_with_remote(tags_only=True)

            tag_version = f"{new_version}"
            result = subprocess.run(['git', 'tag', '-l', tag_version], capture_output=True, text=True, check=True)
            if tag_version in result.stdout:
                print(f"Tag {tag_version} already exists!")
                sys.exit(1)

            # Create tag with message
            tag_message = message or f"Release {tag_version}"
            subprocess.run(['git', 'tag', '-a', tag_version, '-m', tag_message], check=True)

            # Push tag
            subprocess.run(['git', 'push', 'origin', tag_version], check=True)
            print(f"Successfully created and pushed tag: {tag_version}")
            print(f"Tag message: {tag_message}")

        except subprocess.CalledProcessError as e:
            print(f"Error in git operations: {e}")
            sys.exit(1)

    def bump_version(self, bump_type: str, message: Optional[str] = None, rc: bool = False) -> None:
        """Main function to bump version."""
        if bump_type not in self.valid_bump_types:
            print(f"Invalid bump type. Must be one of: {self.valid_bump_types}")
            sys.exit(1)

        # Get current version
        current_version_str, current_version_tuple, is_current_rc = self.get_current_version()
        print(f"Current version: {current_version_str}{'rc' if is_current_rc else ''}")

        # Calculate new version
        new_version = self.calculate_new_version(current_version_tuple, is_current_rc, bump_type, rc)
        print(f"New version will be: {new_version}")
        print(f"Tag message will be: {message}")
        # Confirm with user
        if input("Proceed with version bump? [y/N]: ").lower() != 'y':
            print("Version bump cancelled.")
            sys.exit(0)

        # Create and push tag
        self.create_and_push_tag(new_version, message)

    def _sync_with_remote(self, tags_only: bool = False) -> None:
        if tags_only:
            subprocess.run(['git', 'fetch', '--tags'], capture_output=True, text=True, check=True)
        else:
            subprocess.run(['git', 'fetch', '--all'], capture_output=True, text=True, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump version using git tags")
    parser.add_argument('bump_type', choices=['major', 'minor', 'patch'], help="Type of version bump")
    parser.add_argument('-m', '--message', help="Custom tag message (optional)")
    parser.add_argument('--rc', action='store_true', help="Create a release candidate version")
    parser.add_argument('--dry-run', action='store_true', help="Show what would happen without making changes")

    args = parser.parse_args()

    try:
        bumper = LibVersionBumper()
        bumper.bump_version(args.bump_type, args.message, args.rc)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
