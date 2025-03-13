[Русская версия](README_RU.md)

# EXMACHINA Twitter Bot

<p align="center" style="color: aqua"><b>Twitter Automation with AI</b></p>

<p align="center">
    <a href="./README.md">
        <img src="https://img.shields.io/badge/document-English-blue.svg" alt="EN doc">
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
    </a>
    <a href="./CHANGELOG.md">
        <img src="https://img.shields.io/badge/CHANGELOG-История-blue.svg" alt="Changelog">
    </a>
</p>

<p align="center">
    <!-- Project Stats -->
    <a href="https://github.com/yourusername/exmachina/issues">
        <img src="https://img.shields.io/github/issues/yourusername/exmachina" alt="GitHub issues">
    </a>
    <a href="https://github.com/yourusername/exmachina/network">
        <img src="https://img.shields.io/github/forks/yourusername/exmachina" alt="GitHub forks">
    </a>
    <a href="https://github.com/yourusername/exmachina/stargazers">
        <img src="https://img.shields.io/github/stars/yourusername/exmachina" alt="GitHub stars">
    </a>
    <a href="https://star-history.com/#aivoyager/puti">
        <img src="https://img.shields.io/github/stars/aivoyager/puti?style=social" alt="GitHub star chart">
    </a>
</p>

## About

EXMACHINA is a fork of the [voyager_alpha](https://github.com/aivoyager/puti) project, which was originally designed as a multi-agent system. This fork has been modified to create a specialized Twitter bot that uses GPT-4 for content generation and management.

### Key Differences from Original Project
- Focused on Twitter-specific functionality
- Added web interface for bot management
- Implemented test mode for safe testing
- Added tweet scheduling system
- Enhanced with Twitter-specific features

## Features

- Tweet generation using GPT-4
- Post scheduling
- Trend analysis
- Automatic responses
- Mention monitoring
- Test mode for safe testing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Justgrow123213/EXMACHINA.git
cd EXMACHINA
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file from .env.example:
```bash
cp .env.example .env
```

4. Configure environment variables in .env:
```
TEST_MODE=true
OPENAI_API_KEY=your_api_key
TWITTER_BEARER_TOKEN=your_bearer_token
```

## Usage

1. Start the server:
```bash
python main.py --host 127.0.0.1 --port 8000
```

2. Open web interface:
```
http://localhost:8000
```

## Development

Detailed development information is available in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

Project security policy is described in [SECURITY.md](SECURITY.md).

## Changelog

Change history is available in [CHANGELOG.md](CHANGELOG.md).

## Code of Conduct

Project conduct rules are described in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Fork Documentation

Detailed information about the fork and changes is available in [FORK.md](FORK.md).
