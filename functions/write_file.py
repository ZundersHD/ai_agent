import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        message = "Error: nothing returned"
        if not valid_target_dir:
            message = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_dir):
            message = f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            os.makedirs(working_dir_abs, exist_ok=True)
            with open(target_dir, "w") as f:
                f.write(content)
            message = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        return f'{message}'
    except Exception as e:
        return f"Error: {e}"
