# services/knowledge_base/gap_logger.py
from utils.database import log_gap_db


async def log_gap(question, retrieved_context, confidence):
    """Log a knowledge gap to the persistent database."""
    return log_gap_db(question, retrieved_context, confidence)