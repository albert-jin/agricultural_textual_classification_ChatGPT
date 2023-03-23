import openai
import requests
import streamlit as st
from bs4 import BeautifulSoup
from newspaper import Article
import nltk

nltk.download('punkt')

# Use your OpenAI API key to access GPT-3
openai.api_key = st.secrets["openai_api_key"]


# Write a function to extract an article's content from a page
def extract_article_content(url):
    # Send an HTTP GET request to the page
    page = requests.get(url)

    # Parse the page's HTML content
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract the article's text from the page
    article_text = soup.find(class_="article-text")
    if article_text is not None:
        article_text = article_text.get_text()
    else:
        article_text = "Unable to extract article text."

    return article_text


# Use Streamlit to build the web app
st.title("News Classification App")

# Add a text input field for the user to enter an article link
article_link = st.text_input("Enter a news article link:")

# Add a button for the user to submit the link for classification
if st.button("Classify"):
    # Extract the article's content from the page
    article = Article(article_link)
    article.download()
    article.parse()
    article.nlp()
    article_text = article.summary[0:200]
    # article_text = extract_article_content(article_link)
    st.subheader("Link")
    st.write(article_link)
    st.subheader("Summary")
    st.write(article_text)

    # Create a completion object for GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"The following is an article and the categories it falls into: {article_text} Category: \n\n",
        temperature=0,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )

    # Use GPT-3 to classify the article
    classification = response.choices[0]["text"]

    # Display the classification to the user
    st.subheader("Predicted Category")
    st.success(f"Predicted categories: {classification}")