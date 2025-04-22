from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import base64
from io import BytesIO
import numpy as np
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_wordcloud(texts, title):
    try:
        # Ensure text data is not empty
        if not texts or len(texts) == 0:
            logger.warning(f"Word cloud data is empty: {title}")
            return None
        
        # Filter out empty strings
        texts = [text for text in texts if text and isinstance(text, str)]
        
        if not texts:
            logger.warning(f"Word cloud data is empty after filtering: {title}")
            return None
            
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(texts))
        img = BytesIO()
        wordcloud.to_image().save(img, format='PNG')
        return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
    except Exception as e:
        logger.error(f"Error generating word cloud: {str(e)}")
        return None

@app.route('/')
def index():
    try:
        # Check if data file exists
        data_path = os.path.join('data', 'processed_tweets.csv')
        if not os.path.exists(data_path):
            logger.error(f"Data file does not exist: {data_path}")
            return render_template('error.html', error_message="Data file does not exist")
            
        # Read data
        df = pd.read_csv(data_path)
        logger.info(f"Successfully read data file, total {len(df)} rows")
        
        # Check if required columns exist
        required_columns = ['airline_sentiment', 'airline']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logger.error(f"Data file missing required columns: {missing_columns}")
            return render_template('error.html', error_message=f"Data file missing required columns: {', '.join(missing_columns)}")
            
        # 1. Airline sentiment analysis
        sentiment_counts = df['airline_sentiment'].value_counts()
        fig1 = px.bar(x=sentiment_counts.index, y=sentiment_counts.values,
                     title='Airline Sentiment Analysis',
                     labels={'x': 'Sentiment', 'y': 'Count'})
        
        # Add analysis conclusion for sentiment distribution
        sentiment_analysis = {
            'title': 'Sentiment Distribution Analysis',
            'conclusion': f"""
            <div class="analysis-conclusion">
                <h4>Key Findings:</h4>
                <ul>
                    <li>Overall sentiment distribution shows {sentiment_counts['positive']/len(df)*100:.1f}% positive, {sentiment_counts['negative']/len(df)*100:.1f}% negative, and {sentiment_counts['neutral']/len(df)*100:.1f}% neutral sentiments</li>
                    <li>Negative sentiments are significantly higher than positive ones, indicating potential areas for improvement in airline services</li>
                    <li>The high proportion of neutral sentiments suggests room for enhancing customer engagement</li>
                </ul>
            </div>
            """
        }
        
        # 2. Airline negative reason analysis
        if 'negativereason' in df.columns:
            reason_counts = df['negativereason'].value_counts()
            fig2 = px.bar(x=reason_counts.index, y=reason_counts.values,
                         title='Negative Reason Analysis',
                         labels={'x': 'Reason', 'y': 'Count'})
            
            # Add analysis conclusion for negative reasons
            top_reason = reason_counts.index[0]
            top_reason_count = reason_counts.iloc[0]
            negative_analysis = {
                'title': 'Negative Feedback Analysis',
                'conclusion': f"""
                <div class="analysis-conclusion">
                    <h4>Key Findings:</h4>
                    <ul>
                        <li>The most common negative reason is "{top_reason}", accounting for {top_reason_count/len(df[df['airline_sentiment'] == 'negative'])*100:.1f}% of all negative feedback</li>
                        <li>Top 3 negative reasons account for {sum(reason_counts.iloc[:3])/len(df[df['airline_sentiment'] == 'negative'])*100:.1f}% of all negative feedback</li>
                        <li>This analysis helps identify priority areas for service improvement</li>
                    </ul>
                </div>
                """
            }
        else:
            logger.warning("negativereason column does not exist")
            fig2 = px.bar(x=['No data'], y=[0], title='No negative reason data')
            negative_analysis = {'conclusion': ''}
        
        # 3. Airline sentiment distribution
        if 'airline' in df.columns and 'airline_sentiment' in df.columns:
            airline_sentiment = pd.crosstab(df['airline'], df['airline_sentiment'])
            fig3 = px.imshow(airline_sentiment,
                            title='Airline Sentiment Distribution',
                            color_continuous_scale='RdBu')
            
            # Add analysis conclusion for airline-specific sentiment
            best_airline = airline_sentiment['positive'].idxmax()
            worst_airline = airline_sentiment['negative'].idxmax()
            airline_analysis = {
                'title': 'Airline Performance Analysis',
                'conclusion': f"""
                <div class="analysis-conclusion">
                    <h4>Key Findings:</h4>
                    <ul>
                        <li>{best_airline} has the highest proportion of positive sentiments ({airline_sentiment.loc[best_airline, 'positive']/airline_sentiment.loc[best_airline].sum()*100:.1f}%)</li>
                        <li>{worst_airline} has the highest proportion of negative sentiments ({airline_sentiment.loc[worst_airline, 'negative']/airline_sentiment.loc[worst_airline].sum()*100:.1f}%)</li>
                        <li>This analysis helps identify best practices and areas needing improvement across different airlines</li>
                    </ul>
                </div>
                """
            }
        else:
            logger.warning("airline or airline_sentiment column does not exist")
            fig3 = px.imshow(pd.DataFrame([[0]]), title='No airline sentiment data')
            airline_analysis = {'conclusion': ''}
        
        # 4. Word cloud (using negative reason text)
        if 'negativereason' in df.columns:
            wordcloud = create_wordcloud(
                df['negativereason'].dropna(),
                'Negative Reason Keywords'
            )
        else:
            logger.warning("negativereason column does not exist, cannot generate word cloud")
            wordcloud = None
        
        return render_template('index.html',
                             plot1=fig1.to_html(),
                             plot2=fig2.to_html(),
                             plot3=fig3.to_html(),
                             wordcloud=wordcloud,
                             sentiment_analysis=sentiment_analysis['conclusion'],
                             negative_analysis=negative_analysis['conclusion'],
                             airline_analysis=airline_analysis['conclusion'])
                             
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return render_template('error.html', error_message=f"Error processing request: {str(e)}")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message='Page not found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='Internal server error'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error_message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True) 