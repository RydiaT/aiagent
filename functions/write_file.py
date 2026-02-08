import os


def write_file(working_directory, file_path, content):
    try:
        absolute = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(absolute, file_path))

        valid = os.path.commonpath([absolute, target]) == absolute

        if not valid:
            return f"Error: Cannot list '{file_path}' as it is outside the permitted working directory ({working_directory})\n"
        if  os.path.isdir(target):
            return f"Error: Cannot write to '{file_path}' as it is a directory"

        os.makedirs(file_path, exist_ok=True)

        with open(target, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"