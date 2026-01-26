// Simple state for session ID (reset on page reload is fine for now)
let currentThreadId = null;

export const runQuery = async (query, humanChoice = null, token = null, dbUrl = null) => {
  try {
    const payload = { query };
    if (currentThreadId) {
        payload.thread_id = currentThreadId;
    }
    if (humanChoice !== null) {
        payload.human_choice = humanChoice;
    }
    if (token) {
        payload.token = token;
    }
    if (dbUrl) {
        payload.db_url = dbUrl;
    }

    const response = await fetch('http://localhost:8000/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Update thread ID if provided
    if (data.thread_id) {
        currentThreadId = data.thread_id;
    }
    
    return data;
  } catch (error) {
    console.error("API Error:", error);
    return {
        role: "system",
        content: `Error connecting to backend: ${error.message}. Is the server running?`,
        reasoning: [],
        sql: null,
        data: null
    };
  }
};
