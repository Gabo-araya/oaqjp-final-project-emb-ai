"""
This module implements a Flask server for emotion detection in text.
It provides endpoints for analyzing emotions in text inputs.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detection")

@app.route("/emotionDetector")
def sent_analysis():
    """
    Analyze the emotions in the provided text.
    Returns formatted string with emotion scores and dominant emotion.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')

    # Pass the text to the emotion_detector function and store the response
    response = emotion_detector(text_to_analyze)

    # Check if response contains None values
    if response['dominant_emotion'] is None:
        result = "Invalid text! Please try again! (no dominant_emotion)"
        return result

    # Extract the emotions from the response
    anger = response['anger']
    disgust = response['disgust']
    fear = response['fear']
    joy = response['joy']
    sadness = response['sadness']
    dominant_emotion = response['dominant_emotion']

    # Format the result string
    result = (
            f"For the given statement, the system response is 'anger': {anger}, "
            f"'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} and 'sadness': "
            f"{sadness}. The dominant emotion is {dominant_emotion}."
        )

    # Return a formatted string
    return result


@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
    '''

    return render_template('index.html')

if __name__ == "__main__":
    # This functions executes the flask app and deploys it on localhost:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
