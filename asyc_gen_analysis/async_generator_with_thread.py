import threading
from typing import NoReturn

from openai import OpenAI

from type_extensions import Function, Generation


def async_generator_agent_with_threading(
    client: OpenAI,
    agent_id: str,
    msg_gen: str,
    file_name: str,
    generator_fn: Function,
    generator_loop: Generation,
) -> NoReturn:
    """Async generator agent

    Args:
        client (OpenAI): Client instance
        agent_id (str): Generator agent id
        msg_anlys (str): Prompt for generating the content
        file_name (str): File name to save the generated content
        generator_fn (Function): Generation function
        generator_loop (Generation): Generation loop

    Returns:
        NoReturn:
    """
    thread_name = threading.current_thread().name
    thread = client.beta.threads.create()

    edited_msg_gen = msg_gen + f" Save the file as: {file_name}."

    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=edited_msg_gen
    )
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=agent_id)

    message_content = message.content[0].text.value
    print(f"{thread_name} received message: {message_content}")

    _ = generator_loop(client, thread.id, run.id, generator_fn)
