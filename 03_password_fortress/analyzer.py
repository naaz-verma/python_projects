import re
import math
import string


def analyze_password(password):
    """Analyze a password and return detailed strength metrics."""
    length = len(password)
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    # Character pool size
    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 32

    # Entropy calculation: log2(pool_size ^ length)
    entropy = length * math.log2(pool_size) if pool_size > 0 else 0

    # Detect common patterns
    patterns = detect_patterns(password)

    # Calculate score (0-100)
    score = calculate_score(length, has_upper, has_lower, has_digit, has_special, entropy, patterns)

    # Estimate crack times
    crack_times = estimate_crack_time(pool_size, length)

    # Strength label
    if score >= 80:
        strength = "Very Strong"
        color = "green"
    elif score >= 60:
        strength = "Strong"
        color = "blue"
    elif score >= 40:
        strength = "Medium"
        color = "orange"
    elif score >= 20:
        strength = "Weak"
        color = "red"
    else:
        strength = "Very Weak"
        color = "red"

    return {
        "password": password,
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "pool_size": pool_size,
        "entropy": round(entropy, 2),
        "patterns": patterns,
        "score": score,
        "strength": strength,
        "color": color,
        "crack_times": crack_times,
    }


def detect_patterns(password):
    """Detect weak patterns in a password."""
    patterns = []

    # Repeated characters
    if re.search(r"(.)\1{2,}", password):
        patterns.append("Repeated characters (e.g. aaa)")

    # Sequential numbers
    for seq in ["012", "123", "234", "345", "456", "567", "678", "789"]:
        if seq in password:
            patterns.append("Sequential numbers (e.g. 123)")
            break

    # Sequential letters
    for seq in ["abc", "bcd", "cde", "def", "efg", "xyz"]:
        if seq in password.lower():
            patterns.append("Sequential letters (e.g. abc)")
            break

    # Keyboard patterns
    keyboard_patterns = ["qwerty", "asdf", "zxcv", "qazwsx", "1qaz", "2wsx"]
    for kp in keyboard_patterns:
        if kp in password.lower():
            patterns.append(f"Keyboard pattern ({kp})")
            break

    # Common substitutions
    leet_map = {"@": "a", "0": "o", "1": "l", "3": "e", "$": "s", "!": "i"}
    deleet = password.lower()
    for k, v in leet_map.items():
        deleet = deleet.replace(k, v)
    if deleet != password.lower():
        patterns.append("Leet speak substitutions (@=a, 0=o, etc.)")

    # All same case
    if password.isalpha() and (password.isupper() or password.islower()):
        patterns.append("Single case only")

    # Only digits
    if password.isdigit():
        patterns.append("Numbers only -- very weak!")

    # Common words
    common_words = ["password", "admin", "login", "welcome", "monkey",
                    "dragon", "master", "letmein", "football", "shadow"]
    for word in common_words:
        if word in password.lower():
            patterns.append(f"Contains common word: '{word}'")
            break

    return patterns


def calculate_score(length, has_upper, has_lower, has_digit, has_special, entropy, patterns):
    """Calculate a 0-100 score for password strength."""
    score = 0

    # Length scoring (max 30)
    score += min(length * 3, 30)

    # Character variety (max 25)
    variety = sum([has_upper, has_lower, has_digit, has_special])
    score += variety * 6.25

    # Entropy scoring (max 30)
    score += min(entropy / 2, 30)

    # Pattern penalties
    score -= len(patterns) * 10

    return max(0, min(100, round(score)))


def estimate_crack_time(pool_size, length):
    """Estimate time to brute-force the password at various speeds."""
    if pool_size == 0:
        return {}

    combinations = pool_size ** length

    # Guesses per second for different scenarios
    speeds = {
        "Online attack (1K/sec)": 1_000,
        "Fast hash - MD5 (10B/sec)": 10_000_000_000,
        "Slow hash - bcrypt (10K/sec)": 10_000,
        "Supercomputer (1T/sec)": 1_000_000_000_000,
    }

    results = {}
    for label, rate in speeds.items():
        seconds = combinations / rate
        results[label] = format_time(seconds)

    return results


def format_time(seconds):
    """Convert seconds to a human-readable time string."""
    if seconds < 0.001:
        return "Instant"
    if seconds < 1:
        return f"{seconds * 1000:.0f} milliseconds"
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    if seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    if seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    if seconds < 86400 * 365:
        return f"{seconds / 86400:.1f} days"
    if seconds < 86400 * 365 * 1000:
        return f"{seconds / (86400 * 365):.1f} years"
    if seconds < 86400 * 365 * 1e6:
        return f"{seconds / (86400 * 365 * 1000):.0f} thousand years"
    if seconds < 86400 * 365 * 1e9:
        return f"{seconds / (86400 * 365 * 1e6):.0f} million years"
    return f"{seconds / (86400 * 365 * 1e9):.0f} billion years"


def is_common_password(password, filepath="common_passwords.txt"):
    """Check if password is in the common passwords list."""
    import os
    filepath = os.path.join(os.path.dirname(__file__), filepath)
    try:
        with open(filepath, "r") as f:
            common = {line.strip().lower() for line in f}
        return password.lower() in common
    except FileNotFoundError:
        return False
