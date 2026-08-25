import os
import subprocess

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# Configuration
# ============================================================

ENV_FILE = r"C:\Users\Ananay.Ojha\Downloads\AI-with-Databricks\Response-api\.env"

load_dotenv(ENV_FILE)

client = OpenAI(
    base_url=os.environ["MY_ENDPOINT"],
    api_key=os.environ["MY_KEY"],
)

MODEL = "gpt-5.4-mini"
WORKING_DIRECTORY = os.getcwd()


# ============================================================
# Initial request
# ============================================================
query = input("User: ")

response = client.responses.create(
    model=MODEL,
    instructions=f"""
You are working in this directory:

{WORKING_DIRECTORY}

You can read, create, modify, and delete files and folders
in the current working directory.

You have access to a local shell tool.

When you need information from the filesystem or need to
perform an operation on files, use the shell tool.
""",
   # input="List the files in the current directory.",
    input = query,
    tools=[
        {
            "type": "shell",
            "environment": {
                "type": "local"
            }
        }
    ],
)


# ============================================================
# Shell execution loop
# ============================================================

while True:

    shell_calls_found = False

    for item in response.output:

        if item.type != "shell_call":
            continue

        shell_calls_found = True

        # ----------------------------------------------------
        # The model can request one or more commands.
        # ----------------------------------------------------

        for command in item.action.commands:

            print(f"\nExecuting command: {command}\n")

            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=WORKING_DIRECTORY,
                    capture_output=True,
                    text=True,
                )

                stdout = result.stdout or ""
                stderr = result.stderr or ""

                print("Command output:")

                if stdout:
                    print(stdout)

                if stderr:
                    print(stderr)

                # ------------------------------------------------
                # IMPORTANT:
                #
                # The Responses API expects shell_call_output
                # "output" to be an ARRAY of OBJECTS.
                #
                # Each object contains stdout, stderr and outcome.
                # ------------------------------------------------

                shell_output = {
                    "stdout": stdout,
                    "stderr": stderr,
                    "outcome": {
                        "type": "exit",
                        "exit_code": result.returncode,
                    },
                }

            except Exception as exc:

                print(f"Command execution failed: {exc}")

                shell_output = {
                    "stdout": "",
                    "stderr": str(exc),
                    "outcome": {
                        "type": "exit",
                        "exit_code": 1,
                    },
                }

            # ------------------------------------------------
            # Send command result back to the model.
            # ------------------------------------------------

            response = client.responses.create(
                model=MODEL,
                input=[
                    *response.output,
                    {
                        "type": "shell_call_output",
                        "call_id": item.call_id,
                        "output": [
                            shell_output
                        ],
                    },
                ],
            )


            # ------------------------------------------------
            # The model may now request another shell command.
            # ------------------------------------------------
            break

        # We need to restart processing using the new response.
        break

    # --------------------------------------------------------
    # If there were no shell calls, the model is finished.
    # --------------------------------------------------------

    if not shell_calls_found:
        break


# ============================================================
# Final response
# ============================================================

print("\nFinal response:")
print(response.output_text)
