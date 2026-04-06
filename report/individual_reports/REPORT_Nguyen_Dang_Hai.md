# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- Name: **Nguyễn Đăng Hải**
- ID: **2A202600390**
- Date: **06-04-2026**
- Link repo: **https://github.com/HoangLeminh17/Day-3-Lab-Chatbot-vs-react-agent/tree/haind**

---

## I. Technical Contribution (15 Points)

*Describe your specific contribution to the codebase (e.g., implemented a specific tool, fixed the parser, etc.).*

- **Modules Implementated**:
	- `src/tools/cooking_time.py`: implemented a rule-based tool `estimate_cooking_time`.
	- `run_agent.py`: integrated tool registry with `estimate_cooking_time` and `search`.
	- `src/agent/agent.py`: added tool usage trace in final answer (`Tools used: ...`).

- **Code Highlights**:
	- Built `estimate_cooking_time(...)` with inputs: `dish_type`, `technique`, `ingredients_count`, `servings`, `complexity`, `marinate_minutes`, `needs_thawing`, `needs_preheat`.
	- Added logic to normalize cooking techniques and estimate time ranges.
	- Improved observability by appending tool usage summary to every final response.

- **Documentation**:
	- ReAct loop flow in my implementation:
		1. Agent receives user query.
		2. LLM outputs `Thought` and optional `Action`.
		3. If `Action` exists, agent executes tool and writes `Observation`.
		4. Agent loops until `Final Answer`.
		5. Output includes `Tools used` for debugging and grading evidence.

---

## II. Debugging Case Study (10 Points)

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**:
  - In early runs, the agent often failed to choose the correct tool. For cooking questions, it sometimes returned `Tools used: none`; for source-seeking questions, it could still prefer `estimate_cooking_time` instead of `search`.

- **Log Source**:
  - `logs/2026-04-06.log`
  - I reviewed the structured events `AGENT_START`, `LLM_RESPONSE`, and `AGENT_END` to see which tool the model selected and whether the loop terminated correctly.

- **Diagnosis**:
  - The failure was caused by weak tool routing, not by a syntax bug.
  - The system prompt originally emphasized cooking-related behavior more strongly, so the model biased toward `estimate_cooking_time`.
  - Tool selection was also sensitive to query wording, so vague or short questions led to no action or the wrong action.
  - Without explicit tool trace output, it was difficult to confirm what the agent had actually used.

- **Solution**:
  - I added both `estimate_cooking_time` and `search` to the runtime tool registry in `run_agent.py`.
  - I updated `src/agent/agent.py` so the final answer always includes `Tools used: ...`, which makes tool selection visible in the output.
  - I also refined how I tested the agent:
    - cooking-time questions should trigger `estimate_cooking_time`
    - reference / latest / source-based questions should trigger `search`

- **Result**:
  - The agent became easier to debug because every response now shows which tool was used.
  - This also improved grading transparency because the trace clearly demonstrates the agent’s decision path.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflect on the reasoning capability difference.*

1.  **Reasoning**:
	- `Thought` helps the model break complex questions into steps before answering.
	- ReAct is more suitable than a plain chatbot for tasks that need tools and external facts.
2.  **Reliability**:
	- Agent can be worse on simple questions due to action/parse overhead.
	- If tool descriptions are weak, the model may choose wrong tools.
3.  **Observation**:
	- `Observation` provides grounding from tool outputs and reduces hallucination risk.
	- It directly improves next-step decision quality in the loop.

---

## IV. Future Improvements (5 Points)

*How would you scale this for a production-level AI agent system?*

- **Scalability**:
	- Add a lightweight intent router before ReAct to choose tools more consistently.
	- Support async execution for I/O tools such as web search.
- **Safety**:
	- Add schema validation for action arguments before tool execution.
	- Add allow-list guardrails for valid tool names.
- **Performance**:
	- Cache repeated web search queries.
	- Reuse recent observations in-session to reduce repeated tool calls.

---

> [!NOTE]
> Submit this report by renaming it to `REPORT_[YOUR_NAME].md` and placing it in this folder.
