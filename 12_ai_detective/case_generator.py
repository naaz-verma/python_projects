import json
import re


# Case templates for different settings
CASE_TYPES = {
    "Mansion Mystery": "a wealthy family's countryside mansion during a dinner party",
    "Office Crime": "a corporate office building after hours",
    "Campus Case": "a university campus during exam week",
    "Hotel Heist": "a luxury hotel during a gala event",
}


def generate_case(model, case_type="Mansion Mystery"):
    """Generate a complete murder mystery case using AI.

    Args:
        model: Gemini model instance
        case_type: one of the CASE_TYPES keys

    Returns:
        dict with full case details
    """
    setting = CASE_TYPES.get(case_type, CASE_TYPES["Mansion Mystery"])

    prompt = f"""You are a murder mystery game designer. Create a complete mystery case.

Setting: {setting}

Create a murder mystery with EXACTLY this JSON structure (no markdown, no extra text):
{{
    "title": "A catchy case title",
    "setting": "2-3 sentence description of the crime scene and setting",
    "victim": {{
        "name": "Victim's full name",
        "role": "Their role/job/relationship (e.g., 'CEO of TechCorp')",
        "details": "1-2 sentences about who they were"
    }},
    "crime": {{
        "weapon": "The murder weapon",
        "location": "Specific location where the body was found",
        "time": "Estimated time of death (e.g., 'Between 9 PM and 10 PM')",
        "discovery": "1-2 sentences about how the body was discovered"
    }},
    "suspects": [
        {{
            "name": "Suspect 1 full name",
            "relationship": "Their connection to the victim",
            "personality": "2-3 personality traits",
            "alibi": "What they claim they were doing at the time",
            "motive": "Why they might want the victim dead",
            "is_guilty": false
        }},
        {{
            "name": "Suspect 2 full name",
            "relationship": "Their connection to the victim",
            "personality": "2-3 personality traits",
            "alibi": "What they claim they were doing at the time",
            "motive": "Why they might want the victim dead",
            "is_guilty": false
        }},
        {{
            "name": "Suspect 3 full name",
            "relationship": "Their connection to the victim",
            "personality": "2-3 personality traits",
            "alibi": "What they claim they were doing at the time (this one has a HOLE in their alibi)",
            "motive": "Why they might want the victim dead",
            "is_guilty": true
        }},
        {{
            "name": "Suspect 4 full name",
            "relationship": "Their connection to the victim",
            "personality": "2-3 personality traits",
            "alibi": "What they claim they were doing at the time",
            "motive": "Why they might want the victim dead",
            "is_guilty": false
        }}
    ],
    "clues": [
        "Clue 1: A physical clue found at the crime scene that points toward the guilty suspect",
        "Clue 2: A testimony inconsistency in the guilty suspect's alibi",
        "Clue 3: A piece of evidence that connects the guilty suspect to the weapon or scene"
    ],
    "solution": "2-3 sentences explaining how and why the guilty suspect committed the crime"
}}

IMPORTANT:
- Exactly ONE suspect must have is_guilty: true
- The guilty suspect's alibi should have a subtle inconsistency
- The 3 clues should all point to the guilty suspect but not be too obvious
- Make it solvable but challenging"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)
        text = text.strip()
        case = json.loads(text)

        # Validate structure
        required = ["title", "setting", "victim", "crime", "suspects", "clues", "solution"]
        for field in required:
            if field not in case:
                return get_fallback_case()

        if len(case["suspects"]) != 4:
            return get_fallback_case()

        return case

    except (json.JSONDecodeError, KeyError, IndexError):
        return get_fallback_case()


def get_suspect_prompt(suspect, case):
    """Create a system prompt for AI to role-play as a suspect.

    Args:
        suspect: suspect dict from the case
        case: full case dict

    Returns:
        string prompt for the chat system message
    """
    guilty_note = ""
    if suspect.get("is_guilty"):
        guilty_note = """You ARE the guilty one but you must NOT confess directly.
When questioned closely about your alibi, show subtle nervousness.
Your alibi has a small inconsistency -- if pressed on specific details, get slightly defensive.
Never outright lie when caught in a contradiction, instead get flustered or change the subject."""
    else:
        guilty_note = """You are INNOCENT. Answer honestly and consistently.
You genuinely don't know who did it. You may have suspicions about other suspects.
Your alibi is solid and you can provide details if asked."""

    return f"""You are role-playing as {suspect['name']} in a murder mystery investigation.

