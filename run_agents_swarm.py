import json
import os
import threading

from agent_funcs import img_file_analyzer, img_generator
from agent_loop import agent_loop, agent_loop_anlys_with_func, agent_loop_gen_with_func
from agents_build import agent_builder
from agents_swarm import (
    analyzer_agent_with_threading_swarm,
    controller_agent_with_threading_swarm,
    generator_agent_with_threading_swarm,
)
from communication import ThreadCommunication
from configs import parse_kwargs
from shared_components import create_client


def main():
    comm = ThreadCommunication()
    shutdown_event = threading.Event()

    params = parse_kwargs()

    client = create_client()

    # Make directories to save generation and analysis outputs
    try:
        os.makedirs("data/generation")
        os.makedirs("data/analysis")
    except FileExistsError:
        # directory already exists
        pass

    agents_ids_dir_name = "agents_build/ids/"
    agents_ids_file_name = "agent_ids.json"

    try:
        os.makedirs(agents_ids_dir_name)
    except FileExistsError:
        # directory already exists
        pass

    file_path = os.path.join(agents_ids_dir_name, agents_ids_file_name)

    agents_ids_json = []

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            agents_ids = json.load(f)

            cont_agent_id = agents_ids[0]["controller"]
            gen_agent_id = agents_ids[1]["generator"]
            anlys_agent_id = agents_ids[2]["analyzer"]
    else:
        _, agent_cont = agent_builder(
            client,
            params["sys_prompt_cont"],
            params["num_cont_agent"],
            **params["params_cont"],
        )

        cont_agent_id = agent_cont.id

        _, agent_gen = agent_builder(
            client,
            params["sys_prompt_gen"],
            params["num_gen_agent"],
            **params["params_gen"],
        )

        gen_agent_id = agent_gen.id

        _, agent_anlys = agent_builder(
            client,
            params["sys_prompt_anlys"],
            params["num_anlys_agent"],
            **params["params_anlys"],
        )

        anlys_agent_id = agent_anlys.id

        with open(file_path, "w") as file:
            agents_ids_json.append({"controller": cont_agent_id})
            agents_ids_json.append({"generator": gen_agent_id})
            agents_ids_json.append({"analyzer": anlys_agent_id})

            json.dump(agents_ids_json, file)

    # Unify function arguments
    generator_fn = img_generator
    analyzer_fn = img_file_analyzer

    # Create threads
    controller_thread = threading.Thread(
        target=controller_agent_with_threading_swarm,
        args=(
            client,
            cont_agent_id,
            params["subject"],
            params["file_names"],
            shutdown_event,
            params["thread_count_gen"],
            comm,
            params["cont_time_out"],
            agent_loop,
        ),
        name="Communication-Thread-Controller",
    )

    generator_threads = [
        threading.Thread(
            target=generator_agent_with_threading_swarm,
            args=(
                client,
                gen_agent_id,
                comm,
                params["gen_time_out"],
                shutdown_event,
                generator_fn,
                agent_loop_gen_with_func,
            ),
            name=f"Communication-Thread-Generator-{i}",
        )
        for i in range(params["thread_count_gen"])
    ]

    analyzer_threads = [
        threading.Thread(
            target=analyzer_agent_with_threading_swarm,
            args=(
                client,
                anlys_agent_id,
                comm,
                params["anlys_time_out"],
                shutdown_event,
                analyzer_fn,
                agent_loop_anlys_with_func,
            ),
            name=f"Communication-Thread-Analyzer-{i}",
        )
        for i in range(params["thread_count_anlys"])
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
