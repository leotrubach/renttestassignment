from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    name = models.CharField('Name', max_length=300)
    headquarters = models.OneToOneField(
        'Office',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        unique=True,
        related_name='+'
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk:
            old = Company.objects.get(pk=self.pk)
            if old.headquarters and not self.headquarters:
                raise ValidationError(_('Headquarters cannot be unset'))
        if self.headquarters and self.headquarters.company != self:
            raise ValidationError(_('Headquarters must belong to company'))
        super().save(force_insert, force_update, using, update_fields)


class Office(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    street = models.CharField('Street', max_length=256, blank=True)
    postal_code = models.CharField('Postal Code', max_length=32, blank=True)
    city = models.CharField('City', max_length=128, blank=True, null=True)
    monthly_rent = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk:
            old = Office.objects.get(pk=self.pk)
            if old.company_id != self.company_id and old.company.headquarters_id == self.pk:
                raise ValidationError(_('Cannot change company because office is headquarter'))
        super().save(force_insert, force_update, using, update_fields)