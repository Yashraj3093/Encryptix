import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import bs4 as bs
import urllib.request

# Load the vectorizer and classifier from disk
with open('count_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('nlp_model.pkl', 'rb') as f:
    clf = pickle.load(f)

# Function to recommend movies based on user input
def recommend_movie():
    movie_name = entry.get().lower()
    if movie_name.strip() == '':
        messagebox.showwarning('Warning', 'Please enter a movie name.')
        return
    
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()

    if movie_name not in data['movie_title'].unique():
        messagebox.showinfo('Information', 'Sorry! The movie you requested is not in our database.')
    else:
        i = data.loc[data['movie_title']==movie_name].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        recommended_movies = []
        for j in range(1, 11):  # Top 10 recommended movies
            a = lst[j][0]
            recommended_movies.append(data['movie_title'][a])
        
        messagebox.showinfo('Recommendations', '\n'.join(recommended_movies))

# Function to scrape reviews from IMDB based on IMDB ID
def scrape_reviews(imdb_id):
    try:
        sauce = urllib.request.urlopen(f'https://www.imdb.com/title/{imdb_id}/reviews?ref_=tt_ov_rt').read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        soup_result = soup.find_all("div", {"class": "text show-more__control"})

        reviews_list = []  # list of reviews
        for reviews in soup_result:
            if reviews.string:
                reviews_list.append(reviews.string)
        
        return reviews_list
    except Exception as e:
        return ['Failed to fetch reviews.']

# Function to handle movie recommendation and review scraping
def get_recommendation_and_reviews():
    movie_name = entry.get().lower()
    if movie_name.strip() == '':
        messagebox.showwarning('Warning', 'Please enter a movie name.')
        return

    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()

    if movie_name not in data['movie_title'].unique():
        messagebox.showinfo('Information', 'Sorry! The movie you requested is not in our database.')
    else:
        i = data.loc[data['movie_title'] == movie_name].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        recommended_movies = []
        for j in range(1, 11):  # Top 10 recommended movies
            a = lst[j][0]
            recommended_movies.append(data['movie_title'][a])

        try:
            genres = data.loc[data['movie_title'] == movie_name, 'genres'].values[0]
            messagebox.showinfo('Recommendations', f'Recommended Movies:\n\n' + '\n'.join(recommended_movies) +
                                f'\n\nGenre of {movie_name.capitalize()}: {genres}')
        except KeyError as e:
            messagebox.showerror('Error', f'KeyError: {str(e)}. Check your data columns.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')


# Function to initialize Tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title('Movie Recommendation System')

    label = ttk.Label(root, text='Enter Movie Name:')
    label.pack(pady=10)

    global entry
    entry = ttk.Entry(root, width=40)
    entry.pack(pady=10)

    recommend_button = ttk.Button(root, text='Recommend Movies', command=get_recommendation_and_reviews)
    recommend_button.pack(pady=10)

    root.mainloop()

# Load data and initialize similarity matrix
def create_similarity():
    data = pd.read_csv('main_data.csv')
    count_matrix = vectorizer.transform(data['comb'])
    similarity = cosine_similarity(count_matrix)
    return data, similarity

if __name__ == '__main__':
    create_similarity()  # Initialize similarity matrix and data
    
    # Create the Tkinter GUI
    create_gui()
