"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile for recommendations
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "energetic",
        "target_energy": 0.95,
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for song, score, reasons in recommendations:
        print(f"{song['title']} by {song['artist']} - Score: {score:.2f}")
        for reason in reasons:
            print(f"  • {reason}")
        print()


if __name__ == "__main__":
    main()
