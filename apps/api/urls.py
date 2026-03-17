from django.urls import path
from . import views
from .views import HealthCheckView
from . import agent_views
from . import skills_views

urlpatterns = [
    # Main view
    path("health/", HealthCheckView.as_view(), name="health_check"),
    # Agent API endpoints
    path("agent/chat/", agent_views.agent_chat, name="agent_chat"),
    # Skills API endpoints
    path("skills/", skills_views.list_skills, name="list_skills"),
    path("skills/install/", skills_views.install_skill, name="install_skill"),
    path(
        "skills/<str:skill_name>/", skills_views.uninstall_skill, name="uninstall_skill"
    ),
    path(
        "skills/<str:skill_name>/schema/",
        skills_views.get_skill_schema,
        name="get_skill_schema",
    ),
]
