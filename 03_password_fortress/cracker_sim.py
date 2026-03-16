import hashlib
import time
import string
import itertools


def hash_password(password, algorithm="sha256"):
    """Hash a password using the specified algorithm."""
    if algorithm == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    return hashlib.sha256(password.encode()).hexdigest()


def brute_force_sim(target_password, max_length=4, callback=None):
    """
    Simulate a brute force attack (educational).
    Only works on short passwords for demo purposes.

    Args:
        target_password: The password to crack
        max_length: Maximum length to try (capped at 4 for performance)
        callback: Function called with (attempts, current_guess) for progress updates

    Returns:
        dict with results
    """
    target_hash = hash_password(target_password)
    charset = string.ascii_lowercase + string.digits
    attempts = 0
    start_time = time.time()

    # Cap max_length for demo safety
    max_length = min(max_length, 4)

    for length in range(1, max_length + 1):
        for guess_tuple in itertools.product(charset, repeat=length):
            guess = "".join(guess_tuple)
            attempts += 1

            if callback and attempts % 10000 == 0:
                callback(attempts, guess)

            if hash_password(guess) == target_hash:
                elapsed = time.time() - start_time
                return {
                    "cracked": True,
                    "password": guess,
                    "attempts": attempts,
                    "time": round(elapsed, 3),
                    "speed": round(attempts / elapsed) if elapsed > 0 else attempts,
                }

    elapsed = time.time() - start_time
    return {
        "cracked": False,
        "password": None,
        "attempts": attempts,
        "time": round(elapsed, 3),
        "speed": round(attempts / elapsed) if elapsed > 0 else attempts,
    }


def dictionary_attack_sim(target_password, wordlist=None):
    """
    Simulate a dictionary attack using common passwords.

    Args:
        target_password: The password to try to crack
        wordlist: List of words to try (uses built-in list if None)

    Returns:
        dict with results
    """
    target_hash = hash_password(target_password)
    attempts = 0
    start_time = time.time()

    if wordlist is None:
        import os
        filepath = os.path.join(os.path.dirname(__file__), "common_passwords.txt")
        try:
            with open(filepath, "r") as f:
                wordlist = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            wordlist = ["password", "123456", "admin", "letmein", "welcome"]

    # Try each word and common variations
    for word in wordlist:
        variations = generate_variations(word)
        for variant in variations:
            attempts += 1
            if hash_password(variant) == target_hash:
                elapsed = time.time() - start_time
                return {
                    "cracked": True,
                    "password": variant,
                    "attempts": attempts,
                    "time": round(elapsed, 3),
                    "method": "Dictionary + variations",
                }

    elapsed = time.time() - start_time
    return {
        "cracked": False,
        "password": None,
        "attempts": attempts,
        "time": round(elapsed, 3),
        "method": "Dictionary + variations",
    }


def generate_variations(word):
    """Generate common password variations of a word."""
    variations = [word]
    # Capitalization
    variations.append(word.capitalize())
    variations.append(word.upper())
    # Common suffixes
    for suffix in ["1", "123", "!", "12", "1!", "01", "2024", "2025"]:
        variations.append(word + suffix)
        variations.append(word.capitalize() + suffix)
    # Leet speak
    leet = word.replace("a", "@").replace("e", "3").replace("o", "0").replace("s", "$").replace("i", "1")
    if leet != word:
        variations.append(leet)
    return variations
