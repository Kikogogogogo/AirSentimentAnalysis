# Airline Sentiment Analysis Dashboard

This project provides a web-based dashboard for analyzing sentiment in airline-related tweets. The dashboard visualizes various aspects of airline sentiment data to help understand customer feedback and identify areas for improvement.

## Features

1. **Overall Sentiment Distribution**
   - Interactive bar chart showing the distribution of positive, negative, and neutral sentiments
   - Real-time analysis of sentiment percentages
   - Helps understand general public perception of airlines
   - Identifies overall sentiment trends

2. **Negative Reason Analysis**
   - Detailed breakdown of specific reasons for negative feedback
   - Identifies key areas requiring improvement
   - Shows top negative reasons and their impact
   - Helps prioritize service improvement areas

3. **Airline-Specific Sentiment Analysis**
   - Interactive heatmap comparing sentiment across different airlines
   - Color-coded visualization (red for high frequency, blue for low frequency)
   - Enables performance comparison between airlines
   - Identifies best and worst performing airlines

4. **Word Cloud Visualization**
   - Visual representation of common terms in negative feedback
   - Size of words indicates frequency of occurrence
   - Helps identify recurring issues and themes
   - Provides quick visual summary of main concerns

## Dataset

The analysis is based on the Airline Sentiment dataset, which contains:
- Tweets about various airlines
- Sentiment classification (positive, negative, neutral)
- Airline names
- Negative reasons (for negative tweets)
- Confidence scores
- Timestamps and other metadata

## Technical Stack

- **Backend**: Python Flask
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Word Cloud**: WordCloud
- **Frontend**: Bootstrap 5
- **Additional Libraries**: TextBlob (for sentiment analysis)

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd airline-sentiment-analysis
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the dashboard:
   - Open your web browser
   - Navigate to `http://localhost:5000`

## Requirements

- Python 3.7+
- Flask
- Pandas
- Plotly
- WordCloud
- Bootstrap 5
- TextBlob
- Other dependencies listed in requirements.txt

## Usage

1. Start the application using the instructions above
2. Navigate to the dashboard at `http://localhost:5000`
3. View and analyze the visualizations:
   - Hover over charts for detailed information
   - Use interactive features to explore the data
   - Read analysis conclusions below each visualization
4. Use the insights to:
   - Understand customer sentiment patterns
   - Identify areas for improvement
   - Compare airline performance
   - Make data-driven decisions

## Contributing

We welcome contributions to this project! Here's how you can help:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

For bug reports or feature requests, please open an issue in the repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact:
- Email: kiko.zhao@mail.utoronto.ca
- GitHub: [Your GitHub Profile] 