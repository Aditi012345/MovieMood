import pandas as pd
import streamlit as st
import mymodule as mm

# Initialize session state variables if they don't exist
if 'next_clicked' not in st.session_state:
    st.session_state.next_clicked = False
if 'mood' not in st.session_state:
    st.session_state.mood = None

st.header("Welcome to MovieMood")
st.markdown('<h3>Created by: Aditi Deshpande</h3>', unsafe_allow_html=True)
st.markdown("""
Easily discover your next favorite movie with our intuitive movie finder app! Just tell us your preferences, and our tool will analyze your tastes, recommend personalized picks, and help you explore new genres and hidden gems. No endless scrolling or guesswork—just clear, tailored suggestions and beautifully curated lists to make finding the perfect movie effortless. Whether you're in the mood for a classic, a thriller, or something completely new, our app makes movie night simple and fun!
""", unsafe_allow_html=True)
st.markdown('<h4>Just answer a few questions & voila, you just got something to watch!!</h4>', unsafe_allow_html=True)


dict_mood = {
    "Happy": "Craving some good vibes",
    "Sad": "Need a good cry",
    "Excited": "On a quest for adventure",
    "Relaxed": "Ready to vibe with a cozy flick",
    "Scared": "Crave a thrill"
}

# If the "Next" button hasn't been clicked yet, show mood selection
if not st.session_state.next_clicked:
    st.write("What's your mood today?")
    mood = st.radio("Select your mood:", list(dict_mood.values()))
    if st.button('Next'):
        # Save the selected mood in session state and mark that next was clicked
        st.session_state.next_clicked = True
        st.session_state.mood = mood
# Once the mood is selected, proceed with movie recommendations
else:
    mood = st.session_state.mood
    # Map the selected mood's description back to its key
    mood_name = next((key for key, value in dict_mood.items() if value == mood), None)
    if mood_name:
        # Read the dataset of movies
        df = pd.read_csv("Final.csv")
        # Get recommended movies based on the mood using the external module function
        recommended_movies = mm.recommend_movie(mood_name, df)
        rec_mov = recommended_movies.head()
        if not recommended_movies.empty:
            st.write("Here are some top-rated movies for your mood:")
            st.table(rec_mov)
            # Allow the user to indicate which movies they have watched
            watched_movie = st.multiselect("Have you watched any of these movies? (Select all that apply)", ["No"] + rec_mov["Title"].tolist())
            if st.button('Recommend me a movie'):
                # If the user selects "No" or leaves the selection empty, recommend the first movie
                if "No" in watched_movie or not watched_movie:
                    st.write(f"You should definitely check out **{rec_mov.iloc[0]['Title']}**!")
                else:
                    # Filter out the movies that the user has already watched
                    remaining_movies = rec_mov[~rec_mov["Title"].isin(watched_movie)]
                    if not remaining_movies.empty:
                        st.write(f"You should definitely check out **{remaining_movies.iloc[0]['Title']}**!")
                    else:
                        st.write("Looks like you've watched all the movies on this list! Great job!")
                        # If more recommendations are available in the full list, suggest another movie
                        if len(recommended_movies) > 5:
                            st.write(f"Then you should definitely check out **{recommended_movies.iloc[5]['Title']}**!")
                        else:
                            st.write("However, there are no more recommendations available at the moment.")
    else:
        st.write("Invalid mood selected. Please try again!")
