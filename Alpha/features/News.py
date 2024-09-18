import pyttsx3
from newsapi import NewsApiClient

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    print(text)
    engine.runAndWait()

def get_news(category):
    newsapi = NewsApiClient(api_key='c559126b72764d3ab83d5ff14c82de64')

    top_headlines = newsapi.get_top_headlines(category=category, language='en', country='us')

    if top_headlines['totalResults'] > 0:
        news_summary = f"Here are the top {category} news headlines:\n"
        speak(news_summary)
        
        for article in top_headlines['articles'][:3]:
            news_item = (f"Title: {article['title']}.\n"
                         f"Description: {article['description']}\n")
            
            speak(news_item)
    else:
        no_news = f"Sorry, no news found for the category '{category}'."
        speak(no_news)

def latestNews(category_input):
    categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

    category = category_input.strip().lower()

    if category in categories:
        speak(f"\nFetching {category} news...\n")
        get_news(category)
    else:
        invalid_category_msg = (f"Invalid category. Please choose from the following options: "
                                f"{', '.join(categories)}.")
        speak(invalid_category_msg)