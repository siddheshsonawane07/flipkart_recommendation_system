from flask import Flask, request, jsonify
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from flask_cors import CORS

# Load the data
data = pd.read_csv('csv/orderHistory.csv')

# Data Preprocessing
data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')
data['product_name'] = data['product_name'].astype('category').cat.codes
data['brand'] = data['brand'].astype('category').cat.codes

# Create a pivot table for user-item interactions
user_item_matrix = data.pivot_table(index='uid', columns='pid', values='price', fill_value=0)

# Collaborative Filtering Model
model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(user_item_matrix)

# Function to get similar items (Collaborative Filtering)
def get_similar_items(item_id, n=10):
    distances, indices = model_knn.kneighbors(user_item_matrix.loc[:, item_id].values.reshape(1, -1), n_neighbors=n+1)
    return indices.flatten()[1:]

# Compute item similarity matrix (Content-Based Filtering)
item_features = data[['pid', 'product_name', 'brand']]
item_similarity = cosine_similarity(item_features)

# Function to get similar items (Content-Based Filtering)
def get_similar_items_content_based(item_id, n=10):
    idx = data[data['pid'] == item_id].index[0]
    similar_indices = np.argsort(-item_similarity[idx])[1:n+1]
    return data.iloc[similar_indices]['pid'].values

# Hybrid Recommendation Function
def hybrid_recommendations(user_id, item_id, n=10):
    collaborative_recs = get_similar_items(item_id, n)
    content_based_recs = get_similar_items_content_based(item_id, n)
    
    # Combine recommendations
    hybrid_recs = list(set(collaborative_recs).union(set(content_based_recs)))
    
    return hybrid_recs[:n]

# Initialize Flask App
app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        user_id = request.json['user_id']
        item_id = request.json['item_id']
        # Check if user_id and item_id exist in the data
        if user_id not in data['uid'].values:
            return jsonify({"error": "User ID not found"}), 400
        if item_id not in data['pid'].values:
            return jsonify({"error": "Item ID not found"}), 400

        recommendations = hybrid_recommendations(user_id, item_id)
        return jsonify(recommendations)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
