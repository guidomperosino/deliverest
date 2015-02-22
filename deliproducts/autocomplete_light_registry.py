from django.utils.translation import ugettext_lazy as _

import autocomplete_light
from deliproducts.models import Price

# This will generate a PersonAutocomplete class
autocomplete_light.register(Price,
    # Just like in ModelAdmin.search_fields
    search_fields=['product__name', 'product__description'],
    attrs={
        # This will set the input placeholder attribute:
        'placeholder': _('Producto'),
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 2,
    },
    # This will set the data-widget-maximum-values attribute on the
    # widget container element, and will be set to
    # yourlabs.Widget.maximumValues (jQuery handles the naming
    # conversion).
    widget_attrs={
        'data-widget-maximum-values': 10,
        # Enable modern-style widget !
        'class': 'modern-style',
    },
)