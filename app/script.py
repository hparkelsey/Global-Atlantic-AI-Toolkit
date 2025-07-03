from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required data
nltk.download('vader_lexicon')
nltk.download('punkt')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    print("Received data:", data)
    
    text = data.get('text', '')
    keyword_string = data.get('keywords', '').strip()

    if not text:
        return jsonify({'error': 'Text is required'}), 400

    keywords = [kw.strip().lower() for kw in keyword_string.split(',') if kw.strip()]
    sia = SentimentIntensityAnalyzer()
    sentences = nltk.sent_tokenize(text)

    results = {}

    # No keywords: general summary
    if not keywords:
        sentiment_scores = [sia.polarity_scores(s) for s in sentences]
        avg_scores = average_sentiment_scores(sentiment_scores) if sentiment_scores else None

        results["general"] = {
            'sentiment_scores': sentiment_scores,
            'avg_scores': avg_scores,
            'relevant_sentences': sentences,
            'summary': generate_summary(sentences)
        }
    else:
        for keyword in keywords:
            relevant_sentences = [s for s in sentences if keyword in s.lower()]
            sentiment_scores = [sia.polarity_scores(s) for s in relevant_sentences]
            avg_scores = average_sentiment_scores(sentiment_scores) if sentiment_scores else None

            results[keyword] = {
                'sentiment_scores': sentiment_scores,
                'avg_scores': avg_scores,
                'relevant_sentences': relevant_sentences,
                'summary': generate_summary(relevant_sentences)
            }

    return jsonify(results)

def average_sentiment_scores(sentiment_scores):
    if not sentiment_scores:
        return None

    return {
        'neg': sum(s['neg'] for s in sentiment_scores) / len(sentiment_scores),
        'neu': sum(s['neu'] for s in sentiment_scores) / len(sentiment_scores),
        'pos': sum(s['pos'] for s in sentiment_scores) / len(sentiment_scores),
        'compound': sum(s['compound'] for s in sentiment_scores) / len(sentiment_scores)
    }

def generate_summary(sentences, max_sentences=3):
    if not sentences:
        return []

    sia = SentimentIntensityAnalyzer()
    scored = [(s, abs(sia.polarity_scores(s)['compound'])) for s in sentences]
    sorted_scored = sorted(scored, key=lambda x: x[1], reverse=True)
    top_sentences = [s for s, _ in sorted_scored[:max_sentences]]
    return top_sentences

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from nltk.sentiment import SentimentIntensityAnalyzer
# import nltk
# import socket

# nltk.download('vader_lexicon')
# nltk.download('punkt')

# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

# try:
#     nltk.data.find('tokenizers/punkt_tab')
# except LookupError:
#     nltk.download('punkt_tab')

# app = Flask(__name__)
# CORS(app)

# @app.route('/analyze', methods=['POST'])
# def analyze_sentiment():
#     data = request.json
#     print("Received data:", data)
    
#     text = data.get('text', '')
#     keyword_string = data.get('keywords', '').strip()

#     if not text:
#         return jsonify({'error': 'Text is required'}), 400

#     keywords = [kw.strip().lower() for kw in keyword_string.split(',') if kw.strip()]
#     sia = SentimentIntensityAnalyzer()
#     sentences = nltk.sent_tokenize(text)

#     results = {}

#     # If no keywords are given, analyze the whole text
#     if not keywords:
#         print("No keywords provided. Running general sentiment analysis.")
#         sentiment_scores = [sia.polarity_scores(sentence) for sentence in sentences]
#         avg_scores = average_sentiment_scores(sentiment_scores) if sentiment_scores else None

#         results["general"] = {
#             'sentiment_scores': sentiment_scores,
#             'avg_scores': avg_scores,
#             'relevant_sentences': sentences  # all sentences
#         }

#     else:
#         # Analyze per keyword
#         for keyword in keywords:
#             print("Processing keyword:", keyword)
#             relevant_sentences = [sentence for sentence in sentences if keyword in sentence.lower()]
#             sentiment_scores = [sia.polarity_scores(sentence) for sentence in relevant_sentences]
#             avg_scores = average_sentiment_scores(sentiment_scores) if sentiment_scores else None

#             results[keyword] = {
#                 'sentiment_scores': sentiment_scores,
#                 'avg_scores': avg_scores,
#                 'relevant_sentences': relevant_sentences
#             }

#     print("Final results:", results)
#     return jsonify(results)


# def average_sentiment_scores(sentiment_scores):
#     if not sentiment_scores:
#         return None

#     avg_scores = {
#         'neg': sum(score['neg'] for score in sentiment_scores) / len(sentiment_scores),
#         'neu': sum(score['neu'] for score in sentiment_scores) / len(sentiment_scores),
#         'pos': sum(score['pos'] for score in sentiment_scores) / len(sentiment_scores),
#         'compound': sum(score['compound'] for score in sentiment_scores) / len(sentiment_scores)
#     }

#     return avg_scores

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)


#  LOG  [web] Logs will appear in the browser console
# 127.0.0.1 - - [12/Aug/2024 17:40:48] "OPTIONS /analyze HTTP/1.1" 200 -
# 127.0.0.1 - - [12/Aug/2024 17:40:48] "POST /analyze HTTP/1.1" 500 -
# Traceback (most recent call last):
#   File "C:\Users\hoyun\AppData\Local\Programs\Python\Python312\Lib\site-packages\flask\app.py", line 1498, in __call__
#     return self.wsgi_app(environ, start_response)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\hoyun\AppData\Local\Programs\Python\Python312\Lib\site-packages\flask\app.py", line 1476, in wsgi_app
#     response = self.handle_exception(e)
#                ^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\hoyun\AppData\Local\Programs\Python\Python312\Lib\site-packages\flask_cors\extension.py", line 178, in wrapped_function
#     return cors_after_request(app.make_response(f(*args, **kwargs)))
#                                                 ^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\hoyun\AppData\Local\Programs\Python\Python312\Lib\site-packages\flask\app.py", line 1473, in wsgi_app
#     response = self.full_dispatch_request()
#                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\hoyun\AppData\Local\Programs\Python\Python312\Lib\site-packages\flask\app.py", line 882, in full_dispatch_request
#     rv = self.handle_user_exception(e)
#          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\hoyun\AppData\Local\Programs\Python\Python312\Lib\site-packages\flask_cors\extension.py", line 178, in wrapped_function
#     return cors_after_request(app.make_response(f(*args, **kwargs)))
#                                                 ^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\hoyun\AppData\Local\Programs\Python\Python312\Lib\site-packages\flask\app.py", line 880, in full_dispatch_request
#     rv = self.dispatch_request()
#          ^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\hoyun\AppData\Local\Programs\Python\Python312\Lib\site-packages\flask\app.py", line 865, in dispatch_request
#     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\hoyun\Downloads\CLSentimentAnalysis\CLSA-vF\app\script.py", line 17, in analyze_sentiment
#     subject = data.get('subject').lower()
#               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
# AttributeError: 'NoneType' object has no attribute 'lower'
#  * Detected change in 'C:\\Users\\hoyun\\Downloads\\CLSentimentAnalysis\\CLSA-vF\\app\\script.py', reloading
#  * Restarting with stat