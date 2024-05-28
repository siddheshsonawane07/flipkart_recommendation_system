from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import time
import datetime
import random
app = Flask(__name__)

class Recommender:
    def __init__(self):
        self.orderHistory = pd.read_csv("csv/orderhistory.csv")
        self.browseHistory = pd.read_csv("csv/browsehistory.csv")
        self.products = pd.read_csv("csv/products.csv")
        self.correlationData = pd.read_csv("csv/correlationData.csv")
    
    def getProductRecommendation(self, userId):
        try:
            start_time = time.time()
                        
            userOrders = self.orderHistory[self.orderHistory['uid'] == userId]
            print(userOrders)
            print(f"Fetched user orders in {time.time() - start_time} seconds")
            
            # Filter browse history by user ID
            browseHistory = self.browseHistory[self.browseHistory['uid'] == userId]
            productCorrelationData = self.correlationData.copy()
            
            products = self.products.copy()
            products.columns = ['pid', 'product_name', 'price', 'brand']
            
            if userOrders.empty and browseHistory.empty:
                # If the user has no orders or browse history, recommend random products
                sampleProducts = products.sample(n=20)
                return sampleProducts.values.tolist()
            
            start_time = time.time()
            
            # Adjust product correlation data based on user orders
            for i in range(len(userOrders)):
                pid = userOrders.iloc[i]['pid']
                productCorrelationData.loc[productCorrelationData['pid'] == pid, 'price'] *= userOrders.iloc[i]['quantity']
                
            print(f"Adjusted product correlation data based on user orders in {time.time() - start_time} seconds")
            
            start_time = time.time()
            
            # Adjust product correlation data based on browse history
            browseHistory = browseHistory.sort_values(by='date', ascending=False)
            browseHistory = browseHistory.drop_duplicates(subset='pid', keep='first')
            
            for i in range(min(20, len(browseHistory))):
                pid = browseHistory.iloc[i]['pid']
                timeDelta = datetime.datetime.now() - datetime.datetime.strptime(browseHistory.iloc[i]['date'], '%Y-%m-%d %H:%M:%S')
                decayFactor = max(0.1, 1 - (timeDelta.days / 100))
                productCorrelationData.loc[productCorrelationData['pid'] == pid, 'price'] *= decayFactor
                
            print(f"Adjusted product correlation data based on browse history in {time.time() - start_time} seconds")
            
            start_time = time.time()
            
            # Generate sample products
            sampleProducts = products.sample(n=20)
                
            print(f"Generated sample products in {time.time() - start_time} seconds")
            
            start_time = time.time()
            
            # Calculate scores for products
            productScores = {}
            for index, row in productCorrelationData.iterrows():
                score = row['price'] * row['name']  # You may need to adjust this based on your correlation data structure
                productScores[row['pid']] = score
                
            # Sort products by score and select top 20
            topProducts = sorted(productScores, key=productScores.get, reverse=True)[:20]
            recommendedProducts = products[products['pid'].isin(topProducts)]
            
            print(f"Generated recommended products in {time.time() - start_time} seconds")
            
            return recommendedProducts.values.tolist()
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return []

recommender = Recommender()

@app.route('/recommend/<userId>', methods=['GET'])
def recommend(userId):
    recommendations = recommender.getProductRecommendation(userId)
    return jsonify(recommendations)


@app.route('/log_interaction', methods=['POST'])
def log_interaction():
    try:
        data = request.json
        # Load existing order history CSV
        order_history = pd.read_csv("csv/orderhistory.csv")
        
        # Create a DataFrame from the interaction data
        interaction_data = pd.DataFrame([{
            'oid': data.get('oid'),
            'uid': data.get('uid'),
            'date': pd.Timestamp.now().strftime('%d-%m-%Y'),  # Format date without time
            'product_name': data.get('product_name'),  # Since you mentioned to ignore product_name, let's assume it will be added later if needed.
            'pid': data.get('pid'),
            'price': data.get('price'),
            'brand': data.get('brand')
        }])
        
        # Append the interaction data to the existing order history
        updated_order_history = pd.concat([order_history, interaction_data], ignore_index=True)
        
        # Save the updated order history back to the CSV file
        updated_order_history.to_csv("csv/orderhistory.csv", index=False)
        
        return jsonify({"message": "Interaction logged successfully"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)