from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import time
import datetime
from fuzzywuzzy import fuzz
import random

app = Flask(__name__)

class Recommender:
    def __init__(self):
        self.orderHistory = pd.read_csv(r"csv/orderHistory.csv")
        self.browseHistory = pd.read_csv(r"csv/browseHistory.csv")
        self.products = pd.read_csv(r"csv/products.csv")
        self.correlationData = pd.read_csv(r"csv/correlationData.csv")
    
    def getProductRecommendation(self, userId):
        try:
            start_time = time.time()
            
            userOrders = self.orderHistory[self.orderHistory['uid'] == userId]
            print(userOrders)
            print(f"Fetched user orders in {time.time() - start_time} seconds")
            
            browseHistory = self.browseHistory[self.browseHistory['uid'] == userId]
            productCorrelationData = self.correlationData.copy()
            
            products = self.products.copy()
            products.columns = ['productId', 'productTitle', 'productPrice', 'brand']
            
            if len(userOrders) == 0 and len(browseHistory) == 0:
                sampleProducts = products.sample(n=20)
                return sampleProducts.values.tolist()
            
            start_time = time.time()
            
            for i in range(len(userOrders)):
                productId = userOrders.iloc[i]['productId']
                quantity = userOrders.iloc[i]['quantity']
                productCorrelationData[productId] = productCorrelationData[productId] * quantity
                
            print(f"Adjusted product correlation data in {time.time() - start_time} seconds")
            
            start_time = time.time()
            
            browseHistory = browseHistory.sort_values(by='activityTime', ascending=False)
            browseHistory = browseHistory.drop_duplicates(subset='productId', keep='first')
            
            for i in range(min(20, len(browseHistory))):
                productId = browseHistory.iloc[i]['productId']
                timeDelta = datetime.datetime.now() - datetime.datetime.strptime(browseHistory.iloc[i]['activityTime'], '%Y-%m-%d %H:%M:%S')
                decayFactor = max(0.1, 1 - (timeDelta.days / 100))
                productCorrelationData[productId] = productCorrelationData[productId] * decayFactor
                
            print(f"Adjusted correlation data based on browse history in {time.time() - start_time} seconds")
            
            start_time = time.time()
            
            productIds = products['productId'].tolist()
            sampleProducts = []
            
            for i in range(20):
                chosenProductId = random.choice(productIds)
                productIds.remove(chosenProductId)
                sampleProducts.append(products[products['productId'] == chosenProductId].values.tolist()[0])
                
            print(f"Generated sample products in {time.time() - start_time} seconds")
            
            start_time = time.time()
            
            scoredProducts = {}
            for productId in productIds:
                score = sum(productCorrelationData[productId])
                scoredProducts[productId] = score
                
            topProducts = sorted(scoredProducts, key=scoredProducts.get, reverse=True)[:20]
            recommendedProducts = products[products['productId'].isin(topProducts)]
            
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

if __name__ == '__main__':
    app.run(debug=True)
