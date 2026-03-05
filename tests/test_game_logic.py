from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, message = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, message = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, message = check_guess(40, 50)
    assert result == "Too Low"

# NEW TESTS: Collaborative debugging with Copilot to verify the string conversion bug fix
# These tests specifically target the lexicographic comparison issue that occurred 
# when the secret was converted to a string on even attempts (e.g., "9" > "50" was True)

def test_secret_as_string():
    # BUG FIX VERIFICATION: The original code passed secret as string on even attempts
    # Now check_guess should handle string secrets correctly using numeric comparison
    # Secret as string "50", guess 60 should return "Too High"
    result, message = check_guess(60, "50")
    assert result == "Too High"

def test_secret_and_guess_both_strings():
    # BUG FIX VERIFICATION: Both secret and guess could be strings - should still use numeric comparison
    result, message = check_guess("40", "50")
    assert result == "Too Low"

def test_lexicographic_bug_prevented():
    # CRITICAL BUG FIX: The original bug caused "9" > "50" to be True (lexicographic string comparison)
    # This test ensures numeric comparison is used: 9 < 50 should be "Too Low"
    # If this test fails, the string conversion bug has returned
    result, message = check_guess("9", "50")
    assert result == "Too Low", "String '9' should be compared numerically, not lexicographically"

def test_win_with_string_secret():
    # BUG FIX VERIFICATION: Winning condition works when secret is passed as string
    result, message = check_guess("50", "50")
    assert result == "Win"