from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Dog(models.Model):
    first_name = models.CharField(max_length=64, blank=False, null=False)
    last_name = models.CharField(max_length=64, blank=False, null=False)

    class Meta:
        unique_together = ('first_name', 'last_name')
        verbose_name = _('Dog')
        verbose_name_plural = _('Dogs')


class Visit(models.Model):
    dog = models.ForeignKey(verbose_name=_('Dog'),
                            to=Dog,
                            null=False,
                            blank=False,
                            on_delete=models.CASCADE,
                            related_name='visits'
                            )

    start_date = models.DateField(verbose_name=_(
        'Start Date'), null=False, blank=False)

    end_date = models.DateField(verbose_name=_(
        'End Date'), null=False, blank=False)

    class Meta:
        verbose_name = _('Visit')
        verbose_name_plural = _('Visits')
