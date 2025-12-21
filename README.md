# Alwrity - AI Blog Post Generator

Alwrity is a Streamlit app that generates comprehensive, SEO‑oriented blog posts. It enriches your prompt with web search context using Exa (formerly Metaphor) and writes the article with Google Gemini.

## 🚀 Try Online

**Want to test the tool without installation?** Visit our web version: **[Try AI Blog Writer on Alwrity.com](https://www.alwrity.com/ai-blog-writer)**

## Features

- **Keyword‑driven generation**: Provide a topic/keywords; get a full article.
- **Formats, tone, language**: Choose post type, tone, and language.
- **Search‑augmented writing**: Uses Exa/Metaphor search results to ground content.
- **Built‑in SEO guidance**: Structure, semantic keywords, and E‑E‑A‑T alignment.
- **FAQs + extras**: Adds FAQs, CTA, visual suggestions, and SEO metadata (title, meta, slug, hashtags).

## Tech stack / Dependencies

Install from `requirements.txt`:

- `streamlit`
- `exa_py` (Exa/Metaphor web search)
- `google-genai` (Gemini API)
- `tenacity` (robust retries)

## Getting started (Windows PowerShell tested)

1) Clone:
```powershell
git clone https://github.com/AJaySi/alwrity_blog_writer.git
```
2) Enter the project and install dependencies:
```powershell
cd alwrity_blog_writer
pip install -r requirements.txt
```
3) Run the app:
```powershell
streamlit run blog_from_serp.py
```

## Configuration (API keys)

You can provide keys directly in the app UI (recommended for quick start), or via environment variables.

- **Exa (Metaphor) API key**: get one from [Metaphor/Exa](https://metaphor.systems/) (Exa is the current platform).
- **Google Gemini API key**: create one in [Google AI Studio](https://aistudio.google.com/app/apikey).

Optional environment variables if you prefer not to enter keys in the UI:

```powershell
$env:METAPHOR_API_KEY = "your_exa_or_metaphor_api_key"
$env:GEMINI_API_KEY   = "your_gemini_api_key"
```

When the app starts, you can also paste keys into the `API Configuration` section. The app prefers the UI‑entered keys; if omitted, it falls back to the environment variables above.

## Usage

1. Open the app in your browser after launching.
2. Enter blog keywords, choose post type, tone, and language.
3. Click **Write Blog Post** to generate.
4. The output includes the article body, FAQs, visual suggestions, and SEO metadata.

## Limitations

- Output quality depends on inputs and on search result relevance.
- FAQs are LLM‑generated (guided by SERP context), not guaranteed to match Google PAA exactly.
- API usage for Exa/Metaphor and Gemini may be rate‑limited or billable.

## Roadmap ideas

- Switchable LLMs and search providers.
- Feedback loop to refine style and on‑page SEO.
- More controls for outline and metadata.

---

Contributions and feedback are welcome. Please open issues or PRs to help improve Alwrity.
