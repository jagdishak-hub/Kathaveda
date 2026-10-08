# KathaVeda — Streamlit rebuild

A family scripture-study app with a packaged local SQLite database. Reading, stories, situations, learning and quizzes work without AI calls. Conversation uses one online request, with at most one configured fallback.

## Run

Use Python 3.11 or newer:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The packaged `data/scriptures.sqlite` database is ready to use. `python build_database.py` rebuilds it from the included attributed `data/corpus.json.gz` archive; no separate checkout or online download is required.

## Host and share

Upload this folder to a dedicated GitHub repository. On Streamlit Community Cloud, select that repository and `app.py` as the entry point. Alternatively deploy the included Dockerfile on Railway. Configure access for your intended audience and use the resulting hosted URL. This downloadable package is not itself a hosted URL.

The app owner can configure `KATHAVEDA_OPENROUTER_API_KEY`, `KATHAVEDA_GEMINI_API_KEY`, `KATHAVEDA_GROQ_API_KEY` or `KATHAVEDA_GROK_API_KEY` as private hosting environment variables. These are never displayed in a widget. Alternatively personal keys can be entered in Conversation settings and retained only in the browser's server-side session. Do not commit real keys to GitHub. Choose a model that is available to your provider account; model identifiers and access can change. No valid provider key was available during development, so live online answers are not yet verified.

## Coverage and authenticity

The database contains 22 collections and 4,332 nonempty units (chapters or verses, depending on collection). Brahmavaivarta contains 275 chapters across all four khandas; Krishna-janma-khanda chapter 7 remains absent. Import counts and gaps are recorded in `data/import-status.json`. Use the app's **Coverage & sources** page for current counts, edition details, source links and rights.

**This is not a complete library of all Puranas.** Important partial collections include Skanda (Reva-khanda), Shiva (books 1 and 7), Matsya (1–176), Markandeya (selected 1–93), Padma and Bhavishya. Internal numbering gaps do not detect entirely missing books or missing chapters beyond the final stored number. Completeness must be checked against a specified edition, not inferred from catalogue titles or counts.

Original transcriptions are attributed to Sanskrit Wikisource, GRETIL and Sanskrit Documents. Ancient text, transcription rights and editorial interpretation are distinct. GRETIL exports retain CC BY-NC-SA attribution; Wikisource exports retain source-page attribution and CC BY-SA notices. Sanskrit Documents supplies personal-study/research transcriptions; consult its source reuse terms before public redistribution of those transcriptions. The package is intended for noncommercial study; do not assume every source has identical redistribution terms.

English stories are prepared retellings, awaiting scholarly review. Selected meanings are explanatory paraphrases. Situations and worksheets are modern applications, not literal scripture quotations. No independently reviewed pronunciation recordings are included.

Learning and worksheet progress lasts for the session; download and restore learning progress, and download worksheets before closing. The app does not claim to store permanent personal accounts.

## Validation

```bash
python -m unittest test_app -q
```

Tests inspect database integrity, readable content and catalogue links; open all seven app sections; advance learning; check and advance a quiz; preserve questions when keys are absent; and exercise readable and malformed provider responses for all four providers. Provider calls are mocked in tests, not evidence of successful live API access.

