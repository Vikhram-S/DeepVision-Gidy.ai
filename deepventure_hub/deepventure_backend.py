import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import tensorflow as tf
import random
import requests
from datasets import load_dataset  # Optional, for local training

class DeepVentureBackend:
    def __init__(self, hf_api_token):
        self.hf_api_token = hf_api_token
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = LinearRegression()
        self.simulation_model = self._build_simulation_model()
        self.mentors = {
            "restaurant": ["John Food", "Sarah Chef"],
            "tech": ["Mike Tech"],
            "service": ["Emma Service"]
        }
        self.microlearning = {
            "business": ["Business Strategy", "Market Entry"],
            "marketing": ["Digital Marketing", "Branding"],
            "finance": ["Cash Flow", "Investment Basics"]
        }
        # Train with mock data initially
        self._train_evaluation_model_with_mock_data()

    def _train_evaluation_model_with_mock_data(self):
        # Mock data for initial model (updated later with API data)
        mock_descriptions = ["Great tech startup", "Amazing restaurant", "Service business"]
        mock_scores = [80, 90, 70]
        X = self.vectorizer.fit_transform(mock_descriptions)
        self.model.fit(X, np.array(mock_scores))

    def _build_simulation_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(1,)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def _fetch_hf_data(self, query, limit=5):
        """Fetch data from Hugging Face yelp_review_full dataset"""
        url = "https://datasets-server.huggingface.co/rows"
        params = {
            "dataset": "yelp_review_full",
            "config": "yelp_review_full",
            "split": "train",
            "query": query,  # Search term (approximate match)
            "limit": limit
        }
        headers = {"Authorization": f"Bearer {self.hf_api_token}"}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("rows", [])
        return []

    def evaluate_idea(self, description):
        """Evaluate idea using Hugging Face dataset API"""
        rows = self._fetch_hf_data(description, limit=5)
        if rows:
            avg_rating = np.mean([row["row"]["stars"] * 20 for row in rows])  # Convert 5-star to 100
            X = self.vectorizer.transform([description])
            score = self.model.predict(X)[0]
            return min(max(int((score + avg_rating) / 2), 0), 100)
        return random.randint(50, 90)  # Fallback

    def run_simulation(self, title, description, score):
        """Run simulation using Hugging Face dataset API"""
        normalized_score = score / 100
        prediction = self.simulation_model.predict(np.array([[normalized_score]]))[0][0]
        
        rows = self._fetch_hf_data(description.split()[0], limit=10)
        if rows:
            ratings = [row["row"]["stars"] * 20 for row in rows]
            # Use text length as a proxy for "review count" since API doesn’t provide this
            review_counts = [len(row["row"]["text"]) / 100 for row in rows]
            market_potential = min(np.mean(review_counts), 95)
            risk_factor = 50 - (np.mean(ratings) / 2)
        else:
            market_potential = random.uniform(60, 95)
            risk_factor = random.uniform(10, 40)

        return {
            "success_rate": round(prediction * 100, 2),
            "market_potential": round(market_potential, 2),
            "risk_factor": round(risk_factor, 2)
        }

    def match_mentor(self, description):
        """Match mentor based on keywords"""
        description = description.lower()
        for category, mentors in self.mentors.items():
            if category in description:
                return random.choice(mentors)
        return random.choice(self.mentors["tech"])

    def get_microlearning(self, category):
        """Get microlearning modules"""
        return self.microlearning.get(category, self.microlearning["business"])

    def get_analytics(self):
        """Fetch real-time analytics from Hugging Face dataset API"""
        categories = ["restaurant", "tech", "service"]
        trends = {}
        for category in categories:
            rows = self._fetch_hf_data(category, limit=50)
            if rows:
                ratings = [row["row"]["stars"] * 20 for row in rows]
                trends[category] = round(np.mean(ratings), 2)
            else:
                trends[category] = random.uniform(70, 90)
        
        funding_rounds = int(sum(len(row["row"]["text"]) for row in self._fetch_hf_data("", limit=50)) / 1000)
        sector_growth = round(np.mean([trends[cat] for cat in trends]) / 10, 2)

        return {
            "market_trends": trends,
            "funding_rounds": funding_rounds,
            "sector_growth": sector_growth
        }