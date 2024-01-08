from agents_remove import remove_agents
from shared_components import create_client

client = create_client()

remove_agents(client, 100)
