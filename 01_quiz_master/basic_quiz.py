# ============================================
#        PYTHON QUIZ GAME (Advanced)
# ============================================
# Concepts: Variables, Functions, if/elif/else,
#           for/while loops, input(), print(),
#           Lists, Dictionaries, random module
# ============================================

import random


# --- Question Bank (list of dictionaries) ---

QUESTIONS = [
    {
        "question": "What is the output of: print(2 ** 3)?",
        "options": {"A": "6", "B": "8", "C": "9", "D": "5"},
        "answer": "B",
        "category": "Operators",
        "difficulty": "easy",
    },
    {
        "question": "Which data type stores True or False?",
        "options": {"A": "str", "B": "int", "C": "bool", "D": "float"},
        "answer": "C",
        "category": "Data Types",
        "difficulty": "easy",
    },
    {
        "question": "What does len('hello') return?",
        "options": {"A": "4", "B": "5", "C": "6", "D": "7"},
        "answer": "B",
        "category": "Built-in Functions",
        "difficulty": "easy",
    },
    {
        "question": "Which keyword is used to create a function?",
        "options": {"A": "func", "B": "define", "C": "function", "D": "def"},
        "answer": "D",
        "category": "Functions",
        "difficulty": "easy",
    },
    {
        "question": "What symbol is used for comments in Python?",
        "options": {"A": "//", "B": "#", "C": "--", "D": "**"},
        "answer": "B",
        "category": "Syntax",
        "difficulty": "easy",
    },
    {
        "question": "What does 'str(123)' return?",
        "options": {"A": "123", "B": "'123'", "C": "Error", "D": "None"},
        "answer": "B",
        "category": "Data Types",
        "difficulty": "medium",
    },
    {
        "question": "Which method adds an item to the end of a list?",
        "options": {"A": "add()", "B": "insert()", "C": "append()", "D": "push()"},
        "answer": "C",
        "category": "Data Types",
        "difficulty": "medium",
    },
    {
        "question": "What is the output of: 10 // 3?",
        "options": {"A": "3.33", "B": "3", "C": "4", "D": "1"},
        "answer": "B",
        "category": "Operators",
        "difficulty": "medium",
    },
    {
        "question": "What does 'break' do inside a loop?",
        "options": {
            "A": "Skips current iteration",
            "B": "Ends the program",
            "C": "Exits the loop",
            "D": "Restarts the loop",
        },
        "answer": "C",
        "category": "Syntax",
        "difficulty": "medium",
    },
    {
        "question": "What is the output of: list(range(3))?",
        "options": {
            "A": "[1, 2, 3]",
            "B": "[0, 1, 2]",
            "C": "[0, 1, 2, 3]",
            "D": "[1, 2]",
        },
        "answer": "B",
        "category": "Built-in Functions",
        "difficulty": "medium",
    },
    {
        "question": "What does 'pass' do in Python?",
        "options": {
            "A": "Exits the function",
            "B": "Skips the block",
            "C": "Does nothing (placeholder)",
            "D": "Returns None",
        },
        "answer": "C",
        "category": "Syntax",
        "difficulty": "hard",
    },
    {
        "question": "What is the output of: type([])?",
        "options": {
            "A": "<class 'tuple'>",
            "B": "<class 'dict'>",
            "C": "<class 'list'>",
            "D": "<class 'set'>",
        },
        "answer": "C",
        "category": "Data Types",
        "difficulty": "hard",
    },
]


# --- Helper Functions ---


def get_categories(questions):
    """Return a sorted list of unique categories from the question bank."""
    categories = []
    for q in questions:
        if q["category"] not in categories:
            categories.append(q["category"])
    categories.sort()
    return categories


def filter_questions(questions, category=None, difficulty=None):
    """Filter questions by category and/or difficulty."""
    filtered = []
    for q in questions:
        match = True
        if category and q["category"] != category:
            match = False
        if difficulty and q["difficulty"] != difficulty:
            match = False
        if match:
            filtered.append(q)
    return filtered


def ask_question(q_number, q_dict):
    """Display a question from a dictionary and return 1 if correct, 0 if wrong."""
    print(f"\nQ{q_number}. {q_dict['question']}")
    print(f"   [Difficulty: {q_dict['difficulty'].upper()}]  [Category: {q_dict['category']}]")

    for letter, text in q_dict["options"].items():
        print(f"   {letter}. {text}")

    valid_choices = list(q_dict["options"].keys())
    answer = input("Your answer (A/B/C/D): ").strip().upper()

    while answer not in valid_choices:
        print("Invalid! Please enter A, B, C, or D.")
        answer = input("Your answer (A/B/C/D): ").strip().upper()

    if answer == q_dict["answer"]:
        print("Correct!")
        return 1
    else:
        correct_letter = q_dict["answer"]
        correct_text = q_dict["options"][correct_letter]
        print(f"Wrong! The correct answer was {correct_letter}. {correct_text}")
        return 0


