import math 
from load_dataset_module import *
from collections import OrderedDict 

def number_of_users(): 
    # This function counts a number of users in the dictionary
    user_preference = load_dataset()
    counter = 0
    for key in user_preference:
        counter += 1
    return counter

def common_movies(userPreferences, user1, user2): 
    # This function finds common movies of two users
    intersect = []
    for movie in userPreferences[user1]:
        if movie in userPreferences[user2]:
            intersect.append(movie) 
    return intersect  
                                        
def user_movies(userPreferences, user):
    # This function finds movies of a user
    movies = []
    for movie in userPreferences[user]:
            movies.append(movie) 
    return movies  

def best_match_users(userPreference, user1, similarity_method, simTreshold=0.7, comMoviesTreshold=5):
    # This fucntion finds similar users for a target user
    bestMatchUsers = []
    # Loop that checks every user from 1
    for user in range(number_of_users())[1:]:
        user = str(user)
        # Exclude the user itself
        if user == user1: continue
        (ratingUser1, ratingUser2) = common_movies_ratings(userPreference, user1, user)[0:2]
        # Calculate Pearson similarity of a target user and a user from the loop
        similarity = similarity_method(ratingUser1, ratingUser2)
        commonMovies = common_movies(userPreference, user1, user)
        # Treshold for similar users: similarity more than 0.7 and more than 5 common movies
        if similarity >= simTreshold and len(commonMovies) > comMoviesTreshold:
            bestMatchUsers.append(user)
    return bestMatchUsers

def recommended_movies(userPreferences, user1, similarity_method):
    bestMatchUsers = best_match_users(userPreferences, user1, pearson_similarity)
    # Dictionary for sum of weighted ratings of users for a movie (rating * similarity)
    totals = {}
    # Dictionary for sum of similarities for a movie
    sumSim = {}
    recommendation = {}
    # Loop goes through the list of users with the highest similarities
    for user in bestMatchUsers:
        (ratingUser1, ratingUser2) = common_movies_ratings(userPreferences, user1, user)[0:2]
        similarity = round(similarity_method(ratingUser1, ratingUser2),4)
        # Loop goes through movies of a user from the BestMatchUsers list
        for movie in userPreferences[user]:
            # Only movies that the user from input hasn't rated
            if movie in userPreferences[user1]: continue
            # If movie is not in the dictionary of raitings sums it is created with default value '0'
            totals.setdefault(movie, 0)
            # Movie rating of a user multiplied by similaryty is added to sum of ratings
            totals[movie] += int(userPreferences[user][movie]) * similarity
            # If movie is not in the dictionary of similarities sums it is created with default value '0'
            sumSim.setdefault(movie, 0)
            # User similarity is added to similarity sum for a movie
            sumSim[movie] += similarity
    
    # Loop for sorting movies for recommendations            
    for movie, total in totals.items():
        # Mean rating is calculated from sum of weighted rating divided by the sum of users similarities
        rating = total/sumSim[movie]
        # Only movies with rating > 4 are interesting
        if rating >= 4:
            recommendation[movie] = round(rating,2)
    # Sorting of the recommendation dictionary by values from biggest to smallest
    recommendationOrdered = OrderedDict(sorted(recommendation.items(), key=lambda t: t[1], reverse=True))
    
    return recommendationOrdered

def top_rated_movies(userPreferences):
    totals = {}
    # Dictionary for the counter of users rated a movie
    usersSum = {}
    bestMovies = {}
    for user in range(number_of_users())[1:]:
        user = str(user)
        for movie in userPreferences[user]:
            # If movie is not in the dictionary of raitings sums it is created with default value '0'
            totals.setdefault(movie, 0)
            # Movie rating of a user is added to the sum of ratings
            totals[movie] += int(userPreferences[user][movie])
            # If a movie is not in the users counter dictionary it is created with default value '0'
            usersSum.setdefault(movie, 0)
            # User is added to the users counter for a movie
            usersSum[movie] += 1
    
    for movie, total in totals.items():
        # Only movies rated by more than 20 users
        if usersSum[movie] > 20:
            rating = total/usersSum[movie]
            bestMovies[movie] = round(rating,2)
    # Sorting of the recommendation dictionary by values from biggest to smallest
    bestMoviesOrdered = OrderedDict(sorted(bestMovies.items(), key=lambda t: t[1], reverse=True))
    
    return bestMoviesOrdered

def common_movies_ratings(userPreferences, user1, user2): 
    # This fuction returns 2 lists with ratings of user1 and user2 accordingly
    user1Rating = []
    user2Rating = []
    
    commonMovies = common_movies(userPreferences, user1, user2) 
    
    # Picking ratings of common movies for both users            
    for movie in range(len(commonMovies)):
        user1Rating.append(int(userPreferences[user1][commonMovies[movie]]))
        user2Rating.append(int(userPreferences[user2][commonMovies[movie]]))
    return user1Rating, user2Rating    

def cosine_similarity(user1Rating, user2Rating):
    num = sum(a*b for a,b in zip(user1Rating,user2Rating))
    denom = math.sqrt(sum([a*a for a in user1Rating]))*math.sqrt(sum([a*a for a in user2Rating]))          
    return round(num/float(denom),4) 

def euclidean_similarity(user1Rating, user2Rating):
    try:
        n = len(user1Rating)
        return round((1 - (math.sqrt(sum((pow((a-b),2)) for a,b in zip(user1Rating,user2Rating))))/(math.sqrt(n)*4)), 4)
    # In the case of division by zero the vectors are identical
    except ZeroDivisionError:
        return 1.0
    
def manhattan_similarity(user1Rating, user2Rating):
    try:
        n = len(user1Rating)
        return round((1 - (sum(abs(a-b) for a,b in zip(user1Rating,user2Rating)))/(n*4)), 4)
    # In the case of division by zero the vectors are identical
    except ZeroDivisionError:
        return 1.0
    
def jaccard_similarity(userPreferences, user1, user2):
    intersection = len(list(set(user_movies(userPreferences, user1)) & set(user_movies(userPreferences, user2))))
    union = len(set(user_movies(userPreferences, user1)) | set(user_movies(userPreferences, user2)))
    return round(intersection/union,4)
        
def pearson_similarity(user1Rating, user2Rating):
    try:    
        n = len(user1Rating)
        if n <= 2:
            # The result of pearson similarity becomes meanungful when number of pairs more than 2
            return 0
        else:
            meanUser1 = sum(user1Rating)/n
            meanUser2 = sum(user2Rating)/n
            num = sum((a - meanUser1)*(b - meanUser2) for a,b in zip(user1Rating,user2Rating))
            denom = sum((a - meanUser1)**2 for a in user1Rating) * sum((a - meanUser2)**2 for a in user2Rating)
            return round(num/math.sqrt(denom),4)
    # In the case of division by zero the vectors are identical
    except ZeroDivisionError:
        return 1.0
