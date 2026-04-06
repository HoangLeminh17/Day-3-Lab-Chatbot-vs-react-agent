import re
from typing import List, Dict, Any
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger


class ReActAgent:
    """A ReAct-style agent with Thought-Action-Observation loop."""

    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        tool_descriptions = "\n".join([f"- {t['name']}: {t['description']}" for t in self.tools])
        return f"""
You are an expert in cuisine, cooking, and nutrition.
Here is a list of tools you can use to answer user queries:
{tool_descriptions}

Instructions:
- Analyze ingredients and cooking context carefully.
- Call tools only when needed.
- You can call tools a maximum of 1 time.

Output format:
Thought: your reasoning
Action: tool_name(arguments)
Observation: result of the tool call
Final Answer: your final response
"""

    def run(self, user_input: str) -> str:
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})

        current_prompt = f"User Query: {user_input}\n\n"
        steps = 0

        while steps < self.max_steps:
            result = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
            logger.log_event("LLM_RESPONSE", {"step": steps, "output": result["content"]})

            final_match = re.search(r"Final Answer:\s*(.*)", result["content"], re.IGNORECASE | re.DOTALL)
            if final_match:
                final_answer = final_match.group(1).strip()
                logger.log_event("AGENT_END", {"steps": steps, "final_answer": final_answer})
                return final_answer

            action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", result["content"])
            if action_match:
                tool_name = action_match.group(1)
                args_str = action_match.group(2)
                observation = self._execute_tool(tool_name, args_str)
                current_prompt += f"{result['content']}\nObservation: {observation}\n\n"
            else:
                logger.log_event("AGENT_END", {"steps": steps, "reason": "No action"})
                return result["content"]

            steps += 1

        logger.log_event("AGENT_END", {"steps": steps, "reason": "Max steps"})
        return "Agent stopped: Max steps reached."

    def _execute_tool(self, tool_name: str, args: str) -> str:
        for tool in self.tools:
            if tool["name"] == tool_name:
                parsed_args = self._parse_args(args)
                try:
                    result = tool["fn"](**parsed_args)
                    return str(result)
                except Exception as e:
                    return f"Error executing {tool_name}: {str(e)}"
        return f"Tool {tool_name} not found."

    def _parse_args(self, args_str: str) -> Dict[str, Any]:
        args: Dict[str, Any] = {}
        if not args_str.strip():
            return args

        parts = re.split(r",\s*(?=(?:[^\'\"]*[\'\"][^\'\"]*[\'\"])*[^\'\"]*$)", args_str)
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                key = key.strip()
                value = value.strip()

                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

                try:
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass
                args[key] = value

        return args