from rest_framework import viewsets
from .models import FinancialRecord
from .serializers import FinancialRecordSerializer
from .permissions import IsAnalystOrAdminReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

class FinancialRecordViewSet(viewsets.ModelViewSet):
    queryset = FinancialRecord.objects.all()
    serializer_class = FinancialRecordSerializer
    permission_classes = [IsAnalystOrAdminReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Viewer':
            return FinancialRecord.objects.filter(created_by=user)
        return FinancialRecord.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        income = FinancialRecord.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = FinancialRecord.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense
        })