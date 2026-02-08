import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

from config import RUN_LIMIT
from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from prompts import system_prompt

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")


    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file]
    )
    for _ in range(RUN_LIMIT):

        response = client.models.generate_content(model="gemini-2.5-flash",
                                              contents=messages,
                                              config=types.GenerateContentConfig(
                                                system_instruction=system_prompt,
                                                tools=[available_functions]
                                              ),
                                              )

        if response.candidates:
            for thing in response.candidates:
                messages.append(thing.content)

        if response.usage_metadata:
            if args.verbose:
                print("User prompt: " + args.user_prompt)
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print("Response:")

            results = []

            if response.function_calls:
                for call in response.function_calls:
                    func_result = call_function(call, args.verbose)

                    if not func_result.parts[0].function_response:
                        raise Exception(f"function call {call.name}({call.args}) resulted in no response")

                    if not func_result.parts[0].function_response.response:
                        raise Exception(f"function call {call.name}({call.args}) response field was empty")

                    results.append(func_result.parts[0])

                    if args.verbose:
                        print(f"-> {func_result.parts[0].function_response.response}")

                messages.append(types.Content(role="user", parts=results))
            else:
                print(response.text)

                return
        else:
            raise RuntimeError("failed API request. input:\n" + args.user_prompt)

    print(f"Maximum Iterations {RUN_LIMIT} Reached.")
    exit(1)


if __name__ == "__main__":
    main()

