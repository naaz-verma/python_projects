# ============================================
#        BASIC PYTHON QUIZ GAME
# ============================================
# Concepts: Variables, Functions, if/elif/else,
#           while loop, input(), print()
# ============================================


def ask_question(q_number, question, a, b, c, d, correct):
    """Display a question, take answer, and return 1 if correct, 0 if wrong."""
    print(f"\nQ{q_number}. {question}")
    print(f"   A. {a}")
    print(f"   B. {b}")
    print(f"   C. {c}")
    print(f"   D. {d}")

    answer = input("Your answer (A/B/C/D): ").strip().upper()

    while answer != "A" and answer != "B" and answer != "C" and answer != "D":
        print("Invalid! Please enter A, B, C, or D.")
        answer = input("Your answer (A/B/C/D): ").strip().upper()

    if answer == correct:
        print("Correct!")
        return 1
    else:
        print(f"Wrong! The correct answer was {correct}.")
        return 0


def show_result(score, total):
    """Display the final score and grade."""
    print("\n" + "=" * 40)
    print("          QUIZ COMPLETE!")
    print("=" * 40)

    percentage = round((score / total) * 100)

    print(f"  Score      : {score}/{total}")
    print(f"  Percentage : {percentage}%")

    if percentage >= 80:
        print("  Grade      : Excellent!")
    elif percentage >= 60:
        print("  Grade      : Good Job!")
    elif percentage >= 40:
        print("  Grade      : Keep Learning!")
    else:
        print("  Grade      : Try Again!")

    print("=" * 40)


def run_quiz():
    """Run the quiz by asking each question one by one."""
    print("=" * 40)
    print("   WELCOME TO THE PYTHON QUIZ!")
    print("=" * 40)
    print("Answer each question by typing A, B, C, or D.\n")

    score = 0

    score = score + ask_question(1,
        "What is the output of: print(2 ** 3)?",
        "6", "8", "9", "5",
        "B"
    )

    score = score + ask_question(2,
        "Which data type stores True or False?",
        "str", "int", "bool", "float",
        "C"
    )

    score = score + ask_question(3,
        "What does len('hello') return?",
        "4", "5", "6", "7",
        "B"
    )

    score = score + ask_question(4,
        "Which keyword is used to create a function?",
        "func", "define", "function", "def",
        "D"
    )

    score = score + ask_question(5,
        "What symbol is used for comments in Python?",
        "//", "#", "--", "**",
        "B"
    )

    show_result(score, 5)

    play_again = input("\nWant to play again? (yes/no): ").strip().lower()
    if play_again == "yes":
        run_quiz()
    else:
        print("\nThanks for playing!")


# --- Run the program ---
run_quiz()
