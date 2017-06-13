from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count

from event_exim.models import EventDupeGuesses
from event_store.models import Event

class Command(BaseCommand):

    help = ('Checks events across all sources for events in the same zip code '
            'at the same time and marks them as potential dupes for review.')

    def handle(self, *args, **options):
        potential_dupes = (
                Event.objects.values('zip','starts_at_utc')
                .annotate(count = Count('id'))
                .order_by()
                .filter(count__gt = 1, dupe_id__isnull = True)
            )
        if potential_dupes:
            for dupe in potential_dupes:
                events = (
                    Event.objects
                    .filter(zip = dupe['zip'], starts_at_utc = dupe['starts_at_utc'])
                    .order_by('id')
                )
                source_event = events[0]
                for x in range(1, dupe['count'], 1):
                    dupe_event = events[x]
                    try:
                        (
                            EventDupeGuesses.objects
                            .create_event_dupe(source_event, dupe_event)
                        )
                        print (
                            "Documented duplicate: Events {} and {}"
                            .format(source_event.id, dupe_event.id)
                        )
                    except:
                        print (
                            "Duplicate events {} and {} already documented"
                            .format(source_event.id, dupe_event.id)
                        )