def show_result(score, total, category_scores):
    """Display the final score, grade, and per-category breakdown."""
    print("\n" + "=" * 45)
    print("            QUIZ COMPLETE!")
    print("=" * 45)

    percentage = round((score / total) * 100) if total > 0 else 0

    print(f"  Score      : {score}/{total}")
    print(f"  Percentage : {percentage}%")

    if percentage >= 80:
        grade = "Excellent!"
    elif percentage >= 60:
        grade = "Good Job!"
    elif percentage >= 40:
        grade = "Keep Learning!"
    else:
        grade = "Try Again!"

    print(f"  Grade      : {grade}")

    # Per-category breakdown
    print("\n  Category Breakdown:")
    print("  " + "-" * 35)
    for cat, scores in sorted(category_scores.items()):
        cat_correct = scores["correct"]
        cat_total = scores["total"]
        cat_pct = round((cat_correct / cat_total) * 100) if cat_total > 0 else 0
        print(f"    {cat:<20} {cat_correct}/{cat_total}  ({cat_pct}%)")

    print("=" * 45)
    return {"score": score, "total": total, "percentage": percentage, "grade": grade}


def show_menu():
    """Display quiz settings menu and return user choices."""
    print("\n--- Quiz Settings ---")

    # Choose category
    categories = get_categories(QUESTIONS)
    print("\nCategories:")
    print("  0. All Categories")
    for i, cat in enumerate(categories, 1):
        count = len(filter_questions(QUESTIONS, category=cat))
        print(f"  {i}. {cat} ({count} questions)")

    cat_choice = input("\nPick a category (number): ").strip()
    chosen_category = None
    if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
        chosen_category = categories[int(cat_choice) - 1]

    # Choose difficulty
    print("\nDifficulty:")
    print("  0. All")
    print("  1. Easy")
    print("  2. Medium")
    print("  3. Hard")

    diff_map = {"1": "easy", "2": "medium", "3": "hard"}
    diff_choice = input("Pick difficulty (number): ").strip()
    chosen_difficulty = diff_map.get(diff_choice, None)

    # Shuffle?
    shuffle_choice = input("Shuffle questions? (yes/no): ").strip().lower()
    shuffle = shuffle_choice == "yes"

    return chosen_category, chosen_difficulty, shuffle


def show_history(history):
    """Display past round results."""
    if not history:
        print("\nNo rounds played yet.")
        return

    print("\n" + "=" * 45)
    print("          SCORE HISTORY")
    print("=" * 45)
    for i, record in enumerate(history, 1):
        print(f"  Round {i}: {record['score']}/{record['total']} "
              f"({record['percentage']}%) - {record['grade']}")
    print("=" * 45)


def run_quiz():
    """Main quiz loop with menu, filtering, and history tracking."""
    history = []  # list of result dicts from each round

    playing = True
    while playing:
        print("\n" + "=" * 45)
        print("     WELCOME TO THE PYTHON QUIZ!")
        print("=" * 45)

        # Menu
        chosen_category, chosen_difficulty, shuffle = show_menu()

        # Filter & prepare questions
        quiz_questions = filter_questions(QUESTIONS, chosen_category, chosen_difficulty)

        if not quiz_questions:
            print("\nNo questions match those filters. Try again!")
            continue

        if shuffle:
            random.shuffle(quiz_questions)

        print(f"\n--- Starting quiz: {len(quiz_questions)} questions ---")
        print("Answer each question by typing A, B, C, or D.\n")

        score = 0
        category_scores = {}  # {"Operators": {"correct": 2, "total": 3}, ...}

        for i, q in enumerate(quiz_questions, 1):
            cat = q["category"]
            if cat not in category_scores:
                category_scores[cat] = {"correct": 0, "total": 0}
            category_scores[cat]["total"] += 1

            result = ask_question(i, q)
            score += result
            category_scores[cat]["correct"] += result

        # Show result and save to history
        round_result = show_result(score, len(quiz_questions), category_scores)
        history.append(round_result)

        # Post-quiz menu
        print("\nWhat next?")
        print("  1. Play again")
        print("  2. View score history")
        print("  3. Quit")

        choice = input("Choice (1/2/3): ").strip()

        if choice == "2":
            show_history(history)
            again = input("\nPlay another round? (yes/no): ").strip().lower()
            if again != "yes":
                playing = False
        elif choice == "1":
            continue
        else:
            playing = False

    # Show final history on exit
    if len(history) > 1:
        show_history(history)

    print("\nThanks for playing!")


# --- Run the program ---
run_quiz()
