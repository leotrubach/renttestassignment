from django.shortcuts import render
from django.db.models import Sum
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CompanySerializer, OfficeSerializer, HeadquartersUpdateSerializer
from .models import Company


class CompanyListViewSet(ReadOnlyModelViewSet):

    serializer_class = CompanySerializer
    queryset = Company.objects.annotate(total_rent=Sum('office__monthly_rent'))

    @action(methods=('get', ), detail=True)
    def offices(self, request, pk=None):
        company = self.get_object()
        serializer = OfficeSerializer(company.office_set.all(), many=True)
        return Response(serializer.data)

    @action(methods=('post', ), detail=True)
    def update_headquarters(self, request, pk=None):
        company = self.get_object()
        serializer = HeadquartersUpdateSerializer(instance=company, data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
