#!/bin/bash
# Setup script for Fresco2Video User Study
# Run this script to upload videos to GitHub and generate the CSV

set -e

REPO_NAME="fresco2video-study"

echo "=== Fresco2Video User Study Setup ==="
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "ERROR: GitHub CLI (gh) is not installed."
    echo "Install it with: brew install gh"
    echo "Then authenticate with: gh auth login"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "ERROR: Not authenticated with GitHub."
    echo "Run: gh auth login"
    exit 1
fi

# Get GitHub username
GITHUB_USERNAME=$(gh api user -q .login)
echo "GitHub username: $GITHUB_USERNAME"

# Check if repo exists, if not create it
if gh repo view "$GITHUB_USERNAME/$REPO_NAME" &> /dev/null; then
    echo "Repository $REPO_NAME already exists."
else
    echo "Creating repository $REPO_NAME..."
    gh repo create "$REPO_NAME" --public --description "User study videos for Fresco2Video paper"
fi

# Configure git
cd "$(dirname "$0")"

# Check if remote exists
if git remote get-url origin &> /dev/null; then
    git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
else
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
fi

# Add and commit files
echo "Adding videos to git..."
git add videos/
git add generate_csv.py mturk_template.html

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "No changes to commit."
else
    git commit -m "Add user study videos and scripts"
fi

# Push to GitHub
echo "Pushing to GitHub (this may take a while due to video sizes)..."
git branch -M main
git push -u origin main

echo ""
echo "=== Videos uploaded successfully! ==="
echo ""
echo "Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

# Update generate_csv.py with the correct username
sed -i '' "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" generate_csv.py

# Generate CSV
echo "Generating CSV..."
python3 generate_csv.py

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Files generated:"
echo "  - user_study.csv (full tracking data for analysis)"
echo "  - user_study_mturk.csv (upload this to MTurk)"
echo "  - mturk_template.html (paste this into MTurk template)"
echo ""
echo "Next steps:"
echo "1. Go to MTurk: https://requester.mturk.com/"
echo "2. Create a new HIT"
echo "3. Paste the contents of mturk_template.html"
echo "4. Upload user_study_mturk.csv"
echo "5. Run your study!"
