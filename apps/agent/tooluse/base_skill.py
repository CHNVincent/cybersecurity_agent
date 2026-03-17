from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseSkill(ABC):
    """
    Base class for all skills in the cybersecurity agent
    """

    def __init__(self, name: str, version: str, description: str):
        self.name = name
        self.version = version
        self.description = description

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the skill with provided parameters
        This must be implemented by child classes
        """
        pass

    def validate_parameters(self, **kwargs) -> bool:
        """
        Validate the provided parameters
        """
        return True
