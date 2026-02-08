import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites file text at the specified file_path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to overwrite, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        absolute = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(absolute, file_path))

        valid = os.path.commonpath([absolute, target]) == absolute

        if not valid:
            return f"Error: Cannot list '{file_path}' as it is outside the permitted working directory ({working_directory})\n"
        if  os.path.isdir(target):
            return f"Error: Cannot write to '{file_path}' as it is a directory"

        os.makedirs(os.path.dirname(absolute), exist_ok=True)

        with open(target, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"