"""Trust score calculator for the AEGIS system."""


class TrustScorer:
    """Manages session trust scores based on detected threats and clean messages."""

    # Threat deduction amounts (from Day 5 plan)
    THREAT_DEDUCTIONS = {
        "prompt_injection": 25,
        "jailbreak": 30,
        "refund_abuse": 15,
        "discount_probing": 10,
        "data_extraction": 20,
        "tool_abuse": 25,
        "credential_theft": 30,
        "policy_evasion": 20,
        "fraud_abuse": 25,
    }

    # Recovery amount per clean message
    CLEAN_MESSAGE_RECOVERY = 2

    # Trust score thresholds
    NORMAL_THRESHOLD_MIN = 70
    NORMAL_THRESHOLD_MAX = 100
    CAUTIOUS_THRESHOLD_MIN = 40
    CAUTIOUS_THRESHOLD_MAX = 69
    LOCKDOWN_THRESHOLD_MAX = 39

    # Session state tracking: session_id -> current_score
    _sessions = {}

    def initialize_session(self, session_id: str) -> int:
        """Initialize a new session with trust score 100."""
        self._sessions[session_id] = 100
        return 100

    def get_score(self, session_id: str) -> int:
        """Get current trust score for a session (default 100 if not initialized)."""
        if session_id not in self._sessions:
            return self.initialize_session(session_id)
        return self._sessions[session_id]

    def apply_threat_deduction(self, session_id: str, threat_types: list[str]) -> dict:
        """
        Apply deductions for detected threats.
        Returns a dict with: score_before, threats_deducted, score_after.
        """
        score_before = self.get_score(session_id)
        total_deduction = sum(
            self.THREAT_DEDUCTIONS.get(threat, 0) for threat in threat_types
        )
        score_after = max(0, score_before - total_deduction)
        self._sessions[session_id] = score_after

        return {
            "score_before": score_before,
            "threats_deducted": threat_types,
            "total_deduction": total_deduction,
            "score_after": score_after,
            "mode": self.get_mode(score_after),
        }

    def apply_clean_message_recovery(self, session_id: str) -> dict:
        """
        Apply recovery for a clean message (no threats detected).
        Returns a dict with: score_before, recovery_amount, score_after.
        """
        score_before = self.get_score(session_id)
        score_after = min(100, score_before + self.CLEAN_MESSAGE_RECOVERY)
        self._sessions[session_id] = score_after

        return {
            "score_before": score_before,
            "recovery_amount": self.CLEAN_MESSAGE_RECOVERY,
            "score_after": score_after,
            "mode": self.get_mode(score_after),
        }

    def get_mode(self, score: int) -> str:
        """
        Determine bot mode based on trust score threshold.
        - NORMAL: 70-100
        - CAUTIOUS: 40-69
        - LOCKDOWN: <40
        """
        if score >= self.NORMAL_THRESHOLD_MIN:
            return "NORMAL"
        elif score >= self.CAUTIOUS_THRESHOLD_MIN:
            return "CAUTIOUS"
        else:
            return "LOCKDOWN"

    def reset_session(self, session_id: str) -> int:
        """Reset a session's trust score back to 100."""
        self._sessions[session_id] = 100
        return 100

    def update_score(self, current_score, threats):

        score = current_score

        for threat in threats:
            score -= self.deductions.get(threat, 0)

        score = max(0, score)

        return score