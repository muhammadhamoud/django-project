from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

from accounts.models import Company, Department, JobTitle, Role, UserProfile
from properties.models import Property

User = get_user_model()
fake = Faker()

# python manage.py seed_users

class Command(BaseCommand):
    help = "Seed database with sample users"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        company, _ = Company.objects.get_or_create(name="Demo Company")

        departments = [
            Department.objects.get_or_create(name="IT")[0],
            Department.objects.get_or_create(name="HR")[0],
            Department.objects.get_or_create(name="Finance")[0],
        ]

        job_titles = [
            JobTitle.objects.get_or_create(name="Manager")[0],
            JobTitle.objects.get_or_create(name="Staff")[0],
        ]

        roles = [
            Role.objects.get_or_create(
                code="supervisor",
                defaults={"name": "Supervisor", "company": company},
            )[0],
            Role.objects.get_or_create(
                code="staff",
                defaults={"name": "Staff", "company": company},
            )[0],
        ]

        properties = list(Property.objects.all())

        if not properties:
            self.stdout.write(self.style.WARNING("No properties found. Create some first."))
            return

        created = 0

        for _ in range(100):
            email = fake.unique.email()

            if User.objects.filter(email=email).exists():
                continue

            user = User.objects.create_user(
                email=email,
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_verified=True,
                is_active=True,
            )

            profile, _ = UserProfile.objects.get_or_create(user=user)

            profile.company = company
            profile.department = random.choice(departments)
            profile.job_title = random.choice(job_titles)
            profile.disabled = False
            profile.save()

            profile.roles.set([random.choice(roles)])

            assigned_properties = random.sample(
                properties,
                k=min(len(properties), random.randint(1, 3))
            )
            profile.properties.set(assigned_properties)

            created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} users created successfully!"))