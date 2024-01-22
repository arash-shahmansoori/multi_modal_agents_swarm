import json
import os
import threading

from agent_funcs import img_file_analyzer_async, img_generator_async
from agent_loop import agent_loop_anlys_with_func, agent_loop_gen_with_func
from agents_build import agent_builder
from asyc_gen_analysis import (
    async_analyzer_agent_with_threading,
    async_generator_agent_with_threading,
)
from configs import parse_kwargs
from shared_components import create_client


def main():
    params = parse_kwargs()

    client = create_client()

    agents_ids_dir_name = "agents_build/ids/"
    agents_ids_file_name = "agent_ids_async.json"

    # Make directories to save generation and analysis outputs
    try:
        os.makedirs("data_async/generation")
        os.makedirs("data_async/analysis")

        os.makedirs(agents_ids_dir_name)
    except FileExistsError:
        # directory already exists
        pass

    file_path = os.path.join(agents_ids_dir_name, agents_ids_file_name)

    agents_ids_json = []

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            agents_ids = json.load(f)

            gen_agent_id = agents_ids[0]["generator"]
            anlys_agent_id = agents_ids[1]["analyzer"]

    else:
        _, agent_gen = agent_builder(
            client,
            params["sys_prompt_gen"],
            params["num_gen_agent"],
            **params["params_gen_async"],
        )

        gen_agent_id = agent_gen.id

        _, agent_anlys = agent_builder(
            client,
            params["sys_prompt_anlys"],
            params["num_anlys_agent"],
            **params["params_anlys_async"],
        )

        anlys_agent_id = agent_anlys.id

        with open(file_path, "w") as file:
            agents_ids_json.append({"generator": gen_agent_id})
            agents_ids_json.append({"analyzer": anlys_agent_id})

            json.dump(agents_ids_json, file)

    generator_fn = img_generator_async
    analyzer_fn = img_file_analyzer_async

    subject = params["subject"]

    msg_gen = f"Generate a photo-realistic Image of {subject}"
    msg_anlys = f"Analyze the generated image in the file "

    # Create threads
    generator_threads = [
        threading.Thread(
            target=async_generator_agent_with_threading,
            args=(
                client,
                gen_agent_id,
                msg_gen,
                params["file_names"][i],
                generator_fn,
                agent_loop_gen_with_func,
            ),
            name=f"Thread-Generator-{i}",
        )
        for i in range(params["thread_count_gen"])
    ]

    analyzer_threads = [
        threading.Thread(
            target=async_analyzer_agent_with_threading,
            args=(
                client,
                anlys_agent_id,
                msg_anlys,
                params["file_names"][i],
                analyzer_fn,
                agent_loop_anlys_with_func,
            ),
            name=f"Thread-Analyzer-{i}",
        )
        for i in range(params["thread_count_anlys"])
    ]

    # Start threads & Wait for threads to finish generation
    for generator_thread in generator_threads:
        generator_thread.start()

    for generator_thread in generator_threads:
        generator_thread.join()

    print("Generation completed.")

    # Start threads & Wait for threads to finish analysis
    for analyzer_thread in analyzer_threads:
        analyzer_thread.start()

    for analyzer_thread in analyzer_threads:
        analyzer_thread.join()

    print("Analysis completed.")


if __name__ == "__main__":
    main()
