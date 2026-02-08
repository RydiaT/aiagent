import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        absolute = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(absolute, file_path))

        valid = os.path.commonpath([absolute, target]) == absolute

        if not valid:
            return f"Error: Cannot list '{file_path}' as it is outside the permitted working directory ({working_directory})\n"
        if not os.path.isfile(target):
            return f"Error: File not found or is not a regular file: '{file_path}'"

        with open(target) as file:
            content = file.read(MAX_CHARS)

            if file.read(1):
                content += f"[...File '{file_path}' truncated at {MAX_CHARS} characters]"

        return content
    except Exception as e:
        return f"Error: {e}"