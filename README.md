# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game Purpose & Overview
This is an AI-generated guessing game built with Streamlit where players have limited attempts to guess a secret number within a given range. The game provides "Higher/Lower" hints and tracks score based on efficiency. The starter code intentionally contained multiple bugs to teach debugging and AI collaboration.

### Bugs Found & Fixed

**Bug 1: Hard Difficulty Easier Than Normal**
- **Issue:** Hard mode had range 1-50 while Normal was 1-100, making Hard actually easier
- **Fix:** Updated `get_range_for_difficulty()` in `logic_utils.py` to use range 1-200 for Hard mode.

**Bug 2: String Conversion Breaks Numeric Comparison (CRITICAL)**
- **Issue:** On even-numbered attempts, the code converted `secret` from integer to string, causing `check_guess()` to use lexicographic (alphabetical) string comparison instead of numeric comparison. Example: guess "9" vs secret "50" would return "Too High" (wrong!) because "9" > "50" in string order.
- **Fix:** Refactored `check_guess()` into `logic_utils.py` and removed the conditional type conversion. Now always converts both guess and secret to integers before comparison. The fix ensures "9" < "50" is evaluated numerically (correct!).

**Bug 3: Misleading Comparison Logic**
- **Issue:** Original code had a TypeError exception handler that fell back to string comparison, compounding the string conversion bug
- **Fix:** Removed the exception handler entirely. Both values are now converted to integers upfront, guaranteeing numeric comparison.

**Bug 4: Inconsistent Score Logic (Stretch)**
- **Issue:** Score calculation rewarded +5 points for "Too High" guesses on even attempts but penalized them on odd attempts
- **Fix:** Identified but left as-is (marked as FIXME) since the main bugs were addressed

### Fixes Applied

1. **Refactored Game Logic** - Moved `check_guess()`, `parse_guess()`, `update_score()`, and `get_range_for_difficulty()` from `app.py` into `logic_utils.py`
2. **Fixed String Comparison** - Removed conditional secret conversion; now always uses integer comparison in `check_guess()`
3. **Improved Testability** - Logic separation makes unit testing easier and more focused
4. **Added Comprehensive Tests** - Created 4 new targeted pytest tests verifying the string conversion bug fix:
   - `test_secret_as_string()` - Secret can be passed as string
   - `test_secret_and_guess_both_strings()` - Both as strings with numeric comparison
   - `test_lexicographic_bug_prevented()` - CRITICAL: Ensures "9" < "50" numerically
   - `test_win_with_string_secret()` - Winning works with string secret
5. **Documentation** - Added FIX comments in code and comprehensive reflection.md

**Test Results:** All 7 tests pass ✅

## 📸 Demo

### Game Now Works! ✅

The game has been fixed and is now fully playable:

**How to Play:**
```bash
python -m streamlit run app.py
```

Visit `http://localhost:8501` to play.

**Game Features (Now Fixed):**
- ✅ Consistent hints: "Too High" and "Too Low" are now accurate on all attempts
- ✅ Stable secret number that persists throughout the game session (uses Streamlit session state)
- ✅ Fair difficulty levels with appropriate ranges
- ✅ Score calculation based on efficiency (fewer guesses = higher score)

**Test Results:**
```
============================= test session starts =============================
collected 7 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 14%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 28%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 42%]
tests/test_game_logic.py::test_secret_as_string PASSED                   [ 57%]
tests/test_game_logic.py::test_secret_and_guess_both_strings PASSED      [ 71%]
tests/test_game_logic.py::test_lexicographic_bug_prevented PASSED        [ 85%]
tests/test_game_logic.py::test_win_with_string_secret PASSED             [100%]

============================== 7 passed in 0.03s ==============================
```

**Key Fix Demonstrated:**
The critical test `test_lexicographic_bug_prevented()` verifies that the guess "9" against secret "50" returns "Too Low" using numeric comparison, not "Too High" (which would be wrong in lexicographic string comparison where "9" > "50").

## 🤖 AI Collaboration Process

### How Copilot Helped

**Correct Suggestions:**
- ✅ **Logic Refactoring:** Copilot Agent Mode successfully moved all game logic functions from `app.py` into `logic_utils.py` with proper imports
- ✅ **Bug Analysis:** When provided file context, Copilot correctly traced how the string conversion bug caused a TypeError fallback to string comparison
- ✅ **Test Design:** Helped design targeted tests that specifically verify the numeric comparison bug fix

