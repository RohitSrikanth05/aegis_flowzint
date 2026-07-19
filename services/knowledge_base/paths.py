import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# services/knowledge_base -> services -> project root
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

DB_PATH = os.path.join(PROJECT_ROOT, "db", "chroma")
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "shopnova_data.json")
