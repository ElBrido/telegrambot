# Contributing to BatmanWL Bot

Thank you for your interest in contributing to BatmanWL Bot! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/telegrambot.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Install dependencies
./install_dependencies.sh

# Configure for development
cp .env.example .env
# Edit .env with your test bot credentials

# Run tests
python3 test_bot.py
```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Add comments for complex logic

## Testing

Before submitting a PR, make sure:

1. All existing tests pass: `python3 test_bot.py`
2. Your new features include tests
3. The bot runs without errors
4. Database migrations work correctly
5. All commands respond appropriately

## Adding New Features

### Adding a Premium Feature

1. Add your feature function to `features.py`:
   ```python
   def my_new_feature(param):
       """Description of feature."""
       # Your implementation
       return result
   ```

2. Add a command handler in `bot.py`:
   ```python
   @require_premium
   async def my_feature_command(update: Update, context: ContextTypes.DEFAULT_TYPE, user):
       result = my_new_feature(context.args[0])
       await update.message.reply_text(result)
   ```

3. Register the handler in `main()`:
   ```python
   application.add_handler(CommandHandler("myfeature", my_feature_command))
   ```

4. Update the help text in the `/start` command

### Adding a Free Feature

Follow the same steps as above, but use a regular async function instead of `@require_premium`.

### Adding Database Models

1. Add your model class to `database.py`
2. Create helper functions for CRUD operations
3. Update `init_db()` if needed
4. Test with sample data

## Pull Request Guidelines

- Provide a clear description of what your PR does
- Reference any related issues
- Include screenshots for UI changes
- Update documentation if needed
- Make sure all tests pass
- Keep PRs focused on a single feature or fix

## Reporting Issues

When reporting issues, please include:

- Bot version or commit hash
- Python version
- Operating system
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages or logs
- Configuration (without sensitive data)

## Feature Requests

We welcome feature requests! Please:

- Check if the feature already exists or is planned
- Describe the use case clearly
- Explain why it would be useful
- Provide examples if possible

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them get started
- Focus on what is best for the project
- Show empathy towards other community members

## Questions?

If you have questions about contributing:

- Check the README.md and QUICKSTART.md
- Look through existing issues and PRs
- Open a new issue with the "question" label

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to BatmanWL Bot! 🦇
