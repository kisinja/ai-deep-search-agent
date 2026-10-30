# AI Search Agent

### A multi-source research agent that turns one question into a synthesized, evidence-aware answer

![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20Workflow-1C3C3C)
![LangChain](https://img.shields.io/badge/LangChain-LLM%20Integration-1C3C3C)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000)
![License](https://img.shields.io/badge/License-To%20Be%20Added-lightgrey)

---

## Overview

**AI Search Agent** is a multi-source research application built with **LangGraph, LangChain, Ollama, and Pydantic**. It accepts a natural-language question, gathers information from web and community sources, evaluates the retrieved Reddit discussion, and produces a structured final answer based on multiple perspectives.

The project demonstrates how an LLM can be used as part of a controlled, observable workflow—not only as a chatbot, but as a research agent responsible for searching, filtering, analyzing, and synthesizing information.

### Problem it solves

General-purpose search can leave users with:

- Dozens of disconnected links
- Conflicting results across sources
- Important context buried in community discussions
- No clear separation between factual research and real-world experiences
- Time-consuming manual comparison of search results

AI Search Agent addresses this workflow by coordinating multiple research stages and combining web findings with Reddit posts and top-level community comments into one coherent response.

---

## Key Features

- **Graph-based agent orchestration** — LangGraph models search, analysis, and synthesis as a typed stateful workflow.
- **Parallel multi-source research** — Google, Bing, and Reddit research branches launch from the graph's starting state.
- **Local LLM inference** — Ollama runs the language model privately on the user's machine.
- **Structured Reddit post selection** — Pydantic validates the LLM's selection of the most relevant Reddit URLs.
- **Deep Reddit retrieval** — PullPush provides Reddit search results, while Reddit's public JSON endpoint supplies full post text and top comments.
- **Source-specific analysis** — Separate LLM passes extract insights from Google, Bing, and Reddit content.
- **Evidence-aware synthesis** — The final prompt combines source analyses, identifies complementary perspectives, and highlights contradictions or uncertainty.
- **Interactive CLI experience** — Users can ask multiple questions in a continuous terminal session.
- **Environment-based configuration** — API credentials are loaded through environment variables.

---

## Architecture

```text
                             ┌───────────────┐
                             │ User Question │
                             └───────┬───────┘
                                     │
                             ┌───────▼────────┐
                             │ LangGraph State │
                             └───────┬────────┘
                                     │
                 ┌───────────────────┼───────────────────┐
                 ▼                   ▼                   ▼
          Google Search       Bing Search          Reddit Search
                 │                   │                   │
                 └───────────────────┼───────────────────┘
                                     ▼
                        Analyze & Rank Reddit URLs
                                     │
                                     ▼
                         Retrieve Posts + Comments
                                     │
                 ┌───────────────────┼───────────────────┐
                 ▼                   ▼                   ▼
       Google Analysis       Bing Analysis       Reddit Analysis
                 │                   │                   │
                 └───────────────────┼───────────────────┘
                                     ▼
                         Final Multi-Source Synthesis
                                     │
                                     ▼
                            Comprehensive Answer
```

### Workflow stages

1. **Receive the question**  
   The application stores the user prompt in a typed LangGraph state alongside search and analysis fields.

2. **Collect research from multiple branches**  
   The graph executes Google, Bing, and Reddit search nodes from the initial state. Google and Bing search currently use the Tavily web-search API, while Reddit uses the free PullPush API.

3. **Rank Reddit discussions**  
   Search results are passed through an LLM with Pydantic structured output. The model returns a list of URLs judged most relevant to the original question.

4. **Retrieve community context**  
   The selected Reddit URLs are resolved to public `.json` endpoints. Post titles, self-text, metadata, and up to 15 top-level comments are collected.

5. **Perform source-specific analysis**  
   Dedicated prompt paths extract authoritative facts from Google and Bing results and real-world experiences, opinions, debates, and practical advice from Reddit.

6. **Synthesize the final answer**  
   A final LLM prompt combines all analyses, compares perspectives, and returns a balanced, well-structured response.

---

## Tech Stack

| Technology | Role |
|---|---|
| **Python 3.14+** | Core application language |
| **LangGraph** | Stateful agent orchestration, branching, and execution flow |
| **LangChain** | Chat-model initialization and message abstractions |
| **Ollama** | Local LLM runtime |
| **Qwen 3.5 2B** | Local model used for structured selection, analysis, and synthesis |
| **Tavily** | Web search provider used by the search abstraction |
| **PullPush API** | Free Reddit submission search |
| **Reddit Public JSON** | Full Reddit post and comment retrieval |
| **Pydantic** | Structured output schema for relevant Reddit URLs |
| **python-dotenv** | Environment-variable loading |
| **uv** | Dependency and virtual-environment management |

---

## Project Structure

```text
ai-search-agent/
├── pyproject.toml              # Package metadata and dependencies
├── uv.lock                     # Reproducible dependency lock file
├── .env                        # Local API keys (not committed)
└── src/
    └── ai_search_agent/
        ├── __init__.py         # Package entry point
        ├── main.py             # LangGraph workflow and interactive CLI
        ├── llm.py              # Ollama model configuration
        ├── prompts.py          # Analysis and synthesis prompt templates
        └── web_operations.py   # Tavily and Reddit integrations
```

---

## Getting Started

### Prerequisites

- Python **3.14 or newer**
- [`uv`](https://docs.astral.sh/uv/) for environment and dependency management
- [Ollama](https://ollama.com/) installed and running
- A Tavily API key

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ai-search-agent
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Install and start the local model

```bash
ollama pull qwen3.5:2b
ollama serve
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
```

> Keep `.env` private and never commit API keys or credentials to source control.

### 5. Run the agent

```bash
uv run python src/ai_search_agent/main.py
```

Enter a research question at the prompt:

```text
Ask me anything:
```

Type `exit` to end the session.

---

## Example Usage

```text
Ask me anything: What should a developer consider when choosing between FastAPI and Django?

Starting parallel research process...
Launching Google, Bing, and Reddit searches...

Searching Google for: What should a developer consider when choosing between FastAPI and Django?
Searching Bing for: What should a developer consider when choosing between FastAPI and Django?
Searching Reddit for: What should a developer consider when choosing between FastAPI and Django?

Selected URLs:
   1. https://www.reddit.com/r/.../fastapi_vs_django/

Final Answer:
[Synthesized comparison of performance, ecosystem, development conventions, community
experience, API use cases, admin requirements, and trade-offs from all source analyses]
```

> The exact research results and final wording will vary based on live search data and the local model's output.

---

## Technical Highlights

### Graph-driven agent workflow

The application uses `StateGraph` to make search, retrieval, and synthesis explicit and inspectable. Typed state is passed between nodes instead of burying agent coordination in a single monolithic prompt.

### Parallel research fan-out

Google, Bing, and Reddit searches originate from the graph's start node, enabling independent research branches before downstream processing.

### Structured model output

Rather than parsing loosely generated URL text, Reddit post selection uses a Pydantic schema through LangChain's structured-output interface. This reduces integration errors and makes downstream retrieval more reliable.

### Local-first LLM design

Ollama keeps inference local and removes an API dependency for model execution. The workflow therefore separates:

- **External information retrieval** — Tavily and Reddit
- **Local model reasoning** — analysis and synthesis
- **Application orchestration** — LangGraph state and edges

### Separation of responsibilities

The codebase separates workflow logic (`main.py`), model configuration (`llm.py`), prompts (`prompts.py`), and external integrations (`web_operations.py`) to keep agent behavior easier to extend and evaluate.

---

## What I Learned

Building this project provided hands-on experience with:

- Designing agent workflows with explicit graph nodes and shared state
- Coordinating fan-out and fan-in research stages
- Using structured output to constrain LLM behavior
- Combining web search with community-generated evidence
- Writing specialized prompts for independent analysis tasks
- Designing prompts that preserve uncertainty and conflicting viewpoints
- Integrating a local LLM with LangChain and LangGraph
- Working with third-party APIs and handling partial search or retrieval failures
- Structuring a Python package with `uv` and environment configuration

---

## Known Design Limitations

- The Google and Bing branches currently share the Tavily search abstraction rather than calling separate search engines directly.
- Live API failures are handled locally, but results are not retried through a formal retry policy.
- Reddit retrieval currently limits detailed post analysis to the top 15 top-level comments.
- The CLI does not yet expose source links, citations, confidence scores, or the intermediate graph state by default.
- The response is based on live external data and may change over time.
- There is no automated evaluation harness for answer quality, source relevance, or hallucination detection.

---

## Future Improvements

- [ ] Add separate Google, Bing, and Reddit provider adapters
- [ ] Add streaming output for model analysis and final synthesis
- [ ] Return source-level citations and clickable references
- [ ] Add token usage, latency, and trace metadata
- [ ] Add retries, timeouts, and provider fallback policies
- [ ] Evaluate answer quality with custom RAG/agent metrics
- [ ] Add semantic deduplication across search sources
- [ ] Support recursive Reddit comment retrieval with relevance ranking
- [ ] Add model and provider configuration through CLI arguments
- [ ] Add FastAPI or a web interface for broader application access
- [ ] Add unit and integration tests for graph nodes and API integrations
- [ ] Add persisted conversation and research history

---

## Contributing

Contributions, issue reports, and feature ideas are welcome. For substantial changes, please open an issue first to discuss the proposed design.

---

## License

License information is not yet included. A license may be added before this project is published publicly.
