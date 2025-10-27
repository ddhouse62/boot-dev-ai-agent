import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import functions.config
from call_function import call_function, available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]

if "--verbose" not in sys.argv[2:]:
    is_verbose = False
else:
    is_verbose = True

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]





def main():
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools = [available_functions], system_instruction=functions.config.SYSTEM_PROMPT)
    )
    function_responses = []
    if len(response.function_calls) > 0:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, is_verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if is_verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    else:
        print("Response: ")
        print(response.text)
    
    
    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
