from io import BytesIO


def generate_scene_image(model, description, style="digital art"):
    """
    Generate an image for a story scene.

    Note: Image generation is not available with the free Gemini API tier.
    This function is kept as a placeholder for future use.

    Returns:
        None (image generation disabled)
    """
    return None


def download_image(url):
    """Download an image from URL and return bytes."""
    try:
        import requests
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception:
        return None
