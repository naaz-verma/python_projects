import requests
from io import BytesIO


def generate_scene_image(client, description, style="digital art"):
    """
    Generate an image for a story scene using DALL-E.

    Args:
        client: OpenAI client
        description: Scene description for the image
        style: Art style to apply

    Returns:
        Image URL string, or None on failure
    """
    prompt = f"{description}, {style}, cinematic lighting, detailed, vibrant colors"

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None


def download_image(url):
    """Download an image from URL and return bytes."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception:
        return None
