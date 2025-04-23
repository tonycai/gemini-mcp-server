#!/usr/bin/env python3
import google.generativeai as genai
import os
import sys
import json
import argparse

# MCP protocol handler for Gemini AI
class GeminiServer:
    def __init__(self):
        # Configure the API key
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            self.error("Error: Please set the GOOGLE_API_KEY environment variable.")
            sys.exit(1)
        
        genai.configure(api_key=self.api_key)
    
    def error(self, message):
        """Format and print error messages"""
        error_json = json.dumps({"status": "error", "message": message})
        print(error_json)
    
    def success(self, data):
        """Format and print success responses"""
        response_json = json.dumps({"status": "success", "data": data})
        print(response_json)
    
    def generate_content(self, prompt, model_name="gemini-2.5-pro-preview-03-25"):
        """Generate content using Gemini AI"""
        try:
            # Load the specified Gemini model
            model = genai.GenerativeModel(model_name)
            
            # Generate the response
            response = model.generate_content(prompt)
            
            # Return the generated text
            return response.text
        except Exception as e:
            self.error(f"An error occurred while generating content: {str(e)}")
            sys.exit(1)
    
    def process_command(self, args):
        """Process MCP command"""
        if args.command == "gemini":
            if not args.prompt:
                self.error("Error: Prompt is required")
                sys.exit(1)
            
            model = args.model if args.model else "gemini-2.5-pro-preview-03-25"
            result = self.generate_content(args.prompt, model)
            self.success(result)
        else:
            self.error(f"Unknown command: {args.command}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Gemini AI MCP Server")
    parser.add_argument("command", help="MCP command to execute")
    parser.add_argument("--prompt", help="Prompt for Gemini AI")
    parser.add_argument("--model", help="Gemini model to use")
    
    args = parser.parse_args()
    
    server = GeminiServer()
    server.process_command(args)

if __name__ == "__main__":
    main()