import json
import threading

# from json import JSONDecodeError
from typing import NoReturn

from openai import OpenAI

from type_extensions import Analysis, Function


def async_analyzer_agent_with_threading(
    client: OpenAI,
    agent_id: str,
    msg_anlys: str,
    file_name: str,
    analyzer_fn: Function,
    analyzer_loop: Analysis,
) -> NoReturn:
    """Async analyzer agent based on saved files in a local storage (can be adapted to a database)

    Args:
        client (OpenAI): Client instance
        agent_id (str): Analyzer agent id
        msg_anlys (str): Prompt for analyzing the content
        file_name (str): File name to analyze
        analyzer_fn (Function): Analysis function
        analyzer_loop (Analysis): Analysis loop

    Returns:
        NoReturn:
    """
    thread_name = threading.current_thread().name
    thread = client.beta.threads.create()

    edited_msg_anlys = msg_anlys + f"{file_name}"

    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=edited_msg_anlys
    )

    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=agent_id)

    message_content = message.content[0].text.value
    print(f"{thread_name} received message: {message_content}")

    response = analyzer_loop(client, thread.id, run.id, analyzer_fn)

    # try:
    #     resp = json.loads(response)
    #     final_resp = resp | {"file_name": file_name}
    # except JSONDecodeError as e:
    #     print(f"JSON decoder error {e} occured.")

    #     final_resp = {"response": response} | {"file_name": file_name}

    final_resp = {"response": response} | {"file_name": file_name}

    # Store the JSON data in a file
    with open(f"data_async/analysis/anlys_{file_name}.json", "w") as file:
        json.dump(final_resp, file)

        print(f"Analysis stored for {file_name} successfully.")
