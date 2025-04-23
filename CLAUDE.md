# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run server: `./gemini.sh gemini --prompt "Your prompt" [--model "model-name"]`
- Test directly: `python gemini_server.py gemini --prompt "Your prompt" [--model "model-name"]`
- Install dependencies: `pip install google-generativeai`
- Test stdio mode: `echo '{"command":"gemini","parameters":{"prompt":"Your prompt"}}' | python mcp_gemini_server.py`

## Code Style
- Python: Follow PEP 8 conventions
- Imports: Standard library first, then third-party packages
- Naming: snake_case for variables/functions, CamelCase for classes
- Error handling: Use try/except with specific exception types
- JSON responses: Always use {"status": "success|error", "data|message": value}
- Environment: Use os.environ.get() for environment variables
- Comments: Docstrings for classes and functions
- Parameters: Required parameters first, then optional with defaults
- Exit codes: Use sys.exit(1) for error conditions

## MCP Protocol Support
- CLI mode: Currently implemented via command-line arguments
- Stdio mode: Use JSON input/output via stdin/stdout (.mcp.json configured)
- Response format: Always return properly formatted JSON responses