import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import re
from typing import List, Dict, Any, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger

class ReActAgent:
    """
    SKELETON: A ReAct-style Agent that follows the Thought-Action-Observation loop.
    Students should implement the core loop logic and tool execution.
    """
    
    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        """
        TODO: Implement the system prompt that instructs the agent to follow ReAct.
        Should include:
        1.  Available tools and their descriptions.
        2.  Format instructions: Thought, Action, Observation.
        """
        tool_descriptions = "\n".join([f"- {t['name']}: {t['description']}" for t in self.tools])
        return f"""
        You are an intelligent assistant. You have access to the following tools:
        {tool_descriptions}

        Use the following format:
        Thought: your line of reasoning.
        Action: tool_name(arguments)
        Observation: result of the tool call.
        ... (repeat Thought/Action/Observation if needed)
        Final Answer: your final response.
        """

    def run(self, user_input: str) -> str:
        """
        TODO: Implement the ReAct loop logic.
        1. Generate Thought + Action.
        2. Parse Action and execute Tool.
        3. Append Observation to prompt and repeat until Final Answer.
        """
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})
        
        current_prompt = f"User Query: {user_input}\n\n"
        steps = 0

        while steps < self.max_steps:
            # Generate LLM response
            result = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
            logger.log_event("LLM_RESPONSE", {"step": steps, "output": result["content"]})

            # Check for Final Answer
            final_match = re.search(r"Final Answer:\s*(.*)", result["content"], re.IGNORECASE | re.DOTALL)
            if final_match:
                final_answer = final_match.group(1).strip()
                logger.log_event("AGENT_END", {"steps": steps, "final_answer": final_answer})
                return final_answer
            
            # Parse Action from result
            action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", result["content"])
            if action_match:
                tool_name = action_match.group(1)
                args_str = action_match.group(2)

                # Execute tool
                observation = self._execute_tool(tool_name, args_str)

                # Append to prompt
                current_prompt += f"{result['content']}\nObservation: {observation}\n\n"
            else:
                # No action found, return last response
                logger.log_event("AGENT_END", {"steps": steps, "reason": "No action"})
                return result["content"]
        
            steps += 1
            
        logger.log_event("AGENT_END", {"steps": steps, "reason": "Max steps"})
        return "Agent stopped: Max steps reached."

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Helper method to execute tools by name.
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                # Parse args and call function
                parsed_args = self._parse_args(args)
                try:
                    result = tool['fn'](**parsed_args)
                    return str(result)
                except Exception as e:
                    return f"Error executing {tool_name}: {str(e)}"
        return f"Tool {tool_name} not found."

    def _parse_args(self, args_str: str) -> Dict[str, Any]:
        """
        Simple argument parser for tool calls.
        Supports: key='value', key=value, key="value"
        """
        args = {}
        if not args_str.strip():
            return args
        
        # Split by comma, but handle quotes
        parts = re.split(r',\s*(?=(?:[^\'"]*[\'"][^\'"]*[\'"])*[^\'"]*$)', args_str)
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                # Try to convert to int/float
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass
                args[key] = value
        return args
