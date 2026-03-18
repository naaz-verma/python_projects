class Chatbot:
    """AI chatbot with configurable personality."""

    def __init__(self, model, personality):
        """
        Args:
            model: Gemini GenerativeModel
            personality: dict with name, system_prompt, greeting, etc.
        """
        self.model = model
        self.personality = personality
        self.chat = model.start_chat(history=[])
        self.system_prompt = personality["system_prompt"]
        self.messages = []
        # Send the system prompt as the first message to set the personality
        self.chat.send_message(f"[System instruction] {self.system_prompt}\n\nAcknowledge that you understand your role and wait for the user's first message. Reply only with 'Ready.'")

    def get_greeting(self):
        """Return the personality's greeting message."""
        return self.personality.get("greeting", "Hello! How can I help you?")

    def chat_message(self, user_message):
        """
        Send a message and get a response in character.

        Args:
            user_message: The user's input text

        Returns:
            The chatbot's response string
        """
        self.messages.append({"role": "user", "content": user_message})

        response = self.chat.send_message(user_message)
        reply = response.text

        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def get_history(self):
        """Return the conversation history."""
        return self.messages

    def export_chat(self):
        """Export chat history as a readable string."""
        lines = []
        name = self.personality.get("name", "Bot")
        for msg in self.messages:
            if msg["role"] == "user":
                lines.append(f"You: {msg['content']}")
            else:
                lines.append(f"{name}: {msg['content']}")
            lines.append("")
        return "\n".join(lines)
