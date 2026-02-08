import os.path


def get_files_info(working_directory, directory="."):

    try:
        absolute = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(absolute, directory))

        valid = os.path.commonpath([absolute, target]) == absolute

        if not valid:
            return f"Error: Cannot list '{directory}' as it is outside the permitted working directory ({working_directory})\n"

        if not os.path.isdir(target):
            return f"Error: '{target}' is not a directory\n"

        out = ""

        files = os.listdir(target)

        for file in files:
            if file[0] in "_.":
                continue

            new_path = os.path.join(target, file)
            out += f"- {file}: file_size={os.path.getsize(new_path)} bytes, is_dir={os.path.isdir(new_path)}\n"

            # if os.path.isdir(new_path):
            #     out += get_files_info(working_directory, file)

        return out
    except Exception as e:
        return f"Error: {e}"


# print(get_files_info("", "."))