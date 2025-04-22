import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def generate_wordcloud(texts, title, output_path=None):
    """
    Generate a word cloud visualization
    
    Args:
        texts: List of texts
        title: Chart title
        output_path: Output file path (optional)
    """
    # Combine all texts
    combined_text = ' '.join(texts)
    
    # Create word cloud object
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        max_words=100,
        max_font_size=100
    ).generate(combined_text)
    
    # Draw word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')
    
    # Save or display
    if output_path:
        plt.savefig(output_path)
    else:
        plt.show()
    
    plt.close()

if __name__ == '__main__':
    # Read data
    df = pd.read_csv('data/tweets_sample.csv')
    
    # Generate word clouds for misinformation and non-misinformation tweets separately
    misinfo_texts = df[df['is_misinformation'] == 1]['text']
    non_misinfo_texts = df[df['is_misinformation'] == 0]['text']
    
    # Generate word clouds
    generate_wordcloud(misinfo_texts, 'Misinformation Keywords', 'misinfo_wordcloud.png')
    generate_wordcloud(non_misinfo_texts, 'Non-Misinformation Keywords', 'non_misinfo_wordcloud.png') 