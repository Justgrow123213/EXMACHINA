[Русская версия](README_RU.md)

# EXMACHINA Twitter Bot


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