**Misleading Suggestions:**
- ❌ **Scoring Logic:** Initially suggested the parity-based score calculation might be an intentional game mechanic, which normalized buggy code rather than identifying it as a glitch
  - **How I Verified:** Checked the game flow and found no design reason to reward wrong guesses differently on even/odd attempts

### Collaboration Strategy

1. **Mark Crime Scenes:** Used `# FIXME:` comments before refactoring to identify specific bugs
2. **Trace Execution:** Asked Copilot step-by-step execution traces on specific examples (e.g., "What happens on attempt 2 with guess=9 and secret=50?")
3. **Test-Driven Fixes:** Created targeted pytest tests before and after fixing to verify improvements
4. **Defensive Code Review:** Read AI-generated code looking for conditional logic that changes behavior based on state

### Key Learnings

- AI code can have subtle logic bugs baked in—especially conditional logic that changes types or comparison behavior
- Always verify AI suggestions with execution traces before accepting them
- Targeted tests are better than generic happy-path tests for proving bugs are fixed
- Using tools like pytest and git commits together creates a clear audit trail of debugging work

## 🚀 Optional Extensions

### ✅ Challenge 1: Advanced Edge-Case Testing (COMPLETED)

Implemented comprehensive edge-case testing to verify robustness of game logic functions. Created 17 additional pytest test cases targeting potential failure points:

**parse_guess() Edge Cases Tested:**
- Decimal inputs (e.g., "3.7" → 3)
- Large decimals with many places (99.99999)
- Negative numbers (-5)
- Very large numbers beyond game range (999999)
- Zero and boundary values
- Leading zeros ("007" → 7)
- Whitespace handling ("  50  ")
- Non-numeric inputs ("abc")
- Special characters ("$50")

**check_guess() Edge Cases Tested:**
- Boundary comparisons (0, 1, 100)
- Off-by-one scenarios (49 vs 50, 51 vs 50)
- Negative numbers (-10 vs -5)
- Mixed negative/positive (-5 vs 50)
- Very large numbers (1000000 vs 999999)
- String inputs with leading zeros ("007" vs "50")

**Test Results: 24/24 Passing ✅**

```
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.0.2

collected 24 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  4%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [  8%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 12%]
tests/test_game_logic.py::test_secret_as_string PASSED                   [ 16%]
tests/test_game_logic.py::test_secret_and_guess_both_strings PASSED      [ 20%]
tests/test_game_logic.py::test_lexicographic_bug_prevented PASSED        [ 25%]
tests/test_game_logic.py::test_win_with_string_secret PASSED             [ 29%]
tests/test_game_logic.py::test_parse_guess_with_decimal PASSED           [ 33%]
tests/test_game_logic.py::test_parse_guess_with_large_decimal PASSED     [ 37%]
tests/test_game_logic.py::test_parse_guess_with_negative_number PASSED   [ 41%]
tests/test_game_logic.py::test_parse_guess_with_large_number PASSED      [ 45%]
tests/test_game_logic.py::test_parse_guess_with_zero PASSED              [ 50%]
tests/test_game_logic.py::test_parse_guess_with_leading_zeros PASSED     [ 54%]
tests/test_game_logic.py::test_parse_guess_with_whitespace_string PASSED [ 58%]
tests/test_game_logic.py::test_parse_guess_with_non_numeric PASSED       [ 62%]
tests/test_game_logic.py::test_parse_guess_with_special_characters PASSED [ 66%]
tests/test_game_logic.py::test_check_guess_boundary_zero PASSED          [ 70%]
tests/test_game_logic.py::test_check_guess_boundary_same PASSED          [ 75%]
tests/test_game_logic.py::test_check_guess_off_by_one_low PASSED         [ 79%]
tests/test_game_logic.py::test_check_guess_off_by_one_high PASSED        [ 83%]
tests/test_game_logic.py::test_check_guess_with_negative_numbers PASSED  [ 87%]
tests/test_game_logic.py::test_check_guess_negative_vs_positive PASSED   [ 91%]
tests/test_game_logic.py::test_check_guess_with_very_large_numbers PASSED [ 95%]
tests/test_game_logic.py::test_check_guess_string_with_leading_zeros PASSED [100%]

============================== 24 passed in 0.06s ==============================
```

**Why This Matters:**
These 17 edge-case tests verify that:
- Input parsing handles user typos and unusual formats gracefully
- Numeric comparison works correctly even with negative numbers, very large values, and boundary cases
- The game logic doesn't break under unexpected but valid inputs
- The core bug fix (numeric vs string comparison) holds up across diverse scenarios

These tests catch issues that users might encounter in the wild, ensuring robust game logic and player experience.
