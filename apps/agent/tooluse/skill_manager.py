import importlib.util
import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path


class BaseSkill:
    """
    Base class for all skills in the cybersecurity agent
    """

    def __init__(self, name: str, version: str, description: str):
        self.name = name
        self.version = version
        self.description = description

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the skill with provided parameters
        This must be implemented by child classes
        """
        raise NotImplementedError("Subclasses must implement execute method")

    def validate_parameters(self, **kwargs) -> bool:
        """
        Validate the provided parameters
        """
        return True


class SkillManager:
    """
    Manages loading, installing, uninstalling, and executing skills
    Skills are stored in the skills/ directory with their own skill.json descriptor
    """

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills_map = {}  # Maps skill names to skill instances
        self._scan_skills()

    def _scan_skills(self):
        """
        Scan the skills directory for available skills
        """
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_json_path = skill_dir / "skill.json"
                if skill_json_path.exists():
                    try:
                        with open(skill_json_path, "r", encoding="utf-8") as f:
                            skill_config = json.load(f)

                        # Install the skill
                        self._load_skill_file(skill_dir.name)
                    except Exception as e:
                        print(f"Error loading skill from {skill_dir}: {str(e)}")

    def _load_skill_file(self, skill_name: str) -> Optional[BaseSkill]:
        """
        Load a skill from a Python file based on skill.json configuration
        """
        skill_dir = self.skills_dir / skill_name
        skill_json_path = skill_dir / "skill.json"

        if not skill_json_path.exists():
            print(f"No skill.json found for {skill_name}")
            return None

        with open(skill_json_path, "r", encoding="utf-8") as f:
            skill_config = json.load(f)

        # Extract skill metadata
        name = skill_config.get("name")
        version = skill_config.get("version", "1.0.0")
        description = skill_config.get("description", "")
        entry_point = skill_config.get("entry", "main.handler")

        # Load the Python module from file
        try:
            # Split the entry point to get module name and function
            module_parts = entry_point.split(".")
            module_path = ".".join(module_parts[:-1])
            function_name = (
                module_parts[-1] if module_parts[-1] != "main" else "handler"
            )

            # Create module path
            module_path_full = f"{skill_dir.name}.{module_path}"
            main_py_path = skill_dir / f"{module_parts[0]}.py"

            if not main_py_path.exists():
                print(f"Module file {main_py_path} not found for skill {skill_name}")
                return None

            # Load the module dynamically
            spec = importlib.util.spec_from_file_location(f"skills.{name}", main_py_path)
            if spec is None:
                print(f"Could not load module specification for {main_py_path}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            if spec.loader is not None:
                spec.loader.exec_module(module)
            else:
                print(f"Module loader is None for {main_py_path}")
                return None

            # Get the handler function
            handler_func = getattr(module, function_name, None)

            if handler_func is None:
                print(f"No '{function_name}' function found in {main_py_path}")
                return None

            # Create skill wrapper that implements BaseSkill interface
            class WrappedSkill(BaseSkill):
                def __init__(self, name, version, description, handler_func):
                    super().__init__(name, version, description)
                    self.handler_func = handler_func

                def execute(self, **kwargs):
                    return self.handler_func(**kwargs)

            wrapped_skill = WrappedSkill(name, version, description, handler_func)
            self.skills_map[name] = wrapped_skill

            return wrapped_skill

        except Exception as e:
            print(f"Error loading skill {skill_name}: {str(e)}")
            import traceback

            traceback.print_exc()
            return None

    def install_skill(self, skill_path: str) -> bool:
        """
        Install a skill from the given path (could be local directory or remote archive)
        For now, assumes it's a local directory with skill.json and implementation
        """
        skill_path_obj = Path(skill_path)

        # Validate if it's a valid skill by checking for skill.json
        skill_json_path = skill_path_obj / "skill.json"
        if not skill_json_path.exists():
            print(f"Invalid skill: Missing skill.json in {skill_path}")
            return False

        try:
            # Copy the skill directory to our skills folder
            destination = self.skills_dir / skill_path_obj.name
            if destination.exists():
                print(f"Skill {skill_path_obj.name} already exists")
                return False

            import shutil

            shutil.copytree(skill_path_obj, destination)

            # Load the newly added skill file
            skill_name = skill_path_obj.name
            self._load_skill_file(skill_name)

            print(f"Successfully installed skill: {skill_name}")
            return True

        except Exception as e:
            print(f"Error installing skill from {skill_path}: {str(e)}")
            return False

    def uninstall_skill(self, skill_name: str) -> bool:
        """
        Uninstall a skill by removing it from the skills directory
        """
        try:
            skill_dir = self.skills_dir / skill_name
            if not skill_dir.exists():
                print(f"Skill {skill_name} does not exist")
                return False

            import shutil

            shutil.rmtree(skill_dir)

            # Remove from skills map
            self.skills_map.pop(skill_name, None)

            print(f"Successfully uninstalled skill: {skill_name}")
            return True

        except Exception as e:
            print(f"Error uninstalling skill {skill_name}: {str(e)}")
            return False

    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a given skill with the provided parameters
        """
        if skill_name not in self.skills_map:
            raise ValueError(f"Skill '{skill_name}' not found")

        skill = self.skills_map[skill_name]

        # Validate parameters before execution
        if not skill.validate_parameters(**kwargs):
            raise ValueError(f"Validation failed for skill {skill_name}")

        # Execute the skill
        result = skill.execute(**kwargs)
        return result

    def list_available_skills(self) -> List[Dict[str, Any]]:
        """
        List all available skills with their metadata
        """
        return [
            {
                "name": skill.name,
                "version": skill.version,
                "description": skill.description,
            }
            for skill in self.skills_map.values()
        ]

    def get_skill_schema(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the schema (metadata) for a specific skill
        """
        skill_dir = self.skills_dir / skill_name
        skill_json_path = skill_dir / "skill.json"

        if not skill_json_path.exists():
            return None

        with open(skill_json_path, "r", encoding="utf-8") as f:
            return json.load(f)
