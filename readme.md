# ResearchMind AI

A multi-agent research pipeline with a Streamlit UI. Give it a topic, and four specialized agents handle the rest — searching, scraping, writing, and critiquing — before handing you a finished report.

---

## What it does

Most LLM research tools just throw a web search at the model and call it a day. This one chains four agents together, each with a specific job:

1. **Search Agent** — finds recent, reliable sources on your topic
2. **Reader Agent** — picks the most relevant URL from those results and scrapes it for the actual content
3. **Writer Chain** — combines the search results and scraped content into a structured research report
4. **Critic Chain** — reviews the report and returns honest feedback on quality, gaps, and accuracy

The UI shows you a live pipeline tracker so you know which agent is working at any given moment.

---

## Project structure

```
.
├── app.py          # Streamlit UI
├── pipeline.py     # Orchestrates the four-agent pipeline
├── agents.py       # Agent and chain definitions
└── requirements.txt
```

---

## Setup

Clone the repo and create a virtual environment:

```bash
git clone https://github.com/yourusername/researchmind-ai.git
cd researchmind-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set your API keys in a `.env` file (or however your `agents.py` expects them):

```
OPENAI_API_KEY=...
TAVILY_API_KEY=...   # or whichever search tool your search agent uses
```

Then run:

```bash
streamlit run app.py
```

---

## How the pipeline works

`pipeline.py` drives everything in four sequential steps. Each agent gets the output of the previous one as context — the reader knows what the search found, the writer gets both the search results and the scraped content, and the critic gets the full report.

```python
state["search_results"]  → search_agent
state["scraped_content"] → reader_agent  (uses search_results)
state["report"]          → writer_chain  (uses both above)
state["feedback"]        → critic_chain  (uses report)
```

You can run the pipeline directly from the terminal too:

```bash
python pipeline.py
# Enter a research topic: ...
```

---

## UI details

Built with Streamlit. A few things worth mentioning:

- The pipeline runs in a background thread so the status bar and step tracker stay live while agents are working
- The radar/particle animations in the idle state are pure CSS — no JS libraries
- Tailwind-inspired dark theme, custom fonts loaded from Google Fonts
- Results are split across a two-column layout (search + scraped) with full-width cards for the report and critic review
- Download button at the end exports the full run as a `.txt` file

---

## Customising agents

All agent and chain logic lives in `agents.py`. If you want to swap out the search tool, change the LLM, adjust prompts, or add more steps to the pipeline — that's the only file you need to touch. `pipeline.py` just calls the functions and passes state around.

---

## Requirements

- Python 3.10+
- Streamlit
- LangChain (or whichever framework your agents use)
- An LLM API key
- A search tool API key (Tavily, SerpAPI, etc.)

---

## Known issues / rough edges

- The step tracker advances on a fixed time interval, not actual agent completion — so if one agent is unusually fast or slow, the displayed step might be off
- Very long scraped pages get truncated to 2000 characters in the UI (the full content still goes to the writer)
- No streaming output yet — results appear all at once when the pipeline finishes

---

## License

MIT