import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    try:
        args = parser.parse_args()
    except SystemExit as e:
        sys.exit(e.code)  # Preserve argparse's exit code 2
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0),
    )

    # In main(), replace the if response.function_calls block:
    if response.function_calls:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose="--verbose" in sys.argv)
            
            # Validate result
            if not function_call_result.parts:
                raise Exception("Empty parts in function response")
            if function_call_result.parts[0].function_response is None:
                raise Exception("No function_response in parts[0]")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("No response in function_response")
            
            function_results.append(function_call_result.parts[0])
            
            if "--verbose" in sys.argv:
                print(f"-> {function_call_result.parts[0].function_response.response['result']}")
        
        # For now, just print we have results (next step will feed back to LLM)
        print(f"Got {len(function_results)} function result(s)")
    else:
        print(response.text)

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
