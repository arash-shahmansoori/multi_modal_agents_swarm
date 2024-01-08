import queue
import threading
from queue import Queue
from threading import Event
from typing import Dict, NoReturn

from openai import OpenAI

from type_extensions import Function, Generation


def generator_agent_with_threading_swarm(
    client: OpenAI,
    agent_id: str,
    comm: Dict[str, Queue],
    gen_time_out: int,
    shutdown_event: Event,
    generator_fn: Function,
    generator_loop: Generation,
) -> NoReturn:
    """Generator agent

    Args:
        client (OpenAI): Client instance
        agent_id (str): Generator agent id
        comm (Dict[str, Queue]): Queues for communication between agents
        gen_time_out (int): Time out for the "cont_to_gen" queue
        shutdown_event (Event): Shutdown event
        generator_fn (Function): Generation function
        generator_loop (Generation): Generation loop

    Returns:
        NoReturn:
    """
    thread_name = threading.current_thread().name
    thread = client.beta.threads.create()

    while not shutdown_event.is_set():
        try:
            msg_gen = comm.queues["cont_to_gen"].get(timeout=gen_time_out)
            file_name = msg_gen["file_name"]

            edited_msg_gen = (
                msg_gen["prompt_msg_gen"] + f" Save the file as: {file_name}."
            )

            message = client.beta.threads.messages.create(
                thread_id=thread.id, role="user", content=edited_msg_gen
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=agent_id
            )

            message_content = message.content[0].text.value
            print(f"{thread_name} received message: {message_content}")

            _ = generator_loop(client, thread.id, run.id, generator_fn)

            comm.queues["gen_to_anlys"].put(msg_gen["file_name"])

        except queue.Empty:
            continue

        comm.queues["cont_to_gen"].task_done()
    # Indicate to analyzer that this thread is no longer sending tasks
    comm.queues["gen_to_anlys"].put(None)
