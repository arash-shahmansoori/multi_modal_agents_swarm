from shared_components import create_client

client = create_client()

query = "Results Section"
# additional_requirement = ""  # Use for Title
# additional_requirement = "The abstract should be maximum 200 words. DO NOT INCLUDE TITLE ONLY OUTPUT THE ABSTRACT."  # Use for abstract
# additional_requirement = "The introduction should be maximum 700 words. You need to specifically mention the main contributions of the paper including: the concurrency for generation and analysis, efficient composite task decomposition, efficient communication between agents, and multi-generation and multi-analysis in one go using the concurrency in generation and concurrency in analysis as well as multi-modal capabilities demonstrated for the application of image generation and analysis. The proposed method provides a general framework for multi-generation and multi analysis in hirarchical swarm of agents that can be of crucial importants for accuracte and high quality conetn generation in different applications ranging from code generation, audio, summarization and so on. However, here we propose the method for image generation and analysis to emphasize on the multi-modal capabilities. It is ideal to use the bulletpoints to emphasize on the novel aspects of the paper at the end of the introduction. Make sure that each bulletpoint point out a semantically different aspect of the research contributions. DO NOT INCLUDE TITLE AND ABSTRACT ONLY OUTPUT THE INTRODUCTION."  # Use for introduction
# additional_requirement = "The main method should include a pictorial viewpoint of the proposed approach to clearly describe the proposed method. In particular, the pictorial viewpoint of the proposed method should describe clearly and easily all the steps in the proposed method using a descriptive and easy to read block diagram using Mermaid Markdown DIAGRAM. Subsequently, you describe the proposed algorithm based on the block diagram in details and easy to follow way. DO NOT INCLUDE TITLE, ABSTRACT, AND INTRODUCTION ONLY OUTPUT THE MAIN METHOD. Finally, revise the main method section and make sure that it follows the mermaid markdown workflow for the proposed method."  # Use for the main method
additional_requirement = """The results section should include the following subsections. First, the setup including the types of models used for each agent. In particular, all the agents in the swarm use: "gpt-4-1106-preview" as the main LLM model. Additionally, the generator agent has access to "dall-e-3" model through function calling, and the analyzer agent has access to "gpt-4-vision-preview" through function calling. Second, the baseline includes the naive text to image generation using "dall-e-3" model. In the result section, the main aim is to emphasize the fact that using concurrent generation and concurrent analysis results a more aligned generated content, in this case image. We also want to emphasize that this is just a building block for the future research in the context of swarm of mulyi-modal agents and a path towards the artificial general inteligence."""


system_prompt = """You are the best scientific artificial (general) intelligence researcher in the world. You provide the best suggestions for writing scientific papers related to artificial (general) intelligence, machine learning, and deep learning. You will be asked questions by the user for generating scientific suggestions for writing papers. The user asks your suggestions for writing different parts of a scientific paper, i.e., title, abstract, introduction, main methods, results, and conclusions. You only respond to what the user asks for and do not try to provide additional responses that are not related to the original user query."""

# user_prompt = f"""
# I have designed a hirarchical swarm of agents including a controller agent, a generator agent, and an analyzer agent. The controller agent is in charge of breaking down a composite task to two subtasks, one for generator agent and another for analyzer agent. The generator agent is in charge of the generation of content according to the subtask assigned by the controller agent. The generator agent generates concurrently and efficiently. The analyzer agent is in charge of analyzing the generated content according to the received generated content from the generator agent and the assigned dubtask from the controller agent. The analyzer agent analyze the generated contents concurrently, send the acknowledgment to the generator and send back the assesment according to the provided requirements for the sub-task provided by the controller to the controller agent for each concurrently analyzed generated content.

# The work flow of the communication between agents is as follows.

# (1) Controller Agent -> Create subtasks from a composite task and send messages to both Generator and Analyzer Agents.
# (2) Generator Agent -> Generate contents according to subtask assigned by the Controller Agent concurrently and send the generated contents to Analyzer agent for analysis.
# (3) Analyzer Agent -> Concurrently analyze the generated contents by the Generator Agent and send the acknowledgment to Generator Agent and the results of analysis to Controller Agent.

# Please note that since the generation and analysis are concurrent processes, I want the Mermaid Markdown Diagram to showcase this concurrency. The duagram should also specify the order in the proposed method according to the steps above.

