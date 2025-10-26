# Contributing to AUREX.AI

Thank you for your interest in contributing to AUREX.AI! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Agile Workflow](#agile-workflow)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Standards

- ✅ Use welcoming and inclusive language
- ✅ Be respectful of differing viewpoints
- ✅ Gracefully accept constructive criticism
- ✅ Focus on what is best for the community
- ❌ No harassment, trolling, or insulting comments

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- Node.js 18+ (for dashboard)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/your-org/aurex-ai.git
cd aurex-ai

# Set up Python environment
make setup
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
make install-dev

# Start services
make docker-up

# Verify setup
make api-test
```

---

## 💻 Development Workflow

### 1. Create a Branch

```bash
# Feature branch
git checkout -b feature/your-feature-name

# Bug fix branch
git checkout -b fix/bug-description

# Chore branch
git checkout -b chore/task-description
```

### 2. Make Changes

- Write clean, maintainable code
- Follow coding standards (see below)
- Add tests for new features
- Update documentation

### 3. Test Your Changes

```bash
# Run all tests
make test

# Run code quality checks
make quality

# Run pre-commit hooks
pre-commit run --all-files
```

### 4. Commit Changes

```bash
# Use conventional commit messages
git commit -m "feat: add sentiment analysis endpoint"
git commit -m "fix: resolve cache timeout issue"
git commit -m "docs: update API documentation"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Formatting changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## 📝 Coding Standards

### Python Code Style

We follow **PEP 8** with additional rules enforced by Black and Ruff.

#### Required Standards

1. **Type Hints**: All functions must have type hints
```python
def analyze_sentiment(text: str) -> dict[str, float]:
    """Analyze sentiment of text."""
    pass
```

2. **Docstrings**: All public functions need Google-style docstrings
```python
def fetch_news(source: str) -> list[dict]:
    """
    Fetch news from specified source.

    Args:
        source: News source identifier (e.g., 'forexfactory')

    Returns:
        List of news articles with metadata

    Raises:
        ConnectionError: If unable to connect to news source
    """
    pass
```

3. **Async First**: Use async/await for I/O operations
```python
async def fetch_price() -> float:
    """Fetch current price asynchronously."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()["price"]
```

4. **Error Handling**: Proper exception handling
```python
try:
    result = await risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise
```

5. **Logging**: Use loguru for logging
```python
from loguru import logger

logger.info("Processing sentiment analysis")
logger.error("Failed to fetch news", exc_info=True)
```

### Code Quality Tools

```bash
# Format code
make format

# Lint code
make lint

# Type check
make type-check

# All checks
make quality
```

---

## 🧪 Testing Guidelines

### Test Structure

```python
# apps/backend/tests/test_sentiment.py
import pytest
from backend.services.sentiment import SentimentAnalyzer

class TestSentimentAnalyzer:
    """Test suite for sentiment analysis."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return SentimentAnalyzer()

    def test_positive_sentiment(self, analyzer):
        """Test positive sentiment detection."""
        result = analyzer.analyze("Gold prices surge!")
        assert result["label"] == "positive"
        assert result["score"] > 0.7
```

### Test Categories

- **Unit Tests**: Test individual functions/classes
- **Integration Tests**: Test component interactions
- **API Tests**: Test API endpoints
- **Pipeline Tests**: Test Prefect flows

### Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# With coverage
make test-coverage

# Specific test
pytest apps/backend/tests/test_sentiment.py::TestSentimentAnalyzer::test_positive_sentiment
```

### Test Requirements

- ✅ All new features must have tests
- ✅ Maintain ≥ 80% code coverage
- ✅ Tests must pass before PR approval
- ✅ Use meaningful test names

---

## 🔄 Pull Request Process

### Before Creating PR

1. ✅ All tests pass
2. ✅ Code quality checks pass
3. ✅ Documentation updated
4. ✅ Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe tests performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No new warnings
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs
2. **Code Review**: At least one approval required
3. **Testing**: Manual testing if needed
4. **Merge**: Squash and merge to main

---

## 🏃 Agile Workflow

We follow Agile Scrum methodology:

### Sprint Cycle (2 weeks)

1. **Sprint Planning**: Select stories from backlog
2. **Daily Development**: Commit regularly
3. **Sprint Review**: Demo completed work
4. **Retrospective**: Discuss improvements

### User Story Format

```markdown
**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
```

### Task Board

Check current sprint status:
```bash
make sprint-status
```

View product backlog:
```bash
make backlog
```

---

## 📚 Additional Resources

- [Architecture Documentation](docs/architecture.md)
- [Product Requirements](docs/prd.md)
- [API Documentation](http://localhost:8000/docs)
- [Sprint Planning](docs/SPRINT_PLANNING.md)

---

## 🙋 Getting Help

- **Questions?** Open a GitHub Discussion
- **Bugs?** Create an Issue
- **Ideas?** Share in Discussions

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AUREX.AI! 🚀**

