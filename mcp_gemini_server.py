#!/usr/bin/env python3
"""
MCP Gemini Server - A stdio interface for Google's Gemini AI models
This script provides a bridge between Claude CLI and Google's Gemini AI API
"""

import json
import sys
import os
import time
import traceback
import logging
from datetime import datetime

# Setup logging
LOG_FILE = "/tmp/mcp_gemini_server.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Record start time and process ID for debugging
start_time = datetime.now()
logging.info(f"Server starting at {start_time}, PID: {os.getpid()}")
logging.info(f"Python version: {sys.version}")
logging.info(f"Working directory: {os.getcwd()}")

# Import Google Generative AI package with error handling
try:
    import google.generativeai as genai
    logging.info("Successfully imported google.generativeai")
except ImportError as e:
    error_msg = f"Failed to import google.generativeai: {str(e)}"
    logging.error(error_msg)
    sys.stderr.write(error_msg + "\n")
    sys.exit(1)

# Check for API key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    error_msg = "Error: GOOGLE_API_KEY environment variable not set"
    logging.error(error_msg)
    sys.stderr.write(error_msg + "\n")
    sys.exit(1)

logging.info("GOOGLE_API_KEY is set (value hidden)")

# Configure Gemini API
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    logging.info("Configured Gemini API successfully")
except Exception as e:
    error_msg = f"Failed to configure Gemini API: {str(e)}"
    logging.error(error_msg)
    sys.stderr.write(error_msg + "\n")
    sys.exit(1)

def get_available_models():
    """Get a list of available Gemini models for debugging"""
    try:
        models = genai.list_models()
        model_names = [model.name for model in models if "gemini" in model.name.lower()]
        logging.info(f"Available Gemini models: {model_names}")
        return model_names
    except Exception as e:
        logging.error(f"Failed to list models: {str(e)}")
        return []

# List available models on startup
get_available_models()

def handle_gemini_command(parameters):
    """Handle the gemini command by sending a prompt to the Gemini AI"""
    logging.info(f"Received gemini command with parameters: {parameters}")
    
    prompt = parameters.get("prompt")
    if not prompt:
        error_msg = "Error: 'prompt' parameter is required"
        logging.error(error_msg)
        return {"status": "error", "error": error_msg}
    
    model_name = parameters.get("model", "gemini-2.5-pro-preview-03-25")
    # Strip "models/" prefix if present to ensure compatibility
    if model_name.startswith("models/"):
        model_name = model_name[7:]
    
    logging.info(f"Using model: {model_name}")
    
    try:
        # Time the API call for performance tracking
        start = time.time()
        logging.info(f"Starting Gemini API call at {datetime.now()}")
        
        # Create the model and generate content
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(prompt)
        
        end = time.time()
        logging.info(f"Gemini API call completed in {end - start:.2f} seconds")
        
        # Extract and return the text response
        result = response.text
        logging.info(f"Received response from Gemini (length: {len(result)} chars)")
        return {"status": "success", "result": result}
    
    except Exception as e:
        error_msg = f"Error calling Gemini API: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        return {"status": "error", "error": error_msg}

def handle_execute_command(params):
    """Handle execute command from the Claude CLI"""
    logging.info(f"Handling execute command: {params}")
    
    # Extract the command name and parameters
    command_name = params.get("command", "")
    command_params = params.get("parameters", {})
    
    if command_name == "gemini":
        result = handle_gemini_command(command_params)
        return {"result": result}
    else:
        error_msg = f"Unknown command: {command_name}"
        logging.error(error_msg)
        return {"error": {"message": error_msg}}

