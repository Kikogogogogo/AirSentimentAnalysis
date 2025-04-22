import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
from textblob import TextBlob

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Read processed data
df = pd.read_csv('data/processed_tweets.csv')

# Create figure
plt.figure(figsize=(20, 15))

# 1. Relationship between keyword frequency and engagement
plt.subplot(2, 2, 1)
keywords = ['ai', 'algorithm', 'misinformation', 'social_media']
keyword_data = []
for keyword in keywords:
    keyword_data.append(df[df[keyword] > 0]['retweet_count'].mean())
sns.barplot(x=keywords, y=keyword_data)
plt.title('Average Retweets by Keyword')
plt.xlabel('Keywords')
plt.ylabel('Average Retweet Count')
plt.xticks(rotation=45)

# 2. Analysis of misinformation dissemination effects
plt.subplot(2, 2, 2)
misinfo_data = df[df['misinformation'] > 0]
non_misinfo_data = df[df['misinformation'] == 0]
sns.boxplot(data=[misinfo_data['retweet_count'], non_misinfo_data['retweet_count']])
plt.title('Comparison of Dissemination Effects: Misinformation vs Non-Misinformation')
plt.xlabel('Information Type')
plt.ylabel('Retweet Count')
plt.xticks([0, 1], ['Misinformation', 'Non-Misinformation'])

# 3. Relationship between sentiment analysis and keywords
plt.subplot(2, 2, 3)
sns.heatmap(df[['sentiment'] + keywords].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation between Sentiment Analysis and Keywords')

# 4. Word cloud generation function
def generate_wordcloud(texts, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(texts))
    plt.subplot(2, 2, 4)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')

# Generate word clouds for tweets with and without misinformation separately
misinfo_texts = df[df['misinformation'] > 0]['text']
non_misinfo_texts = df[df['misinformation'] == 0]['text']

# Adjust layout
plt.tight_layout()
plt.show()

# Additional analysis: Dissemination patterns of recommendation algorithm related content
plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
algorithm_texts = df[df['algorithm'] > 0]['text']
generate_wordcloud(algorithm_texts, 'Keywords in Recommendation Algorithm Related Tweets')

plt.subplot(1, 2, 2)
ai_texts = df[df['ai'] > 0]['text']
generate_wordcloud(ai_texts, 'Keywords in AI Related Tweets')
plt.tight_layout()
plt.show()

# Time series analysis (if time data exists)
if 'created_at' in df.columns:
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['hour'] = df['created_at'].dt.hour
    
    plt.figure(figsize=(10, 6))
    hourly_engagement = df.groupby('hour')['retweet_count'].mean()
    sns.lineplot(x=hourly_engagement.index, y=hourly_engagement.values)
    plt.title('Average Retweet Count by Hour')
    plt.xlabel('Hour')
    plt.ylabel('Average Retweet Count')
    plt.show() 