Your character:
- Name: {suspect['name']}
- Relationship to victim ({case['victim']['name']}): {suspect['relationship']}
- Personality: {suspect['personality']}
- Your alibi: {suspect['alibi']}
- Your motive: {suspect['motive']}

{guilty_note}

Rules:
- Stay in character at all times
- Give responses of 2-4 sentences
- React emotionally when appropriate (nervous, angry, sad, defensive)
- You know about the other suspects but don't accuse anyone directly
- If asked about the crime: you were shocked and saddened (or pretend to be)
- Answer questions naturally, as a real person would during an interrogation"""


def get_guilty_suspect(case):
    """Find and return the guilty suspect from the case.

    Args:
        case: full case dict

    Returns:
        suspect dict of the guilty person
    """
    for suspect in case["suspects"]:
        if suspect.get("is_guilty"):
            return suspect
    # Fallback: return the third suspect (who should be guilty per our prompt)
    return case["suspects"][2]


def check_accusation(case, accused_name):
    """Check if the player accused the right suspect.

    Args:
        case: full case dict
        accused_name: name of the suspect the player is accusing

    Returns:
        dict with 'correct', 'guilty_name', 'solution'
    """
    guilty = get_guilty_suspect(case)
    accused_lower = accused_name.strip().lower()
    guilty_lower = guilty["name"].strip().lower()

    correct = accused_lower == guilty_lower or accused_lower in guilty_lower or guilty_lower in accused_lower

    return {
        "correct": correct,
        "guilty_name": guilty["name"],
        "solution": case["solution"],
    }


def get_fallback_case():
    """Return a pre-built case if AI generation fails."""
    return {
        "title": "The Library Incident",
        "setting": "A quiet evening at the Thornwood Mansion. The wealthy bibliophile Lord Thornwood has been found dead in his private library.",
        "victim": {
            "name": "Lord Edmund Thornwood",
            "role": "Wealthy book collector and mansion owner",
            "details": "A 65-year-old retired businessman known for his rare book collection worth millions.",
        },
        "crime": {
            "weapon": "A heavy bronze bookend shaped like an eagle",
            "location": "The private library, near the rare books section",
            "time": "Between 8 PM and 9 PM",
            "discovery": "The butler discovered the body at 9:15 PM when bringing evening tea.",
        },
        "suspects": [
            {
                "name": "Victoria Thornwood",
                "relationship": "Lord Thornwood's daughter",
                "personality": "Elegant, composed, and ambitious",
                "alibi": "Claims she was in the garden taking a phone call from 7:30 to 9 PM",
                "motive": "Stands to inherit the entire estate worth 10 million",
                "is_guilty": False,
            },
            {
                "name": "Professor Harold Quinn",
                "relationship": "Lord Thornwood's long-time friend and fellow collector",
                "personality": "Intellectual, nervous, and fidgety",
                "alibi": "Says he was in the guest room reading from 7 PM onwards",
                "motive": "Lord Thornwood recently outbid him for a rare first edition",
                "is_guilty": False,
            },
            {
                "name": "Sebastian Marsh",
                "relationship": "Lord Thornwood's personal secretary",
                "personality": "Quiet, organized, and resentful",
                "alibi": "Claims he was in his office filing paperwork, but cannot name which documents",
                "motive": "Was about to be fired after 15 years of service and replaced by a younger assistant",
                "is_guilty": True,
            },
            {
                "name": "Diana Cross",
                "relationship": "Lord Thornwood's business partner",
                "personality": "Sharp, direct, and calculating",
                "alibi": "Was on a video call with overseas clients from 7:45 to 8:45 PM (verified)",
                "motive": "A disputed business deal worth 2 million",
                "is_guilty": False,
            },
        ],
        "clues": [
            "A fragment of a monogrammed cufflink with the initials 'S.M.' was found near the body",
            "Sebastian claims he was filing paperwork all evening, but the office printer log shows no activity after 6 PM",
            "Security camera footage shows Sebastian entering the library corridor at 8:22 PM, contradicting his statement of being in his office",
        ],
        "solution": "Sebastian Marsh killed Lord Thornwood out of resentment for being fired. He entered the library at 8:22 PM, confronted Lord Thornwood about his termination, and struck him with the bronze bookend in a fit of rage. His cufflink broke off during the struggle.",
    }
