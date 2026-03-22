import streamlit as st
import requests

# 🔴 PUT YOUR AZURE DETAILS HERE
AZURE_KEY = "FALSE"
AZURE_ENDPOINT = "https://cognitiveservices.azure.com/"

# -----------------------------
# Rule-based chatbot
# -----------------------------
def rule_based_response(user_input):
    text = user_input.lower()

    if "hi" in text or "hello" in text:
        return "Hello! How can I help you today?"
    elif "help" in text:
        return "I can help with hours, location, and services."
    elif "hours" in text:
        return "We are open from 9 AM to 5 PM."
    elif "location" in text:
        return "We are located in Dallas, Texas."
    elif "services" in text:
        return "We provide support and information services."
    elif "bye" in text:
        return "Goodbye!"
    else:
        return None

# -----------------------------
# Azure Sentiment
# -----------------------------
def analyze_sentiment(text):
    url = f"{AZURE_ENDPOINT}language/:analyze-text?api-version=2023-04-01"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "kind": "SentimentAnalysis",
        "analysisInput": {
            "documents": [{
                "id": "1",
                "language": "en",
                "text": text
            }]
        }
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    return data["results"]["documents"][0]["sentiment"]

# -----------------------------
# Azure Key Phrases
# -----------------------------
def extract_key_phrases(text):
    url = f"{AZURE_ENDPOINT}language/:analyze-text?api-version=2023-04-01"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "kind": "KeyPhraseExtraction",
        "analysisInput": {
            "documents": [{
                "id": "1",
                "language": "en",
                "text": text
            }]
        }
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    return data["results"]["documents"][0]["keyPhrases"]

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🤖 Azure AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Try rule-based first
    response = rule_based_response(user_input)

    if response:
        bot_reply = response
    else:
        try:
            sentiment = analyze_sentiment(user_input)
            key_phrases = extract_key_phrases(user_input)

            bot_reply = f"""I used Azure AI to analyze your input.

Sentiment: {sentiment}
Key Topics: {', '.join(key_phrases)}
"""
        except Exception as e:
            bot_reply = f"Azure AI error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)
