import os
from openai.types.chat import ChatCompletionToolParam


schema_get_files_info: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default without input is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        header = f'Result for {directory} directory:'
        message = "Error: nothing returned"
        if not valid_target_dir:
            message = f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            message = f'    Error: "{directory}" is not a directory'
        else:
            if directory == ".":
                directory = "current"
            else:
                directory = f"'{directory}'"
            items: list[str] = []
            for item in os.listdir(target_dir):
                items.append(f"  - {item}: file_size={os.path.getsize(os.path.join(target_dir, item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, item))}")
                message = "\n".join(items[::-1])
        return f'{header}\n{message}'
    except Exception as e:
        return f"Error: {e}"
