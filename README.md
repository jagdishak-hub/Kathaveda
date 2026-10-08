# The Reading Room

A family scripture-study companion for reading, learning, practical reflection and games. Built in Streamlit. Live: https://kathaveda-production.up.railway.app/

## Run

Use Python 3.12. Run `python -m pip install -r requirements.txt`, then `python build_database.py` and `python -m streamlit run app.py`. The database is reconstructed from the included attributed source archives and integrity-checked parts. No AI call is needed to read stored texts.

## Current reading library

30 attributed source collections and 9,485 nonempty reading units. Units can be verses, hymns, chapters or sections; this is not a story count. There are 26 prepared retellings and 29 historical collected folktales, kept distinct from scripture.

New editions include Annie Besant’s 1922 Sanskrit/English Gita (701 readings; chapter 13 includes an opening Arjuna question), GRETIL Ramayana, Rigveda and Narasimha Purana; historical English translations of Ramayana (Griffith, books 1–6), Vishnu Purana (Dutt/Wilson, six parts) and Mahabharata (Ganguli, all 18 books). Mahabharata source section numbers have internal gaps; scope is the electronic edition, not an independently collated complete critical text. Original numbering is retained.

**The full set of Puranas is still incomplete.** Skanda is Reva-khanda; Shiva contains books 1 and 7; Matsya, Markandeya, Padma and Bhavishya are partial. Use Coverage & sources for edition details and gaps. The separate 801-link GRETIL discovery inventory is not imported text and includes non-Hindu literature.

Source text, historical translation, prepared explanation and modern application are labelled separately. Retellings and application guides await specialist review. Historical English can be difficult for children; it is not advertised as a simple modern translation. GRETIL rights are CC BY-NC-SA; Wikisource transcription rights and source-page public-domain conditions are recorded. Project Gutenberg translations retain full source licence text in the archives. Sanskrit Documents has separate personal-study/research terms: do not assume all transcriptions have unrestricted redistribution rights.

## Learning and conversation

Learning supports sequential practice, meanings where available, self-recording and scheduled recall review. A linked human recording for Gita 2.48 is attributed but not teacher-verified. A full verified pronunciation course is still missing.

Settings accepts all four provider keys: Gemini, OpenRouter, Groq and Grok. A preferred provider is tried first, followed by other configured providers until one succeeds. Model names are editable. API keys and progress can be saved in an encrypted study profile with a passphrase. Railway mounts persistent storage at `/data/study` via `KATHAVEDA_STUDY_DIR`. Private questions are not stored in the public chapter cache. Shared chapter explanations are generated once and reused. Real provider access has not been validated with a user key; fallback is tested with mocked responses.

## Games and remaining work

Scripture-specific quizzes, character clues, dynasty links and event sequences support refreshable rounds. Each game has 25 named learning stages. Gita stages 1–18 follow its chapters; Narayaneeyam stages follow its early dasakams and episodes; Bhagavatam stages focus on source episodes before later connection rounds. Broader source coverage within every stage, full verified audio, specialist-reviewed simple meanings and complete source-edition coverage remain unfinished.

## Validation and imports

`python -m unittest test_app test_study -q` checks all pages, database integrity, reading, next-verse navigation, refreshable games, question retention, encryption and ordered provider fallback. Import scripts require `lxml`; normal app operation reads shipped archives and does not require it. Import scripts preserve source attribution and electronic edition numbering.
