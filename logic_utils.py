def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIXME: Hard difficulty should be harder than Normal, not easier
        # Currently returns 1-50, but should return a larger range
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    
    FIX: Refactored from app.py using Copilot Agent mode as part of the 
    logic-to-utils separation to improve testability and separation of concerns.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    
    FIX: Refactored from app.py using Copilot Agent mode to fix the string conversion bug.
    Removed the TypeError exception handler that enabled lexicographic string comparison.
    Now always converts both values to integers for consistent numeric comparison.
    This fixes the bug where guesses on even attempts would produce inverted hints.
    """
    # FIX: Always treat both as integers for proper numeric comparison
    # (Previously had try-except that fell back to string comparison on TypeError)
    guess_int = int(guess)
    secret_int = int(secret)
    
    if guess_int == secret_int:
        return "Win", "🎉 Correct!"
    
    if guess_int > secret_int:
        return "Too High", "📈 Go HIGHER!"
    else:
        return "Too Low", "📉 Go LOWER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
