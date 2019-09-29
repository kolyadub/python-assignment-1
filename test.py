from similarity_module import * 
from load_dataset_module import *
from os import sys

# Variables for main menu and similarities menu, dictionary with user preferences and number of users
simOptions = ["1","2","3","4","5","6"]
menuOptions = ["1","2","3","4","5"]
userPreferences = load_dataset()
numberOfUsers = number_of_users()

def cont(question,fnc):  
    # This function asks about continuation. 
    # Arguments are string with a question and function name to continue
    con = custom_input(question)
    if con == 'y':
        fnc()
    elif con == 'q':
        print("\nBye!")
        sys.exit(0)
    elif con == 'n':
        if fnc == main:
            print("\nBye!")
            sys.exit(0)
        else:
            return 
    else:
        print("Please, enter 'y' or 'n'")
        cont(question,fnc)

def custom_input(inputText):
    # This function checks whether user inputs 'q', and if they do program terminates
    inputValue = input(inputText)
    if inputValue == 'q':
        print("\nBye!")
        exit()
    else:
        return inputValue


def print_dict_10_by_10(question, exitFnc, dictionary):
    # Prints dictionary records 10 by 10. Arguments allow user to continue from a particular moment of the program
    counter = 1
    for movie, rating in dictionary.items():
        print('{0}. {1} - {2}'.format(counter, movie, rating))
        if counter%10 == 0:
            next = custom_input("\nShow next 10? (y/n)")
            while next != 'y' and next != 'n':
                print("Please, enter 'y' or 'n'")
                next = custom_input("\nShow next 10? (y/n)")
            if next == 'y':
                print("\n")
            else:
                cont(question, exitFnc)
                return    
        counter += 1
    cont(question, exitFnc)
    
def similarity_choice():
    # This function printes the list of similarities and returns a choice
    print("\nEnter a similarity method to check similarities between users: ")
    print("1 - Cosine similarity")
    print("2 - Manhattan similarity")
    print("3 - Jaccard similarity")
    print("4 - Euclidean similarity")
    print("5 - Pearson similarity")
    print("6 - All of them")
    print("For exit enter 'q'")
    return custom_input("Enter here:")
    
def two_users_similarity():
    # This fuction is a menu option for conducting two user comparison
    while True: 
        try:
            print("\nEnter ids of users (1-{0}). For exit enter 'q'".format(numberOfUsers))
            user1 = custom_input("Enter the first user id: ")
            user2 = custom_input("Enter the second user id: ") 
            # Obtaining users ratings in a list
            (ratingUser1, ratingUser2) = common_movies_ratings(userPreferences, user1, user2)[0:2] 
            break
        except KeyError:
            # In the case when input is not numbers from 1 to a number of users
            print("Input is incorrect! Only numbers from 1 to {0}".format(numberOfUsers))
    
    commonMovies = common_movies(userPreferences, user1, user2)
    
    # If the list of common movies is empty
    if len(commonMovies) == 0:     
        print("These users have no movies in common")
        cont("Compare other two users? (y/n)",two_users_similarity)   
        cont("Return to main menu? (y/n)",main)    
    
    print("\nCommon movies of these users are: ")
    for movie in range(len(commonMovies)):
        print("{0}:\nUser One - {1}, User Two - {2}".format(commonMovies[movie], ratingUser1[movie], ratingUser2[movie]))
    if len(commonMovies) == 1: print("There is only one movie rated by both users")
    else:
        print("\nThere are {0} movies rated by both users".format(len(commonMovies)))
    similarity = similarity_choice()
    # Checking if the similarity choice is numbers from 1 to 6 and only one symbol
    while any(ext in similarity for ext in simOptions) == 0 or len(similarity) > 1:
        print("Wrong input!")
        similarity = similarity_choice()
    
    if similarity == "1":
        print("\nAccording to Cosine, the similarity is: ",cosine_similarity(ratingUser1, ratingUser2))
    elif similarity == "2":
        print("\nAccording to Manhatan, the similarity is: ",manhattan_similarity(ratingUser1, ratingUser2))
    elif similarity == "3":
        print("\nAccording to Jaccard, the similarity is: ",jaccard_similarity(userPreferences ,user1, user2))
    elif similarity == "4":
        print("\nAccording to Euclidean, the similarity is: ",euclidean_similarity(ratingUser1, ratingUser2))
    elif similarity == "5":
        print("\nAccording to Pearson, the similarity is: ",pearson_similarity(ratingUser1, ratingUser2))
    elif similarity == "6":
        print("\nAccording to Cosine, the similarity is: ",cosine_similarity(ratingUser1, ratingUser2))
        print("According to Manhatan, the similarity is: ",manhattan_similarity(ratingUser1, ratingUser2))
        print("According to Jaccard, the similarity is: ",jaccard_similarity(userPreferences ,user1, user2))
        print("According to Euclidean, the similarity is: ",euclidean_similarity(ratingUser1, ratingUser2))
        print("According to Pearson, the similarity is: ",pearson_similarity(ratingUser1, ratingUser2))
    # It is possible to repeat the comparison or return to the main menu
    cont("\nCompare two other users? (y/n)",two_users_similarity)   
    cont("Return to main menu? (y/n)",main)    
 
    
