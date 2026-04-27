"""
Gemini API integration for AI-powered music recommendations.

Requires GEMINI_API_KEY in your .env file.
"""

import os
import json
import re
import google.generativeai as genai

_model = None


def get_model() -> genai.GenerativeModel:
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Add it to a .env file in the project root: GEMINI_API_KEY=your_key"
            )
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel("gemini-2.0-flash")
    return _model


def _parse_json(text: str) -> dict | list:
    """Parse JSON from Gemini's response, stripping any markdown fences."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def analyze_song(song_name: str) -> dict:
    """
    Ask Gemini to identify a song and return its musical attributes.

    Returns a dict with keys:
      title, artist, genre, mood, energy (0-1), acousticness (0-1),
      tempo_bpm, valence (0-1), danceability (0-1), description
    """
    model = get_model()

    prompt = (
        "You are a music expert. Identify this song and return ONLY a JSON object "
        "— no markdown fences, no prose — with exactly these fields:\n"
        "{\n"
        '  "title": "exact song title",\n'
        '  "artist": "artist name",\n'
        '  "genre": "one of: pop, indie pop, synthwave, electronic, hip-hop, R&B, '
        'soul, reggae, lofi, ambient, jazz, rock, metal, folk, country, blues, classical, k-pop",\n'
        '  "mood": "one of: energetic, intense, happy, angry, chill, peaceful, '
        'relaxed, focused, sad, melancholic, moody, nostalgic, romantic, euphoric",\n'
        '  "energy": <float 0.0-1.0>,\n'
        '  "acousticness": <float 0.0-1.0>,\n'
        '  "tempo_bpm": <integer>,\n'
        '  "valence": <float 0.0-1.0>,\n'
        '  "danceability": <float 0.0-1.0>,\n'
        '  "description": "1-2 sentence vibe description"\n'
        "}\n\n"
        f"Song to analyze: {song_name}"
    )

    response = model.generate_content(prompt)
    return _parse_json(response.text)


def recommend_songs_ai(preferences: dict, k: int = 5) -> list:
    """
    Ask Gemini to recommend k real songs matching the given taste preferences.

    preferences keys: favorite_genre, favorite_mood, target_energy (0-1), likes_acoustic (bool)

    Returns a list of dicts, each with:
      title, artist, genre, mood, energy, acousticness, tempo_bpm, score (0-1), reasons (list[str])
    """
    model = get_model()

    pref_text = (
        f"- Genre: {preferences['favorite_genre']}\n"
        f"- Mood: {preferences['favorite_mood']}\n"
        f"- Energy level: {preferences['target_energy']} (0=very calm, 1=very intense)\n"
        f"- Likes acoustic: {preferences['likes_acoustic']}"
    )

    prompt = (
        "You are a music recommendation expert with deep knowledge of real songs. "
        "Return ONLY a JSON array — no markdown fences, no prose — where each element has:\n"
        "{\n"
        '  "title": "song title",\n'
        '  "artist": "artist name",\n'
        '  "genre": "genre",\n'
        '  "mood": "mood",\n'
        '  "energy": <float 0.0-1.0>,\n'
        '  "acousticness": <float 0.0-1.0>,\n'
        '  "tempo_bpm": <integer>,\n'
        '  "score": <float 0.0-1.0 how well it fits the preferences>,\n'
        '  "reasons": ["reason 1", "reason 2", "reason 3"]\n'
        "}\n\n"
        f"Recommend {k} real songs for a listener with these preferences:\n{pref_text}"
    )

    response = model.generate_content(prompt)
    return _parse_json(response.text)


def find_similar_songs_ai(song_name: str, k: int = 5) -> tuple[dict, list]:
    """
    Ask Gemini to analyze a song and find k similar real songs.

    Returns (source_song_dict, list_of_similar_song_dicts).
    """
    model = get_model()

    prompt = (
        "You are a music expert. Analyze the given song and find similar real songs. "
        "Return ONLY a JSON object — no markdown fences, no prose — with exactly two keys:\n"
        "{\n"
        '  "source_song": {\n'
        '    "title": "...", "artist": "...", "genre": "...", "mood": "...",\n'
        '    "energy": <0-1>, "acousticness": <0-1>, "tempo_bpm": <int>,\n'
        '    "valence": <0-1>, "danceability": <0-1>,\n'
        '    "description": "1-2 sentence vibe description"\n'
        '  },\n'
        '  "recommendations": [\n'
        '    {\n'
        '      "title": "...", "artist": "...", "genre": "...", "mood": "...",\n'
        '      "energy": <0-1>, "acousticness": <0-1>, "tempo_bpm": <int>,\n'
        '      "score": <0-1>, "reasons": ["why it is similar", "reason 2"]\n'
        '    }\n'
        '  ]\n'
        "}\n\n"
        f"Find {k} songs similar to: {song_name}"
    )

    response = model.generate_content(prompt)
    result = _parse_json(response.text)
    return result["source_song"], result["recommendations"]
