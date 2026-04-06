# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Trần Trung Hậu
- **Student ID**: 2A202600317
- **Date**: 6/4/2026

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implementated**: `src/tools/searching.py`, `src/tools/search_recipe.py`
- **Code Highlights**:
  - In `src/tools/searching.py`: integrated Tavily search (`max_results=5`), extracted `response['results']`, and formatted each returned item into numbered text blocks for the agent.
  - Added empty-result handling in `searching.py` with fallback message: `No results found for this query.` so the agent can reason safely when retrieval fails.
  - In `src/tools/search_recipe.py`: implemented `search_recipes(query)` as a recipe-focused wrapper around `search()`, enriching the query and returning domain-oriented output for cooking requests.
- **Documentation**:
  - The ReAct loop calls tools when it needs external knowledge; these two files provide that observation channel.
  - `search_recipe.py` routes food-related intents to retrieval logic, while `searching.py` performs the actual web lookup and result formatting.
  - The formatted search output is fed back as `Observation`, helping the model produce a more grounded final answer.

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: During ReAct execution, the agent frequently produced incorrect tool calls (missing/invalid query argument) and in some runs did not call any tool at all, even when external information was required.
- **Log Source**: `logs/2026-04-06.log`
- **Diagnosis**: The main issue came from unstable action formatting and weak tool-call constraints in the prompt/parser boundary. As a result, the model sometimes generated malformed `Action` inputs or skipped the tool-calling step and answered directly.
- **Solution**: I debugged the tool-calling flow by validating input before execution, tightening the action format expectation in prompt instructions, and improving query construction in `src/tools/searching.py` and `src/tools/search_recipe.py` so tool calls are more consistent and usable.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1.  **Reasoning**: How did the `Thought` block help the agent compared to a direct Chatbot answer? <br>
    **Answer**: The `Thought` block made the reasoning process explicit before taking an action. Instead of answering immediately like a direct chatbot, the agent could decide whether external information was needed, then choose an appropriate tool call. This improved answer quality for recipe questions because retrieval was triggered more intentionally.

2.  **Reliability**: In which cases did the Agent actually perform *worse* than the Chatbot? <br>
    **Answer**: The agent performed worse when the tool calls were malformed or when the model failed to call tools at all. In those cases, the agent's answer was often less accurate than a direct chatbot response because it either produced an invalid query or skipped retrieval, leading to hallucinated or incomplete answers.
3. **Observation**: How did the environment feedback (observations) influence the next steps? <br>
   **Answer**: Observations were critical because they grounded the next reasoning step with retrieved evidence. When observations were clear and relevant, the agent could refine and finalize answers confidently. When observations were weak or empty, the agent either produced vague follow-up actions or lower-quality final responses, showing that observation quality directly impacted decision quality.
---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Standardize all tools with a shared input/output schema (e.g., Pydantic) and move tool execution to an async task queue so the agent can handle many concurrent requests reliably.
- **Safety**: Add a tool-call guard layer that validates action format and required parameters before execution, plus a retry/fallback policy when a tool call is malformed or skipped.
- **Performance**: Introduce caching for repeated search queries and use a lightweight retrieval index (vector DB) to reduce external API calls and speed up response time in multi-tool scenarios.

---

> [!NOTE]
> Submit this report by renaming it to `REPORT_[YOUR_NAME].md` and placing it in this folder.
