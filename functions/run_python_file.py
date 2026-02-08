import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file from the filepath relative to the working directory, providing STDOUT and STDERR",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments for the python file (optional)",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        absolute = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(absolute, file_path))

        valid = os.path.commonpath([absolute, target]) == absolute

        if not valid:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory ({working_directory})\n"
        if not os.path.isfile(target):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        if not file_path[-3:] == ".py":
            return f"Error: \"{file_path}\" is not a Python file (ends in {file_path[-3:]})"

        command = ["python", target]
        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        out = ""

        if result.returncode != 0:
            out += f"Process exited with code {result.returncode}\n"
        if len(result.stdout) == 0 and len(result.stderr) == 0:
            out += f"No output produced\n"
        else:
            out += f"STDOUT: {result.stdout}\n"
            out += f"STDERR: {result.stderr}\n"

        return out
    except Exception as e:
        return f"Error: executing Python file: {e}"