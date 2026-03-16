# Subject configurations for AI Tutor

SUBJECTS = {
    "Mathematics": {
        "emoji": "🔢",
        "topics": ["Algebra", "Geometry", "Trigonometry", "Calculus", "Statistics", "Number Theory"],
        "description": "From basic algebra to advanced calculus",
    },
    "Science": {
        "emoji": "🔬",
        "topics": ["Physics", "Chemistry", "Biology", "Earth Science", "Astronomy", "Environmental Science"],
        "description": "Explore the natural world through science",
    },
    "History": {
        "emoji": "📜",
        "topics": ["Ancient Civilizations", "Medieval History", "World Wars", "Indian History", "Modern History", "Historical Figures"],
        "description": "Journey through time and civilizations",
    },
    "Programming": {
        "emoji": "💻",
        "topics": ["Python Basics", "Data Structures", "Algorithms", "Web Development", "Object-Oriented Programming", "Databases"],
        "description": "Learn to code and build software",
    },
    "English": {
        "emoji": "📚",
        "topics": ["Grammar", "Vocabulary", "Essay Writing", "Literature", "Poetry Analysis", "Public Speaking"],
        "description": "Master the English language",
    },
    "General Knowledge": {
        "emoji": "🌍",
        "topics": ["Geography", "Current Affairs", "Arts & Culture", "Sports", "Technology", "Famous Personalities"],
        "description": "Broaden your knowledge across topics",
    },
}

LEVELS = ["Beginner", "Intermediate", "Advanced"]

LEARNING_MODES = {
    "Explain": "Explain a concept clearly with examples",
    "Practice": "Give me a practice problem to solve",
    "Quiz Me": "Test my understanding with questions",
    "Simplify": "Break this down in simpler terms",
    "Real World": "Show me real-world applications of this concept",
}


def get_subject_names():
    return list(SUBJECTS.keys())


def get_subject(name):
    return SUBJECTS.get(name)
