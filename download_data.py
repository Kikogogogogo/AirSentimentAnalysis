import pandas as pd
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import numpy as np
import json
from textblob import TextBlob
import re

def download_and_process_data():
    # Define keyword dictionary
    keywords = {
        'ai': r'\bai\b|\bartificial intelligence\b',
        'algorithm': r'\balgorithm\b|\brecommendation\b',
        'misinformation': r'\bmisinformation\b|\bfake news\b|\bdisinformation\b',
        'social_media': r'\bsocial media\b|\btwitter\b|\bfacebook\b|\binstagram\b'
    }
    
    # Check if kaggle.json exists in current directory
    if os.path.exists('kaggle.json'):
        # Read kaggle.json content
        with open('kaggle.json', 'r') as f:
            credentials = json.load(f)
        
        # Set environment variables
        os.environ['KAGGLE_USERNAME'] = credentials['username']
        os.environ['KAGGLE_KEY'] = credentials['key']
    
    # Initialize Kaggle API
    api = KaggleApi()
    api.authenticate()
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Download multiple related datasets
    datasets = [
        'crowdflower/twitter-airline-sentiment',
        'kaushiksuresh147/twitter-sentiment-analysis',
        'therohk/misinformation-on-twitter'
    ]
    
    all_data = []
    for dataset in datasets:
        try:
            api.dataset_download_files(dataset, path='data', unzip=True)
            # Read and process data
            if 'Tweets.csv' in os.listdir('data'):
                df = pd.read_csv('data/Tweets.csv')
                # Add dataset identifier
                df['dataset'] = dataset.split('/')[-1]
                all_data.append(df)
        except Exception as e:
            print(f"Error processing dataset {dataset}: {str(e)}")
    
    # Merge all datasets
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Data cleaning and feature engineering
        def extract_features(text):
            # Calculate text length
            length = len(text)
            # Calculate sentiment score
            sentiment = TextBlob(text).sentiment.polarity
            # Detect possible keywords
            keyword_counts = {
                key: len(re.findall(pattern, text.lower()))
                for key, pattern in keywords.items()
            }
            return pd.Series([length, sentiment] + list(keyword_counts.values()))
        
        # Apply feature extraction
        features = combined_df['text'].apply(extract_features)
        features.columns = ['text_length', 'sentiment'] + list(keywords.keys())
        
        # Merge features
        processed_df = pd.concat([combined_df, features], axis=1)
        
        # Save processed data
        processed_df.to_csv('data/processed_tweets.csv', index=False)
        print("Data processing completed!")
    else:
        print("No datasets were successfully processed")

if __name__ == '__main__':
    download_and_process_data() 