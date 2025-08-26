# Contributing to AIDocMate

Thank you for your interest in contributing to AIDocMate! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork the Repository
- Go to the [AIDocMate repository](https://github.com/yourusername/aidocmate)
- Click the "Fork" button in the top right corner
- Clone your forked repository to your local machine

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
```

### 3. Make Your Changes
- Write clean, readable code
- Add comments where necessary
- Follow the existing code style
- Update documentation if needed

### 4. Test Your Changes
```bash
# Run Python tests
pytest

# Run frontend tests (if applicable)
cd frontend
npm test
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "Add: brief description of your changes"
```

### 6. Push and Create a Pull Request
```bash
git push origin feature/your-feature-name
```
Then create a Pull Request on GitHub with a clear description of your changes.

## 📝 Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Keep functions small and focused
- Add docstrings for public functions

### JavaScript/React
- Use consistent indentation (2 spaces)
- Follow ESLint rules
- Use functional components with hooks
- Keep components small and focused

### General
- Write meaningful commit messages
- Keep changes focused and atomic
- Test your changes thoroughly
- Update relevant documentation

## 🐛 Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

## 💡 Feature Requests

For feature requests:
- Describe the feature clearly
- Explain why it would be useful
- Provide examples if possible
- Consider implementation complexity

## 🔧 Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/aidocmate.git
   cd aidocmate
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Set up frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## 🧪 Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for good test coverage
- Test both positive and negative cases

## 📚 Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update API documentation
- Include examples and use cases

## 🚀 Release Process

1. Ensure all tests pass
2. Update version numbers
3. Update CHANGELOG.md
4. Create a release tag
5. Deploy to production

## 📞 Getting Help

- Check existing issues and discussions
- Ask questions in GitHub Discussions
- Join our community chat (if available)
- Contact maintainers directly

## 🎯 Areas for Contribution

- Bug fixes and improvements
- New features and enhancements
- Documentation improvements
- Test coverage improvements
- Performance optimizations
- UI/UX improvements
- Internationalization support

## 📄 License

By contributing to AIDocMate, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AIDocMate! 🚀
