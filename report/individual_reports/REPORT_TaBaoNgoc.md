# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Tạ Bảo Ngọc 
- **Student ID**: 2A202600286
- **Date**: 06/04/2026

---

## I. Technical Contribution (15 Points)

*Implemented a robust `unit_converter` tool to handle kitchen-specific unit conversions within the ReAct loop.*

- **Modules Implementated**: `src/tools/unit_converter.py`
- **Code Highlights**:
  ```python
  def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
      # Normalize units
      from_unit = from_unit.lower().strip()
      to_unit = to_unit.lower().strip()

      # Define conversion factors to a base unit (Weight: gram, Volume: ml)
      weight_units = {'g': 1.0, 'gram': 1.0, 'kg': 1000.0, 'oz': 28.35, 'ounce': 28.35, 'lb': 453.59, 'pound': 453.59}
      volume_units = {'ml': 1.0, 'milliliter': 1.0, 'l': 1000.0, 'cup': 240.0, 'tbsp': 15.0, 'tsp': 5.0, 'fl oz': 29.57}

      # Combined units for easier lookup
      all_units = {**weight_units, **volume_units}
      
      # Convert to base unit -> Target unit logic...
  ```
- **Documentation**: The `unit_converter` tool is designed specifically for kitchen tasks, allowing the ReAct Agent to accurately convert measurements (e.g., cups to ml, or grams to ounces) during recipe generation. It handles unit normalization (lowercasing, stripping plural 's') and provides feedback for unsupported units, ensuring the Agent's reasoning remains grounded in accurate data.

---

## II. Debugging Case Study (10 Points)

*Troubleshooting the "Direct Answer" behavior where the Agent ignores tools.*

- **Problem Description**: When asked for a recipe with specific measurement conversions, the Agent (using Gemini-1.5-Flash) initially provided a direct response without following the ReAct sequence (Thought, Action, Observation).
- **Log Source**: `logs/2026-04-06.log`
  ```json
  {"timestamp": "2026-04-06T08:50:05.886350", "event": "LLM_RESPONSE", "data": {"step": 0, "output": "Chào bạn! Dưới đây là công thức cho món mì sốt cà chua..."}}
  ```
- **Diagnosis**: 
  1. The `tools` list in `run_agent.py` was empty during initialization, meaning the prompt built in `get_system_prompt` contained an empty list of available tools.
  2. The LLM (Gemini) defaulted to its internal knowledge base because the system prompt didn't strictly "force" a tool check when no tools were present, leading to a standard chatbot response instead of a ReAct sequence.
- **Solution**: 
  1. Correctly integrated the `unit_converter` tool into the `tools` list in `run_agent.py`.
  2. Updated the `system_prompt` to include safety rules like: *"NEVER output any measurements or recipe steps unless you have used a tool to get that data."*

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Reflection on the reasoning capability difference.*

1.  **Reasoning**: The `Thought` block acts as a "scratchpad" for the agent. In a standard Chatbot, the model often jumps to an answer based on statistical likelihood. In ReAct, the `Thought` forces the model to articulate *why* it needs a conversion (e.g., "The user asked for grams but the recipe uses cups, so I must first convert 2 cups to ml").
2.  **Reliability**: The ReAct Agent can perform *worse* than a Chatbot if the tool execution fails or if the argument parser is too strict. For instance, if the LLM outputs `Action: convert(2, 'cups', 'ml')` but the tool expects `value=2, from_unit='cups'`, the parser might fail, leading to an error observation that stalls the agent.
3.  **Observation**: Observations provide critical grounded feedback. When the tool returns "Error: Unit not supported", the Agent can pause, rethink its strategy, and perhaps try a different unit or admit limitation, rather than hallucinating an incorrect conversion.

---

## IV. Future Improvements (5 Points)

*Scaling the cooking agent for production.*

- **Scalability**: Implement a tool registry decorator (e.g., `@register_tool`) to allow dynamic scaling of the toolset without manually updating the `tools` list in `run_agent.py`.
- **Safety**: Introduce a "Sanity Check" tool that validates if measurements in the final recipe are realistic (e.g., preventing "100 tbsp of salt" due to a conversion error).
- **Performance**: Use a more robust regex or JSON-based action parsing to handle complex tool arguments, reducing parsing failures seen with simpler string manipulation.

---
