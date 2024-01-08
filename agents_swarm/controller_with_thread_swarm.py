import queue
import threading
from queue import Queue
from threading import Event
from typing import Dict, List, NoReturn

from asteval import Interpreter
from openai import OpenAI

from prompts import create_user_prompt_gen_anlys
from type_extensions import Control


def controller_agent_with_threading_swarm(
    client: OpenAI,
    agent_id: str,
    subject: str,
    file_names: List[str],
    shutdown_event: Event,
    thread_count_gen: int,
    comm: Dict[str, Queue],
    cont_time_out: int,
    controller_loop: Control,
) -> NoReturn:
    """Controller agent

    Args:
        client (OpenAI): Client instance
        agent_id (str): Controller agent id
        subject (str): The subject of content to be generated
        file_names (List[str]): List of file names to save the generated contents
        shutdown_event (Event): Shutdown event
        thread_count_gen (int): Thread counts for generation
        comm (Dict[str, Queue]): Queues for communication between agents
        cont_time_out (int): Time out for the "anlys_to_cont" queue
        controller_loop (Control): Control loop function

    Returns:
        NoReturn:
    """
    thread_name = threading.current_thread().name
    thread = client.beta.threads.create()

    for file_name in file_names:
        user_prompt = create_user_prompt_gen_anlys(subject, file_name)

        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_prompt
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=agent_id
        )

        message_content = message.content[0].text.value
        print(f"{thread_name} received message: {message_content}")

        response = controller_loop(client, thread.id, run.id)
        aeval = Interpreter()

        try:
            cont_msg = aeval(response)

            for k, _ in cont_msg.items():
                if k == "gen":
                    msg_gen = {
                        "prompt_msg_gen": f"Generate a photo-realistic Image of {subject}",
                        "file_name": f"{file_name}",
                    }
                    comm.queues["cont_to_gen"].put(msg_gen)
                elif k == "anlys":
                    msg_anlys = {
                        "prompt_msg_anlys": f"Analyze the generated image in the file ",
                        "file_name": f"{file_name}",
                    }
                    comm.queues["cont_to_anlys"].put(msg_anlys)

        except AttributeError as e:
            print(f"The following error occured: {e}")

    # Signal generator's shutdown event after dispatching
    shutdown_event.set()

    # Wait for message from analyzer
    while True:
        try:
            result = comm.queues["anlys_to_cont"].get(
                timeout=cont_time_out
            )  # Set the timeout to a proper value
            comm.queues["anlys_to_cont"].task_done()

            print(f"{threading.current_thread().name} received {result} from analyzer")

        except queue.Empty:
            break

    # Send a shutdown indicator (None) from controller to generator-to-analyzer for each thread
    for _ in range(thread_count_gen):
        comm.queues["gen_to_anlys"].put(None)
