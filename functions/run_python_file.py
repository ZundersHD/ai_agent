import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        message = "Error: nothing returned"
        if not valid_target_dir:
            message = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_dir):
            message = f'Error: "{file_path}" does not exist or is not a regular file'
        elif not target_dir.endswith(".py"):
            message = f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_dir]
            command.extend(args or [])
            executed = subprocess.run(command, capture_output=True, text=True, timeout=30)
            output: list[str] = []
            if executed.returncode != 0:
                output.append(f"Process exited with code {executed.returncode}")
            if executed.stdout == "" and executed.stderr == "":
                output.append("No output produced")
            else:
                if executed.stdout != "":
                    output.append(f"STDOUT: {executed.stdout.removesuffix("\n")}")
                if executed.stderr != "":
                    output.append(f"STDERR: {executed.stderr.removesuffix("\n")}")
            message = "\n".join(output[::-1])
        return f'{message}'
    except Exception as e:
        return f"Error: executing Python file: {e}"
