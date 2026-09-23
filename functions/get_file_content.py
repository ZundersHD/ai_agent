import os
from openai.types.chat import ChatCompletionToolParam

from config import MAX_CHARS


schema_get_file_content: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Read the content of a specified file relative to the working directory, also check if the file exists",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Filepath of a file to read the contents of, relative to the working directory",
                },
            },
            "required": ["file_path"]
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        message = "Error: nothing returned"
        if not valid_target_dir:
            message = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_dir):
            message = f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_dir, "r") as f:
                content = f.read(MAX_CHARS).removesuffix("\n")
                if f.read(1):
                    content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            message = content
        return f'{message}'
    except Exception as e:
        return f"Error: {e}"
