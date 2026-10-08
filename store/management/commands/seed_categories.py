from django.core.management.base import BaseCommand

from store.tests.seed import seed_categories


class Command(BaseCommand):
    help = "Create store categories and their subcategories."

    def handle(self, *args, **options):
        created_categories, created_subcategories = seed_categories()
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created_categories} categories and {created_subcategories} subcategories."
            )
        )