def best_match():
    # This fuction is a menu option for finding of best match users for a target user
    # Input of a user id which accept only numbers from 1 to the number of users
    while True:
        try:
            user1 = custom_input("\nEnter user id: ")
            bestMatchUsers = best_match_users(userPreferences, user1,pearson_similarity)     
            break
        except KeyError:
            print("Input is incorrect! Only numbers from 1 to {0}".format(numberOfUsers))
    
    print("Best match users are:")
    # If the list is not empty
    if bool(bestMatchUsers) == 1:
        for user in bestMatchUsers: print(user, end = ", ")
    # If the list is empty
    else:
        print("Similar users for the target user were not found!")   
    # It is possible to find best match users for another user or return to the main menu   
    cont("\nFind best match users for another user? (y/n)",best_match)   
    cont("Return to main menu? (y/n)",main)    

def top_movies():
    # This is a menu option for the best rated movies
    topMovies = top_rated_movies(userPreferences)
    print_dict_10_by_10("Return to main menu? (y/n)", main, topMovies)
        
def movie_rating():
    # This function is a menu option for finding movies and their ratings
    movieInput = custom_input("Enter a movie name: ")
    
    while len(movieInput) < 2:
        print("Please, enter at least two symbols")
        movieInput = custom_input("Enter a movie name: ")
    
    topMovies = top_rated_movies(userPreferences)
    searchResult = {}

    for movie, rating in topMovies.items():
        # Every movie is compared with the string from the input. If the string is in the name of a movie
        # it is stored in the searchResult dictionary. Search is case insensitive 
        if (movie.lower()).find(movieInput.lower()) != -1:
            searchResult[movie] = rating
    #Check if search result is not empty
    if bool(searchResult) == 1:
        for movie, rating in searchResult.items():
            print(movie,"-", rating)
    else:
        print("No movies were found!")       
    # It is possible to search another movie or return to the main menu   
    cont("\nFind one more movie? (y/n)",movie_rating)   
    cont("Return to main menu? (y/n)",main)    
           
def movies_recommendation():
    # Input of a user id which accept only numbers from 1 to the number of users
    while True: 
        try:
            user1 = custom_input("\nEnter user id: ")
            recommendedMovies = recommended_movies(userPreferences, user1,pearson_similarity)
            break
        except KeyError:
            print("Input is incorrect! Only numbers from 1 to {0}".format(numberOfUsers))
    
    print("Movies recommendation for",user1,": \n")
    # It is possible to show movies 10 by 10, find another recommendation or return to the main menu 
    print_dict_10_by_10("\nFind recommendation for another user? (y/n)", movies_recommendation, recommendedMovies)
    cont("Return to main menu? (y/n)",main)  
      
def main():  
    # The main function for the initial option choice
    print("\nPlease, make your choice (1-5). For exit enter 'q' at any time.") 
    print("1 - Compare two users")
    print("2 - Find best match users for a target user")
    print("3 - Find movies recommendations for a user")
    print("4 - Show top rated movies")
    print("5 - Check the rating of a movie")
    choice = custom_input("Enter here:")
    # Checking if the option choice is numbers from 1 to 5
    while any(ext in choice for ext in menuOptions) == 0 or len(choice) > 1:
        print("Wrong input!")
        choice = custom_input("Please, correct your input: ")
    
    if choice == "1":
        two_users_similarity()
    elif choice == "2":
        best_match()
    elif choice == "3":
        movies_recommendation()
    elif choice == "4":
        top_movies()
    elif choice == "5":
        movie_rating()
    
if __name__ == '__main__':
    main()