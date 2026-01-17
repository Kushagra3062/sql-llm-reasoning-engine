# SQL LLM Agent with Human-in-the-Loop & self-Correction

A robust, agentic SQL query generator capable of handling complex reasoning, ambiguity detection, and self-correction. Built with **LangGraph**, **FastAPI**, and **React**.

## 🚀 Key Features

### 🧠 Advanced Reasoning
- **Multi-Step Planner**: Decomposes complex questions (e.g., "Find customers who bought Rock but not Jazz") into logical steps before generating SQL.
- **Self-Correction**: The Planner Agent validates its own plans against the schema. If it makes a mistake (e.g., missing `GROUP BY`), it catches the error and retries automatically.
- **Ambiguity Detection**: High-precision semantic analysis detects vague terms (e.g., "Top Artist", "Recent").
    - *Example*: "Best selling artist" triggers an interruption to ask: "By Revenue or By Quantity?"

### 👤 Human-in-the-Loop (HIL)
- **Interactive Clarification**: The system pauses execution when critical ambiguity is detected.
- **Frontend Integration**: Users are presented with multiple-choice options in the chat interface to resolve ambiguity, and the agent resumes execution with the chosen context.

### 🛡️ Robust Architecture
- **Schema-Aware**: Uses a compressed schema representation to minimize token usage while maintaining accuracy.
- **Safety Checks**: Validates generated SQL against a whitelist of allowed operations (read-only) before execution.
- **Error Handling**: Graceful handling of API rate limits (429) and database errors, with user-friendly feedback.

### ✨ Modern UI
- **React Frontend**: Clean, responsive interface with Markdown support.
- **Structured Reasoning**: Displays the agent's internal "thought process" (Plan, Steps, Assumptions) in a collapsible, verified UI component.
- **Data Visualization**: Renders SQL results in sortable, styled tables.

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js & npm
- A Groq API Key (or compatible LLM key)

### 1. Backend Setup
```bash
cd d:\sql_llm_agent
# Create virtual environment (optional but recommended)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# OR using uv
uv sync

# Set environment variables
# Create a .env file with:
# GROQ_API_KEY=your_key_here
```

### 2. Frontend Setup
```bash
cd d:\sql_llm_agent\frontend
npm install
```

---

## 🏃‍♂️ Usage

### Start the Backend
The FastAPI server runs on port `8000`.
```bash
# From root directory
uv run main.py
```

### Start the Frontend
The React app runs on port `5173`.
```bash
# From frontend directory
cd frontend
npm run dev
```

### Example Queries
1. **Simple**: "Show me all tracks by AC/DC."
2. **Ambiguous (Triggers HIL)**: "Who are the top artists?" (Agent will ask: By sales? By count?)
3. **Complex (Triggers Planner)**: "List customers who have purchased tracks from 'Rock' genre but never 'Jazz'."

---

## 📂 Project Structure

- `main.py`: Entry point. Defines the LangGraph workflow and FastAPI endpoints.
- `agents/`:
    - `dsds.py`: Ambiguity detection and Human-in-the-Loop logic.
    - `planner_agent.py`: High-level query planning and self-correction loop.
    - `answering_agent.py`: Final response synthesis.
- `frontend/`: React application source code.
    - `src/components/Chat`: Chat bubble and input components.
    - `src/components/Visualizations`: Reasoning accordion and SQL data tables.
- `tools/`: Database connection and execution tools.

## 🤝 Contributing
Feel free to open issues/PRs for improvements!
