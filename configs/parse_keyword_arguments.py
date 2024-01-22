from typing import Dict

from agent_funcs_schemes import (
    img_file_analyzer_async_fn,
    img_file_analyzer_fn,
    img_generator_async_fn,
    img_generator_fn,
)
from prompts import system_prompt_anlys, system_prompt_cont, system_prompt_gen
from type_extensions import T


def parse_kwargs() -> Dict[str, T]:
    params_cont = {"name": "Controller", "model": "gpt-4-1106-preview"}

    cont_time_out = 100
    num_cont_agent = 1

    # The subject structure is formed as follows: [main subject]. [More details about the main subject].
    subject = "A futuristic cityscape. The image should include flying cars and tall skyscrapers with holographic advertisements."

    sys_prompt_cont = system_prompt_cont

    sys_prompt_gen = system_prompt_gen
    params_gen = {
        "name": "Generator",
        "model": "gpt-4-1106-preview",
        "tools": [img_generator_fn],
    }
    params_gen_async = {
        "name": "Generator",
        "model": "gpt-4-1106-preview",
        "tools": [img_generator_async_fn],
    }

    gen_time_out = 1
    # Set this to the number of available threads for generation for multi agent generation
    # or to one for single agent generation
    num_gen_agent = 1
    thread_count_gen = 2

    sys_prompt_anlys = system_prompt_anlys
    params_anlys = {
        "name": "Analyzer",
        "model": "gpt-4-1106-preview",
        "tools": [img_file_analyzer_fn],
    }
    params_anlys_async = {
        "name": "Analyzer",
        "model": "gpt-4-1106-preview",
        "tools": [img_file_analyzer_async_fn],
    }

    anlys_time_out = 90
    # Set this to the number of available threads for analysis for multi agent analysis
    # or to one for single agent analysis
    num_anlys_agent = 1
    thread_count_anlys = 2

    file_names = [
        f"futuristic_cityscape_{i}.png" for i in range(1, thread_count_gen + 1)
    ]

    return {
        "params_cont": params_cont,
        "cont_time_out": cont_time_out,
        "num_cont_agent": num_cont_agent,
        "sys_prompt_cont": sys_prompt_cont,
        "params_gen": params_gen,
        "params_gen_async": params_gen_async,
        "gen_time_out": gen_time_out,
        "num_gen_agent": num_gen_agent,
        "thread_count_gen": thread_count_gen,
        "sys_prompt_gen": sys_prompt_gen,
        "params_anlys": params_anlys,
        "params_anlys_async": params_anlys_async,
        "anlys_time_out": anlys_time_out,
        "num_anlys_agent": num_anlys_agent,
        "thread_count_anlys": thread_count_anlys,
        "sys_prompt_anlys": sys_prompt_anlys,
        "subject": subject,
        "file_names": file_names,
    }
