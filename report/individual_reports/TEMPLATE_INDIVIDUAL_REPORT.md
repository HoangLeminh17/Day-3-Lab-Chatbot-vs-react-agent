# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- Name: **Nguyễn Đăng Hải**
- ID: **2A202600390**
- Date: **06-04-2026**

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
	- Agent often returned `Tools used: none` or always selected `estimate_cooking_time`, even when the user asked for web references.

- **Log Source**:
	- `logs/2026-04-06.log`
	- Main events analyzed: `AGENT_START`, `LLM_RESPONSE`, `AGENT_END`.

- **Diagnosis**:
	- Tool selection was sensitive to query wording and prompt constraints.
	- Runtime did not initially expose clear evidence of tool decisions in final output.
	- Search behavior can fail when search API key env var is incorrect.

- **Solution**:
	- Added both tools directly in `run_agent.py` tool registry.
	- Updated `agent.py` to always append `Tools used: ...` for transparent trace.
	- Switched to explicit evaluation prompts:
		- cooking time queries -> expect `estimate_cooking_time`
		- source/reference/latest queries -> expect `search`

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
