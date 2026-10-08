from store.models import Category, Subcategory

CATEGORIES = {
    "Living Room": ["Sofas", "Tables", "Chairs"],
    "Bedroom": ["Beds", "Wardrobes"],
    "Office": ["Desks", "Storage"],
}


def seed_categories() -> tuple[int, int]:
    created_categories = 0
    created_subcategories = 0

    for category_name, subcategory_names in CATEGORIES.items():
        category, category_created = Category.objects.get_or_create(name=category_name) # type: ignore
        created_categories += category_created

        for subcategory_name in subcategory_names:
            _, subcategory_created = Subcategory.objects.get_or_create( # type: ignore
                name=subcategory_name,
                defaults={"category": category},
            )
            created_subcategories += subcategory_created

    return created_categories, created_subcategories
