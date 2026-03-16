class Chatbot:
    """AI chatbot with configurable personality."""

    def __init__(self, client, personality):
        """
        Args:
            client: OpenAI client
            personality: dict with name, system_prompt, greeting, etc.
        """
        self.client = client
        self.personality = personality
        self.messages = [
            {"role": "system", "content": personality["system_prompt"]}
        ]

    def get_greeting(self):
        """Return the personality's greeting message."""
        return self.personality.get("greeting", "Hello! How can I help you?")

    def chat(self, user_message):
        """
        Send a message and get a response in character.

        Args:
            user_message: The user's input text

        Returns:
            The chatbot's response string
        """
        self.messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=0.8,
            max_tokens=500,
        )

        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})

        return reply

    def get_history(self):
        """Return the conversation history (excluding system prompt)."""
        return [m for m in self.messages if m["role"] != "system"]

    def export_chat(self):
        """Export chat history as a readable string."""
        lines = []
        name = self.personality.get("name", "Bot")
        for msg in self.messages:
            if msg["role"] == "system":
                continue
            elif msg["role"] == "user":
                lines.append(f"You: {msg['content']}")
            else:
                lines.append(f"{name}: {msg['content']}")
            lines.append("")
        return "\n".join(lines)
