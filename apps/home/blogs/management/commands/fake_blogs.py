import random
from django.core.management.base import BaseCommand
from faker import Faker
from blogs.models import Post, BlogTag, BlogCategory, BlogImage
from django.contrib.auth import get_user_model
# Get a random user
User = get_user_model()
user = User.objects.first()  # Assuming you have users in your database

class Command(BaseCommand):
    help = 'Generate 100 blog posts using Django Faker'

    def handle(self, *args, **options):
        fake = Faker()
        categories = BlogCategory.objects.all()
        tags = BlogTag.objects.all()

        for _ in range(100):
            category = random.choice(categories)
            tags_list = random.sample(list(tags), random.randint(1, len(tags)))
            name = fake.sentence(nb_words=6, variable_nb_words=True)
            description = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
            status = random.choice(['Drafted', 'Published', 'Trashed', 'Review'])
            meta_description = name #fake.paragraph(nb_sentences=1, variable_nb_sentences=True)
            meta_keywords = fake.words(nb=5)
            meta_author = fake.name()
            is_page = fake.boolean()

            post = Post.objects.create(
                name=name,
                description=description,
                author=user,
                category=category,
                status=status,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                meta_author=meta_author,
                is_page=is_page,
                # image=fake.image_url(),
            )
            post.tags.add(*tags_list)

            # Generate blog images
            for _ in range(random.randint(1, 3)):
                BlogImage.objects.create(
                    post=post,
                    image=fake.image_url(),
                )

        self.stdout.write(self.style.SUCCESS('Successfully generated 100 blog posts'))
