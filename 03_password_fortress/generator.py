import random
import string


def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True,
                      use_special=True, exclude_ambiguous=False):
    """Generate a secure random password."""
    charset = ""
    required = []

    if use_lower:
        lower = string.ascii_lowercase
        if exclude_ambiguous:
            lower = lower.replace("l", "").replace("o", "")
        charset += lower
        required.append(random.choice(lower))

    if use_upper:
        upper = string.ascii_uppercase
        if exclude_ambiguous:
            upper = upper.replace("I", "").replace("O", "")
        charset += upper
        required.append(random.choice(upper))

    if use_digits:
        digits = string.digits
        if exclude_ambiguous:
            digits = digits.replace("0", "").replace("1", "")
        charset += digits
        required.append(random.choice(digits))

    if use_special:
        special = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        charset += special
        required.append(random.choice(special))

    if not charset:
        charset = string.ascii_letters + string.digits
        required = [random.choice(charset)]

    # Fill remaining length
    remaining = length - len(required)
    password_chars = required + [random.choice(charset) for _ in range(max(0, remaining))]

    # Shuffle so required chars aren't always at the start
    random.shuffle(password_chars)

    return "".join(password_chars)


def generate_passphrase(num_words=4, separator="-", capitalize=True):
    """Generate a memorable passphrase from random words."""
    # A curated list of simple, memorable words
    words = [
        "apple", "brave", "cloud", "dance", "eagle", "flame", "grape", "happy",
        "ivory", "jungle", "knife", "lemon", "magic", "noble", "ocean", "piano",
        "quest", "river", "storm", "tiger", "ultra", "vivid", "whale", "xenon",
        "yacht", "zebra", "arrow", "bloom", "chess", "dream", "frost", "globe",
        "heart", "index", "joker", "karma", "lotus", "maple", "night", "orbit",
        "pearl", "quilt", "reign", "solar", "torch", "unity", "verse", "wings",
        "pixel", "spark", "blaze", "coral", "delta", "ember", "forge", "ghost",
        "haven", "crown", "prism", "azure", "lunar", "cyber", "nexus", "vault",
        "omega", "pulse", "scout", "trail", "stone", "breeze", "cliff", "dusk",
        "fable", "glint", "hover", "lance", "marsh", "north", "olive", "plume",
    ]

    chosen = random.sample(words, min(num_words, len(words)))
    if capitalize:
        chosen = [w.capitalize() for w in chosen]

    return separator.join(chosen)
