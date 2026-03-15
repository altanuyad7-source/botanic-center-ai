# 🏢 Community Democracy AI (Botanic Center Town Prototype)

An open-source, AI-powered governance and transparency tool designed to solve communication bottlenecks in micro-democracies like apartment owners' associations and neighborhood councils.

## ⚠️ The Problem: Bottlenecked Micro-Democracies
In our community of 480 families (roughly 2,000 residents) in Ulaanbaatar, Mongolia, democratic participation breaks down at the administrative bottleneck. We have one General Manager handling all infrastructure, finance, and community requests. 

When a single manager is overwhelmed by unstructured complaints across multiple channels, data-driven planning becomes impossible. Transparency vanishes, residents feel unheard, and unnecessary arguments replace constructive community building.

## 💡 The Solution: AI-Powered Transparency
This prototype demonstrates how modern Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) can empower under-resourced communities to govern effectively. 

By automating ticket triage, categorizing sentiment, and allowing residents to query official financial and governance documents, this system allows a 1-to-2 person management team to operate with the efficiency and transparency of a full municipal staff.

### Core Features
* **Intelligent Request Intake (Triage):** Residents submit issues in natural language (English or Mongolian). The LLM instantly extracts the category, urgency, and sentiment, translating it if necessary.
* **Institutional Memory (RAG):** Residents can ask questions like *"How was our money spent?"* and the AI will generate answers strictly based on the community's official PDFs (Bylaws, Financial Reports).
* **Resident Dashboard:** A public-facing transparency portal showing real-time budget tracking, major community issues, and upcoming democratic priorities for residents to upvote.
* **Manager Dashboard:** An internal operations view that aggregates complaint trends, tracks community satisfaction, and helps the manager draft automated, context-aware responses to residents.

## 🛠️ Tech Stack (Prototype)
* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Orchestration:** [LlamaIndex](https://www.llamaindex.ai/)
* **LLM & Embeddings:** OpenAI (`gpt-4o-mini`, `text-embedding-3-small`)
* **Data Processing:** Pandas & PyPDF

*(Note: The production version aims to migrate to Next.js and Supabase/pgvector for secure, scalable deployment).*

---

## 🚀 How to Run the Prototype Locally

If you would like to test this prototype on your local machine, follow these steps:

### 1. Clone the repository
`git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME`

### 2. Install dependencies
Ensure you have Python installed, then run:
`pip install streamlit pandas openai llama-index pypdf`

###3. Add Community Documents
Create a folder named data in the root directory. Place at least one PDF inside this folder (e.g., a dummy financial report or HOA rules document). The RAG engine requires this to build its index on startup.

`mkdir data
 Add your PDF files into the /data folder`

### 4. Set your API Key
The application requires an OpenAI API key to run the LLM and Embedding models. Open logic.py and replace the placeholder string with your valid API key:
`os.environ["OPENAI_API_KEY"] = "sk-your-api-key-here"`

### 5. Launch the App
`streamlit run app.py`

The application will build the document vector index and launch the dashboards in your default web browser at http://localhost:8501.

### 🤝 Open Source Commitment
This prototype was built as a proof-of-concept for the Mozilla Foundation Democracy x AI Cohort. If fully funded, the underlying architecture will be open-sourced to allow other under-resourced communities, HOAs, and neighborhood councils worldwide to deploy their own localized democracy management tools.