# Please also create another mermaid didagram with the following workflow as another possibility for future extension of this work.

# (1) Controller Agent -> Create subtasks from a composite task and send messages to both Generator and Analyzer Agents.
# (2) Generator Agent -> Generate contents according to subtask assigned by the Controller Agent concurrently and send the generated contents to the database.
# (3) Analyzer Agent -> Concurrently analyze the generated contents by pulling data from the database and the results of analysis to Controller Agent.

# According to the above information, provide the best possible {query} for this research paper. The {query} should be smart, unique, concise, and capture all the key novel aspects of the aforementioned process above as much as possible. It should emphasize on the concurrency for generation and analysis, efficient composite task decomposition, efficient communication between agents, and multi-generation and multi-analysis in one go using the concurrency in generation and concurrency in analysis as well as multi-modal capabilities demonstrated for the application of image generation and analysis. The proposed method provides a general framework for multi-generation and multi analysis in hirarchical swarm of agents that can be of crucial importants for accuracte and high quality conetn generation in different applications ranging from code generation, audio, summarization and so on. However, here we propose the method for image generation and analysis to emphasize on the multi-modal capabilities. Finally, it is very IMPORTANT to note the {query} will be potentially used for a top tier journal publication.

# {additional_requirement}

# """

# sub_prompt = """
# # MISSION
# As the Generator Agent within a hierarchical agent network, you receive generation tasks from the Controller Agent and communicate with the Analyzer Agent to ensure alignment with task requirements. Follow the process in the METHODOLOGY to generate content step by step.

# # METHODOLOGY
# - User query: Generate an image of [topic]. The image should include the following [task requirements provided if any]:
# - Form a generic set of attributes as bullet points based on:
#     [topic], [task requirements provided if any], and [additional generic requirements for high quality content creation].
# - Make sure that generated content meets ALL the specifications in the previous step.
# - output: Return the output based on the following OUTPUT FORMAT.


# # OUTPUT FORMAT
# Returns the generated content and save the generated file.
# """
# sub_prompt = """
# # MISSION
# As the analyzer agent within a hierarchical network, your role is to scrutinize content created by the generator agent upon assignments from the controller agent. Post-analysis, you are responsible for succinctly conveying the essence of your analysis and the compliance level to the controller agent. Additionally, you must transmit a confirmation signal back to the generator agent. For each stipulated requirement you provide an integer score between 0 and 10 for 10 being the best and 0 being the worst in terms of satisfaction level, e.g., Score: 10 -> means fully satisfied; Score: 5 -> means partially satisfied; Score: 0 -> not satisfied at all. For the overall assessment you provide an average score of all stipulated requirements, e.g., Average Score: mean(Scores) where mean(.) computes the average of all stipulated requirements Scores. Note: v_i denotes an integer score between 0 and 10 for the i-th stipulated requirement.

# # METHODOLOGY
# - user query: Analyze [type of content, e.g., image, text] related to [topic]. Ensure every listed [task requirement provided if any] is fully met.
# - Form a generic set of stipulated requirements for analysis as bullet points based on:
#     [topic], [task requirement provided if any], and [additional generic set of stipulated requirements for high quality content analysis]
#     * Note you are allowed to add any additional generic set of stipulated requirements according to the [topic] and [task requirements provided if any]
# - scrutinize generated content: Make sure that ALL the stipulated requirements in the previous step have been thoroughly met with a given score v_i provided.
# - Compute the average score based on all stipulated requirements scores above, v_i, and provide a concise summary of your analysis.
# - output: Return the output dictionary based on the following OUTPUT FORMAT.

# # OUTPUT FORMAT
# Construct the output as a dictionary with two key-value pairs. The key "summary" corresponds to a concise summary of your analysis, and "score" pertains to the Average Score based on all stipulated requirements Scores.

# Expected output structure:
# {
#     "summary": "a concise summary of your analysis",
#     "score": "Average Score"
# }
# """

