def recommend_movie(mood,df):
    mood_to_genre = {
    "Happy": ["Comedy", "Animation", "Romance", "Musical", "Family"],
    "Sad": ["Drama", "Documentary", "Biography"],
    "Excited": ["Action", "Adventure", "Science Fiction", "Sport", "War"],
    "Scared": ["Horror", "Thriller", "Mystery"],
    "Relaxed": ["Slice of Life", "Musical", "Fantasy"],
}

    # Map mood to genres
    genres = mood_to_genre.get(mood, [])
    
    # Filter movies
    filtered_movies = df[df['Genre'].apply(lambda x: any(g in x for g in genres))]
    
    # Sort by ratings (descending)
    filtered_movies = filtered_movies.sort_values(by="Rating", ascending=False)
    
    return filtered_movies[['Title', 'Rating']].head(10)
