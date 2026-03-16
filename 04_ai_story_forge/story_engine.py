import json


class StoryEngine:
    """Manages the interactive story using OpenAI."""

    GENRES = {
        "Fantasy": "a magical fantasy world with wizards, dragons, and ancient kingdoms",
        "Sci-Fi": "a futuristic sci-fi universe with space travel, aliens, and advanced technology",
        "Horror": "a suspenseful horror setting with eerie atmosphere (keep it PG-13, suitable for teens)",
        "Mystery": "a gripping mystery with clues, suspects, and plot twists",
        "Adventure": "an exciting adventure with exploration, treasure, and danger",
    }

    def __init__(self, client):
        self.client = client
        self.history = []  # list of {"role": ..., "content": ...}
        self.genre = None
        self.turn_count = 0

    def start_story(self, genre, character_name="the hero"):
        """Begin a new story in the chosen genre."""
        self.genre = genre
        self.turn_count = 0
        self.history = []

        genre_desc = self.GENRES.get(genre, genre)

        system_prompt = f"""You are a master storyteller creating an interactive choose-your-own-adventure story.

Setting: {genre_desc}
Main character: {character_name}

Rules:
- Write vivid, immersive story segments (3-5 paragraphs)
- End EVERY response with exactly 3 choices for the reader
- Make choices meaningful -- they should lead to different story paths
- Include suspense, emotion, and sensory details
- Keep content appropriate for teenagers
- Maintain story continuity based on previous choices

IMPORTANT: Always end your response with choices in this exact format:
---CHOICES---
1. [First choice description]
2. [Second choice description]
3. [Third choice description]"""

        self.history.append({"role": "system", "content": system_prompt})
        self.history.append({"role": "user", "content": f"Begin the {genre} story. Set the scene and introduce {character_name}."})

        response = self._get_response()
        self.turn_count += 1
        return self._parse_response(response)

    def make_choice(self, choice_text):
        """Continue the story based on the player's choice."""
        self.history.append({
            "role": "user",
            "content": f"I choose: {choice_text}\n\nContinue the story based on this choice. Remember to end with 3 new choices in the ---CHOICES--- format."
        })

        response = self._get_response()
        self.turn_count += 1
        return self._parse_response(response)

    def _get_response(self):
        """Call OpenAI API and return the response text."""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            temperature=0.9,
            max_tokens=1000,
        )
        content = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": content})
        return content

    def _parse_response(self, text):
        """Split the response into story text and choices."""
        if "---CHOICES---" in text:
            parts = text.split("---CHOICES---")
            story_text = parts[0].strip()
            choices_text = parts[1].strip()

            choices = []
            for line in choices_text.split("\n"):
                line = line.strip()
                if line and line[0].isdigit():
                    # Remove the number prefix (1. , 2. , 3. )
                    choice = line.split(".", 1)[-1].strip()
                    choices.append(choice)

            return {"story": story_text, "choices": choices[:3]}

        # Fallback: no choices delimiter found
        return {"story": text, "choices": []}

    def get_scene_description(self, story_text):
        """Generate a short image prompt from the current scene."""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Convert the following story scene into a single concise image description (under 50 words) suitable for an AI image generator. Focus on the visual elements: setting, characters, lighting, mood. Use descriptive art style terms. Do not include text or words in the image."},
                {"role": "user", "content": story_text[:500]}
            ],
            temperature=0.7,
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
