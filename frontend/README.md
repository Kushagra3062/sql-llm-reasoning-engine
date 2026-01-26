# Text-to-SQL Frontend Demo

This is a premium React-based frontend for a Text-to-SQL system, developed as a demo for the "MarketWise" problem statement.

## Features
- **Modern Dark UI**: A "premium" look with smooth transitions and variables-based theming.
- **Reasoning Trace**: Visualizes the AI's "thought process" using an accordion.
- **Data Visualization**: Renders SQL and Result Tables clearly.
- **Schema Explorer**: Interactive sidebar to view database tables and columns.
- **Mock Demo Mode**: Simulates intelligent responses for specific demo queries.
- **Canned Queries**: Clickable sample queries in the sidebar.

## Setup
1. Install dependencies:
   ```bash
   npm install
   ```
2. Run the dev server:
   ```bash
   npm run dev
   ```

## Demo Scenarios
Try asking these questions to see the system in action:
1. **Simple**: "How many customers are from Brazil?"
2. **Moderate**: "Which 5 artists have the most tracks?"
3. **Reasoning**: "Which customers have never made a purchase?" (Shows complex LEFT JOIN logic)
4. **Ambiguous**: "Show me recent orders" (Triggers a clarifying question)
   - Follow up with: "Last year" or "2013"

## Project Structure
- `src/components/Chat`: Chat input, bubbles, thinking indicator.
- `src/components/Visualizations`: Special UI for Reasoning, SQL, and Tables.
- `src/components/Layout`: Sidebar and Main wrapper.
- `src/analysis/mockService.js`: Logic simulating the backend LLM/SQL engine.
