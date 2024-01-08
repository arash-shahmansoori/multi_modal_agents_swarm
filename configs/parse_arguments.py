import argparse
from argparse import Namespace


def parse_args() -> Namespace:
    # Commandline arguments
    parser = argparse.ArgumentParser(description="Arguments for Multi-Modal Swarm")
    ### Parameters for Multi-Modal Swarm ###
    parser.add_argument("--num_threads", default=2, type=int)

    args = parser.parse_args()
    return args
