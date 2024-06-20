import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import pickle

# Load your data
data = pd.read_csv('main_data.csv')

# Train CountVectorizer
cv = CountVectorizer()
count_matrix = cv.fit_transform(data['comb'])

# Save the vectorizer
with open('count_vectorizer.pkl', 'wb') as f:
    pickle.dump(cv, f)
