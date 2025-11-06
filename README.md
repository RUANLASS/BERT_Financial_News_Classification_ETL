## BERT Financial News Classification ETL

This project demonstrates an end-to-end ETL pipeline and NLP classification system for financial news, designed with a strong focus on scalability, automation, and deployment-readiness.

It highlights my ability to:
- Build production-grade ETL pipelines using Prefect
- Deploy and serve Hugging Face Transformer models via Streamlit
- Integrate modern MLOps practices (caching, orchestration, version control).

Project Overview
- Training: Fine-tuned a pretrained Hugging-Face BERT model on Google Colab using the [financial news topic](https://huggingface.co/datasets/zeroshot/twitter-financial-news-topic) dataset
- Extract: Collect financial news data from multiple sources (e.g., RSS feeds, APIs).
- Transform: Preprocess text (tokenization, cleaning, batching).
- Load: Persist structured outputs into a database for downstream tasks.
- Serve
  - Interactive Streamlit UI where users can:
  - View recent news headlines.
  - Run them through the trained BERT classifier.
  - Explore classification labels like Analyst Update, Fed | Central Banks, Company | Product News, Treasuries, etc.

Tech Stack:
- Language: Python
- Modeling: Transformers (Hugging Face)
- Orchestration: Prefect 2.0
- UI: Streamlit
- Data Storage: SQLite
- Version Control: Git 

Project Structure
BERT_Finance/  <br />
│── prefect_flows/      # ETL pipelines (Prefect flows) <br />
│── bert-finance-model/   # (ignored in repo, hosted on Hugging Face Hub) <br />
│── model_run.py         # Streamlit app entry point <br />
│── requirements.txt      # Dependencies <br />
│── README.md           # Project documentation <br />

Running the Project
1. Clone the repo: 
  git clone https://github.com/RUANLASS/BERT_Financial_News_Classification_ETL.git
  cd BERT_Finance
2. Install dependencies
  pip install -r requirements.txt

3. Run Prefect ETL pipeline
  prefect deployment run etl-flow/etl-deployment

4. Run Streamlit app
  streamlit run model_run.py

The fine-tuned model is hosted on Hugging Face Hub:
https://huggingface.co/lakshyasarin/bert-finance-model

Key Takeaways 
- MLOps and Automation: Implemented Prefect flows for scheduled ETL runs.
- Scalable Deployment: Streamlit UI integrated with Hugging Face Hub.

Next Steps:
- Extend classification to sentiment analysis (positive/negative/neutral).
- Add Docker containerization for easier deployment.
- Integrate with real-time news APIs.

