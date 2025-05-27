# 🤝 Contributing to Interactive Video Subtitle Generator

First off, thank you for considering contributing to the Interactive Video Subtitle Generator! 🎉 

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to project maintainers.

## 🚀 Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/SubtitleGenerator.git
   cd SubtitleGenerator
   ```

2. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💻 Development Process

1. **Make your changes**
   - Write clean, documented code
   - Follow the style guidelines
   - Add tests for new features

2. **Test your changes**
   ```bash
   pytest
   flake8
   mypy src/
   ```

3. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions/classes
   - Update example usage if applicable

## 📤 Pull Request Process

1. **Update your fork**
   ```bash
   git remote add upstream https://github.com/original/SubtitleGenerator.git
   git fetch upstream
   git merge upstream/main
   ```

2. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**
   - Use a clear, descriptive title
   - Reference any related issues
   - Describe your changes in detail
   - Include screenshots for UI changes

4. **Code Review**
   - Address review comments
   - Make requested changes
   - Keep the PR updated

## 📝 Style Guidelines

### Python Code Style

- Follow PEP 8 guidelines
- Use type hints
- Maximum line length: 127 characters
- Use descriptive variable names
- Add docstrings to functions and classes

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Reference issues and pull requests
- Keep first line under 72 characters

### Documentation

- Use clear, concise language
- Include code examples
- Keep formatting consistent
- Update table of contents

## 🎯 Focus Areas

We're particularly interested in contributions that:

- 🚀 Improve performance
- 🎨 Enhance user interface
- 🌍 Add language support
- 🐛 Fix bugs
- 📚 Improve documentation
- ✨ Add new features

## ❓ Questions?

Feel free to:
- 📮 Open an issue
- 💬 Start a discussion
- 📧 Contact maintainers

Thank you for contributing! 🙏 