from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image, ImageDraw, ImageFont

from portfolio.models import Collection, Photo, Photographer

SAMPLE_COLLECTIONS = [
    {
        "title": "St. Petersburg After Rain",
        "description": "Wet cobblestones and canal light across the city, one quiet block at a time.",
        "color_a": (40, 60, 90),
        "color_b": (120, 140, 160),
        "photos": [
            ("Canal at Dusk", "Griboyedov Canal", "2025-09-12"),
            ("Wet Cobblestones", "Palace Square", "2025-09-12"),
            ("Reflections", "Fontanka River", "2025-09-13"),
            ("Streetlamp Glow", "Nevsky Prospekt", "2025-09-13"),
        ],
    },
    {
        "title": "Faces of Summer",
        "description": "Portraits and fleeting moments from long, bright afternoons.",
        "color_a": (200, 140, 60),
        "color_b": (230, 200, 120),
        "photos": [
            ("Afternoon Light", "", "2025-06-20"),
            ("Market Crowd", "Old Town Square", "2025-06-21"),
            ("Golden Hour Portrait", "", "2025-06-22"),
            ("Summer Rooftop", "", "2025-06-23"),
            ("Ice Cream Break", "", "2025-06-24"),
        ],
    },
    {
        "title": "Quiet Places",
        "description": "Empty rooms, still water, and the spaces between things.",
        "color_a": (70, 80, 70),
        "color_b": (150, 160, 140),
        "photos": [
            ("Empty Chapel", "", "2025-03-02"),
            ("Still Water", "Lake District", "2025-03-03"),
            ("Morning Fog", "", "2025-03-04"),
        ],
    },
]


def make_placeholder_image(name, size, color_a, color_b, label):
    width, height = size
    image = Image.new("RGB", size, color=color_a)
    draw = ImageDraw.Draw(image)

    for y in range(height):
        t = y / max(height - 1, 1)
        row_color = tuple(
            int(color_a[i] + (color_b[i] - color_a[i]) * t) for i in range(3)
        )
        draw.line([(0, y), (width, y)], fill=row_color)

    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), label, font=font)
    text_position = (
        (width - (bbox[2] - bbox[0])) / 2,
        (height - (bbox[3] - bbox[1])) / 2,
    )
    draw.text(text_position, label, fill=(255, 255, 255), font=font)

    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    return ContentFile(buffer.getvalue(), name=f"{slugify(name)}.jpg")


class Command(BaseCommand):
    help = "Seed the database with sample collections/photos and a photographer profile for local preview."

    def handle(self, *args, **options):
        self._seed_photographer()
        self._seed_collections()
        self.stdout.write(self.style.SUCCESS("Sample data seeded."))

    def _seed_photographer(self):
        photographer, _ = Photographer.objects.update_or_create(
            pk=1,
            defaults={
                "name": "Jane Doe",
                "bio": (
                    "I'm a photographer who chases quiet light and honest moments. "
                    "This portfolio collects a few of the stories I've followed with a camera."
                ),
                "instagram_url": "https://instagram.com/example",
                "email": "hello@example.com",
                "phone": "+1 555 0100",
            },
        )
        photographer.portrait = make_placeholder_image(
            "portrait", (600, 600), (90, 90, 90), (30, 30, 30), "Portrait"
        )
        photographer.hero_background = make_placeholder_image(
            "hero-background", (1920, 1080), (20, 30, 40), (80, 100, 110), "Hero Background"
        )
        photographer.hero_foreground_object = make_placeholder_image(
            "hero-foreground", (800, 800), (60, 40, 30), (120, 90, 60), "Hero Object"
        )
        photographer.save()

    def _seed_collections(self):
        sample_slugs = [slugify(c["title"]) for c in SAMPLE_COLLECTIONS]
        Photo.objects.filter(collection__slug__in=sample_slugs).delete()
        Collection.objects.filter(slug__in=sample_slugs).delete()

        for order, data in enumerate(SAMPLE_COLLECTIONS):
            collection = Collection.objects.create(
                title=data["title"],
                slug=slugify(data["title"]),
                description=data["description"],
                is_published=True,
                display_order=order,
                cover_image=make_placeholder_image(
                    f"{data['title']}-cover",
                    (1200, 1500),
                    data["color_a"],
                    data["color_b"],
                    data["title"],
                ),
            )

            for photo_order, (title, location, capture_date) in enumerate(
                data["photos"]
            ):
                Photo.objects.create(
                    collection=collection,
                    title=title,
                    alt_text=title,
                    location=location,
                    capture_date=capture_date,
                    is_published=True,
                    display_order=photo_order,
                    image=make_placeholder_image(
                        f"{data['title']}-{title}",
                        (1600, 1200),
                        data["color_b"],
                        data["color_a"],
                        title,
                    ),
                )
