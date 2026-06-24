# test_chat.py
import httpx
import json

BASE_URL = "http://localhost:8000"

test_messages = [
    # SALES (7 messages)
    ("What pricing plans do you offer?", "SALES"),
    ("Can I upgrade my current subscription?", "SALES"),
    ("Do you have a student discount?", "SALES"),
    ("I want to buy the premium plan", "SALES"),
    ("What's included in the enterprise package?", "SALES"),
    ("Is there a free trial available?", "SALES"),
    ("How much does the Pro plan cost per month?", "SALES"),

    # SUPPORT (7 messages)
    ("I can't log into my account", "SUPPORT"),
    ("The app keeps crashing on startup", "SUPPORT"),
    ("How do I reset my password?", "SUPPORT"),
    ("My data isn't syncing across devices", "SUPPORT"),
    ("I'm getting a 500 error on the dashboard", "SUPPORT"),
    ("How do I export my data?", "SUPPORT"),
    ("The notifications aren't working on my phone", "SUPPORT"),

    # CARE (6 messages)
    ("I've been waiting 3 days for a refund and nothing has happened", "CARE"),
    ("I want to cancel my subscription immediately", "CARE"),
    ("This product is terrible and I want my money back", "CARE"),
    ("I'm very frustrated with your customer service", "CARE"),
    ("My account was charged twice and nobody is helping me", "CARE"),
    ("I'm thinking of leaving and switching to a competitor", "CARE"),
]

def run_tests():
    correct = 0
    results = []

    print("\n🔍 Running AEGIS Chat Engine Tests")
    print("=" * 65)

    with httpx.Client(timeout=60.0) as client:
        for i, (message, expected) in enumerate(test_messages, 1):
            try:
                response = client.post(
                    f"{BASE_URL}/chat",
                    json={"message": message, "session_id": f"test-{i}"},
                )
                data = response.json()
                got_intent = data.get("intent", "ERROR")
                trust_score = data.get("trust_score", "N/A")
                mode = data.get("mode", "N/A")
                match = got_intent == expected

                if match:
                    correct += 1

                status = "✅" if match else "❌"
                print(f"[{i:02d}] {status} Expected={expected:7s} Got={got_intent:7s} | Score={trust_score} | Mode={mode}")
                print(f"      MSG: {message[:60]}")
                print()

            except Exception as e:
                print(f"[{i:02d}] 💥 ERROR: {e}")
                print()

    print("=" * 65)
    print(f"✅ Intent Accuracy: {correct}/{len(test_messages)} correct ({round(correct/len(test_messages)*100)}%)")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()