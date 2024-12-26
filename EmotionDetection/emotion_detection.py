#emotion_detection.py

import requests
import json

def emotion_detector(text_to_analyse):
    if not text_to_analyse or text_to_analyse.strip() == "":
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # URL of the sentiment analysis service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    # Constructing the request payload in the expected format
    json_input = { "raw_document": { "text": text_to_analyse } }
    # Custom header specifying the model ID for the sentiment analysis service
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    try:
        # Sending a POST request to the sentiment analysis API
        response = requests.post(url, json=json_input, headers=header)

        # Parsing the JSON response from the API
        formatted_response = json.loads(response.text)

        # print(f"response.status_code = {response.status_code}")

        # Check for bad request
        if response.status_code == 400:
            result = {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }

            return result

        if response.status_code == 200:
            # Extracting emotion scores
            emotions = formatted_response['emotionPredictions'][0]['emotion']
            
            # Creating the result dictionary with emotion scores
            result = {
                'anger': emotions['anger'],
                'disgust': emotions['disgust'],
                'fear': emotions['fear'],
                'joy': emotions['joy'],
                'sadness': emotions['sadness']
            }
            
            # Finding the dominant emotion (emotion with highest score)
            dominant_emotion = max(result.items(), key=lambda x: x[1])[0]
            result['dominant_emotion'] = dominant_emotion
        
            return result
        
    # except requests.exceptions.RequestException as e:
    #     print(f"Error making the request: {e}")
    #     return None
    # except (KeyError, json.JSONDecodeError) as e:
    #     print(f"Error processing the response: {e}")
    #     return None
    except Exception:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }