# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: SongRec1.0 

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This recommender suggests songs from a small catalog that best match a listener's stated taste. It does not predict what a user will click on or stream next — instead it takes a snapshot of their preferences (a favorite genre, a mood they are in the mood for, how energetic they want the music to feel, and whether they like acoustic or produced sounds) and finds the songs that fit that description most closely. It assumes the user already knows what they want and can describe it upfront; it does not learn or update based on what they actually listen to. This is a classroom simulation built for learning purposes, not a production system.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The system scores every song against a user's preferences using four rules, then returns the five highest-scoring songs.

**Rule 1 — Genre (up to 0.25 points).** If a song's genre exactly matches what the user asked for, it gets full points. If the genre is related but not identical — for example, the user likes lofi and the song is jazz — it gets half points. Unrelated genres get nothing.

**Rule 2 — Mood (up to 0.25 points).** Works the same way as genre. An exact mood match gets full points. A similar mood — for example, "happy" and "energetic" are treated as neighbors — gets half points. Unrelated moods get nothing.

**Rule 3 — Energy (up to 0.30 points).** Each song has an energy level between 0 (very calm) and 1 (very intense). The closer the song's energy is to what the user wants, the more points it earns. A perfect match gives the full 0.30; a song at the opposite extreme gives close to zero.

**Rule 4 — Acousticness (up to 0.20 points).** If the user likes acoustic music, songs that sound raw and organic score higher. If the user prefers a produced, polished sound, the opposite is true. A fully acoustic song scores the maximum for an acoustic lover and near zero for someone who prefers produced music.

The four scores are added together (maximum possible total: 1.0), and the top five songs are recommended. Energy and acousticness weights were adjusted from the original — energy was reduced slightly and acousticness raised — so that a preference for acoustic music has a more visible effect on the results.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog contains 20 songs spanning 16 genres — including pop, hip-hop, lofi, jazz, metal, folk, and classical — and 13 moods ranging from energetic and happy to sad and melancholic. Each song has five numeric features: energy, tempo, valence, danceability, and acousticness. The dataset was not changed from its original form. Its main limits are size and balance: rock and metal together have only 2 songs, so fans of those genres always see the same results, and there are no songs with mid-range energy (roughly 0.59 to 0.74), which quietly penalizes users who prefer moderate-intensity music. Broader tastes like K-pop, Latin, or country-pop are missing entirely.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best when a user's preferences are consistent with each other — for example, someone who likes calm music, chooses a calm genre like lofi, and targets a low energy level will see results that feel genuinely right. The Chill Lofi Listener scored 0.98 on their top match because all four rules pointed at the same song at once. A second pattern the scoring captures well is genre neighborhood: a hip-hop fan will naturally surface R&B and soul songs in their top five, which matches how real listeners often discover adjacent genres. The energy rule also handles contrast cleanly — a high-energy user and a low-energy user will almost never share the same top results, which is the expected behavior. The main imbalance is that these strengths only hold when the catalog has enough songs to cover the preference; genres with only one or two songs in the dataset, like rock and metal, break this pattern and push the same songs to the top every time.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One significant weakness discovered during testing is that the energy scoring unfairly disadvantages users who prefer moderate-energy music. The song catalog has a clear gap in the middle range — most songs are either very calm or very high-energy, with almost nothing in between — so a user who wants something in that middle ground can never receive a strong energy match, no matter how well their other preferences align. Because energy is the highest-weighted signal in the scoring formula, this gap quietly penalizes an entire category of listeners, making their top recommendations feel like compromises rather than genuine matches. In contrast, users who prefer extreme energy levels — either very calm or very intense — have several songs closely matching their target and consistently receive higher scores. This is a structural bias baked into the data itself, meaning no adjustment to the scoring weights alone can fix it; the catalog would need more songs in the moderate energy range to treat all users equally.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

We tested eight profiles in total: three everyday listeners (High Energy Pop Fan, Chill Lofi Listener, Hip-Hop Cruise) and five adversarial profiles designed to stress-test the system (High-Energy Sad Paradox, K-Pop Euphoric, Superhuman Energy Seeker, Acoustic Metal Head, Serene but Intense). For each profile we looked at which songs appeared in the top five and whether the reasons shown actually matched what the user asked for. The biggest surprise was that the Chill Lofi Listener scored almost perfectly (0.98) because all four signals — genre, mood, energy, and acousticness — lined up at the same time, while the adversarial profiles exposed that a single strong signal like energy can completely override everything else. We also found that the K-Pop Euphoric profile returned five songs at nearly identical scores, which looks confident on the surface but actually means the system had no idea what to recommend. Running the adversarial profiles side by side with the normal ones made it clear that the system works well when preferences are consistent, but quietly falls apart when they conflict.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

The most useful next step would be adding a minimum score threshold so the system can decline to recommend rather than always returning five results regardless of fit. Beyond that, replacing the hand-coded genre and mood clusters with data-driven song groupings based on the actual numeric features would make the similarity logic more accurate and easier to expand. A diversity rule that prevents the top five from being too similar to each other would also help users discover more of the catalog.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

The most surprising finding was that a system with simple rules can look very confident while being completely wrong — the K-Pop profile returned five songs with no explanation, as if it knew what it was doing. It made me realize that apps like Spotify are probably hiding a lot of uncertainty behind a polished surface. The exercise also showed that testing with normal users is not enough; the edge cases were where the real weaknesses showed up.