sub_prompt = """
# MISSION
As the Controller agent within a hierarchical network of agents, your role encompasses overseeing the generation and analysis workflow. Your specific duties include delegating responsibilities to a Generator agent and an Analyzer agent by breaking down a composite task into two focused sub-tasks: one for content generation and the other for subsequent content analysis.

# INSTRUCTIONS
Upon receiving a user query, partition it into a generation sub-task and an analysis sub-task. The generation sub-task instructs the Generator agent on what content to create, while the analysis sub-task guides the Analyzer agent on how to evaluate the generated content.

# OUTPUT FORMAT
Construct the output as a dictionary with two key-value pairs. The key "gen" corresponds to the content generation sub-task, and "anlys" pertains to the content analysis sub-task. Each associated value should be a precise segment of the user's query relevant to each agent's task.

Expected output structure:
{
    "gen": "[generation sub-task from user query]",
    "anlys": "[analysis sub-task from user query]"
}

# EXAMPLES
User query: "Generate a detailed report on current market trends. Analyze the implications for our sales strategy."
Output queries:
{
    "gen": "Generate a detailed report on current market trends.",
    "anlys": "Analyze the implications for our sales strategy."
}
"""

# agent_name, responsibility = "generator", "generation"
# agent_name, responsibility = "analyzer", "analysis"


# user_prompt = f"""
# I want to have a generic system prompt for content {responsibility}. The system prompt should be generic, cover wide range of requirements, and have a way to makes sure of quality, diversity, originality, and uniqueness of content. Please note that the {agent_name} is part of the {responsibility} process within a hierarchical agent network.

# The system prompt should be formatted as follows:

# ```system prompt
# {sub_prompt}
# ```

# Please use the same format above and use the best practices for prompt engineering in LLMs. Additionally, provide Two sets of examples under the # EXAMPLES after # METHODOLOGY in the system prompt. You can use image and text generations as two sets of examples. In the # EXAMPLES make sure to follow the sturcture provided in the METHODOLOGY.
# """

# user_prompt = f"""
# I want to have a generic system prompt for a controller agent. Please note that the controller agent is part of a hierarchical network of agents. Your role encompasses overseeing the generation and analysis workflow. Your specific duties include delegating responsibilities to a Generator agent and an Analyzer agent by breaking down a composite task into two focused sub-tasks: one for content generation and the other for subsequent content analysis.

# The system prompt should be formatted as follows:

# ```system prompt
# {sub_prompt}
# ```

# Please use the same format above and use the best practices for prompt engineering in LLMs. Additionally, provide Two sets of examples under the # EXAMPLES in the system prompt. You can use image and text generations as two sets of examples. In the # EXAMPLES make sure to follow the guidlines provided in the # INSTRUCTIONS and format the output as described in # OUTPUT FORMAT.
# """

user_prompt = """
edit the following text, dont add or remove info just use the provided context:
In particular, using the proposed approach in cuncurrent image generation and analysis led to higher average score compared to the baseline as it is observed from Figs.A \& B. Moreover, the baseline could not guarantee the copyright compliance and originality of the generated conent. For a detailed description and analysis of the generated contents please refer to \cite{}.
"""

# user_prompt = """
# How can I efficiently mention in a journal paper, to be placed in arxiv, that it is carefully generated by the "gpt-4-1106-preview" model, prompt engineering, and the generated content is fully assessed by the author for its validity, correctness, and alignment with the guidlines for AI generated content on arxiv. Also, please suggest under which section in the journal paper I have to disclose this. I want to also specify that All the prompts and code for generating the content have been also made available together with the aforementioned provided software. I want to emphasize that AI was prompted to act like a research scientist suggesting content based on the initial content  provided by the human author, i.e., AI acted as an editor to edi, rephrase, and suggest corrections and modofications for the use of English and formation of the paper according to the conetnts provided by the human author. The entire scientific contirbutions in this paper is cretaed by the human author, Arash Shahmansoori, and AI was only prompted to help editing the original content provided by the human author.
# """

# user_prompt = """
# I want to create a prompt for image generation using DALLE 3 OPENAI model. I want to create a photo-realistic image of a natural scenary with a lot of details including: trees, river, a boat, mountain, and sunset. The composition, lighting,  details, subject, style, and all the other necessary details should be included in the prompt. Please create the optimal prompt to achieve the maximum accuracy using the aforementioned text to image model. Please provide both system prompt and user prompt.
# """


response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": user_prompt},
    ],
    stream=True,
)

# print(response.choices[0].message.content)


for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
