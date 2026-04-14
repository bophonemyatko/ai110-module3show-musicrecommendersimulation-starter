# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

In real world recommendation system, it's a real time live model algorithm working to make sure a song is ready for us after listening. It learn from other users(users with the same music taste) what songs they listen to afterward, so that they can recommend the same song. It's like an implication, if a user or multiple users listens to song B right after A, the users who listened to song A might also listens to song B. That's is collabaritive filtering. Another way is content based filtering, where the system breaks down a song into different attributes and give them a numeric score and recommend a song with the similar or exact score. 

This system uses content-based filtering. Every song in the catalog is scored against a user's taste profile, and the top-scoring songs are returned as recommendations. There are no other users involved — the system only looks at song attributes and what the user says they like.

**What features does each `Song` use?**

Each song carries four attributes the recommender scores against:
- `genre` — the musical genre (e.g. pop, lofi, metal)
- `mood` — the emotional feel (e.g. energetic, chill, melancholic)
- `energy` — a float from 0.0 (very calm) to 1.0 (very intense)
- `acousticness` — a float from 0.0 (fully produced) to 1.0 (fully acoustic)

**What information does the `UserProfile` store?**

The user profile stores four preference fields that mirror the song attributes:
- `favorite_genre` — the genre the user prefers most
- `favorite_mood` — the mood the user prefers most
- `target_energy` — the energy level they are aiming for (0.0–1.0)
- `likes_acoustic` — whether they prefer acoustic-sounding songs (True/False)

**How does the `Recommender` compute a score for each song?**

Each song receives a total score between 0.0 and 1.0, built from four weighted rules:

| Rule | Weight | How it works |
|---|---|---|
| Genre match | 0.25 | Exact match → full points. Same genre cluster (e.g. pop and indie pop) → half points. Unrelated → 0. |
| Mood match | 0.25 | Exact match → full points. Same mood cluster (e.g. energetic and intense) → half points. Unrelated → 0. |
| Energy proximity | 0.35 | Continuous score: `(1 - abs(song.energy - target_energy)) × 0.35`. Closer = higher score. |
| Acousticness | 0.15 | If `likes_acoustic` is True: `song.acousticness × 0.15`. Otherwise the inverse. |

Genre and mood use similarity clusters instead of pure exact matching so that closely related genres and moods still earn partial credit rather than scoring zero.

**How do we choose which songs to recommend?**

Every song in the catalog is scored using the formula above. Songs are then sorted from highest score to lowest, and the top `k` (default: 5) are returned as recommendations.

---
![alt text](image.png)

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

