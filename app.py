import streamlit as st
import re
from collections import defaultdict

MAX_LENGTH = 15
# Set up the page
st.set_page_config(page_title="WordPlay - Word Guessing Game", layout="wide")
st.title("WordPlay - Word Guessing Game")
st.write("Find possible words from a set of letters with optional constraints.")
st.info(
    """### How to use this app:
1. Enter a list of letters that you want to use to form words.
2. Select the length of the word you want to find.
3. Optionally, add constraints by selecting which letter should be at a specific position.
4. Click 'Find Words' to see all possible words that can be formed with your letters and constraints.
        
NOTE: The app currently limits the word length to **15** letters."""
)
st.markdown("---")


# Load words from the file
@st.cache_data
def load_words():
    with open("words.txt", "r") as file:
        # Read all words and filter out very short words and words with special characters
        words = [
            word.strip().lower()
            for word in file
            if word.strip() and len(word.strip()) >= 2
        ]
        # Remove words with special characters, keeping only alphabetic words
        words = [word for word in words if re.match(r"^[a-z]+$", word)]
    return words


# Group words by length for faster filtering
@st.cache_data
def group_words_by_length(words):
    word_groups = defaultdict(list)
    for word in words:
        word_groups[len(word)].append(word)
    return word_groups


# Check if a word can be formed from the given letters
def can_form_word(word, letters):
    letter_count = {}
    for letter in letters:
        letter_count[letter] = letter_count.get(letter, 0) + 1

    for letter in word:
        if letter not in letter_count or letter_count[letter] == 0:
            return False
        letter_count[letter] -= 1

    return True


# Find all possible words that can be formed with the given letters and constraints
def find_possible_words(letters, word_length, constraints):
    all_words = group_words_by_length(load_words()).get(word_length, [])
    possible_words = []

    for word in all_words:
        # Check if the word matches all constraints
        matches_constraints = True
        for position, letter in constraints.items():
            if position < len(word) and word[position] != letter:
                matches_constraints = False
                break

        # If word matches constraints and can be formed from the letters
        if matches_constraints and can_form_word(word, letters):
            possible_words.append(word)

    # Return unique words only
    return list(dict.fromkeys(possible_words))


# Main app layout
st.subheader("Step 1: Enter Letters")
letter_input = st.text_input(
    "Enter a list of letters (without spaces):", max_chars=MAX_LENGTH
)
letters = [letter.lower() for letter in letter_input if letter.isalpha()]

if letters:
    st.write(f"You entered {len(letters)} letters: {', '.join(letters)}")

    st.subheader("Step 2: Select Word Length")
    # max_length = min(MAX_LENGTH, len(letters))  # Limit max length to 15 or the number of letters
    word_length_options = list(range(3, len(letters) + 1))

    # Initialize session state variables if they don't exist
    if "previous_word_length" not in st.session_state:
        st.session_state.previous_word_length = 6  # Default value
    if "constraints" not in st.session_state:
        st.session_state.constraints = {}

    # Use a callback to handle word length changes
    def on_word_length_change():
        if st.session_state.word_length != st.session_state.previous_word_length:
            st.session_state.constraints = {}  # Clear all constraints
            st.session_state.previous_word_length = st.session_state.word_length

    word_length = st.selectbox(
        "Select word length:",
        word_length_options,
        index=min(3, len(word_length_options) - 1),
        key="word_length",
        on_change=on_word_length_change,
    )

    st.subheader("Step 3: Add Constraints (Optional)")
    st.write("Select letters for specific positions in the word:")

    # Create a grid of dropdowns for position constraints
    constraints = {}
    cols = st.columns(word_length)  # Limit to 8 columns per row for better display

    for i in range(word_length):
        with cols[i]:
            # Use a unique key that includes the word length to force recreation when length changes
            key = f"pos_{word_length}_{i}"
            # Get default value from session state if it exists
            default_index = 0
            if i in st.session_state.constraints:
                try:
                    default_index = letters.index(st.session_state.constraints[i]) + 1
                except ValueError:
                    default_index = 0

            letter = st.selectbox(
                f"Letter #{i+1}", [""] + letters, index=default_index, key=key
            )
            if letter:
                constraints[i] = letter.lower()
                st.session_state.constraints[i] = letter.lower()
            elif i in st.session_state.constraints:
                del st.session_state.constraints[i]

    # Button to find words
    st.subheader("Step 4: Find Possible Words")
    if st.button("Find Words"):
        with st.spinner("Searching for words..."):
            possible_words = find_possible_words(letters, word_length, constraints)

            if possible_words:
                st.success(f"Found {len(possible_words)} possible words!")
                st.write("Possible words:")

                # Display words in a nice format
                word_columns = st.columns(3)
                sorted_words = sorted(possible_words)
                
                # Calculate number of rows needed
                num_words = len(sorted_words)
                rows = (num_words + 2) // 3  # Round up division
                
                # Fill columns vertically
                for col in range(3):
                    for row in range(rows):
                        idx = row + (col * rows)
                        if idx < num_words:
                            word_columns[col].write(f"• {sorted_words[idx]}")
            else:
                st.warning("No words found that match your criteria.")
else:
    st.warning("Please enter at least one letter to start.")
