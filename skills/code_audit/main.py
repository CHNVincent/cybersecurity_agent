import os
import json
from typing import Dict, Any, List
from apps.agent.brain.base import BaseLLM
from apps.agent.brain.ali_bailian import AliBailianLLM


def handler(
    file_path: str, language: str = None, timeout_seconds: int = 120
) -> Dict[str, Any]:
    """
    Handles code audit requests - analyzes code files for security vulnerabilities

    Args:
        file_path: The path to the code file to be audited
        language: The language of source code (python, javascript, java, etc.)
        timeout_seconds: Max time in seconds for the audit (not currently used)

    Returns:
        Dict with audit results including vulnerabilities found and recommendations
    """

    # Read the code file
    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": f"File not found: {file_path}",
            "results": [],
        }

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
    except Exception as e:
        return {
            "success": False,
            "error": f"Could not read file: {str(e)}",
            "results": [],
        }

    # If language wasn't provided, try to guess from extension
    if not language:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".py":
            language = "python"
        elif ext in [".js", ".jsx"]:
            language = "javascript"
        elif ext == ".java":
            language = "java"
        elif ext in [".cpp", ".cxx", ".cc"]:
            language = "cpp"
        elif ext == ".cs":
            language = "csharp"
        else:
            language = "unknown"

    # Initialize the LLM for code analysis
    # For simplicity, we'll create a basic configuration based on AliBailian
    # but in a real implementation, this would come from configuration
    try:
        import os
        from dotenv import load_dotenv

        load_dotenv()

        api_key = os.getenv("ALI_BAILIAN_API_KEY")
        model_name = os.getenv("ALI_BAILIAN_MODEL", "codeqwen-plus")
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

        if not api_key:
            return {
                "success": False,
                "error": "API key not configured. Please set ALI_BAILIAN_API_KEY in environment.",
                "results": [],
            }

        # Create LLM instance for code analysis
        llm = AliBailianLLM(api_key=api_key, model_name=model_name, base_url=base_url)

        # Construct the prompt for code analysis
        prompt = f"""
        You are an advanced cybersecurity expert specializing in code vulnerability assessment. 
        Analyze the following {language} code for security vulnerabilities and common security issues.
        
        Provide a detailed security audit report with:
        1. Identified vulnerabilities with severity levels (Critical, High, Medium, Low)
        2. Specific code locations where issues exist (line numbers if possible)
        3. Brief explanations of why each is a security concern
        4. Recommended fixes or code improvements
        5. Risk mitigation suggestions
        
        Vulnerability categories to look for include:
        - Input validation issues
        - SQL Injection
        - Cross-site Scripting (XSS)
        - Buffer overflows
        - Improper error handling
        - Weak authentication mechanisms
        - Data exposure
        - Cryptographic weaknesses
        - Access control issues
        
        For {language} code specifically, consider language-specific vulnerabilities.
        
        Code to analyze:
        {file_content}
        
        Return the results in a JSON format with fields:
        - "summary": brief executive summary with number of vulnerabilities found
        - "vulnerabilities": array of objects with "type", "severity", "location", "description", and "recommendation" properties
        - "overall_risk_score": integer from 1-10 (1=low, 10=high)
        - "security_grade": letter grade (A-F) for the code's security posture
        """

        messages = [{"role": "user", "content": prompt}]

        # Call the LLM to perform analysis
        response_data = llm.chat(messages)

        # Extract LLM response
        audit_result = (
            response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        )

        # For now, return the raw analysis result (in production, this should be properly parsed)
        return {
            "success": True,
            "file_path": file_path,
            "language": language,
            "raw_result": audit_result,
            "results": [],  # In a real implementation, we'd properly parse the JSON result
        }

    except Exception as e:
        return {"success": False, "error": f"Analysis failed: {str(e)}", "results": []}


# Additional helper functions for enhanced code audit could be added here
def parse_vulnerabilities_from_response(response_text: str) -> List[Dict[str, Any]]:
    """
    Helper function to parse structured vulnerability data from LLM response
    (In a real implementation, we'd properly validate JSON responses)
    """
    # Try to extract JSON from response
    import re

    json_match = re.search(r"({.*})", response_text, re.DOTALL)

    if json_match:
        import json

        try:
            parsed_data = json.loads(json_match.group(1))
            return parsed_data
        except json.JSONDecodeError:
            pass

    # If JSON parsing fails, return basic structure
    return {
        "summary": "Analysis completed, but result could not be parsed into structured format",
        "vulnerabilities": [],
        "overall_risk_score": 5,
        "security_grade": "C",
    }
