# Gemini AI MCP Server

This project integrates Google's Gemini AI models with Claude CLI via the MCP protocol.

## Core Features

- **MCP Protocol Integration**: Seamless integration with Claude CLI through standardized MCP protocol
- **Multiple Model Support**: Compatible with various Gemini AI models including 2.5 Pro and 1.5 series
- **JSON Response Format**: Structured JSON responses for reliable parsing and integration
- **Error Handling**: Robust error handling with informative error messages
- **Command-line Arguments**: Flexible command-line interface with optional parameters
- **Environment Configuration**: Simple API key configuration through environment variables

## Setup

1. Ensure you have the Google Generative AI Python package installed:
   ```
   pip install google-generativeai
   ```

2. Set your Google API key as an environment variable:
   ```
   export GOOGLE_API_KEY=your_api_key
   ```

3. Make sure the shell script is executable:
   ```
   chmod +x gemini.sh
   ```

## Usage with Claude CLI

1. Configure Claude CLI to use this MCP server by adding the directory to your MCP search path

2. Use the Gemini command through Claude CLI:
   ```
   claude mcp gemini --prompt "Your prompt here"
   ```

3. Optionally specify a different Gemini model:
   ```
   claude mcp gemini --prompt "Your prompt here" --model "gemini-1.5-pro"
   ```

## Testing the Server Directly

You can test the server directly without Claude CLI:

```
./gemini.sh gemini --prompt "Explain quantum physics simply"
```

## Available Models

- gemini-2.5-pro-preview-03-25 (default)
- gemini-1.5-pro
- gemini-1.5-flash

## MCP Integration

This server implements the MCP protocol for seamless integration with Claude CLI. The `mcp.json` file defines the available commands and parameters.

## Architecture

```
gemini_server/
├── mcp.json            # MCP protocol definition
├── gemini_server.py    # Core server implementation
├── gemini.sh           # Shell wrapper script
├── genai.py            # Original implementation (reference)
├── README.md           # Documentation
└── changes.log         # Implementation changes log
```