def process_request(request):
    """Process a request from stdin following the MCP protocol"""
    try:
        # Check if this is a notification (no id field in JSON-RPC)
        is_notification = "method" in request and "id" not in request
        
        # If it's a notification, just log it and return None
        if is_notification:
            method = request.get("method", "")
            logging.info(f"Received notification: {method}")
            return None  # No response needed for notifications
        
        # Check if this is a method-based protocol message
        if "method" in request:
            method = request.get("method")
            params = request.get("params", {})
            
            logging.info(f"Processing method: {method}")
            
            # Handle initialization
            if method == "initialize":
                protocol_version = params.get("protocolVersion")
                logging.info(f"Received initialization request with protocol version: {protocol_version}")
                return {
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "commands": [{
                                "name": "gemini",
                                "description": "Generate content using Google's Gemini AI model",
                                "parameters": [
                                    {
                                        "name": "prompt",
                                        "type": "string",
                                        "description": "The prompt to send to Gemini AI",
                                        "required": True
                                    },
                                    {
                                        "name": "model",
                                        "type": "string",
                                        "description": "The Gemini model to use",
                                        "required": False,
                                        "default": "gemini-2.5-pro-preview-03-25"
                                    }
                                ]
                            }]
                        },
                        "serverInfo": {
                            "name": "GeminiConnector",
                            "version": "0.2.0"
                        }
                    }
                }
            
            # Handle shutdown
            elif method == "shutdown":
                logging.info("Received shutdown request")
                return {"result": None}
            
            # Handle execute command
            elif method == "execute":
                return handle_execute_command(params)
            
            # Handle unknown methods
            else:
                error_msg = f"Unknown method: {method}"
                logging.error(error_msg)
                return {"error": {"message": error_msg}}
        
        # Legacy command handling for direct testing
        elif "command" in request:
            command = request.get("command")
            parameters = request.get("parameters", {})
            
            logging.info(f"Processing legacy command: {command}")
            
            if command == "gemini":
                return handle_gemini_command(parameters)
            else:
                error_msg = f"Unknown command: {command}"
                logging.error(error_msg)
                return {"status": "error", "error": error_msg}
        
        else:
            error_msg = "Invalid request format: missing 'method' or 'command'"
            logging.error(error_msg)
            return {"error": {"message": error_msg}}
    
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        logging.error(error_msg)
        logging.error(traceback.format_exc())
        return {"error": {"message": error_msg}}

def main():
    """Main function that reads from stdin and writes to stdout"""
    logging.info("Server is ready to process requests")
    
    # Send a startup message to stderr (won't interfere with stdio protocol)
    sys.stderr.write("Gemini server is ready\n")
    
    try:
        # Use binary mode to avoid any text encoding issues
        for line in sys.stdin.buffer:
            try:
                line_str = line.decode('utf-8').strip()
                # Only log the first 200 chars to avoid huge log files
                log_preview = line_str[:200] + ("..." if len(line_str) > 200 else "")
                logging.info(f"Received input line: {log_preview}")
                
                # Parse the JSON request
                request = json.loads(line_str)
                logging.info("Successfully parsed JSON request")
                
                # Process the request
                result = process_request(request)
                
                # Skip response for notifications (result is None)
                if result is None:
                    logging.info("No response needed for notification")
                    continue
                
                # Get the JSON-RPC ID if present
                json_rpc_id = request.get("id")
                
                # Create response with ID if provided
                response = result
                if json_rpc_id is not None:
                    response = {"jsonrpc": "2.0", "id": json_rpc_id}
                    if "error" in result:
                        response["error"] = result["error"]
                    else:
                        response["result"] = result.get("result")
                
                # Convert to JSON
                response_json = json.dumps(response)
                # Log a preview of the response
                log_preview = response_json[:200] + ("..." if len(response_json) > 200 else "")
                logging.info(f"Sending response: {log_preview}")
                
                # Write the response and flush immediately
                sys.stdout.write(response_json + "\n")
                sys.stdout.flush()
                logging.info("Response sent and flushed")
                
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON: {str(e)}"
                logging.error(error_msg)
                # Only send error response if not a notification
                if "id" in request:
                    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": request.get("id"), "error": {"message": error_msg}}) + "\n")
                    sys.stdout.flush()
                
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                logging.error(error_msg)
                logging.error(traceback.format_exc())
                # Try to get the request ID if available
                request_id = getattr(request, "get", lambda x: None)("id")
                if request_id is not None:
                    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": request_id, "error": {"message": error_msg}}) + "\n")
                    sys.stdout.flush()
    
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt, shutting down")
    except Exception as e:
        logging.error(f"Fatal error in main loop: {str(e)}")
        logging.error(traceback.format_exc())
    
    logging.info("Server shutting down")

if __name__ == "__main__":
    main()
