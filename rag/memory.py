# memory.py
from typing import Optional, List
from backend.user_database import SessionLocal, Conversation, SearchHistory, User
import datetime


class DBMemory:
    """
    Per-user memory stored in DB.
    - When a user logs in, load their last N conversation turns.
    - Save each new turn to DB.
    - Also store search history entries.
    """

    def __init__(self, window: int = 8):
        self.window = window

    def append_turn(self, user_id: int, role: str, content: str):
        db = SessionLocal()
        try:
            conv = Conversation(user_id=user_id, role=role, content=content, ts=datetime.datetime.now(datetime.timezone.utc))
            db.add(conv)
            db.commit()
        finally:
            db.close()

    def get_recent(self, user_id: int) -> List[dict]:
        db = SessionLocal()
        try:
            rows = db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.ts.desc()).limit(self.window).all()
            # return in chronological order
            return [{"role": r.role, "content": r.content, "ts": r.ts.isoformat()} for r in reversed(rows)]
        finally:
            db.close()

    def clear_user(self, user_id: int):
        db = SessionLocal()
        try:
            db.query(Conversation).filter(Conversation.user_id == user_id).delete()
            db.commit()
        finally:
            db.close()

    # Search history helpers
    def append_search(self, user_id: int, query: str, snippet: str = None):
        db = SessionLocal()
        try:
            sh = SearchHistory(user_id=user_id, query=query, result_snippet=snippet, ts=datetime.datetime.now(datetime.timezone.utc))
            db.add(sh)
            db.commit()
        finally:
            db.close()

    def get_search_history(self, user_id: int, limit=20):
        db = SessionLocal()
        try:
            rows = db.query(SearchHistory).filter(SearchHistory.user_id == user_id).order_by(SearchHistory.ts.desc()).limit(limit).all()
            return [{"query": r.query, "snippet": r.result_snippet, "ts": r.ts.isoformat()} for r in rows]
        finally:
            db.close()

    def combined_context(self, user_id: int) -> str:
        """
        Combine recent conversation and search history into a compact string for prompts.
        """
        convs = self.get_recent(user_id)
        searches = self.get_search_history(user_id, limit=10)
        s = []
        if convs:
            s.append("Conversation history (recent):")
            for c in convs:
                s.append(f"{c['role']}: {c['content']}")
        if searches:
            s.append("\nRecent searches:")
            for srow in searches:
                s.append(f"- {srow['query']} (snippet: {srow['snippet']})")
        return "\n".join(s)


