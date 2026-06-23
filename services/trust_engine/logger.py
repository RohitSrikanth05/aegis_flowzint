"""Event logging for trust engine decisions."""

from datetime import datetime
from typing import Optional


class TrustLogger:
    """Logs trust-related events with timestamps and session context."""

    def __init__(self):
        """Initialize the logger with an in-memory event store."""
        self.events = []

    def log_threat_detection(
        self,
        session_id: str,
        message: str,
        threats_detected: list[str],
        score_before: int,
        score_after: int,
    ) -> dict:
        """
        Log detection of threat(s) in a message.

        Args:
            session_id: Session identifier
            message: The user message that triggered threats
            threats_detected: List of threat types detected
            score_before: Trust score before deduction
            score_after: Trust score after deduction

        Returns:
            The logged event dict
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "event_type": "threat_detection",
            "threats": threats_detected,
            "message": message,
            "score_before": score_before,
            "score_after": score_after,
            "deduction": score_before - score_after,
        }
        self.events.append(event)
        return event

    def log_clean_message(
        self,
        session_id: str,
        message: str,
        score_before: int,
        score_after: int,
    ) -> dict:
        """
        Log a clean message (no threats) with score recovery.

        Args:
            session_id: Session identifier
            message: The user message
            score_before: Trust score before recovery
            score_after: Trust score after recovery

        Returns:
            The logged event dict
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "event_type": "clean_message",
            "message": message,
            "score_before": score_before,
            "score_after": score_after,
            "recovery": score_after - score_before,
        }
        self.events.append(event)
        return event

    def log_mode_change(
        self,
        session_id: str,
        mode_from: str,
        mode_to: str,
        current_score: int,
    ) -> dict:
        """
        Log a trust mode change (NORMAL → CAUTIOUS, CAUTIOUS → LOCKDOWN, etc).

        Args:
            session_id: Session identifier
            mode_from: Previous mode
            mode_to: New mode
            current_score: Current trust score

        Returns:
            The logged event dict
        """
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "event_type": "mode_change",
            "mode_from": mode_from,
            "mode_to": mode_to,
            "score": current_score,
        }
        self.events.append(event)
        return event

    def log_session_reset(self, session_id: str) -> dict:
        """Log a session reset."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "event_type": "session_reset",
            "score": 100,
        }
        self.events.append(event)
        return event

    def get_session_events(self, session_id: str) -> list[dict]:
        """Retrieve all logged events for a specific session."""
        return [e for e in self.events if e.get("session_id") == session_id]

    def get_all_events(self) -> list[dict]:
        """Retrieve all logged events."""
        return self.events.copy()

    def clear_logs(self, session_id: Optional[str] = None) -> int:
        """
        Clear logs for a specific session or all sessions.

        Args:
            session_id: If provided, clear only this session's logs.
                        If None, clear all logs.

        Returns:
            Number of events cleared
        """
        if session_id is None:
            count = len(self.events)
            self.events = []
            return count
        else:
            old_count = len(self.events)
            self.events = [e for e in self.events if e.get("session_id") != session_id]
            return old_count - len(self.events)