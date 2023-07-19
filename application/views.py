
from django.shortcuts import render,redirect
from django.http import HttpResponse
import pandas as pd
from pandas import DataFrame
import requests
from pymongo import MongoClient
from django.core.mail import send_mail

# for pickel file from static folder
from django.contrib.staticfiles import finders



# # sending mail
# send_mail(
#         "Movie recommendation system",
#         "Thank for using the App. Have a good Day",
#         "ketanmogre1998@gmail.com",
#         ["nikhilmogre1998@gmail.com"],
#         fail_silently=False,
#     )



# connect to mongoDB Atlas
client = MongoClient('mongodb+srv://Nikhil:pwskills@cluster0.siytt6m.mongodb.net/?retryWrites=true&w=majority')
# new database
db = client['movie_database']
# created collection
cursor = db['movies_details']
# created collection 
combine_data = db['extracted_details_actor_crew_tag']


# find file from static folder
movies_path = finders.find('data1/movies.pkl')
similarity_path = finders.find('data2/similarity.pkl')

# read the file 
movies_df = pd.read_pickle(movies_path)
similarity = pd.read_pickle(similarity_path)


# All movie list are extracted from file
movies_lst=movies_df['title']




# function is for fetching the movie poster
def fetch_poster(movie_id):
    try: 
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b8d0f958de8242ac18a57db0c313c5c1&language=en-US'
                    .format(movie_id))
        data = response.json()

        # Check if poster_path is None
        if data["poster_path"] is None:
            return None

        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    
    except: 
        return HttpResponse('No poster')



# give recommended movie for users
def recom(request, movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[:20]

    recommended_movies = []
    recommended_movie_posters = []
    # made to resolve issue 
    recom_movie_details={}
    user_movie_details = {}

    for ind,i in enumerate(movies_list):
        if ind!=0:
            movie_id = movies_df.iloc[i[0]].movie_id
            recommended_movies.append(movies_df.iloc[i[0]].title)
            recommended_movie_posters.append(fetch_poster(movie_id))
            # made new dic
            recom_movie_details[movies_df.iloc[i[0]].title]=fetch_poster(movie_id)

        else:
            movie_id = movies_df.iloc[i[0]].movie_id
            # print(movie_id)
            movie_id = int(movie_id)

            # take data after merging data
            data_1 = combine_data.find({'movie_id':movie_id})
            # taken data from movies_details
            data_2 = cursor.find({'id':movie_id})

            # print(data_1)
            for d,k in zip(data_1,data_2):

                user_movie_details['url']=fetch_poster(movie_id)

                user_movie_details['Title'] = d['title']
                user_movie_details['Actors'] = d['cast'][0] +', ' +d['cast'][1] + ', ' +d['cast'][2]
                user_movie_details['Director of movie'] = d['crew'][0]
                # user_movie_details['Title'] = k['title']
                user_movie_details['overview'] = k['overview']
                user_movie_details['Release Date'] = k['release_date']
                user_movie_details['Rating'] = k['vote_average']
                # converting time in hr and minutes.
                Q = int(k['runtime']//60 )
                R = int(k['runtime'] - Q*60)
                time = '{} hr {} min'.format(Q,R)
                user_movie_details['Runtime in minutes'] = time

                
    
    # exp = {'movies_name': recommended_movies, 'movies_poster': recommended_movie_posters}
    # return render(request, 'user_recom_movies.html', {'output': exp})
    # return recom_movie_details,user_movie_details
    return render(request,'recom.html',{'output':recom_movie_details,'user':user_movie_details})


def index(request):
    # movies_lst = Movie.objects.values_list('title', flat=True)
    return render(request, 'front.html', {'new': movies_lst})

def movie(request):
    if request.method == 'POST':
        user = request.POST['mymovie']
        send_mail(
        "Movie recommendation system",
        "Thank for using the App. Have a good Day",
        "ketanmogre1998@gmail.com",
        ["nikhilmogre1998@gmail.com"],
        fail_silently=False,
        )
        
        return recom(request,user)

