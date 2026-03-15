# Contributing to Sophia-RustChain Bridge

Thanks for your interest in contributing! This guide will help you get started.

## Getting Started

1. **Fork** this repository
2. **Clone** your fork locally
3. **Create a branch** for your changes: `git checkout -b my-feature`
4. **Make your changes** and test them
5. **Commit** with a clear message
6. **Push** to your fork and open a **Pull Request**

## Development Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/sophia-rustchain-bridge.git
cd sophia-rustchain-bridge

# Install Python dependencies
pip install -r requirements.txt

# Run the governance API
python sophia_governance_api.py

# Open the demo UI
open governance_demo.html
```

## Project Structure

- `sophia_governance_api*.py` — Backend API servers (Flask)
- `*.html` — Frontend demo UIs
- `rustchain_governance_contract.rs` — Rust smart contract
- `deploy_*.sh` — Deployment scripts

## Code Style

- **Python**: Follow PEP 8, use type hints where practical
- **HTML/JS**: Clean, readable markup with comments for complex sections
- **Rust**: Follow standard Rust formatting (`cargo fmt`)
- **Commits**: Use conventional commit format (`feat:`, `fix:`, `docs:`, `chore:`)

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Include a clear description of what changed and why
- Reference any related issues (e.g., `Fixes #123`)
- Test your changes locally before submitting

## Reporting Issues

- Use GitHub Issues for bugs or feature requests
- Include reproduction steps for bugs
- Check existing issues first

## Code of Conduct

Be respectful and constructive. We're building together.
