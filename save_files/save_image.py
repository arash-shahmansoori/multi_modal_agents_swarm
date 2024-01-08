import os
from io import BytesIO

import dotenv
import requests
from PIL import Image

dotenv.load_dotenv()


def save_img_from_url(url: str, save_name: str = "image.png") -> str:
    """Save the generated image from a url"""
    response = requests.get(url)
    # Open the image
    img = Image.open(BytesIO(response.content))

    img.save(os.path.join("./data/generation/", save_name))

    status = f"Image {save_name} saved."
    return status


def save_img_from_url_volumes(url: str, save_name: str = "image.png") -> str:
    """Save the generated image from a url and persist saved images in volumes"""
    response = requests.get(url)
    # Open the image
    img = Image.open(BytesIO(response.content))

    # img.save(os.path.join("./data/images/", save_name))

    # Persist saved images in images volume
    img_path = os.getenv("GEN_PATH")
    img.save(os.path.join(img_path, save_name))

    status = f"Image {save_name} saved."
    return status
