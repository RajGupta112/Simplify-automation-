from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from .models import Lead

from .serializers import LeadCreateSerializer

from .tasks import process_lead_workflow


class LeadCreateAPIView(APIView):

    def post(self, request):

        serializer = LeadCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            lead = serializer.save()

            # Trigger async workflow
            process_lead_workflow.delay(
                str(lead.id)
            )

            return Response(
                {
                    "success": True,
                    "message": (
                        "Lead submitted successfully. "
                        "Your personalized audit report "
                        "is being generated."
                    ),
                    "lead_id": lead.id,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )