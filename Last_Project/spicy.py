import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import nltk
from nltk.corpus import stopwords
import re
import json
import time
import spacy

# Make sure you run this once to download stopwords
nltk.download('stopwords')

ENGLISH_STOPWORDS = set(stopwords.words('english'))

# Load spaCy model for NER and POS tagging
nlp = spacy.load("en_core_web_sm")

# Gemini API setup (replace with your own API key)
import google.generativeai as genai
GEMINI_API_KEY = ''
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- Utilities ----------
def clean_visible_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    all_texts = soup.stripped_strings  # Generator of all text with whitespace stripped
    return ' '.join(all_texts)

def filter_using_ner_and_pos(text):
    """Filter text using NER and POS tagging to preserve relevant data."""
    doc = nlp(text)
    filtered_words = []

    # Keep entities (like PERSON, ORGANIZATION, etc.) and important POS (like nouns, proper nouns, numbers)
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN', 'NUM', 'ADJ'] or token.ent_type_:
            filtered_words.append(token.text)

    return ' '.join(filtered_words)

def remove_stopwords(text):
    words = re.findall(r"\b\w+\b", text.lower())
    filtered_words = [w for w in words if w not in ENGLISH_STOPWORDS and len(w) > 2]
    return ' '.join(filtered_words)

def call_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# ---------- Core Logic ----------
def process_single_url(url):
    print(f"Processing: {url}")
    response = requests.get(url, timeout=10)
    cleaned_text = clean_visible_text(response.text)
    filtered_text = filter_using_ner_and_pos(cleaned_text)

    prompt = f"""
    Here is the cleaned and filtered visible text content from a website:
    {filtered_text}

    Please analyze this content and extract all meaningful data points.
    Present them in JSON format with clearly labeled fields.
    you cannot produce content that is not in the text.
    """
    result = call_gemini(prompt)
    #result = 0

    print("-----") 
    print("Filtered Text:")
    print("-----")
    print(filtered_text)
    listu = [i for i in filtered_text.split()]
    print(f"Word count (before set): {len(listu)}")
    
    setu = set(listu)
    print(f"Unique words count: {len(setu)}")
    print("-----")
    print("Unique Set:")
    print(setu)
    print("-----")
    print("Result from AI:")
    print(result)
    print("-----")

    return result

def deduplicate_links_with_ai(urls):
    prompt = f"""
    I have these website URLs:
    {chr(10).join(urls)}

    Please return only the most distinct URLs by checking semantic similarity. Avoid near duplicates or versions of the same page.
    Return in list format.
    """
    result = call_gemini(prompt)
    print("\n===== Distinct URLs According to AI =====")
    print(result)
    return extract_urls_from_text(result)

def extract_urls_from_text(text):
    return list(set(re.findall(r'https?://\S+', text)))

def process_multiple_urls(urls):
    distinct_urls = deduplicate_links_with_ai(urls)
    print("\nProceeding with scraping from filtered distinct URLs...\n")
    unique_data_set = set()

    for url in distinct_urls:
        try:
            response = requests.get(url, timeout=10)
            cleaned_text = clean_visible_text(response.text)
            filtered_text = filter_using_ner_and_pos(cleaned_text)
            unique_data_set.update(filtered_text.split())
            time.sleep(1)
        except Exception as e:
            print(f"Failed to process {url}: {e}")

    combined_text = ' '.join(unique_data_set)
    prompt = f"""
    This is a merged and cleaned text from multiple unique websites:
    {combined_text}

    Please extract and display the most relevant data points from it in a structured JSON format.
    """
    result = call_gemini(prompt)
    print("\n===== Combined Data Points from All URLs =====")
    print(result)
    return result

# ---------- Main ----------
def main():
    mode = input("Choose mode: 1 - Single URL | 2 - Multiple URLs: ")

    if mode == '1':
        url = input("Enter the URL: ").strip()
        process_single_url(url)

    elif mode == '2':
        links_input = input("Enter multiple URLs separated by commas: ")
        urls = [url.strip() for url in links_input.split(',') if url.strip()]
        process_multiple_urls(urls)

    else:
        print("Invalid option. Please select 1 or 2.")

if __name__ == '__main__':
    main()
