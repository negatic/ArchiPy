#!/bin/bash
# Script to update changelogs after a new release

# Ensure we're in the project root
cd "$(git rev-parse --show-toplevel)" || exit 1

# Get the latest tag
LATEST_TAG=$(git tag -l | sort -V | tail -n1)

if [ -z "$LATEST_TAG" ]; then
    echo "Error: No git tags found"
    exit 1
fi

echo "Generating changelog for $LATEST_TAG..."
python scripts/generate_changelogs.py --tag "$LATEST_TAG"

# Update the index.md file with new tag information
echo "Updating changelogs index..."
python scripts/generate_changelogs.py

echo "Done! Changelog files updated:"
echo "- changelogs/changelog_$LATEST_TAG.md"
echo "- changelogs/index.md"

echo ""
echo "Next steps:"
echo "1. Review the generated changelog files"
echo "2. Commit the changes:"
echo "   git add changelogs/"
echo "   git commit -m \"docs: update changelogs for $LATEST_TAG\""
echo "3. Push the changes"
