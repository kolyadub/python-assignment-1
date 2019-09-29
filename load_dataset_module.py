from os import sys

def load_dataset(): 
    # This function creates a new dictionary from files u.item and u.data
    movies = {} 
    userPreference = {}
    try:
        fileMovies = open("movies/u.item")
        fileUsers = open("movies/u.data")
    except FileNotFoundError:
        print("Files are not found! Please, correct the file names or change their location.")
        sys.exit(0)
    
    for line in fileMovies:
        # Spliting by the '|' symbol
        (movieId, movieName) = line.split("|")[0:2]   
        # Creating a dictionary value from the first (movie id) and the second (movie name) element of the movieLine list
        movies[movieId] = movieName    
    
    for line in fileUsers:
        (userId, movieId, rating) = line.split("\t")[0:3]
        # If the user doesn't exist, create a new user with the value {}
        userPreference.setdefault(userId, {}) 
        # Replacing a movie id with the corresponding movie name
        movieName = movies[movieId]  
        # Adding a new 'movie - rating' value to the user 
        userPreference[userId][movieName] = rating 
    
    fileMovies.close()
    fileUsers.close()
        
    return userPreference
