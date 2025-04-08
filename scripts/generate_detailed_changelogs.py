#!/usr/bin/env python3
"""
Enhanced script to generate detailed changelog files for each Git tag.
This script extracts detailed information about changes between tags and creates
comprehensive changelog files with structured information.
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


def get_file_changes(start_tag, end_tag):
    """Get detailed file changes between tags."""
    if start_tag is None:
        range_spec = end_tag
    else:
        range_spec = f"{start_tag}..{end_tag}"

    # Get list of changed files with status (A=added, M=modified, D=deleted)
    file_changes = run_cmd(f"git diff --name-status {range_spec}")

    # Parse file changes
    changes = {'added': [], 'modified': [], 'deleted': [], 'renamed': []}

    for line in file_changes.split('\n'):
        if not line.strip():
            continue

        parts = line.split('\t')
        status = parts[0]

        if status.startswith('A'):
            changes['added'].append(parts[-1])
        elif status.startswith('M'):
            changes['modified'].append(parts[-1])
        elif status.startswith('D'):
            changes['deleted'].append(parts[-1])
        elif status.startswith('R'):
            changes['renamed'].append((parts[1], parts[2]))  # From, To

    return changes


def group_files_by_component(files):
    """Group files by component (e.g., adapters, utils, models)."""
    components = defaultdict(list)

    for file in files:
        if 'adapters/' in file:
            component = 'adapters'
            subcomponent = file.split('adapters/')[1].split('/')[0] if '/adapters/' in file else 'core'
            components[f"{component}/{subcomponent}"].append(file)
        elif 'helpers/' in file:
            component = 'helpers'
            if 'decorators/' in file:
                components['helpers/decorators'].append(file)
            elif 'utils/' in file:
                components['helpers/utils'].append(file)
            elif 'interceptors/' in file:
                components['helpers/interceptors'].append(file)
            elif 'metaclasses/' in file:
                components['helpers/metaclasses'].append(file)
            else:
                components['helpers/core'].append(file)
        elif 'models/' in file:
            component = 'models'
            if 'entities/' in file:
                components['models/entities'].append(file)
            elif 'dtos/' in file:
                components['models/dtos'].append(file)
            elif 'errors/' in file:
                components['models/errors'].append(file)
            elif 'types/' in file:
                components['models/types'].append(file)
            else:
                components['models/core'].append(file)
        elif 'configs/' in file:
            components['configs'].append(file)
        elif file.startswith('docs/'):
            components['documentation'].append(file)
        elif file.startswith('tests/') or file.startswith('features/'):
            components['tests'].append(file)
        else:
            components['other'].append(file)

    return components


def analyze_tag_changes(start_tag, end_tag):
    """Analyze changes between two tags in detail."""
    print(f"Analyzing changes between {start_tag or 'beginning'} and {end_tag}...")

    # Get commits
    if start_tag is None:
        range_spec = end_tag
    else:
        range_spec = f"{start_tag}..{end_tag}"

    # Get commit messages
    commits = run_cmd(f"git log {range_spec} --pretty=format:'%s'").split("\n")
    commits = [c for c in commits if c]

    # Get file changes
    file_changes = get_file_changes(start_tag, end_tag)

    # Group files by component
    added_by_component = group_files_by_component(file_changes['added'])
    modified_by_component = group_files_by_component(file_changes['modified'])
    deleted_by_component = group_files_by_component(file_changes['deleted'])

    # Get a sample of actual code changes
    significant_files = []

    # Look for Python files that might contain important changes
    for change_type in ['added', 'modified']:
        for file in file_changes.get(change_type, []):
            if file.endswith('.py') and not file.endswith('__init__.py'):
                if (
                    'adapters/' in file or 'models/' in file or
                    'helpers/utils' in file or 'configs/' in file
                ):
                    significant_files.append(file)

    # Limit to 5 most significant files
    significant_files = significant_files[:5]

    # Get the most significant changes
    significant_changes = []
    for file in significant_files:
        try:
            if file in file_changes.get('added', []):
                # If file is new, get its content
                file_content = run_cmd(f"git show {end_tag}:{file}")
                if not file_content:  # Skip if unable to get content
                    continue

                # Extract class and function definitions
                definitions = re.findall(r'(?:class|def)\s+([^\(:]+)', file_content)
                if definitions:
                    significant_changes.append({
                        'file': file,
                        'type': 'added',
                        'definitions': definitions[:5],  # Limit to top 5 definitions
                    })
            else:
                # If file was modified, get the diff
                # Make sure start_tag is defined
                if start_tag is None:
                    continue

                diff = run_cmd(f"git diff {start_tag}..{end_tag} -- {file}")
                if not diff:  # Skip if unable to get diff
                    continue

                # Extract the most significant parts of the diff
                added_lines = [
                    line[1:] for line in diff.split('\n') if line.startswith('+') and
                    not line.startswith('+++') and
                    not line.strip() == '+'
                ]

                significant_additions = []
                for line in added_lines:
                    # Look for class, function definitions, or important configuration
                    if re.search(r'^\s*(?:class|def)\s+([^\(:]+)', line):
                        significant_additions.append(line.strip())
                    elif re.search(r'^\s*[A-Z_]+ *= *', line):  # Configuration constants
                        significant_additions.append(line.strip())

                if significant_additions:
                    significant_changes.append({
                        'file': file,
                        'type': 'modified',
                        'changes': significant_additions[:5],  # Limit to top 5 changes
                    })
        except Exception as e:
            print(f"Error analyzing file {file}: {e}")

    # Categorize commits
    categorized_commits = defaultdict(list)
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
            categorized_commits[category].append(message)

    return {
        'commits': categorized_commits,
        'file_changes': file_changes,
        'added_by_component': added_by_component,
        'modified_by_component': modified_by_component,
        'deleted_by_component': deleted_by_component,
        'significant_changes': significant_changes,
    }


def extract_features_from_changes(changes, tag):
    """Extract key features from the changes analysis."""
    features = []

    # Check the tag and provide specific features for known versions
    if tag == "0.13.0":
        return [
            "Complete MinIO Integration",
            "Robust Error Handling",
            "Performance Optimizations",
            "Comprehensive Documentation",
        ]
    elif tag == "0.12.0":
        return [
            "Keycloak Authentication",
            "Role-Based Authorization",
            "Resource-Based Authorization",
            "Asynchronous Support",
        ]
    elif tag == "0.11.0":
        return [
            "Keycloak Integration",
            "Asynchronous Adapters",
            "TTL Cache Decorator",
        ]
    elif tag == "0.10.0":
        return [
            "Redis Caching",
            "Email Services Integration",
            "Enhanced Configuration Management",
        ]
    elif tag == "0.9.0":
        return [
            "TOTP Security Features",
            "Time-based One-Time Password Generator",
            "Enhanced Authentication",
        ]
    elif tag == "0.8.0":
        return [
            "Redis Adapter",
            "Key-value Storage",
            "Mock Testing Utilities",
        ]
    elif tag == "0.7.0":
        return [
            "SQLAlchemy ORM Integration",
            "Database Connection Pool",
            "Transaction Management",
        ]

    # For unknown versions, use the automated extraction
    # Add features based on new components
    for component, files in changes.get('added_by_component', {}).items():
        if len(files) > 2:  # If there are multiple files in a new component
            if 'adapters/' in component:
                adapter_name = component.split('/')[1]
                features.append(f"New {adapter_name.capitalize()} integration")
            elif component == 'helpers/utils':
                features.append("New utility functions")
            elif component == 'helpers/decorators':
                features.append("New decorators for code organization")
            elif component == 'models/dtos':
                features.append("New data transfer objects")

    # Add features based on significant code changes
    for change in changes.get('significant_changes', []):
        if change['type'] == 'added':
            file = change['file']
            if 'adapters/' in file and not any(f for f in features if 'integration' in f.lower()):
                adapter_name = file.split('adapters/')[1].split('/')[0]
                features.append(f"New {adapter_name.capitalize()} adapter")
            elif 'utils/' in file and 'definitions' in change and any(d for d in change['definitions'] if 'Utils' in d):
                util_names = [d for d in change['definitions'] if 'Utils' in d]
                if util_names:
                    util_name = util_names[0].replace('Utils', '')
                    features.append(f"New {util_name} utilities")

    # Add features based on commit messages
    for category, messages in changes.get('commits', {}).items():
        if category == 'added':
            for message in messages:
                if 'support' in message.lower() or 'integration' in message.lower():
                    features.append(message)

    # If we don't have enough features, add some based on modified files
    if len(features) < 3:
        for component, files in changes.get('modified_by_component', {}).items():
            if len(files) > 3 and not any(component in f for f in features):
                features.append(f"Improved {component.replace('/', ' ')} functionality")

    # Ensure features are unique and limit to top 5
    unique_features = []
    for feature in features:
        if feature not in unique_features:
            unique_features.append(feature)

    return unique_features[:5]


def create_technical_details(changes):
    """Create technical details section based on the changes."""
    details = {}

    # Look for architectural changes
    if changes['added_by_component'].get('adapters/core') or any('ports.py' in f for f in changes['file_changes']['added']):
        details['Architecture'] = [
            "Follows the ports and adapters pattern (hexagonal architecture)",
            "Clear separation between interfaces (ports) and implementations (adapters)",
            "Dependency inversion for better testability and flexibility",
        ]

    # Look for performance improvements
    if any('cache' in f or 'performance' in f for f in changes['file_changes']['added'] + changes['file_changes']['modified']):
        details['Performance'] = [
            "Optimized for high throughput and low latency",
            "Caching mechanisms for frequently accessed data",
            "Efficient resource utilization",
        ]

    # Look for error handling
    if any('error' in f or 'exception' in f for f in changes['file_changes']['added'] + changes['file_changes']['modified']):
        details['Error Handling'] = [
            "Comprehensive error handling with domain-specific exceptions",
            "Detailed error messages with localization support",
            "Consistent error types across the application",
        ]

    # Look for configuration changes
    if any(f.startswith('archipy/configs/') for f in changes['file_changes']['modified'] + changes['file_changes']['added']):
        details['Configuration'] = [
            "Flexible configuration options with sensible defaults",
            "Environment variable support for all settings",
            "Configuration validation to prevent runtime errors",
        ]

    return details


def generate_usage_examples(tag, changes):
    """Generate usage examples based on the changes."""
    examples = {}

    # Use predefined examples for specific versions
    if tag == "0.13.0":
        examples['MinIO Operations'] = '''```python
# Initialize the MinIO adapter
from archipy.adapters.minio.adapters import MinioAdapter
minio = MinioAdapter()

# Create a bucket and upload a file
minio.make_bucket("my-bucket")
minio.put_object("my-bucket", "document.pdf", "/path/to/document.pdf")

# Generate a presigned URL for temporary access
download_url = minio.presigned_get_object("my-bucket", "document.pdf", expires=3600)
```'''
        return examples

    elif tag == "0.12.0":
        examples['Keycloak Authentication'] = '''```python
from fastapi import FastAPI, Depends
from archipy.helpers.utils.keycloak_utils import KeycloakUtils

app = FastAPI()

@app.get("/api/profile")
def get_profile(user: dict = Depends(KeycloakUtils.fastapi_auth(
    required_roles={"user"},
    admin_roles={"admin"}
))):
    return {
        "user_id": user.get("sub"),
        "username": user.get("preferred_username")
    }
```'''
        examples['Resource-Based Authorization'] = '''```python
@app.get("/api/users/{user_uuid}/info")
def get_user_info(
    user_uuid: UUID,
    user_info: dict = Depends(KeycloakUtils.fastapi_auth(
        resource_type_param="user_uuid",
        resource_type="users",
        required_roles={"user"},
        admin_roles={"admin", "superadmin"}
    ))
):
    # Users can only access their own info unless they have admin role
    return {
        "message": f"User info for {user_uuid}",
        "username": user_info.get("preferred_username")
    }
```'''
        return examples

    elif tag == "0.11.0":
        examples['Keycloak Integration'] = '''```python
from archipy.adapters.keycloak.adapters import KeycloakAdapter

# Initialize adapter with configuration from global config
keycloak = KeycloakAdapter()

# Authenticate and get access token
token = keycloak.get_token("username", "password")

# Get user information
user_info = keycloak.get_userinfo(token)

# Verify token validity
is_valid = keycloak.validate_token(token)
```'''
        return examples

    elif tag == "0.10.0" or tag == "0.8.0":
        examples['Redis Operations'] = '''```python
# Initialize the Redis adapter
from archipy.adapters.redis.adapters import RedisAdapter
redis = RedisAdapter()

# Basic operations
redis.set("user:1:name", "John Doe")
name = redis.get("user:1:name")

# Using with TTL
redis.set("session:token", "abc123", ttl=3600)  # Expires in 1 hour
```'''
        return examples

    elif tag == "0.9.0":
        examples['TOTP Generation'] = '''```python
from archipy.helpers.utils.totp_utils import TOTPUtils
from uuid import uuid4

# Generate a TOTP code
user_id = uuid4()
totp_code, expires_at = TOTPUtils.generate_totp(user_id)

# Verify a TOTP code
is_valid = TOTPUtils.verify_totp(user_id, totp_code)

# Generate a secure key for TOTP initialization
secret_key = TOTPUtils.generate_secret_key_for_totp()
```'''
        return examples

    elif tag == "0.7.0":
        examples['SQLAlchemy Integration'] = '''```python
from archipy.adapters.orm.sqlalchemy.adapters import SQLAlchemyAdapter
from archipy.models.entities.sqlalchemy.base_entities import BaseEntity

# Initialize ORM adapter
orm = SQLAlchemyAdapter()

# Define models
class User(BaseEntity):
    __tablename__ = "users"
    name = Column(String(100))
    email = Column(String(100), unique=True)

# Perform operations
with orm.session() as session:
    # Create
    new_user = User(name="John Doe", email="john@example.com")
    session.add(new_user)
    session.commit()

    # Read
    user = session.query(User).filter_by(email="john@example.com").first()
```'''
        return examples

    # For other versions, determine examples from the changes
    # Check for specific components to create examples for
    try:
        if any('adapters/minio' in comp for comp in changes.get('added_by_component', {}).keys()):
            examples['MinIO Operations'] = '''```python
# Initialize the MinIO adapter
from archipy.adapters.minio.adapters import MinioAdapter
minio = MinioAdapter()

# Create a bucket and upload a file
minio.make_bucket("my-bucket")
minio.put_object("my-bucket", "document.pdf", "/path/to/document.pdf")

# Generate a presigned URL for temporary access
download_url = minio.presigned_get_object("my-bucket", "document.pdf", expires=3600)
```'''

        if any('adapters/redis' in comp for comp in changes.get('added_by_component', {}).keys()):
            examples['Redis Operations'] = '''```python
# Initialize the Redis adapter
from archipy.adapters.redis.adapters import RedisAdapter
redis = RedisAdapter()

# Basic operations
redis.set("user:1:name", "John Doe")
name = redis.get("user:1:name")

# Using with TTL
redis.set("session:token", "abc123", ttl=3600)  # Expires in 1 hour
```'''

        if 'keycloak_utils' in ' '.join(changes.get('file_changes', {}).get('added', [])):
            examples['Keycloak Authentication'] = '''```python
from fastapi import FastAPI, Depends
from archipy.helpers.utils.keycloak_utils import KeycloakUtils

app = FastAPI()

@app.get("/api/profile")
def get_profile(user: dict = Depends(KeycloakUtils.fastapi_auth(
    required_roles={"user"},
    admin_roles={"admin"}
))):
    return {
        "user_id": user.get("sub"),
        "username": user.get("preferred_username")
    }
```'''

        if 'jwt_utils' in ' '.join(changes.get('file_changes', {}).get('added', [])):
            examples['JWT Token Handling'] = '''```python
from archipy.helpers.utils.jwt_utils import JWTUtils
from uuid import uuid4

# Create tokens
user_id = uuid4()
access_token = JWTUtils.create_access_token(user_id)
refresh_token = JWTUtils.create_refresh_token(user_id)

# Verify token
payload = JWTUtils.verify_access_token(access_token)
```'''

        if 'password_utils' in ' '.join(changes.get('file_changes', {}).get('added', [])):
            examples['Password Handling'] = '''```python
from archipy.helpers.utils.password_utils import PasswordUtils

# Hash a password
password = "SecureP@ssword123"
hashed = PasswordUtils.hash_password(password)

# Verify password
is_valid = PasswordUtils.verify_password(password, hashed)

# Generate a secure password
secure_password = PasswordUtils.generate_password()
```'''
    except Exception as e:
        print(f"Error generating examples: {e}")

    return examples


def generate_detailed_changelog(tag, prev_tag, analysis_results, output_dir):
    """Generate a detailed changelog for a tag."""
    release_date = get_tag_date(tag)

    # Check if file already exists and should be preserved
    output_file = os.path.join(output_dir, f"changelog_{tag}.md")
    if os.path.exists(output_file):
        print(f"Changelog for {tag} already exists at {output_file}. Keeping existing file.")
        return analysis_results

    if not analysis_results:
        analysis_results = analyze_tag_changes(prev_tag, tag)

    # Extract key features
    key_features = extract_features_from_changes(analysis_results, tag)

    # Create technical details
    technical_details = create_technical_details(analysis_results)

    # Generate usage examples
    usage_examples = generate_usage_examples(tag, analysis_results)

    # Start building the changelog content
    changelog_content = f"# Changelog for ArchiPy {tag}\n\n"
    changelog_content += f"## Release Date: {release_date}\n\n"

    # Add overview
    changelog_content += "## Overview\n\n"
    if key_features:
        changelog_content += f"Version {tag} introduces " + " and ".join(key_features[:2]) + ".\n\n"
    else:
        changelog_content += f"Version {tag} includes various improvements and bug fixes.\n\n"

    # Add key features
    if key_features:
        changelog_content += "## Key Features\n\n"
        for feature in key_features:
            changelog_content += f"- **{feature}**\n"
        changelog_content += "\n"

    # Add sections for each change category
    categories = [
        ("Added", "added", "New features and functionality"),
        ("Changed", "changed", "Changes to existing functionality"),
        ("Fixed", "fixed", "Bug fixes and improvements"),
        ("Removed", "removed", "Removed features or functionality"),
        ("Deprecated", "deprecated", "Features that will be removed in future versions"),
        ("Security", "security", "Security enhancements"),
    ]

    for title, key, description in categories:
        if key in analysis_results['commits'] and analysis_results['commits'][key]:
            changelog_content += f"## {title}\n\n"

            # Group by component if possible
            by_component = defaultdict(list)
            for message in analysis_results['commits'][key]:
                # Try to identify component from message
                component = "General"
                for comp in ['adapter', 'model', 'config', 'util', 'decorator', 'test']:
                    if comp in message.lower():
                        component = comp.capitalize() + "s"
                        break
                by_component[component].append(message)

            # Output by component
            for component, messages in by_component.items():
                if component != "General":
                    changelog_content += f"### {component}\n\n"
                for message in messages:
                    changelog_content += f"- {message}\n"
                changelog_content += "\n"

            # If there was only "General" component, don't add the extra newline
            if len(by_component) == 1 and "General" in by_component:
                changelog_content += "\n"

    # Add technical details if available
    if technical_details:
        changelog_content += "## Technical Details\n\n"
        for section, details in technical_details.items():
            changelog_content += f"### {section}\n\n"
            for detail in details:
                changelog_content += f"- {detail}\n"
            changelog_content += "\n"

    # Add usage examples if available
    if usage_examples:
        changelog_content += "## Usage Examples\n\n"
        for title, example in usage_examples.items():
            changelog_content += f"### {title}\n\n"
            changelog_content += f"{example}\n\n"

    # Add compatibility section
    changelog_content += "## Compatibility\n\n"
    changelog_content += "- Compatible with Python 3.10 and above\n"
    changelog_content += "- Works with FastAPI for web applications\n"
    changelog_content += "- Supports both synchronous and asynchronous operations\n"

    # Save to file
    filename = os.path.join(output_dir, f"changelog_{tag}.md")
    with open(filename, "w") as f:
        f.write(changelog_content)

    print(f"Generated detailed changelog for {tag} at {filename}")

    # Return the analysis results for potential reuse
    return analysis_results


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
        analysis_results = analyze_tag_changes(prev_tag, tag)
        generate_detailed_changelog(tag, prev_tag, analysis_results, output_dir)
    else:
        # Generate changelog for all tags
        tags = get_tags()
        print(f"Found {len(tags)} tags")

        prev_tag = None
        prev_analysis = None
        for tag in tags:
            # We can reuse some analysis between tags
            analysis_results = analyze_tag_changes(prev_tag, tag)
            prev_analysis = generate_detailed_changelog(tag, prev_tag, analysis_results, output_dir)
            prev_tag = tag


if __name__ == "__main__":
    main()
