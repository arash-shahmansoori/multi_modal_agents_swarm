import queue
import threading
import time
from queue import Queue
from threading import Event
from typing import Dict, List, NoReturn


def controller_agent_with_threading_mock_swarm(
    subject: str,
    file_names: List[str],
    shutdown_event: Event,
    thread_count_gen: int,
    comm: Dict[str, Queue],
) -> NoReturn:
    for file_name in file_names:
        time.sleep(5)  # To replicate controller delay

        msg_gen = {
            "prompt_msg_gen": f"Generate a photo-realistic Image of {subject} and save the file as: {file_name}.",
            "file_name": f"{file_name}",
        }
        comm.queues["cont_to_gen"].put(msg_gen)

        msg_anlys = {
            "prompt_msg_anlys": f"Analyze the generated image of {subject} in the file {file_name}.",
            "file_name": f"{file_name}",
        }
        comm.queues["cont_to_anlys"].put(msg_anlys)

    # Signal generator's shutdown event after dispatching
    shutdown_event.set()

    # Wait for message from analyzer
    while True:
        try:
            result = comm.queues["anlys_to_cont"].get(
                timeout=20
            )  # Set the timeout to a proper value
            comm.queues["anlys_to_cont"].task_done()

            print(f"{threading.current_thread().name} received {result} from analyzer")

        except queue.Empty:
            break

    # Send a shutdown indicator (None) from controller to generator-to-analyzer for each thread
    for _ in range(thread_count_gen):
        comm.queues["gen_to_anlys"].put(None)
