import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)  # Pass api_key here
    query = " ".join(sys.argv[1:])
    
    messages = []
    messages.append(types.Content(role="user", parts=[types.Part(text=query)]))
    
    for i in range(20):
        print(f"\n--- Iteration {i+1} ---")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # ← ADD THIS
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt
            )
        )
        
        # Add model response to history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        # Handle function calls (unchanged)
        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose="--verbose" in sys.argv)
                
                if not function_call_result.parts or \
                   function_call_result.parts[0].function_response is None or \
                   function_call_result.parts[0].function_response.response is None:
                    raise Exception("Invalid function response")
                
                function_responses.append(function_call_result.parts[0])
                
                if "--verbose" in sys.argv:
                    print(f"-> {function_call_result.parts[0].function_response.response['result']}")
            
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print("Final response:")
            print(response.text)
            return
        
    print("Error: Max iterations (20) reached")
    sys.exit(1)



if __name__ == "__main__":
    main()
