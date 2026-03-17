import asyncio
import json
from typing import Dict, Any, List, Optional
import threading


class MCPServer:
    """
    Model Context Protocol (MCP) server for providing tools to models and connecting to other agents
    """

    def __init__(self, host: str = "localhost", port: int = 8080, skill_manager=None):
        self.host = host
        self.port = port
        self.skill_manager = skill_manager
        self.tools_registered = {}
        self.clients = set()
        self.running = False
        self._server_thread = None
        print(
            "MCP Server initialized (without websocket support). Actual websocket functionality requires 'websockets' package."
        )

    def register_tool(
        self, tool_name: str, description: str, parameters: Dict[str, Any], handler_func
    ):
        """
        Register a new tool/resource with its schema and handler function
        """
        tool = {
            "name": tool_name,
            "description": description,
            "input_schema": {"type": "object", "properties": parameters},
            "handler": handler_func,
        }
        self.tools_registered[tool_name] = tool

    def register_skill_as_tool(self, skill_name: str):
        """
        Register a skill as an MCP tool for external access
        """
        if self.skill_manager and skill_name in self.skill_manager.skills_map:
            skill = self.skill_manager.skills_map[skill_name]
            # Get the skill params from its description or from skill.json if needed
            self.register_tool(
                tool_name=f"skill::{skill_name}",
                description=skill.description,
                parameters={},  # Will be updated based on skill.json
                handler_func=self._create_skill_handler(skill_name),
            )

    def _create_skill_handler(self, skill_name: str):
        """
        Create a handler function to execute a skill through MCP
        """

        def handler(params: Dict[str, Any]) -> Dict[str, Any]:
            if self.skill_manager:
                try:
                    result = self.skill_manager.execute_skill(skill_name, **params)
                    return {"success": True, "result": result}
                except Exception as e:
                    return {"success": False, "error": str(e)}
            else:
                return {"success": False, "error": "Skill manager not available"}

        return handler

    def start(self):
        """
        Start the MCP server (stub implementation - requires websockets package)
        """
        print(
            "MCP server start requested. This would normally start a websocket server on "
            f"ws://{self.host}:{self.port} but actual implementation requires 'websockets' package."
        )
        if not self.running:
            print(
                "WARNING: MCP functionality will be limited without websockets package installed."
            )
            self.running = True

    def stop(self):
        """
        Stop the MCP server
        """
        if self.running:
            self.running = False
            print("MCP server stopped.")

    def is_running(self) -> bool:
        """
        Check if the server is currently running
        """
        return self.running
