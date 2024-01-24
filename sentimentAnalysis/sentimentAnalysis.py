import nltk
import json
import requests
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from nltk.corpus import sentiwordnet
from nltk.tokenize import word_tokenize
import pytesseract
from PIL import Image
import io
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

# data will be stored on analysis_classified_date and output to a json file
# analysis_classified_date will have structure of {Date:date : {Positive, Negative, Dayattitude} 

stock_name = "SPY"
image_analyse_activate = True

# download post sets from json file
with open(f"wallstreetbets_{stock_name}_posts_2022.json") as json_file:
    posts = json.load(json_file)

nltk.download('punkt')
nltk.download('sentiwordnet')
nltk.download('wordnet')
nltk.download('vader_lexicon')

posts_classified_date = {}
for user, post in posts.items():
    try:
        posts_classified_date[datetime.fromtimestamp(post["created_utc"]).date()].append((post["title"], post['url']))
    except:
        posts_classified_date[datetime.fromtimestamp(post["created_utc"]).date()] = [(post["title"], post['url'])]

# support functions for json output

def remove_first_last_line(s):
    lines = s.split('\n')
    lines = lines[1:-1]
    return '\n'.join(lines)

def add_json_boundaries(filename):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("{\n" + content)
        f.seek(0, 2)
        f.write("\n}")

# sentiment analysis support functions 

# sentiment analysis using sentiWordNet
def sentiWordNet_analysis(text):
    words = word_tokenize(text)
    pos_score = neg_score = obj_score = 0
    for word in words:
        synsets = list(sentiwordnet.senti_synsets(word))
        if synsets:
            # Take the first synset only, as it represents the most common usage of the word
            synset = synsets[0]
            pos_score += synset.pos_score()
            neg_score += synset.neg_score()
            obj_score += synset.obj_score()
    # Calculate the final sentiment score
    if pos_score > neg_score:
        return pos_score
    elif pos_score < neg_score:
        return 0 - neg_score
    else:
        return 0

# sentiment analysis using vadar
def vader_analysis(text):
    vader = SentimentIntensityAnalyzer()
    sentiment_scores_vader = vader.polarity_scores(text)
    return sentiment_scores_vader['compound']

# sentiment analysis using textblob
def textblob_analysis(text):
    blob = TextBlob(text)
    sentiment_scores_textblob = blob.sentiment
    return sentiment_scores_textblob.polarity

# helper function for images to text input
def image_to_text(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))

    # Extract text from the image using pytesseract
    text = pytesseract.image_to_string(img)
    return text

# call to perform three analysis and combined them to three outputs Positive, Negetive, OverallAttitude
def comboAnalysis(post):
    positive = 0
    negative = 0
    for i in post:
        sentiment_score = (sentiWordNet_analysis(i[0]) + textblob_analysis(i[0]) + vader_analysis(i[0])) / 3 # average the sum of three analysis
        # image analysis perform only when image analysis is activated and there is a associated URL
        if image_analyse_activate and i[1] != None:
            file_type = i[1].split('.')[-1]
            if file_type == "jpg" or file_type == 'png': # only look for url leads to a picture
                img_text = image_to_text(i[1])
                if img_text.split(" ")[-1] == "deleted." and img_text.split(" ")[-2] == "probably": # make sure image is not reddit default error picture indicate user deleted picture
                    img_senti_score = (sentiWordNet_analysis(i[1]) + textblob_analysis(i[1]) + vader_analysis(i[1])) # average the sum of three analysis
                    sentiment_score += img_senti_score
        if sentiment_score < 0:
            negative += 1
        elif sentiment_score > 0:
            positive += 1
        else:
            pass

    if positive > negative:
        overallAttitude = 'positive'
    elif negative > positive:
        overallAttitude = 'negative'
    else:
        overallAttitude = 'neutual'
    return positive, negative, overallAttitude


analysis_classified_date = {} # dictionary hold value of date: {Int:positive, Int:negative, "Positive"/"Negative"/"Neutural": DayAttitude}
count = 0 # number to keep track of the progress of analysis
for date in posts_classified_date.keys():
    positive, negative, dayAttitude = comboAnalysis(posts_classified_date[date])
    analysis_classified_date[date] = {'positive': positive, 'negative': negative, 'dayAttitude': dayAttitude}
    print(f"{count} day completed")
    count += 1

# convert data to json file output
filename = f'sentiment_analysis_wallstreetbets_{stock_name}_posts_2022.json'
for date, data in analysis_classified_date.items():
    with open(filename, 'a') as f:
        toAdd = json.dumps({date.strftime('%Y-%m-%d') : data}, indent=2, cls=json.JSONEncoder)
        toAdd = remove_first_last_line(toAdd)
        f.write(toAdd)
        f.write(',')
add_json_boundaries(filename)