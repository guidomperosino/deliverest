# -*- coding: utf-8 -*-

"""Deliverest URL definitions."""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from deliorders.views import home, search, add_to_cart, load_order, add_dialog, cart, confirm_cart, cart_status, user_confirmed_tf
from deliproducts.views import price, search_ajax
from delicontacts.views import account_settings

urlpatterns = [
    url(r'^$', home,
        name="home"),
    url(r'^categoria/(?P<category>[^/]+)/$',
        home, name="category"),
    url(r'^buscar/$',
        search, name="search"),
    url(r'^agregar/$',
        add_to_cart, name="add_to_cart"),
    url(r'^agregar-producto/$',
        add_dialog, name="add_dialog"),
    url(r'^producto/(?P<id>[^/]+)$',
        price, name="price"),
    url(r'^recargar-pedido/$',
        load_order, name="load_order"),
    url(r'^carrito/$',
        cart, name="shopping_cart"),
    url(r'^confirmar-carrito/$',
        confirm_cart, name="confirm_cart"),
    url(r'^estado-carrito/$',
        cart_status, name="cart_status"),
    url(r'^confirm-tf/$',
        user_confirmed_tf, name="confirm_tf"),

    url(r'^buscar-ajax/$',
        search_ajax, name="product_search_ajax"),

    url(r'^cuenta/$',
        account_settings, name="account_settings"),
    url(r'^cuenta/(?P<mode>[^/]+)/$',
        account_settings, name="account_settings_mode"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    # Auth views
    url('^', include('django.contrib.auth.urls')),

    # Social login related
    url(r'^accounts/', include('allauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT})
    ]