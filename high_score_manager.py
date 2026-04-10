import json
import os

HIGHSCORE_FILE = "highscores.json"


def load_high_scores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            scores = json.load(f)
            # Ensure scores is a list and contains dictionaries with 'name' and 'score'
            if not isinstance(scores, list):
                return []
            for entry in scores:
                if (
                    not isinstance(entry, dict)
                    or "name" not in entry
                    or "score" not in entry
                ):
                    return []
            return scores
    except json.JSONDecodeError:
        # Handle cases where the JSON file is corrupt or empty
        return []
    except Exception as e:
        print(f"Error loading high scores: {e}")
        return []


def save_high_scores(scores):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump(scores, f, indent=4)
    except Exception as e:
        print(f"Error saving high scores: {e}")


def add_high_score(new_name, new_score):
    scores = load_high_scores()
    scores.append({"name": new_name, "score": new_score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    # Keep only the top 10 scores
    scores = scores[:10]
    save_high_scores(scores)
