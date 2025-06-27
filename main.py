import os
from ocr_engine import extract_text
from link_extractor import extract_links
from db import init_db, insert_record
import shutil
from auto_tagger import detect_category


IMAGES_DIR = "images"
PROCESSED_DIR = "processed"

def process_images():
    
    init_db()
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    for image_name in os.listdir(IMAGES_DIR):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(IMAGES_DIR, image_name)
            print(f" Processing {image_name}...")

            try:
                text = extract_text(img_path)
                links = extract_links(text)
                category = detect_category(text)
                insert_record(image_name, text, links, category)
                

                shutil.move(img_path, os.path.join(PROCESSED_DIR, image_name))
                print(f" Saved: {image_name} | Links: {links}")
            except Exception as e:
                print(f" Error processing {image_name}: {e}")

if __name__ == "__main__":
    process_images()
