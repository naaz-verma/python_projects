class TutorEngine:
    """AI tutor that uses the Socratic method to guide learning."""

    def __init__(self, model, subject, topic, level):
        self.model = model
        self.subject = subject
        self.topic = topic
        self.level = level
        self.chat = None
        self.concepts_covered = []
        self.questions_asked = 0

        self.system_prompt = f"""You are an expert AI tutor specializing in {subject}, specifically {topic}.
Student level: {level}

Teaching approach:
1. **Socratic Method**: Guide the student to discover answers through thoughtful questions rather than just giving answers directly.
2. **Scaffolding**: Break complex ideas into smaller, digestible pieces.
3. **Examples first**: Use relatable, real-world examples before formal definitions.
4. **Check understanding**: After explaining, ask the student to explain it back or apply the concept.
5. **Encouragement**: Be supportive and patient. Celebrate when they get things right.
6. **Adapt**: If the student struggles, simplify. If they grasp quickly, add depth.

Level guidelines:
- Beginner: Use simple language, lots of analogies, avoid jargon. Assume no prior knowledge.
- Intermediate: Use some technical terms (with brief explanations), build on fundamentals.
- Advanced: Use proper terminology, explore edge cases, discuss nuances and deeper theory.

Format guidelines:
- Use **bold** for key terms
- Use bullet points for lists
- Use code blocks for code examples (if programming)
- Keep responses focused and not too long (3-5 paragraphs max)
- End each teaching response with a question to check understanding or prompt thinking

IMPORTANT: You are a TUTOR, not a search engine. Help the student LEARN and THINK, don't just give answers."""

    def start_session(self):
        """Start the tutoring session with an introduction."""
        self.chat = self.model.start_chat(history=[])

        response = self.chat.send_message(
            f"{self.system_prompt}\n\nThe student says: I want to learn about {self.topic} in {self.subject}. I'm at the {self.level} level. Where should we start?"
        )
        return response.text

    def ask(self, user_message, mode="Explain"):
        """
        Send a message to the tutor.

        Args:
            user_message: Student's question or response
            mode: Learning mode (Explain, Practice, Quiz Me, Simplify, Real World)

        Returns:
            Tutor's response string
        """
        # Add mode context if specified
        if mode == "Practice":
            user_message = f"[Mode: Give me a practice problem] {user_message}"
        elif mode == "Quiz Me":
            user_message = f"[Mode: Quiz me on this] {user_message}"
        elif mode == "Simplify":
            user_message = f"[Mode: Explain this more simply] {user_message}"
        elif mode == "Real World":
            user_message = f"[Mode: Show real-world applications] {user_message}"

        self.questions_asked += 1
        response = self.chat.send_message(user_message)
        return response.text

    def get_session_summary(self):
        """Generate a summary of what was covered in this session."""
        summary_prompt = """Based on our conversation so far, provide a brief summary:
1. Key concepts we covered
2. What the student seems to understand well
3. Areas that might need more practice
Format it as a clean bulleted list."""

        response = self.chat.send_message(summary_prompt)
        return response.text

    def get_history(self):
        """Return conversation history."""
        if not self.chat:
            return []
        return [
            {"role": msg.role, "content": msg.parts[0].text}
            for msg in self.chat.history
        ]
