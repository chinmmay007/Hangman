import streamlit as st
import random

# Initial Setup (only runs once)
if 'word' not in st.session_state:
    st.session_state.words = {
        "Animals": ['lion','tiger','monkey','cat','dog','elephant','donkey','hippopotamus','cow','goat','frog'],
        "Colours": ['black','brown','yellow','orange','red','green','white','pink','blue','purple','golden','silver','grey'],
        "Fruits": ['orange','mango','strawberry','mulberry','raspberry','plum','cherry','jackfruit','watermelon','muskmelon','apple','jamun']
    }

    st.session_state.stages = [
    '''
       +------+
        |     |
              |
              |
              |
              |
    ==========''',
    '''
       +------+
       |      |
       O      |
              |
              |
              |
    ==========''',
    '''
       +------+
       |      |
       O      |
       |      |
              |
              |
    ==========''',
    # '''
    #    +---+
    #    |   |
    #    O   |
    #   /|   |
    #        |
    #        |
    # =========''',
    '''
       +------+
       |      |
       O      |
      /|\\    |
              |
              |
    ==========''',
    '''
       +------+
       |      |
       O      |
      /|\\    |
      /       |
              |
    ==========''',
    '''
       +------+
       |      |
       O      |
      /|\\    |
      / \\    |
              |
    =========='''
    ]

    st.session_state.category = random.choice(list(st.session_state.words.keys()))
    st.session_state.word = random.choice(st.session_state.words[st.session_state.category])
    st.session_state.letters = set(st.session_state.word)
    st.session_state.guessed_letters = set()
    st.session_state.wrong_attempts = 0
    st.session_state.max_attempts = len(st.session_state.stages) - 1
    st.session_state.input_guess = ''

# Game UI
st.success(f"Category: {st.session_state.category}")
st.text(st.session_state.stages[st.session_state.wrong_attempts])

display_word = [letter if letter in st.session_state.guessed_letters else '_' for letter in st.session_state.word]
st.write("Current word: ", ' '.join(display_word))

# Input and Guess Button
with st.form("guess_form", clear_on_submit=True):
    guess = st.text_input("Guess a letter", max_chars=1).lower()
    submit = st.form_submit_button("Submit")

if submit:
    if not guess.isalpha() or len(guess) != 1:
        st.warning("Enter a single letter.")
    elif guess in st.session_state.guessed_letters:
        st.warning("You already guessed that letter.")
    elif guess in st.session_state.letters:
        st.session_state.guessed_letters.add(guess)
        st.session_state.letters.remove(guess)
        st.success("✅ Correct guess!")
    else:
        st.session_state.guessed_letters.add(guess)
        st.session_state.wrong_attempts += 1
        st.error("❌ Wrong guess.")

# Check Game Status
if len(st.session_state.letters) == 0:
    st.balloons()
    st.success(f"🎉 You won! The word was: {st.session_state.word}")
    if st.button("Play Again"):
        st.session_state.clear()

elif st.session_state.wrong_attempts >= st.session_state.max_attempts:
    st.error(f"💀 Game Over! The word was: {st.session_state.word}")
    if st.button("Try Again"):
        st.session_state.clear()
else:
    st.info(f"Attempts left: {st.session_state.max_attempts - st.session_state.wrong_attempts}")
    st.write("Guessed letters: ", ', '.join(sorted(st.session_state.guessed_letters)))
