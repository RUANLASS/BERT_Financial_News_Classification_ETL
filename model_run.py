import streamlit as st
import torch
import sqlite3
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification

# -----------------------------
# Label Map
# -----------------------------
label_map = {
    0: "Analyst Update",
    1: "Fed | Central Banks",
    2: "Company | Product News",
    3: "Treasuries | Corporate Debt",
    4: "Dividend",
    5: "Earnings",
    6: "Energy | Oil",
    7: "Financials",
    8: "Currencies",
    9: "General News | Opinion",
    10: "Gold | Metals | Materials",
    11: "IPO",
    12: "Legal | Regulation",
    13: "M&A | Investments",
    14: "Macro",
    15: "Markets",
    16: "Politics",
    17: "Personnel Change",
    18: "Stock Commentary",
    19: "Stock Movement"
}

# -----------------------------
# Load model + tokenizer
# -----------------------------
@st.cache_resource
def load_model():
    model_path = "RUANLASS/bert-finance-model"
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    return model, tokenizer

model, tokenizer = load_model()

def predict(text: str) -> str:
    """Classify a single headline."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    pred_id = torch.argmax(outputs.logits, dim=1).item()
    return label_map[pred_id]

# -----------------------------
# Load news from SQLite
# -----------------------------
def load_news_from_db(limit: int = 200):
    conn = sqlite3.connect("news.db")
    df = pd.read_sql(
        f"SELECT title, link, published FROM news ORDER BY published DESC LIMIT {limit}",
        conn
    )
    conn.close()
    return df

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("📊 Financial News Classification Dashboard")

# Manual input
headline = st.text_input("Enter a financial headline:")
if headline:
    pred = predict(headline)
    st.write("Predicted class:", pred)

# Classify headlines from DB
st.header("📰 Classify Latest News from Database")
if st.button("Run Classification"):
    df = load_news_from_db(limit=200)

    # Add prediction column
    df["predicted_topic"] = df["title"].apply(predict)

    # Show grouped results
    for topic in sorted(df["predicted_topic"].unique()):
        st.subheader(f"📌 {topic}")
        topic_df = df[df["predicted_topic"] == topic]

        for _, row in topic_df.iterrows():
            st.markdown(
                f"- [{row['title']}]({row['link']})  \n"
                f"<small>{row['published']}</small>",
                unsafe_allow_html=True
            )
