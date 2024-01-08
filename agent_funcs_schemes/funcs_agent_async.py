img_generator_async_fn = {
    "type": "function",
    "function": {
        "name": "img_generator_async",
        "description": "Generate an image based on user prompt",
        "parameters": {
            "type": "object",
            "properties": {
                "client": {
                    "type": "string",
                    "description": "The LLM openai client.",
                },
                "prompt": {
                    "type": "string",
                    "description": "The user prompt to generate an image, e.g., a nice waterfall.",
                },
                "save_name": {
                    "type": "string",
                    "description": "The image name to be saved as.",
                },
            },
            "required": ["client", "prompt", "save_name"],
        },
    },
}


img_file_analyzer_async_fn = {
    "type": "function",
    "function": {
        "name": "img_file_analyzer_async",
        "description": "Analyze the generated image from a given file",
        "parameters": {
            "type": "object",
            "properties": {
                "image_name": {
                    "type": "string",
                    "description": "The name of the saved image file to analyze.",
                },
                "prompt": {
                    "type": "string",
                    "description": "The user prompt to analyze an image.",
                },
            },
            "required": ["image_path", "prompt"],
        },
    },
}
