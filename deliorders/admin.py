# -*- coding: utf-8 -*-

from decimal import Decimal

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.conf.urls import url
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from .models import Order, OrderItem, ORDER_STATUS_CHOICES
from delidelivery.models import DeliveryMethod
from deliproducts.models import Price

import autocomplete_light


# Help class for default filter
class DefaultListFilter(SimpleListFilter):
    all_value = '_all'

    def default_value(self):
        raise NotImplementedError()

    def queryset(self, request, queryset):
        if self.parameter_name in request.GET and request.GET[self.parameter_name] == self.all_value:
            return queryset

        if self.parameter_name in request.GET:
            return queryset.filter(**{self.parameter_name: request.GET[self.parameter_name]})

        return queryset.filter(**{self.parameter_name: self.default_value()})

    def choices(self, cl):
        yield {
            'selected': self.value() == self.all_value,
            'query_string': cl.get_query_string({self.parameter_name: self.all_value}, []),
            'display': _(u'All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup) or (self.value() == None and force_text(self.default_value()) == force_text(lookup)),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }


class StatusFilter(DefaultListFilter):
    title = _(u'Estado ')
    parameter_name = 'status__exact'

    def lookups(self, request, model_admin):
        return ORDER_STATUS_CHOICES

    def default_value(self):
        return 200


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = autocomplete_light.modelform_factory(OrderItem, fields='__all__')


class OrderAdminChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super(OrderAdminChangeList, self).get_results(*args, **kwargs)
        self.order_sum = Decimal(0.0)
        for order in self.result_list.all():
            self.order_sum = self.order_sum + order.get_order_total()


class OrderAdmin(admin.ModelAdmin):
    list_filter = (StatusFilter, 'delivery_method', 'delivery_date', 'when_create')
    exclude = ('code', 'when_closed', 'when_delivered', 'reconciled', 'delivery_address')
    readonly_fields = ('delivery_price', 'get_order_total')
    search_fields = ('code', 'customer__name')
    list_display = ('code', 'customer', 'get_contact_mode', 'delivery_method', 'get_order_total',
        'get_customer_address', 'get_customer_phone', 'delivery_date', 'when_create', 'status')
    inlines = [OrderItemInline]
    actions = ['close_orders', 'deliver_orders', 'reconcile_orders', 'balance_report']

    form = autocomplete_light.modelform_factory(Order, fields='__all__')

    def get_changelist(self, request):
        return OrderAdminChangeList

    def get_contact_mode(self, obj):
        if obj.customer is None:
            return "Cliente eliminado"

        return obj.customer.email if (obj.contact_mode == 100 and obj.customer.email) else obj.get_contact_mode_display()
    get_contact_mode.admin_order_field = 'customer'
    get_contact_mode.short_description = _(u'Contacto')

    def get_customer_address(self, obj):
        if obj.customer is None:
            return "Cliente eliminado"
        return obj.customer.address
    get_customer_address.admin_order_field = 'customer'
    get_customer_address.short_description = _(u'Dirección de entrega')

    def get_customer_phone(self, obj):
        if obj.customer is None:
            return "Cliente eliminado"
        return obj.customer.phone
    get_customer_phone.admin_order_field = 'customer'
    get_customer_phone.short_description = _(u'Teléfono de contacto')

    def get_urls(self):
        urls = super(OrderAdmin, self).get_urls()
        my_urls = [
            url(r'^products_report/$', self.products_report, name='admin_order_products_report'),
            url(r'^print_orders/$', self.print_orders, name='admin_order_print'),
            url(r'^print_orders/(?P<delivery_method_id>[0-9]{1,4})/$', self.print_orders, name='admin_order_print'),
        ]
        return my_urls + urls

    def products_report(self, request):
        # Not-delivered orders
        pending_orders = Order.objects.filter(Q(status=200) | Q(status=400))
        delivery_methods = list(DeliveryMethod.objects.all().order_by('code'))
        result_headers = ['Product'] + delivery_methods + ['Total']

        results = {}
        for order in pending_orders:
            for item in order.orderitem_set.all():
                if item.product.pk not in results:
                    prod = item.product
                    item_display = "%s (%s)" % (
                        prod.product.name,
                        prod.presentation
                    )
                    results[item.product.pk] = [item_display] + [0 for i in delivery_methods] + [0]
                for pos, delivery_method in enumerate(delivery_methods):
                    if order.delivery_method_id == delivery_method.id:
                        results[item.product.pk][pos + 1] += item.quantity
                results[item.product.pk][-1] += item.quantity

        results = results.values()
        results = sorted(results, key=lambda i: i[0])

        return render(request, self.order_report_template, {
            'title': _(u'Reporte de cantidades de producto'),
            'result_headers': result_headers,
            'results': results
        })

    def print_orders(self, request, delivery_method_id=None):
        pending_orders = Order.objects.filter(Q(status=200) | Q(status=400))
        delivery_methods = DeliveryMethod.objects.all()
        delivery_method = None
        title_append = ""

        if delivery_method_id:
            delivery_method = get_object_or_404(
                DeliveryMethod,
                pk=delivery_method_id
            )
            pending_orders = pending_orders.filter(
                delivery_method_id=delivery_method_id)
            title_append = _(u" para ") + '"' + delivery_method.name + '"'

        return render(request, self.order_print_template, {
            'title': _(u'Ordenes a entregar') + title_append,
            'delivery_method': delivery_method,
            'delivery_methods': delivery_methods,
            'orders': pending_orders
        })

    def balance_report(self, request, queryset):
        from django.db.models import ExpressionWrapper, F, FloatField, Sum

        results = OrderItem.objects.filter(
            order__in=queryset
        ).values(
            'product__pk'
        ).order_by(
            'product__product__name'
        ).annotate(
            total_quantity=Sum('quantity')
        ).annotate(
            total_cost=ExpressionWrapper(F('total_quantity') * F('product__buy_price'), output_field=FloatField()),
            total_sell_price=ExpressionWrapper(F('total_quantity') * F('product__sell_price'), output_field=FloatField())
        ).annotate(profit=ExpressionWrapper(F('total_sell_price') - F('total_cost'), output_field=FloatField()))

        totals = [0, 0, 0, 0, 0]
        for p in results:
            price = Price.objects.get(pk=p['product__pk'])
            p['display'] = unicode(price)
            totals[1] += p['total_quantity']
            totals[2] += p['total_cost']
            totals[3] += p['total_sell_price']
            totals[4] += p['profit']

        return render(request, self.order_balance_template, {
            'title': _(u'Balance'),
            'results': results,
            'totals': totals
        })

    def change_orders_status(self, queryset, from_status, to_status):
        if hasattr(from_status, '__contains__'):
            compare = from_status
        else:
            compare = (from_status,)

        for order in queryset:
            if order.status in compare:
                order.status = to_status
                order.save()

    def close_orders(self, request, queryset):
        self.change_orders_status(queryset, (20, 100), 200)

    def deliver_orders(self, request, queryset):
        self.change_orders_status(queryset, 200, 300)

    def reconcile_orders(self, request, queryset):
        self.change_orders_status(queryset, (300, 400), 600)

    close_orders.short_description = _(u"Cerrar pedidos")
    deliver_orders.short_description = _(u"Marcar pedidos entregados")
    balance_report.short_description = _(u"Balance de pedidos")
    reconcile_orders.short_description = _(u"Conciliar pedidos")

    order_report_template = 'admin/products_report.html'
    order_print_template = 'admin/orders_print.html'
    order_balance_template = 'admin/orders_balance.html'


admin.site.register(Order, OrderAdmin)
