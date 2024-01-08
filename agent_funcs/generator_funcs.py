import openai
from openai import OpenAI

from save_files import save_img_from_url, save_img_from_url_volumes


def img_generator(client: OpenAI, **kwargs) -> str:
    """Generate an image based on user prompt"""

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=kwargs["prompt"],
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        print(image_url)

        img_creation_status = save_img_from_url(image_url, kwargs["save_name"])
        print(img_creation_status)

    except openai.OpenAIError as e:
        image_url = e.error

    return image_url


def img_generator_docker(client: OpenAI, **kwargs) -> str:
    """Generate an image based on user prompt with docker containers"""

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=kwargs["prompt"],
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        print(image_url)

        img_creation_status = save_img_from_url_volumes(image_url, kwargs["save_name"])
        print(img_creation_status)

    except openai.OpenAIError as e:
        image_url = e.error

    return image_url
