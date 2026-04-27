"""
Streamlit Music Recommender UI

Run from the project root:
  streamlit run src/app.py
"""

import os
import sys
from pathlib import Path

# Make sure src/ is on the path so we can import recommender and ai_helper
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from recommender import load_songs, recommend_songs, GENRE_CLUSTERS, MOOD_CLUSTERS

# ── Constants ────────────────────────────────────────────────────────────────

DATA_PATH = Path(__file__).parent.parent / "data" / "songs.csv"

GENRES = sorted(set(GENRE_CLUSTERS.keys()) | {"k-pop"})
MOODS  = sorted(set(MOOD_CLUSTERS.keys())  | {"euphoric"})

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Music Recommender",
    page_icon="🎵",
    layout="wide",
)

# ── Load local songs (cached) ─────────────────────────────────────────────────

@st.cache_data
def get_songs():
    return load_songs(str(DATA_PATH))

songs = get_songs()

# ── Header ───────────────────────────────────────────────────────────────────

st.title("🎵 Music Recommender")
st.markdown("Discover music tailored to your taste — powered by your **local library** or **AI (Gemini)**.")

# ── Source toggle ─────────────────────────────────────────────────────────────

col_title, col_toggle = st.columns([4, 1])
with col_toggle:
    use_ai = st.toggle("🤖 AI mode (Gemini)", value=False)

if use_ai:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.warning(
            "**AI mode is on but no API key was found.**  \n"
            "Add `GEMINI_API_KEY=your_key` to a `.env` file in the project root, "
            "then restart the app."
        )

st.divider()

# ── Helpers ──────────────────────────────────────────────────────────────────

def render_song_card(song: dict, score: float, reasons: list[str], key: str):
    """Render a single song result as an expander card."""
    label = f"**{song['title']}** — {song['artist']}  &nbsp; `score: {score:.2f}`"
    with st.expander(label):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Genre",        song.get("genre",        "—"))
        c2.metric("Mood",         song.get("mood",         "—"))
        c3.metric("Energy",       f"{song.get('energy', 0):.2f}")
        c4.metric("Acousticness", f"{song.get('acousticness', 0):.2f}")
        if song.get("tempo_bpm"):
            st.caption(f"Tempo: {song['tempo_bpm']} BPM")
        if reasons:
            st.markdown("**Why this song?**")
            for r in reasons:
                st.markdown(f"- {r}")


def render_source_card(song: dict):
    """Render the analyzed source song in a bordered container."""
    st.markdown(f"### Analyzing: *{song.get('title', 'Unknown')}* by {song.get('artist', 'Unknown')}")
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Genre",        song.get("genre",        "—"))
        c2.metric("Mood",         song.get("mood",         "—"))
        c3.metric("Energy",       f"{song.get('energy', 0):.2f}")
        c4.metric("Acousticness", f"{song.get('acousticness', 0):.2f}")
        if song.get("description"):
            st.caption(song["description"])


# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["🎛️ Browse by Preferences", "🔍 Find Similar to a Song"])

# ============================================================
# TAB 1 — Browse by Preferences
# ============================================================
with tab1:
    st.subheader("Set Your Music Preferences")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        genre = st.selectbox("Favorite Genre", GENRES, index=GENRES.index("pop"))
        mood  = st.selectbox("Favorite Mood",  MOODS,  index=MOODS.index("happy"))

    with col_b:
        energy = st.slider(
            "Energy Level", 0.0, 1.0, 0.7, 0.05,
            help="0 = very calm / quiet,  1 = very intense / hyped"
        )
        k = st.slider("How many recommendations?", 3, 10, 5, key="k1")

    with col_c:
        likes_acoustic = st.checkbox("I like acoustic / unplugged music", value=False)

    if st.button("🎵 Get Recommendations", key="btn_prefs", type="primary"):
        prefs = {
            "favorite_genre": genre,
            "favorite_mood":  mood,
            "target_energy":  energy,
            "likes_acoustic": likes_acoustic,
        }

        if use_ai:
            try:
                from ai_helper import recommend_songs_ai
                with st.spinner("Asking Gemini for recommendations…"):
                    results = recommend_songs_ai(prefs, k=k)
                st.success(f"**{len(results)} AI-powered recommendations:**")
                for i, song in enumerate(results):
                    render_song_card(
                        song,
                        score=song.get("score", 0.0),
                        reasons=song.get("reasons", []),
                        key=f"ai_pref_{i}",
                    )
            except Exception as e:
                st.error(f"Gemini error: {e}")
        else:
            results = recommend_songs(prefs, songs, k=k)
            st.success(f"**{len(results)} recommendations from your local library:**")
            for i, (song, score, reasons) in enumerate(results):
                render_song_card(song, score, reasons, key=f"local_pref_{i}")


# ============================================================
# TAB 2 — Find Similar to a Song
# ============================================================
with tab2:
    st.subheader("Find Songs Similar to One You Love")
    st.caption(
        "Type any real song name. AI will analyze it and find similar songs — "
        "from the internet (AI mode) or your local library (local mode)."
    )

    song_input = st.text_input(
        "Song name (and optionally the artist)",
        placeholder="e.g.  Blinding Lights by The Weeknd",
    )
    k2 = st.slider("How many recommendations?", 3, 10, 5, key="k2")

    if st.button("🔍 Find Similar Songs", key="btn_song", type="primary"):
        if not song_input.strip():
            st.warning("Please enter a song name.")

        elif use_ai:
            # AI mode — Gemini finds similar songs from the internet
            try:
                from ai_helper import find_similar_songs_ai
                with st.spinner(f"Asking Gemini to find songs similar to '{song_input}'…"):
                    source_song, similar = find_similar_songs_ai(song_input, k=k2)

                render_source_card(source_song)

                st.markdown(f"### {len(similar)} Similar Songs (from the internet)")
                for i, song in enumerate(similar):
                    render_song_card(
                        song,
                        score=song.get("score", 0.0),
                        reasons=song.get("reasons", []),
                        key=f"ai_sim_{i}",
                    )
            except Exception as e:
                st.error(f"Gemini error: {e}")

        else:
            # Local mode — use Gemini to analyze the song, then match against local CSV
            try:
                from ai_helper import analyze_song
                with st.spinner(f"Asking Gemini to analyze '{song_input}'…"):
                    source_song = analyze_song(song_input)

                render_source_card(source_song)

                # Build a taste profile from the analyzed song and search local library
                prefs = {
                    "favorite_genre": source_song["genre"],
                    "favorite_mood":  source_song["mood"],
                    "target_energy":  source_song["energy"],
                    "likes_acoustic": source_song["acousticness"] > 0.5,
                }
                results = recommend_songs(prefs, songs, k=k2)

                st.markdown(f"### {len(results)} Similar Songs from Local Library")
                for i, (song, score, reasons) in enumerate(results):
                    render_song_card(song, score, reasons, key=f"local_sim_{i}")

            except Exception as e:
                st.error(f"Error: {e}")
                if "GEMINI_API_KEY" in str(e):
                    st.info(
                        "Note: **Local + Song Search** still uses Gemini to analyze the song name. "
                        "Set your API key to use this feature."
                    )
