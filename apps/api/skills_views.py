from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from typing import Dict, Any
import json
import zipfile
from apps.agent.tooluse.skill_manager import SkillManager


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_skills(request):
    """
    Endpoint to list all available skills
    """
    try:
        skill_manager = SkillManager()
        skills = skill_manager.list_available_skills()
        return Response({"skills": skills})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def install_skill(request):
    """
    Endpoint to install a skill from uploaded zip or by path
    Expected payload: {
        'skill_file': 'zip file of skill',
        ...
    }
    """
    try:
        uploaded_file = request.FILES.get("skill_file")

        if not uploaded_file:
            return Response(
                {"error": "No skill file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Save and extract the uploaded file temporarily
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "zip":
            # Save the zip file temporarily
            temp_file_path = default_storage.save(
                f"skills/temp_{uploaded_file.name}", ContentFile(uploaded_file.read())
            )

            # Unzip to the skills directory
            with zipfile.ZipFile(default_storage.path(temp_file_path), "r") as zip_ref:
                # Extract to a temporary location first - for real implementation we'd validate
                from pathlib import Path

                temp_dir = (
                    Path(default_storage.path(temp_file_path)).parent
                    / f"temp_unpack_{uuid.uuid4()}"
                )
                zip_ref.extractall(temp_dir)

                # Validate that it's a proper skill (has skill.json)
                skill_json_path = temp_dir / "skill.json"
                if not skill_json_path.exists():
                    return Response(
                        {"error": "Invalid skill format: Missing skill.json file"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Now install the skill from the temp directory
                skill_manager = SkillManager()
                success = skill_manager.install_skill(str(temp_dir))

                # Clean up temp files
                import shutil

                shutil.rmtree(temp_dir)

                if success:
                    return Response({"status": "Skill installed successfully"})
                else:
                    return Response(
                        {"error": "Failed to install skill"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

        else:
            # If not a zip, assume it's just a single directory path provided elsewhere
            # For this example, we'll say it needs to be a local path
            skill_path = request.data.get("skill_path")
            if not skill_path:
                return Response(
                    {"error": "Non-zip uploads require specifying a local skill path"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Attempt direct installation from path
            skill_manager = SkillManager()
            success = skill_manager.install_skill(skill_path)

            if success:
                return Response({"status": "Skill installed successfully"})
            else:
                return Response(
                    {"error": "Failed to install skill"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def uninstall_skill(request, skill_name):
    """
    Endpoint to uninstall a skill
    """
    try:
        skill_manager = SkillManager()
        success = skill_manager.uninstall_skill(skill_name)

        if success:
            return Response({"status": f"Skill {skill_name} uninstalled successfully"})
        else:
            return Response(
                {"error": f"Failed to uninstall skill {skill_name}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_skill_schema(request, skill_name):
    """
    Endpoint to get the schema for a specific skill
    """
    try:
        skill_manager = SkillManager()
        schema = skill_manager.get_skill_schema(skill_name)

        if schema:
            return Response({"schema": schema})
        else:
            return Response(
                {"error": f"Skill {skill_name} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Add import for uuid (at the top of the file, but since we can't modify previous imports...)
import uuid
