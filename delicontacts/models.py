# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from delidelivery.models import DeliveryMethod

CONTACT_MODE_CHOICES = (
    (50, _(u'Web')),
    (100, _(u'E-mail')),
    (200, _(u'Facebook')),
    (300, _(u'Telefono')),
    (400, _(u'Otro')),
)


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name=_(u'nombre'))
    email = models.EmailField(verbose_name=_(u'e-mail'))
    address = models.TextField(verbose_name=_(u'dirección de envío'))
    phone = models.CharField(max_length=200, verbose_name=_(u'teléfono'))

    class Meta:
        verbose_name = _(u'persona')
        verbose_name_plural = _(u'personas')
        ordering = ('name',)

    def __str__(self):
        return u"%s" % (self.name)


@python_2_unicode_compatible
class Customer(Person):
    contact_mode = models.IntegerField(choices=CONTACT_MODE_CHOICES, default=100, verbose_name=_(u'forma de contacto'))
    prefered_delivery_method = models.ForeignKey(
        DeliveryMethod,
        verbose_name=_(u'forma de envío preferida'),
        on_delete=models.PROTECT,
    )
    last_confirmed_tf = models.DateTimeField(
        verbose_name=_(u'última confirmación de ventana de entrega'),
        null=True
    )
    subscribed_to_newsletter = models.BooleanField(default=True, verbose_name='suscripto a newsletter')
    associated_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_(u'usuario vinculado'),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _(u'cliente')
        verbose_name_plural = _(u'clientes')

    def __str__(self):
        return u"%s <%s> (%s)" % (self.name, self.email if self.email else u'sin email', self.address)

    def delivery_method_name(self):
        return self.prefered_delivery_method.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('delicontacts.views.account_settings')
