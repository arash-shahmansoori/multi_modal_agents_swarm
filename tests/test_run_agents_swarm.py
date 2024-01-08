import queue
import threading

from agents_swarm_mock import (
    analyzer_agent_with_threading_mock_swarm,
    controller_agent_with_threading_mock_swarm,
    generator_agent_with_threading_mock_swarm,
)


class ThreadCommunication:
    def __init__(self):
        self.queues = {
            "cont_to_gen": queue.Queue(),
            "cont_to_anlys": queue.Queue(),
            "gen_to_anlys": queue.Queue(),
            "anlys_to_gen": queue.Queue(),
            "anlys_to_cont": queue.Queue(),
        }


def main():
    comm = ThreadCommunication()
    shutdown_event = threading.Event()

    thread_count_gen = 2
    thread_count_anlys = 2

    params = {"subject": "a flower", "file_names": ["flower_1.png", "flower_2.png"]}

    # Create threads
    controller_thread = threading.Thread(
        target=controller_agent_with_threading_mock_swarm,
        args=(
            params["subject"],
            params["file_names"],
            shutdown_event,
            thread_count_gen,
            comm,
        ),
        name="Communication-Thread-Controller",
    )

    generator_threads = [
        threading.Thread(
            target=generator_agent_with_threading_mock_swarm,
            args=(
                comm,
                shutdown_event,
            ),
            name=f"Communication-Thread-Generator-{i}",
        )
        for i in range(thread_count_gen)
    ]

    analyzer_threads = [
        threading.Thread(
            target=analyzer_agent_with_threading_mock_swarm,
            args=(
                comm,
                shutdown_event,
            ),
            name=f"Communication-Thread-Analyzer-{l}",
        )
        for l in range(thread_count_anlys)
    ]

    # Start threads
    controller_thread.start()

    for generator_thread in generator_threads:
        generator_thread.start()

    for analyzer_thread in analyzer_threads:
        analyzer_thread.start()

    # Wait for threads to finish
    controller_thread.join()

    for generator_thread in generator_threads:
        generator_thread.join()

    for analyzer_thread in analyzer_threads:
        analyzer_thread.join()

    # All threads have completed their tasks
    print("All tasks completed.")


if __name__ == "__main__":
    main()
