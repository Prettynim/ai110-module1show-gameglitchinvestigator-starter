# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

**Bug 1: Hard difficulty is easier than Normal**
- Expected: Hard difficulty should have a larger number range than Normal (making it harder to guess).
- Actually happened: Hard was set to range 1-50, while Normal was 1-100. Players could win Hard mode faster because there are fewer numbers to guess from.
- Root cause: Line 8 in `get_range_for_difficulty()` returns `1, 50` for Hard instead of a larger range.

**Bug 2: Secret converts to string on even attempts**
- Expected: The secret number should always remain an integer for consistent comparisons throughout the game.
- Actually happened: Every time the player made an even-numbered attempt (2nd, 4th, 6th, etc.), the secret was converted to a string, breaking the numeric comparison logic in `check_guess()`.
- Root cause: Lines 155-158 have conditional logic that converts the secret to `str(st.session_state.secret)` when `attempt_number % 2 == 0`.

**Bug 3: String comparison produces inverted/incorrect hints**
- Expected: When comparing a guess to the secret, numeric values should be compared numerically (9 < 50).
- Actually happened: Due to the string conversion bug, the comparison became lexicographic instead of numeric (e.g., "9" > "50" is True in string comparison), causing hints like "Too High" and "Too Low" to be backwards or inconsistent.
- Root cause: The TypeError handling in `check_guess()` (lines 36-43) uses string comparison, which doesn't work correctly for numbers.

**Bug 4: Score logic rewards incorrect guesses on even attempts**
- Expected: Players should be consistently penalized for guesses that don't narrow down the search space efficiently.
- Actually happened: The `update_score()` function rewards players with +5 points for "Too High" guesses on even attempts, while penalizing them on odd attempts. This creates an unfair and illogical scoring system.
- Root cause: Lines 54-56 have logic that checks if `attempt_number % 2 == 0` and gives points differently based on parity rather than consistency.

---

## 2. How did you use AI as a teammate?

**AI Tool Used:** GitHub Copilot with workspace file context

**Correct AI Analysis - Understanding the String Conversion Glitch:**
- Copilot correctly identified that lines 158-160 in `app.py` convert the secret to a string on even attempts: `if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)`. 
- When I provided the file context and asked it to trace the logic, Copilot showed how this breaks the `check_guess()` function by forcing a TypeError that falls back to string comparison, which produces inverted hints for numbers like "9" > "50" being True in lexicographic order.
- I verified this by mentally tracing through an attempt: on attempt 2, the secret becomes "50" (string), causing `50 > "50"` to throw a TypeError, then `"9" > "50"` returns True (wrong!).

**Misleading AI Analysis - Initial Scoring Logic:**
- Copilot initially suggested the scoring logic in `update_score()` might be intentionally rewarding "Too High" guesses on even attempts as an unusual game mechanic.
- This was misleading because it normalized buggy code rather than identifying it as a glitch. I verified this was indeed a bug by looking at the game flow—there's no game design reason to give +5 points for wrong guesses, and it makes the scoring fundamentally unfair and inconsistent.

---

## 3. Debugging and testing your fixes

**How I Decided a Bug Was Fixed:**
I used pytest to verify fixes before testing in the live game. For the string conversion bug, I created a specific test called `test_lexicographic_bug_prevented()` that checks if `check_guess("9", "50")` returns "Too Low" using numeric comparison (not lexicographic). This test would have failed with the original buggy code because "9" > "50" is True in string comparison, but passes now with numeric comparison.

**Test Results:**
I ran `python -m pytest tests/test_game_logic.py -v` and created 4 new tests targeting the string conversion bug:
- `test_secret_as_string()` - Verifies secret can be a string
- `test_secret_and_guess_both_strings()` - Tests both as strings with correct numeric comparison
- `test_lexicographic_bug_prevented()` - **Critical**: Ensures "9" < "50" numerically (not lexicographically)
- `test_win_with_string_secret()` - Winning condition works with string secret

All 7 tests passed (3 original + 4 new), confirming the numeric comparison logic is now consistent across all attempts.

**AI's Role in Testing:**
The AI subagent helped refactor the logic functions into `logic_utils.py` and removed the TypeError exception handler that was enabling string comparison fallback. This isolated the issue and made the logic testable. I then wrote the actual test cases based on the bug I understood.

---

## 4. What did you learn about Streamlit and state?

**Why the Secret Number Behavior Changed on Even Attempts:**
The secret didn't "change," but it was **converted to a different type** on even attempts. Streamlit stores the secret as an integer in `st.session_state.secret`, but the buggy code deliberately converted it to a string (`str(st.session_state.secret)`) when `attempt_number % 2 == 0`. This meant that on attempt 2, the comparison logic received a string "50" instead of integer 50, causing the TypeError handler to kick in and use string comparison instead of numeric comparison.

**Streamlit Reruns and Session State Explained:**
Streamlit reruns the entire script from top to bottom every time a user interaction occurs (button click, text input, etc.). Session state is a persistent dictionary (`st.session_state`) that survives these reruns, storing game data like the secret number, attempts, and score. Without session state, the secret would reset to a new random number on every rerun. With it properly used, the secret stays the same throughout the game session because it's only initialized once with `if "secret" not in st.session_state:`.

**The Change That Fixed It:**
I removed the conditional type conversion completely. The refactored `check_guess()` function in `logic_utils.py` now always converts both guess and secret to integers immediately: `guess_int = int(guess)` and `secret_int = int(secret)`. This ensures numeric comparison always happens, regardless of whether the attempt number is odd or even, making the game behavior consistent.

---

## 5. Looking ahead: your developer habits

**Habits I'll Reuse:**
I'll always mark bugs with `# FIXME:` comments before refactoring or fixing them. This gives me a specific "crime scene" to reference and makes it easy to track what's broken. I'll also write targeted pytest tests that specifically target the bug (like `test_lexicographic_bug_prevented()`) rather than just general happy-path tests. This creates executable documentation of what was broken and proof that it's fixed.

**What I'll Do Differently Next Time:**
Instead of accepting AI suggestions at face value, I'll ask the AI to trace through the logic step-by-step on a specific example (like "what happens on attempt 2 with guess=9 and secret=50?"). This made it obvious that the TypeError exception handler was enabling string comparison, which the AI initially missed. I should be more aggressive about asking for execution traces rather than just code review.

**How This Changed My Thinking About AI Code:**
AI-generated code can look plausible and well-structured, but it can still have subtle logic bugs baked in—sometimes intentionally as "glitches" for educational purposes. I now understand that I need to read AI code more defensively, looking for conditional logic that changes behavior based on input state (like the `if attempt % 2 == 0` conversion), and I'll use tests to verify assumptions rather than trusting the code structure alone.
