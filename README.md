# Telugu Voice-Based Government Scheme Agent 🏛️

## 📝 Overview
A voice-first agentic AI system designed to help Telugu-speaking users in rural Telangana discover and apply for government welfare schemes. 

This project was built to demonstrate a **Level 3 AI Agent** that can:
1.  🗣️ **Listen & Speak:** Full Speech-to-Text (STT) and Text-to-Speech (TTS) pipeline in Telugu.
2.  🧠 **Reason:** Uses an LLM to autonomously decide when to ask for more info, check eligibility, or execute an application.
3.  💾 **Act:** Writes successful applications to a local mock database (`applications.csv`), simulating a real government portal submission.

## 🚀 Key Features
* **Native Language Support:** Optimized for Telugu (te-IN) interaction.
* **Agentic Workflow:** Built with **LangGraph** (Planner-Executor-Evaluator loop).
* **Persistence:** Saves application data to a CSV file as "proof of work."
* **Robustness:** Handles network errors, silence, and ineligible scenarios gracefully.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Orchestration:** LangChain & LangGraph
* **LLM:** Kwaipilot/KAT-Coder-Pro (via OpenRouter)
* **Voice Pipeline:** Google SpeechRecognition (STT) & gTTS (TTS)
* **Tools:** Python (CSV handling, Logic filtering)

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-link>
    cd telugu_agent
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**
    * Open `agent.py` and ensure `OPENROUTER_API_KEY` is set.

4.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

5.  **Usage**
    * Click the "Tap to Speak" button.
    * Speak in Telugu (e.g., "Naa vayasu 50, nenu Raithu").
    * The agent will reply with audio and text.
    * If you apply, check the `applications.csv` file for the record!

## 📂 Project Structure
```text
├── app.py              # Main Streamlit UI & Voice logic
├── agent.py            # LangGraph Brain configuration
├── tools.py            # Eligibility logic & CSV Writer tool
├── applications.csv    # Generated file (Mock Database)
└── requirements.txt    # Python dependencies