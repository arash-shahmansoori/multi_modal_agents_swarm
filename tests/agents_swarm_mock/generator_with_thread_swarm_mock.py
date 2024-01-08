import queue
import time
from queue import Queue
from threading import Event
from typing import Dict, NoReturn


def generator_agent_with_threading_mock_swarm(
    comm: Dict[str, Queue], shutdown_event: Event
) -> NoReturn:
    while not shutdown_event.is_set():
        try:
            msg_gen = comm.queues["cont_to_gen"].get(timeout=1)

            time.sleep(5)  # To replicate the delay for generation

            response = f"Generated the image in file >> "
            print(response, msg_gen["file_name"])

            comm.queues["gen_to_anlys"].put(msg_gen["file_name"])

        except queue.Empty:
            continue

        comm.queues["cont_to_gen"].task_done()
    # Indicate to analyzer that this thread is no longer sending tasks
    comm.queues["gen_to_anlys"].put(None)
