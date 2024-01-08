from typing import List


def create_requirements(subject: str, color_range: str, texture: str) -> str:
    requirements_blueprint = f"""
    1. **Subject**: A prominently featured, detailed {subject}, with petal tips extending to the edges of the image.
    2. **Color Palette**: Employ a vivid and dynamic color range—orange: {color_range} —to create a visually striking look.
    3. **Texture and Detail**: Introduce a {texture} into {subject} and background elements, incorporating woven or rippled effects for added depth and a tactile feel.
    4. **Light and Shadow**: Use highlights and shadows to impart a three-dimensional, luminous quality to the {subject}.
    5. **Style**: Combine realistic aspects with fantasy to produce a surreal art piece, with exaggerated shapes and flourishes that imply movement.
    6. **Composition**: Aim for a balanced, symmetrical layout that draws the viewer's attention to the {subject} at the center.
    """
    return requirements_blueprint


def create_user_prompt_gen(subjects: List[str], file_names: List[str]) -> List[str]:
    user_prompt_gen = []
    for subject, file_name in zip(subjects, file_names):
        user_prompt_gen.append(
            f"Generate a photo-realistic Image of {subject}. Save the file as: {file_name}"
        )
    return user_prompt_gen


def create_user_prompt_anlys(file_name: str) -> str:
    user_prompt_anlys = f"Analyze the image in file: {file_name} in details."
    return user_prompt_anlys


def create_user_prompt_gen_anlys(subject: str, file_name: str) -> str:
    user_prompt_gen_anlys = f"Generate a photo-realistic Image of {subject} and save the file as: {file_name}. Analyze the generated image in the file {file_name}."

    return user_prompt_gen_anlys
