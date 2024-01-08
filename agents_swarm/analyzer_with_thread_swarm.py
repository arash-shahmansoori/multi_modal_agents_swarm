import json
import queue
import threading

# from json import JSONDecodeErrors
from queue import Queue
from threading import Event
from typing import Dict, NoReturn

from openai import OpenAI
from openai.types.beta import Assistant

from type_extensions import Analysis, Function


def analyzer_agent_with_threading_swarm(
    client: OpenAI,
    agent_id: str,
    comm: Dict[str, Queue],
    anlys_time_out: int,
    shutdown_event: Event,
    analyzer_fn: Function,
    analyzer_loop: Analysis,
) -> NoReturn:
    """Analyzer agent

    Args:
        client (OpenAI): Client instance
        agent_id (str): Analyzer agent id
        comm (Dict[str, Queue]): Queues for communication between agents
        anlys_time_out (int): Time out for the "gen_to_anlys" queue
        shutdown_event (Event): Shutdown event
        analyzer_fn (Function): Analysis function
        analyzer_loop (Analysis): Analysis loop

    Returns:
        NoReturn:
    """

    while not shutdown_event.is_set() or not comm.queues["gen_to_anlys"].empty():
        file_name = None
        msg_anlys = None

        try:
            file_name = comm.queues["gen_to_anlys"].get(timeout=anlys_time_out)

            if file_name is None:
                break

            comm.queues["gen_to_anlys"].task_done()

        except queue.Empty:
            pass

        if file_name:
            thread_name = threading.current_thread().name
            thread = client.beta.threads.create()

            try:
                # Handle possible empty queue exception
                msg_anlys = comm.queues["cont_to_anlys"].get_nowait()
                comm.queues["cont_to_anlys"].task_done()

                edited_msg_anlys = msg_anlys["prompt_msg_anlys"] + f"{file_name}"

                message = client.beta.threads.messages.create(
                    thread_id=thread.id, role="user", content=edited_msg_anlys
                )

                run = client.beta.threads.runs.create(
                    thread_id=thread.id, assistant_id=agent_id
                )

                message_content = message.content[0].text.value
                # print(f"{thread_name} received message: {message_content}")

                response = analyzer_loop(client, thread.id, run.id, analyzer_fn)

                # try:
                #     resp = json.loads(response)
                #     final_resp = resp | {"file_name": file_name}
                # except JSONDecodeError as e:
                #     print(f"JSON decoder error {e} occured.")

                #     final_resp = {"response": f"{response}"} | {"file_name": file_name}

                final_resp = {"response": f"{response}"} | {"file_name": file_name}

                # Store the JSON data in a file
                with open(f"data/analysis/anlys_{file_name}.json", "w") as file:
                    json.dump(final_resp, file)

                    print(f"Analysis stored for {file_name} successfully.")

                comm.queues["anlys_to_cont"].put(response)

            except queue.Empty:
                pass
