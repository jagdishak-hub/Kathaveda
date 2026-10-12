# Tattvika

**Read · Understand · Explore · Reflect**

Tattvika is a source-first Hindu literature, learning, reflection, stories and games companion built in Streamlit.

Live app: https://kathaveda-production.up.railway.app/

> Repository continuity note: the GitHub repository and Railway service retain the historical `Kathaveda` name so existing deployments, storage and URLs are not broken. The product name going forward is **Tattvika**.

## Current library

The shipped literature database currently contains **31 attributed source collections and 9,942 nonempty reading units**. Units may be verses, hymns, chapters or sections; they are not story counts. The database also contains prepared retellings and a separate historical folktale collection.

The reading library includes, among other collections:

- Bhagavad Gita, including Annie Besant's 1922 Sanskrit/English edition
- Srimad Bhagavatam
- Narayaneeyam
- Valmiki Ramayana sources, including GRETIL and Griffith material
- Mahabharata — Ganguli, across all 18 books of the electronic edition
- complete named Sanskrit Shiva Purana edition — 457 chapters across seven samhitas
- Vishnu Purana historical translations
- Rigveda source material
- Narasimha Purana
- Upanishadic, hymn, stotra and Saraswati literature collections
- additional Puranic material with explicit coverage status

Not every Purana is complete. Partial or restricted collections remain clearly labelled in **Coverage & sources** rather than being represented as complete scripture editions.

## Core product areas

### Library / Reading Room
Canonical source text and historical translations are kept distinct from generated explanations. Source, edition, coverage and rights metadata remain visible.

### Stories
Prepared retellings and historical folktales are kept separate from scripture. Retellings are labelled as retellings and are not presented as canonical source text.

### Learn & Review
Sequential practice, meanings where available, self-recording, saved progress and scheduled recall review.

### Converse
Grounded conversation over stored literature with prepared local answers where available and provider-assisted answers otherwise. Supported providers include OpenRouter, Gemini, Groq and Grok, with ordered fallback across configured providers. Evidence links are shown after responses.

### Games
Scripture-specific quizzes, character clues, dynasty links and event sequences with refreshable rounds, streaks, lotus points, achievements and 25 learning stages.

### Study my text
Session-private TXT, PDF and DOCX study uploads with search and provider-assisted explanation. Uploaded material is not added to the shared public corpus.

### Sources & integrity
The coverage report exposes edition, source, rights, review state and known coverage gaps. A title existing in the catalogue never implies that every part of every edition is complete.

## Source policy

Tattvika separates:

1. original/source transcription
2. historical translation
3. prepared explanation
4. modern application
5. story retelling

One attributed source/edition is used within each stored collection. Alternative editions may coexist as separately named collections; they are not silently blended into a single canonical text.

GRETIL, Wikisource, Project Gutenberg, Sanskrit Documents and other sources retain their respective attribution and reuse conditions. Do not infer unrestricted redistribution rights merely because a text is old.

## Persistence and privacy

Study profiles can persist progress and provider settings. Railway mounts persistent storage at `/data` through `KATHAVEDA_STUDY_DIR`. Private questions are not stored in the public chapter cache. Shared generated chapter explanations are cached separately.

## Validation

Run:

```bash
python -m unittest test_app test_study -q
```

The test suite covers pages, database integrity, reading navigation, game refresh behavior, question retention, encrypted profile handling and ordered provider fallback.

## Local run

Python 3.12 is recommended.

```bash
python -m pip install -r requirements.txt
python build_database.py
python -m streamlit run app.py
```

Normal operation reads the shipped attributed source archives. Import scripts may require additional parsing dependencies such as `lxml`.

## Current quality bar

Tattvika is being developed to the same product standard as BioSage: broad curated content, clear provenance, persistent study state, graceful provider fallback, usable non-AI paths, explicit incomplete-state handling, and features that work as connected parts of one literature system rather than isolated demos.
