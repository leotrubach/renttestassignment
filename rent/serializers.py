from rest_framework import serializers
from .models import Company, Office


class HeadquartersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('street', 'postal_code', 'city')


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('pk', 'street', 'postal_code', 'city', 'monthly_rent')


class CompanySerializer(serializers.ModelSerializer):
    headquarters = HeadquartersSerializer()
    total_rent = serializers.DecimalField(
        max_digits=Office._meta.get_field('monthly_rent').max_digits,
        decimal_places=Office._meta.get_field('monthly_rent').decimal_places)

    class Meta:
        model = Company
        fields = ('pk', 'name', 'headquarters', 'total_rent')


class HeadquartersUpdateSerializer(serializers.ModelSerializer):
    headquarters = serializers.PrimaryKeyRelatedField(queryset=Office.objects.all())

    def get_fields(self):
        fields = super().get_fields()
        queryset = Office.objects.filter(company=self.instance)
        fields['headquarters'].queryset = queryset
        return fields


    class Meta:
        model = Company
        fields = ['headquarters']