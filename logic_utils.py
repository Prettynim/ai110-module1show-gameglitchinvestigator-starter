def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """
    Determines the number range based on the selected difficulty level.

    Args:
        difficulty (str): The difficulty level ("Easy", "Normal", "Hard").

    Returns:
        tuple[int, int]: A tuple containing the (min, max) range for the secret number.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Hard difficulty should be harder than Normal.
        # Increased range to 1-200 (was 1-50).
        return 1, 200
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """
    Parses the raw user input into an integer guess.
    
    Handles input validation including checking for empty strings,
    non-numeric characters, and floating point numbers (which are truncated).

    Args:
        raw (str): The raw input string from the user.

    Returns:
        tuple[bool, int | None, str | None]: A tuple containing (success_status, parsed_value, error_message).
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


def check_guess(guess: int | str, secret: int | str) -> tuple[str, str]:
    """
    Compares the user's guess against the secret number.
    
    Ensures safe numeric comparison by converting inputs to integers,
    preventing lexicographic comparison bugs (e.g. "9" > "50").

    Args:
        guess (int | str): The user's guess.
        secret (int | str): The secret number to match.

    Returns:
        tuple[str, str]: A tuple containing the outcome ("Win", "Too High", "Too Low") and a feedback message.
    """
    # FIX: Always treat both as integers for proper numeric comparison
    # (Previously had try-except that fell back to string comparison on TypeError)
    guess_int = int(guess)
    secret_int = int(secret)
    
    if guess_int == secret_int:
        return "Win", "🎉 Correct!"
    
    if guess_int > secret_int:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Calculates the new score based on the guess outcome and attempt efficiency.

    Args:
        current_score (int): The player's current score.
        outcome (str): The result of the guess ("Win", "Too High", "Too Low").
        attempt_number (int): The current attempt count.

    Returns:
        int: The updated score.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIXME: Scoring logic is inconsistent (rewards wrong guesses on even attempts)
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
