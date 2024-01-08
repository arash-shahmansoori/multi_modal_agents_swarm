import queue
import time
from queue import Queue
from threading import Event
from typing import Dict, NoReturn


def analyzer_agent_with_threading_mock_swarm(
    comm: Dict[str, Queue], shutdown_event: Event
) -> NoReturn:
    while not shutdown_event.is_set() or not comm.queues["gen_to_anlys"].empty():
        file_name = None
        msg_anlys = None

        try:
            file_name = comm.queues["gen_to_anlys"].get(timeout=10)

            if file_name is None:
                break

            comm.queues["gen_to_anlys"].task_done()

        except queue.Empty:
            pass

        if file_name:
            try:
                # Handle possible empty queue exception
                msg_anlys = comm.queues["cont_to_anlys"].get_nowait()
                comm.queues["cont_to_anlys"].task_done()

                message_analyzer = msg_anlys["prompt_msg_anlys"]

                time.sleep(10)  # To replicate the delay in analysis

                response = f"Response to >> {message_analyzer}"
                print(response)

                comm.queues["anlys_to_cont"].put(response)

            except queue.Empty:
                pass
