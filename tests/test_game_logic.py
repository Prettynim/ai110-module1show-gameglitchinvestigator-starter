from logic_utils import check_guess, parse_guess

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

# ============================================================================
# CHALLENGE 1: Advanced Edge-Case Testing
# ============================================================================
# These tests verify robustness of parse_guess and check_guess with unusual inputs

def test_parse_guess_with_decimal():
    # Edge case: User enters decimal input (e.g., "3.7")
    # Expected: Should truncate to integer without error
    ok, guess_int, err = parse_guess("3.7")
    assert ok is True
    assert guess_int == 3
    assert err is None

def test_parse_guess_with_large_decimal():
    # Edge case: User enters decimal with many decimal places
    # Expected: Should handle gracefully and convert to integer
    ok, guess_int, err = parse_guess("99.99999")
    assert ok is True
    assert guess_int == 99
    assert err is None

def test_parse_guess_with_negative_number():
    # Edge case: Game range is 1-100, but user enters negative number
    # Expected: Should accept the input (validation is game logic, not parse_guess)
    ok, guess_int, err = parse_guess("-5")
    assert ok is True
    assert guess_int == -5
    assert err is None

def test_parse_guess_with_large_number():
    # Edge case: User enters a very large number beyond game range
    # Expected: Should parse successfully (range checking is game's responsibility)
    ok, guess_int, err = parse_guess("999999")
    assert ok is True
    assert guess_int == 999999
    assert err is None

def test_parse_guess_with_zero():
    # Edge case: Input is "0" (boundary of typical game range)
    # Expected: Should parse successfully
    ok, guess_int, err = parse_guess("0")
    assert ok is True
    assert guess_int == 0
    assert err is None

def test_parse_guess_with_leading_zeros():
    # Edge case: Input like "007" (common accidental format)
    # Expected: Should convert to integer 7 correctly
    ok, guess_int, err = parse_guess("007")
    assert ok is True
    assert guess_int == 7
    assert err is None

def test_parse_guess_with_whitespace_string():
    # Edge case: User enters spaces (e.g., " 50 ")
    # Expected: Python's int() strips whitespace, so should work
    ok, guess_int, err = parse_guess("  50  ")
    assert ok is True
    assert guess_int == 50
    assert err is None

def test_parse_guess_with_non_numeric():
    # Edge case: User enters letters or symbols
    # Expected: Should fail with error message
    ok, guess_int, err = parse_guess("abc")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."

def test_parse_guess_with_special_characters():
    # Edge case: User enters special characters
    # Expected: Should fail gracefully
    ok, guess_int, err = parse_guess("$50")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."

def test_check_guess_boundary_zero():
    # Edge case: Compare guess of 0 against secret
    # Expected: Numeric comparison should work correctly
    result, message = check_guess(0, 50)
    assert result == "Too Low"

def test_check_guess_boundary_same():
    # Edge case: Both guess and secret are boundary values
    # Expected: Should be exact match
    result, message = check_guess(1, 1)
    assert result == "Win"

def test_check_guess_off_by_one_low():
    # Edge case: Guess is one less than secret
    # Expected: Should be "Too Low"
    result, message = check_guess(49, 50)
    assert result == "Too Low"

def test_check_guess_off_by_one_high():
    # Edge case: Guess is one more than secret
    # Expected: Should be "Too High"
    result, message = check_guess(51, 50)
    assert result == "Too High"

def test_check_guess_with_negative_numbers():
    # Edge case: Both guess and secret are negative
    # Expected: Numeric comparison should still work
    result, message = check_guess(-10, -5)
    assert result == "Too Low"

def test_check_guess_negative_vs_positive():
    # Edge case: Guess is negative, secret is positive
    # Expected: Negative should be "Too Low"
    result, message = check_guess(-5, 50)
    assert result == "Too Low"

def test_check_guess_with_very_large_numbers():
    # Edge case: Both values are very large
    # Expected: Numeric comparison should still work correctly
    result, message = check_guess(1000000, 999999)
    assert result == "Too High"

def test_check_guess_string_with_leading_zeros():
    # Edge case: String representation with leading zeros
    # Expected: Should convert and compare numerically (007 < 50)
    result, message = check_guess("007", "50")
    assert result == "Too Low"
