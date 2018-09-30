import decimal
import random
from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from .models import Company, Office


class CompanyTest(TestCase):
    def test_wrong_company_headquarters(self):
        c1 = Company(name='Company 1')
        c1.save()
        c2 = Company(name='Company 2')
        c2.save()
        office = Office(company=c1, street='Broadway', postal_code='12345', city='New York', monthly_rent=10)
        office.save()
        c2.headquarters = office
        with self.assertRaises(ValidationError):
            c2.save()

    def test_headquarters_cannot_be_unset(self):
        c1 = Company(name='Company 1')
        c1.save()
        office = Office(company=c1, street='Broadway', postal_code='12345', city='New York', monthly_rent=10)
        office.save()
        c1.headquarters = office
        c1.save()
        c1.headquarters = None
        with self.assertRaises(ValidationError):
            c1.save()

    def disallow_change_company_if_office_is_headquarter(self):
        c1 = Company(name='Company 1')
        c1.save()
        c2 = Company(name='Company 2')
        c2.save()
        office = Office(company=c1, street='Broadway', postal_code='12345', city='New York', monthly_rent=10)
        office.save()
        c1.headquarters = office
        c1.save()
        office.company = c2
        with self.assertRaises(ValidationError):
            office.save()

    def test_company_change(self):
        c1 = Company(name='Company 1')
        c1.save()
        c2 = Company(name='Company 2')
        c2.save()
        office = Office(company=c1, street='Broadway', postal_code='12345', city='New York', monthly_rent=10)
        office.save()
        office2 = Office(company=c1, street='Park', postal_code='12345', city='Washington', monthly_rent=20)
        office2.save()
        c1.headquarters = office
        c1.save()
        office2.company = c2
        office2.save()

    def test_change_headquarters(self):
        c1 = Company(name='Company 1')
        c1.save()
        office = Office(company=c1, street='Broadway', postal_code='12345', city='New York', monthly_rent=10)
        office.save()
        office2 = Office(company=c1, street='Park', postal_code='12345', city='Washington', monthly_rent=20)
        office2.save()
        c1.headquarters = office
        c1.save()
        c1.headquarters = office2
        c1.save()


class RestAPITest(TestCase):
    def test_update_headquarters(self):
        c1 = Company(name='Company 1')
        c1.save()
        c2 = Company(name='Company 2')
        c2.save()
        office = Office(company=c1, street='Broadway', postal_code='12345', city='New York', monthly_rent=10)
        office.save()
        office2 = Office(company=c1, street='Park', postal_code='12345', city='Washington', monthly_rent=20)
        office2.save()
        office3 = Office(company=c2, street='Street 3', postal_code='12345', city='Washington', monthly_rent=20)
        office3.save()
        client = APIClient()
        client.post(reverse('company-update-headquarters', kwargs={'pk': c1.pk}), {'headquarters': office.pk})
        c1.refresh_from_db()
        self.assertEqual(c1.headquarters, office)
        client.post(reverse('company-update-headquarters', kwargs={'pk': c1.pk}), {'headquarters': office2.pk})
        c1.refresh_from_db()
        self.assertEqual(c1.headquarters, office2)
        # Test wrong office
        response = client.post(reverse('company-update-headquarters', kwargs={'pk': c1.pk}), {'headquarters': office3.pk})
        self.assertEqual(response.status_code, 400)
        c1.refresh_from_db()
        self.assertNotEqual(c1.headquarters, office3)

    def test_monthly_rent(self):
        companies = [Company.objects.create(name='Company{}'.format(i)) for i in range(10)]
        totals = {}
        for company in companies:
            rents = [decimal.Decimal(random.randint(100, 10000)) / 100 for i in range(10)]
            totals[company.pk] = sum(rents)
            for rent in rents:
                Office.objects.create(
                    company=company,
                    street='Street',
                    postal_code='Postal code',
                    city='City',
                    monthly_rent=rent)
        client = APIClient()
        response = client.get(reverse('company-list'))
        for o in response.data:
            self.assertEqual(decimal.Decimal(o['total_rent']), totals[o['pk']])