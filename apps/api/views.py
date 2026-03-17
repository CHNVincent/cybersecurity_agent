from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


def index(request):
    """
    Main index view for the cybersecurity agent application
    """
    return render(request, "index.html")


@method_decorator(csrf_exempt, name="dispatch")
class HealthCheckView(View):
    """
    Simple health check endpoint
    """

    def get(self, request):
        return JsonResponse({"status": "healthy", "service": "cybersecurity-agent"})

    def post(self, request):
        # Accept POST requests for health checks from load balancers
        return JsonResponse({"status": "healthy", "service": "cybersecurity-agent"})
