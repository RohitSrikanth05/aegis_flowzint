"""
INTEGRATION GUIDE FOR UNNATHI'S TRUST ENGINE
For Swathi (Backend) - Day 6 Integration

This module provides trustworthiness detection, scoring, escalation, and logging.
"""

# ============================================================================
# QUICK START FOR SWATHI
# ============================================================================

"""
1. IMPORT THE MODULES
   from services.trust_engine.detector import TrustDetector
   from services.trust_engine.scorer import TrustScorer
   from services.trust_engine.logger import TrustLogger
   from services.trust_engine.escalation import TrustEscalation

2. INITIALIZE (per session)
   detector = TrustDetector()
   scorer = TrustScorer()
   logger = TrustLogger()
   escalation = TrustEscalation()
   
   session_id = request.session_id
   scorer.initialize_session(session_id)

3. IN YOUR /chat ENDPOINT
   
   # Detect threats
   threats = detector.analyze(user_message)
   
   # Apply scoring
   if threats:
       result = scorer.apply_threat_deduction(session_id, threats)
   else:
       result = scorer.apply_clean_message_recovery(session_id)
   
   # Get current mode
   trust_score = result["score_after"]
   mode = result["mode"]
   
   # Log events
   if threats:
       logger.log_threat_detection(session_id, user_message, threats, 
                                    result["score_before"], trust_score)
   else:
       logger.log_clean_message(session_id, user_message,
                               result["score_before"], trust_score)
   
   # Get mode-specific system prompt
   system_prompt = escalation.get_system_prompt(mode)
   
   # Use system_prompt when calling Claude
   # Include threats and mode in events

4. RETURN IN ChatResponse
   {
       "reply": "<LLM response>",
       "session_id": session_id,
       "intent": "<SALES|SUPPORT|CARE>",
       "trust_score": trust_score,
       "confidence_score": <from Rohit>,
       "events": [
           "Prompt injection attempt detected",
           "Session flagged - trust score: 42",
           "Mode switched to CAUTIOUS",
           ...
       ]
   }

# ============================================================================
# THREAT TYPES (9 categories)
# ============================================================================

THREATS = {
    "prompt_injection": -25,     # Trying to override system instructions
    "jailbreak": -30,             # Trying to remove restrictions
    "refund_abuse": -15,          # Repeated refund requests
    "discount_probing": -10,      # Repeated discount requests
    "data_extraction": -20,       # Requesting confidential data
    "tool_abuse": -25,            # Trying to use admin tools
    "credential_theft": -30,      # Requesting API keys/secrets
    "policy_evasion": -20,        # Trying to bypass policies
    "fraud_abuse": -25,           # Fraud/manipulation attempts
}

# ============================================================================
# TRUST MODES
# ============================================================================

MODES = {
    "NORMAL": (70, 100),      # Full service, flexible
    "CAUTIOUS": (40, 69),     # Limited exceptions, escalation
    "LOCKDOWN": (0, 39),      # Restricted, no discounts/refunds
}

# ============================================================================
# ARCHITECTURE
# ============================================================================

"""
User Message
    ↓
[detector.analyze()]           ← Fast path: <5ms
    ↓
Threats? {list}
    ↓
[scorer.apply_threat_deduction()]  ← Deduct points, get new mode
    ↓
Score & Mode Updated
    ↓
[escalation.get_system_prompt()]   ← Get mode-specific prompt
    ↓
[logger.log_*()]               ← Log for audit trail
    ↓
Enhanced LLM Call
    ↓
Return ChatResponse with threats, score, mode, events
"""

# ============================================================================
# OPTIONAL: ADVANCED LLM VERIFICATION
# ============================================================================

"""
For high-confidence detections or uncertain cases:

result = detector.analyze_with_llm_verification(
    message,
    verify_categories=["prompt_injection", "credential_theft"]
)

Returns:
{
    "threats": [...],
    "verifications": {
        "prompt_injection": {
            "verified": True,
            "confidence": 0.95,
            "reason": "User message attempts to override instructions..."
        }
    }
}

Recommendation: Only use if score < 50 to avoid latency.
"""

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

"""
Each session has its own trust score and history:

- Initialize: scorer.initialize_session(session_id) → score = 100
- Reset: scorer.reset_session(session_id) → score = 100
- Get events: logger.get_session_events(session_id) → list of events
- Clear logs: logger.clear_logs(session_id)

Session persists across messages until reset (useful for demo resets).
"""

# ============================================================================
# IMPORTANT: LOCKDOWN BEHAVIOR
# ============================================================================

"""
When score drops below 40 (LOCKDOWN mode):

1. System prompt changes to restrict bot
2. Bot REFUSES all discounts, refunds, policy exceptions
3. All such requests return:
   "Your session has been flagged for suspicious activity. 
    Please contact our support team at support@shopnova.com"
4. Bot only answers basic product questions
5. Session can recover with clean messages (+2 per message)

This is intentional - don't override!
"""

# ============================================================================
# TESTING UNNATHI'S MODULES
# ============================================================================

"""
Run tests from /services/trust_engine/:

1. Basic functionality:
   python3 test_cases.py
   
2. Escalation behavior:
   python3 test_escalation.py
   
3. Ollama integration:
   python3 test_ollama_integration.py
   
4. LLM advanced:
   python3 test_llm_advanced.py
   
5. Full pipeline:
   python3 test_full_pipeline.py

All tests should pass ✓
"""

# ============================================================================
# REQUIREMENTS
# ============================================================================

"""
- Python 3.8+
- ollama package: pip install ollama
- Ollama service running locally (optional, for LLM verification)
  Get from: https://ollama.ai/
  Run: ollama serve
  Pull model: ollama pull llama3.2:3b
"""

# ============================================================================
# INTEGRATION CHECKLIST
# ============================================================================

"""
☐ Import all 4 modules
☐ Initialize per session
☐ Call detector.analyze() on user messages
☐ Call scorer.apply_threat_deduction/recovery()
☐ Get system prompt from escalation module
☐ Log events with logger
☐ Return trust_score and mode in ChatResponse
☐ Display threats and events in UI (for Shreyas)
☐ Test with demo scripts on Day 7

Contact Unnathi if: 
- Detection missing obvious attacks
- Scores not updating correctly
- Mode transitions wrong
- Ollama integration failing
"""
