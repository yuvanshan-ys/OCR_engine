from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

model = SentenceTransformer("all-MiniLM-L6-v2") 

def fetch_notes():
    conn = sqlite3.connect("data/knowledge.db")
    c = conn.cursor()
    c.execute("SELECT id, image_name, extracted_text, category, links, created_at FROM knowledge")
    rows = c.fetchall()
    conn.close()
    return rows

def semantic_search(user_query, top_k=5):
    data = fetch_notes()
    texts = [row[2] for row in data]

    query_emb = model.encode([user_query])
    text_embs = model.encode(texts)

    scores = cosine_similarity(query_emb, text_embs)[0]
    top_indices = scores.argsort()[::-1][:top_k]

    results = [data[i] for i in top_indices]
    return results
