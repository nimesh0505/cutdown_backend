from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import logging


log = logging.getLogger("django")

class HealthCheckView(APIView):
    permission_classes = [AllowAny,]
    allowed_methods = ("get")
    
    def get(self, request: Request):
        return Response(data={"Server is running"}, status=status.HTTP_200_OK)


class CutDownUrlView(APIView):
    permission_classes = [AllowAny,]
    allowed_methods = ("post")
    
    
        
    def post(self, request: Request):
        pass