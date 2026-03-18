class StoryEngine:
    """Manages the interactive story using Gemini."""

    GENRES = {
        "Fantasy": "a magical fantasy world with wizards, dragons, and ancient kingdoms",
        "Sci-Fi": "a futuristic sci-fi universe with space travel, aliens, and advanced technology",
        "Horror": "a suspenseful horror setting with eerie atmosphere (keep it PG-13, suitable for teens)",
        "Mystery": "a gripping mystery with clues, suspects, and plot twists",
        "Adventure": "an exciting adventure with exploration, treasure, and danger",
    }

    def __init__(self, model):
        self.model = model
        self.chat = None
        self.genre = None
        self.turn_count = 0

    def start_story(self, genre, character_name="the hero"):
        """Begin a new story in the chosen genre."""
        self.genre = genre
        self.turn_count = 0

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

        self.chat = self.model.start_chat(history=[])

        response = self.chat.send_message(
            f"{system_prompt}\n\nBegin the {genre} story. Set the scene and introduce {character_name}."
        )

        self.turn_count += 1
        return self._parse_response(response.text)

    def make_choice(self, choice_text):
        """Continue the story based on the player's choice."""
        response = self.chat.send_message(
            f"I choose: {choice_text}\n\nContinue the story based on this choice. Remember to end with 3 new choices in the ---CHOICES--- format."
        )

        self.turn_count += 1
        return self._parse_response(response.text)

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
        response = self.model.generate_content(
            f"Convert the following story scene into a single concise image description (under 50 words) suitable for an AI image generator. Focus on the visual elements: setting, characters, lighting, mood. Use descriptive art style terms. Do not include text or words in the image.\n\n{story_text[:500]}"
        )
        return response.text.strip()
