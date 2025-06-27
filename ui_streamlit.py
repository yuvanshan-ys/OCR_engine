import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import os
import shutil
from ocr_engine import extract_text
from link_extractor import extract_links
from auto_tagger import detect_category
from db import insert_record
from semantic_search import semantic_search

DB_PATH = "data/knowledge.db"
PROCESSED_DIR = "processed"

def get_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM knowledge ORDER BY created_at DESC", conn)
    conn.close()
    return df

def save_image(image_file):
    img_path = os.path.join("images", image_file.name)
    with open(img_path, "wb") as f:
        f.write(image_file.getbuffer())
    return img_path

def main():
    st.set_page_config(page_title="AI Knowledge Vault", layout="wide")
    st.title("AI Knowledge Vault Dashboard")

    #theme toggle 

    theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown(
            """
            <style>
            body { background-color: #1e1e1e; color: white; }
            .st-bw { background-color: #2c2c2c !important; color: white; }
            </style>
            """,
            unsafe_allow_html=True,
    )

    st.sidebar.header("Upload Screenshot")
    image_file = st.sidebar.file_uploader("Upload one or more image", type=["png", "jpg", "jpeg"], accept_multiple_files= True)

    if image_file:
        img_path = save_image(image_file)
        st.sidebar.image(Image.open(img_path), caption= image_file.name , use_column_width=True)

        with st.spinner(f"Extracting text from {image_file.name} ..."):
            try:
                text = extract_text(img_path)
                links = extract_links(text)
                category = detect_category(text)
                insert_record(image_file.name, text, links, category)

                shutil.move(img_path, os.path.join(PROCESSED_DIR, image_file.name))
                st.sidebar.success(f"{image_file.name} processed!")
            except Exception as e:
                st.sidebar.error(f"Error in {image_file.name}: {str(e)}")

    st.subheader("Semantic Search")
    user_query = st.text_input("Ask a question or describe a topic:")

    if user_query:
        results = semantic_search(user_query)
        st.markdown("### Top Matching Notes")
        for r in results:
            st.markdown(f"""
            **File**: `{r[1]}`
            **Category**: `{r[3]}`
            **Extracted Text**:  
            `{r[2][:300]}...`
            **Links**: {r[4]}
            **Created At**: {r[5]}
            ---
            """)


    st.subheader("Your Screenshot Notes")
    df = get_data()

    # Filter section
    search_text = st.text_input("Search text or keywords")
    filter_category = st.selectbox("Filter by Category", ["All"] + sorted(df["category"].unique().tolist()))

    # if filter_category != "All":
    #     df = df[df["category"] == filter_category]

    # if search_text:
    #     df = df[df["extracted_text"].str.contains(search_text, case=False)]
    with st.expander("Search & Filters"):
        col1, col2 = st.columns([2, 1])
        with col1:
            search_text = st.text_input("Search by keyword or content", placeholder="e.g. LLM, CAP theorem")
        with col2:
            filter_category = st.selectbox("Filter by Category", ["All"] + sorted(df["category"].unique().tolist()))

        if filter_category != "All":
            df = df[df["category"] == filter_category]

        if search_text:
            df = df[df["extracted_text"].str.contains(search_text, case=False)]


    # st.dataframe(df[["image_name", "category", "extracted_text", "links", "created_at"]], use_container_width=True)
    st.markdown("### All Notes")
    st.dataframe(
        df[["image_name", "category", "extracted_text", "links", "created_at"]],
        use_container_width=True,
        height=500
)


if __name__ == "__main__":
    main()
