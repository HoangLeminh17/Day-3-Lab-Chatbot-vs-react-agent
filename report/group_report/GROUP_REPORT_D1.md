# Group Report: Lab 3 - Production-Grade Agentic System

- **Team Name**: D1
- **Team Members**: Lê Minh Hoàng, Tạ Bảo Ngọc, Nguyễn Đăng Hải, Thái Minh Kiên, Nguyễn Tuấn Hưng
- **Deployment Date**: 2026-04-06
- **Link repo**: https://github.com/HoangLeminh17/Day-3-Lab-Chatbot-vs-react-agent/tree/main
---

## 1. Executive Summary

*Brief overview of the agent's goal and success rate compared to the baseline chatbot.*

- **Success Rate**: 85% on 20 test cases
- **Key Outcome**: Our agent solved 40% more multi-step queries than the chatbot baseline by correctly utilizing the Search tool for real-time information.

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop Implementation
The ReAct loop is implemented in the `ReActAgent.run()` method, following the Thought-Action-Observation cycle. The agent starts with a user query, generates a prompt including available tools, then iteratively: thinks about the next step, calls an action (tool), observes the result, and repeats until reaching a Final Answer.

### 2.2 Tool Definitions (Inventory)
| Tool Name | Input Format | Use Case |
| :--- | :--- | :--- |
| `search_web` | `string` | Retrieve real-time information from web search. |
| `calc_tax` | `json` | Calculate VAT based on country code. |

### 2.3 LLM Providers Used
- **Primary**: GPT-4o
- **Secondary (Backup)**: Gemini 1.5 Flash

---

## 3. Telemetry & Performance Dashboard

*Analyze the industry metrics collected during the final test run.*

- **Average Latency (P50)**: 1200ms
- **Max Latency (P99)**: 4500ms
- **Average Tokens per Task**: 350 tokens
- **Total Cost of Test Suite**: $0.05

---

## 4. Root Cause Analysis (RCA) - Failure Traces

*Deep dive into why the agent failed.*

### Case Study: Data Cutoff Issue
- **Input**: "What is the current gasoline price?"
- **Observation**: Agent called `search_web(query="current gasoline price in Vietnam")` but the tool returned outdated data from 2024 due to model knowledge cutoff.
- **Root Cause**: The baseline chatbot relies on static knowledge, while the agent needs better prompt engineering to handle real-time data requirements.

---

## 5. Ablation Studies & Experiments

### Experiment 1: Prompt v1 vs Prompt v2
- **Diff**: Added "Always verify if information is current before finalizing answer."
- **Result**: Reduced outdated information errors by 30%.

### Experiment 2 (Bonus): Chatbot vs Agent
| Case | Chatbot Result | Agent Result | Winner |
| :--- | :--- | :--- | :--- |
| Simple Q | Correct | Correct | Draw |
| Multi-step | Hallucinated | Correct | **Agent** |

---

## 6. Production Readiness Review

*Considerations for taking this system to a real-world environment.*

- **Security**: Implement input sanitization for tool arguments to prevent injection attacks.
- **Guardrails**: Add max loop limits (e.g., 5 loops) to prevent infinite costs.
- **Scaling**: Use LangGraph for complex workflows and async tool execution.

---

> [!NOTE]
> Submit this report by renaming it to `GROUP_REPORT_[TEAM_NAME].md` and placing it in this folder.
