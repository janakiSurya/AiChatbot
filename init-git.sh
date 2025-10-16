#!/bin/bash

# Git Initialization Script for Boku AI Assistant

set -e

echo "🔧 Initializing Git repository for Boku AI Assistant..."

# Initialize git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
else
    echo "✅ Git repository already initialized"
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Boku AI Assistant

- Optimized conversational AI assistant for Surya Gouthu's portfolio
- Uses HuggingFace Mistral-7B with hybrid vector/keyword search
- Clean, efficient codebase with environment-based configuration
- Includes Docker support and CI/CD pipeline
- Creative greetings and natural third-person responses"

# Set up remote (you'll need to create the repository first)
echo "🌐 To connect to a remote repository:"
echo "   git remote add origin <your-repository-url>"
echo "   git branch -M main"
echo "   git push -u origin main"

echo "✅ Git repository initialized successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Create a repository on GitHub/GitLab"
echo "2. Copy the repository URL"
echo "3. Run: git remote add origin <repository-url>"
echo "4. Run: git push -u origin main"
echo ""
echo "🔐 Don't forget to:"
echo "- Set HF_API_KEY as a secret in your repository"
echo "- Configure environment variables for deployment"
