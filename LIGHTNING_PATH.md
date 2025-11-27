## RAG Lightning Path: n8n + LangChain + Chroma (≈ 1 hour)

This guide shows you how to go from zero to a working **chat UI in n8n** that talks to a **RAG backend** built with **LangChain + Chroma + OpenAI**.

You will:
- Build a vector database from `data/books/alice_in_wonderland.md`
- Query it from Python
- Connect n8n’s chat UI to the RAG backend via a simple CLI

---

### 0. Prerequisites (≈ 5 minutes)

- **Python**: 3.10+ installed
- **Node.js**: 18.17+ installed (for n8n)
- **OpenAI API key**

From the project root:

```bash
# (Optional) create & activate a virtualenv
pip install -r requirements.txt
pip install "unstructured[md]"
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
```

---

### 1. Build the vector database with LangChain + Chroma (≈ 10 minutes)

The script `create_database.py` will:
- Load markdown files from `data/books/`
- Split them into overlapping chunks
- Embed them with `OpenAIEmbeddings`
- Store them in a local Chroma DB under `chroma/`

Run:

```bash
python create_database.py
```

You should see output indicating how many chunks were created and saved.

---

### 2. Query the database from Python (≈ 10–15 minutes)

You can use the existing CLI script to sanity-check that your RAG pipeline works end-to-end:

```bash
python query_data.py "How does Alice meet the Mad Hatter?"
```

This will:
- Load the persisted Chroma DB from `chroma/`
- Retrieve the most relevant chunks
- Ask an OpenAI chat model to answer using only that context

---

### 3. Use `rag_cli.py`: a JSON-based RAG CLI for n8n (≈ 10 minutes)

The file `rag_cli.py` wraps the same RAG logic but prints **exactly one JSON object** to stdout:

```jsonc
{
  "answer": "<final answer text>",
  "sources": ["data/books/alice_in_wonderland.md", "..."]
}
```

Try it:

```bash
python rag_cli.py "How does Alice meet the Mad Hatter?"
```

This JSON shape is what the n8n workflow expects.

---

### 4. Start n8n (≈ 5 minutes)

From any terminal:

```bash
npx n8n
```

Then open `http://localhost:5678` in your browser.

You can also follow the more detailed options in `N8N_SETUP.md` if you prefer a global install or Docker.

---

### 5. Import and run the RAG chat workflow in n8n (≈ 15–20 minutes)

1. In the n8n UI, click **“Import from File”**.
2. Select `n8n_workflow.json` from this repository.
3. Open the imported workflow and inspect the nodes:
   - **`When chat message received`**: provides a chat UI and exposes `chatInput`.
   - **`Execute RAG CLI`**: runs  
     `python rag_cli.py "{{ $json.chatInput }}"`  
     in the workflow’s working directory.
   - **`Code in JavaScript`**: parses the JSON from `rag_cli.py` and formats:
     - The answer
     - The list of sources (files) used
4. Click **“Activate”** or **“Execute Workflow”** (depending on your n8n version).
5. Open the chat panel in the top-right, say **“hi”**, then ask something about Alice in Wonderland, e.g.:

   > How does Alice meet the Mad Hatter?

You should see a grounded answer plus a list of source files.

---

### 6. Where to go next

Once this Lightning Path works end-to-end, you can:

- **Swap documents**: drop your own `.md` files into `data/books/`, re-run `create_database.py`, and chat with your own docs.
- **Turn the CLI into an API**: wrap the RAG call in a small FastAPI/Flask app and call it from n8n with an HTTP Request node instead of `Execute Command`.
- **Add more tools/agents in n8n**: now that you have a solid RAG backbone, you can re-introduce more advanced Agent nodes and tools on top.
