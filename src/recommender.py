from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

# --- Similarity clusters ---

GENRE_CLUSTERS = {
    "pop":        "pop_electronic",
    "indie pop":  "pop_electronic",
    "synthwave":  "pop_electronic",
    "electronic": "pop_electronic",
    "hip-hop":    "urban_rhythm",
    "R&B":        "urban_rhythm",
    "soul":       "urban_rhythm",
    "reggae":     "urban_rhythm",
    "lofi":       "chill_ambient",
    "ambient":    "chill_ambient",
    "jazz":       "chill_ambient",
    "rock":       "rock_spectrum",
    "metal":      "rock_spectrum",
    "folk":       "acoustic_roots",
    "country":    "acoustic_roots",
    "blues":      "acoustic_roots",
    "classical":  "acoustic_roots",
}

MOOD_CLUSTERS = {
    "energetic":   "high_energy_positive",
    "intense":     "high_energy_positive",
    "happy":       "high_energy_positive",
    "angry":       "high_energy_negative",
    "chill":       "low_energy_calm",
    "peaceful":    "low_energy_calm",
    "relaxed":     "low_energy_calm",
    "focused":     "low_energy_calm",
    "sad":         "low_energy_negative",
    "melancholic": "low_energy_negative",
    "moody":       "low_energy_negative",
    "nostalgic":   "low_energy_negative",
    "romantic":    "neutral_warm",
}


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a (score, reasons) tuple rating a song 0.0–1.0 against the user's taste profile."""
    score = 0.0
    reasons = []

    # --- Rule 1: Genre match (max 0.25) ---
    song_genre = song["genre"]
    user_genre = user_prefs["favorite_genre"]
    if song_genre == user_genre:
        score += 0.25
        reasons.append(f"genre exact match: {song_genre} (+0.25)")
    elif GENRE_CLUSTERS.get(song_genre) == GENRE_CLUSTERS.get(user_genre):
        score += 0.12
        reasons.append(f"genre similar to {user_genre}: {song_genre} (+0.12)")

    # --- Rule 2: Mood match (max 0.25) ---
    song_mood = song["mood"]
    user_mood = user_prefs["favorite_mood"]
    if song_mood == user_mood:
        score += 0.25
        reasons.append(f"mood exact match: {song_mood} (+0.25)")
    elif MOOD_CLUSTERS.get(song_mood) == MOOD_CLUSTERS.get(user_mood):
        score += 0.12
        reasons.append(f"mood similar to {user_mood}: {song_mood} (+0.12)")

    # --- Rule 3: Energy proximity (max 0.35) ---
    energy_contribution = (1.0 - abs(song["energy"] - user_prefs["target_energy"])) * 0.35
    score += energy_contribution
    reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f} (+{energy_contribution:.2f})")

    # --- Rule 4: Acousticness bonus (max 0.15) ---
    if user_prefs["likes_acoustic"]:
        acoustic_contribution = song["acousticness"] * 0.15
        reasons.append(f"acousticness {song['acousticness']:.2f} (likes acoustic) (+{acoustic_contribution:.2f})")
    else:
        acoustic_contribution = (1.0 - song["acousticness"]) * 0.15
        reasons.append(f"acousticness {song['acousticness']:.2f} (prefers produced) (+{acoustic_contribution:.2f})")
    score += acoustic_contribution

    return round(score, 4), reasons


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]            = int(row["id"])
            row["energy"]        = float(row["energy"])
            row["tempo_bpm"]     = float(row["tempo_bpm"])
            row["valence"]       = float(row["valence"])
            row["danceability"]  = float(row["danceability"])
            row["acousticness"]  = float(row["acousticness"])
            songs.append(row)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score every song, sort highest to lowest, and return the top k as (song, score, reasons) tuples."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
