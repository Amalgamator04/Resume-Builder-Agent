
import json
from pathlib import Path
from typing import Any

from PIL import Image
from google import genai
from google.genai import types


def call_gemini(prompt: str, image_path: str | None = None) -> Any:
    """Call Gemini and return the model's JSON response as Python data.

    Put the required response keys/shape in ``prompt``. Set
    ``GEMINI_API_KEY`` in the process environment before calling this.
    Optionally provide a local image path for multimodal prompts.
    """
    api_key = "AIzaSyCMuxXcw2ZaAxLUO34pDXbUZ6KDQD48Z-o"
    if not api_key:
        raise ValueError("Set the GEMINI_API_KEY environment variable first.")

    contents: list[Any] = [prompt]
    if image_path:
        with Image.open(Path(image_path)) as image:
            contents.append(image.copy())

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    try:
        return json.loads(response.text)
    except json.JSONDecodeError as exc:
        raise ValueError("Gemini returned a response that was not valid JSON.") from exc