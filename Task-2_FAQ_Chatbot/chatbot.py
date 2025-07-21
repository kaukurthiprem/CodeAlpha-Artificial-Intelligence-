import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data (only once needed)
nltk.download('punkt')
nltk.download('stopwords')

# Define your FAQs
faq_pairs = {
    "what is ai": "AI stands for Artificial Intelligence.",
    "what is python": "Python is a programming language used widely in AI.",
    "what is machine learning": "Machine Learning is a subset of Artificial Intelligence.",
    "how does ai work": "AI works by learning from data and making decisions.",
    "what is nlp": "NLP stands for Natural Language Processing.",
    "who are you": "I am your FAQ chatbot.",
    "what can you do": "I can answer basic questions about AI."
}

# Prepare questions and answers
questions = list(faq_pairs.keys())
answers = list(faq_pairs.values())

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# Chat loop
print("Bot: Hello! Ask me something about AI (type 'exit' to quit).")

while True:
    user_input = input("You: ").lower().strip()
    
    if user_input in ['exit', 'quit', 'bye']:
        print("Bot: Goodbye!")
        break

    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)
    best_match_index = similarity.argmax()
    best_score = similarity[0, best_match_index]

    if best_score > 0.3:
        print("Bot:", answers[best_match_index])
    else:
        print("Bot: Sorry, I didn't understand that.")
