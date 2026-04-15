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

    profiles = [
        {
            "name": "High Energy Pop Fan",
            "favorite_genre": "pop",
            "favorite_mood": "energetic",
            "target_energy": 0.95,
            "likes_acoustic": True,
        },
        {
            "name": "Chill Lofi Listener",
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "likes_acoustic": True,
        },
        {
            "name": "Hip-Hop Cruise",
            "favorite_genre": "hip-hop",
            "favorite_mood": "happy",
            "target_energy": 0.70,
            "likes_acoustic": False,
        },
        {
            "name": "High-Energy Sad Paradox",
            "favorite_genre": "rock",
            "favorite_mood": "sad",
            "target_energy": 0.90,
            "likes_acoustic": False,
        },
        {
            "name": "K-Pop Euphoric",
            "favorite_genre": "k-pop",
            "favorite_mood": "euphoric",
            "target_energy": 0.80,
            "likes_acoustic": False,
        },
        {
            "name": "Superhuman Energy Seeker",
            "favorite_genre": "electronic",
            "favorite_mood": "energetic",
            "target_energy": 1.5,
            "likes_acoustic": False,
        },
        {
            "name": "Acoustic Metal Head",
            "favorite_genre": "metal",
            "favorite_mood": "angry",
            "target_energy": 0.97,
            "likes_acoustic": True,
        },
        {
            "name": "Serene but Intense",
            "favorite_genre": "jazz",
            "favorite_mood": "intense",
            "target_energy": 0.50,
            "likes_acoustic": True,
        },
    ]

    for profile in profiles:
        name = profile.pop("name")
        recommendations = recommend_songs(profile, songs, k=5)
        print(f"\n--- {name} ---\n")
        for song, score, reasons in recommendations:
            print(f"{song['title']} by {song['artist']} - Score: {score:.2f}")
            for reason in reasons:
                print(f"  • {reason}")
            print()


if __name__ == "__main__":
    main()
