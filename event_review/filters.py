from django.utils.translation import ugettext_lazy as _

from huerta.filters import CollapsedSimpleListFilter


class SortFilter(CollapsedSimpleListFilter):
    title = 'Sort'
    parameter_name = 'sort'
    multiselect_enabled = False

    def lookups(self, request, model_admin):
        return (('-created_at', _('Recently created')),
                ('starts_at', _('Earliest')),
                ('max_attendees', _('Largest max attendees')),
                ('attendee_count', _('Most attendee signups')),
                ('zip', _('Zipcode')))

    def queryset(self, request, queryset):
        val = self.value()
        return queryset.order_by(val) if val else queryset
