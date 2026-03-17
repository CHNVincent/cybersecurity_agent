from typing import List, Dict, Any, Optional
from ..brain.base import BaseLLM


class Planner:
    """
    Planning module for the cybersecurity agent
    Responsible for generating execution steps based on user goals and available skills
    """

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def generate_plan(
        self,
        goal: str,
        available_skills: List[Dict[str, Any]],
        conversation_context: Optional[List[Dict[str, str]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate an execution plan based on the user's goal and available skills

        Args:
            goal: The user's objective
            available_skills: List of available skills with their parameters
            conversation_context: Previous conversation messages for context

        Returns:
            List of steps in the execution plan
        """
        # Create a system message to guide the LLM in planning
        system_message = {
            "role": "system",
            "content": "You are a cybersecurity assistant. Your job is to create step-by-step execution plans for achieving user goals. "
            "Based on the provided goal and available tools (skills), create a sequential plan of actions. "
            "Each action should be represented as a dictionary with keys: "
            "'step_number': int, 'action': str (describe what to do), 'tool_name': str (if using a tool), "
            "'parameters': dict of required parameters, 'reason': str (why this step is needed), "
            "'depends_on_previous_step': bool.",
        }

        # Create the user message with the goal and available skills
        user_message = {
            "role": "user",
            "content": f"Please create an execution plan for the following goal: '{goal}'\n\n"
            f"Available tools/skills: {available_skills}\n\n"
            f"Please return only the plan as a JSON array without additional text.",
        }

        # Prepare messages for the LLM
        messages = [system_message, user_message]
        if conversation_context:
            # Make sure conversation_context is a list before slicing
            context_messages = (
                conversation_context[-5:] if len(conversation_context) > 0 else []
            )
            messages = (
                [system_message] + context_messages + [user_message]
            )  # Use last 5 messages as context

        # Call the LLM to generate the plan
        response = self.llm.chat(messages)

        # Extract the plan from the response
        plan_text = (
            response.get("choices", [{}])[0].get("message", {}).get("content", "")
        )

        # For now, return a simple mock plan - in a real implementation we'd parse the JSON response
        return self._parse_plan(plan_text, available_skills)

    def _parse_plan(
        self, plan_text: str, available_skills: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Parse the LLM response into a structured plan
        In a real implementation, this would properly parse JSON response
        """
        # For now, returning a mock response to avoid parsing complexity
        # In a real implementation, we would properly validate and parse the JSON output
        import re
        import json

        # Try to extract JSON array from the response
        try:
            # Look for JSON array in the response
            json_match = re.search(r"\[.*\]", plan_text, re.DOTALL)
            if json_match:
                plan_json_str = json_match.group(0)
                plan = json.loads(plan_json_str)
                # Verify that each step has required fields
                for step in plan:
                    if "action" not in step:
                        step["action"] = "Unknown action"
                    if "tool_name" not in step:
                        step["tool_name"] = None
                    if "parameters" not in step:
                        step["parameters"] = {}
                    if "reason" not in step:
                        step["reason"] = "N/A"
                    if "depends_on_previous_step" not in step:
                        step["depends_on_previous_step"] = False

                return plan
        except (json.JSONDecodeError, KeyError):
            pass

        # If we couldn't parse JSON, return mock plan
        return [
            {
                "step_number": 1,
                "action": f"Analyze the provided goal: {plan_text[:100]}...",
                "tool_name": None,
                "parameters": {},
                "reason": "Initial analysis of the user request",
                "depends_on_previous_step": False,
            }
        ]
