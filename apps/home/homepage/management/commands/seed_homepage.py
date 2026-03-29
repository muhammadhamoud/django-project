from decimal import Decimal
import os
import random
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand
from faker import Faker

from homepage.models import (
    SiteInformation, SiteInformationAdditional, SiteMetaData,
    Marketing, Service, Feature, BusinessCategory, Offering,
    Project, TeamMember, Testimonial, Framework,
    PricingSection, PricingPlan, PricingFeature, PricingPlanLimit
)

fake = Faker()

app = 'roinsight'
current_path = Path(__file__).resolve().parent.parent.parent
df = pd.ExcelFile(os.path.join(current_path, "fixtures", f"{app}.xlsx"))

site = df.parse(sheet_name='site', dtype=str).fillna('')
sitemetadata = df.parse(sheet_name='sitemetadata', dtype=str).fillna('')
service = df.parse(sheet_name='service', dtype=str).fillna('')
marketing = df.parse(sheet_name='marketing', dtype=str).fillna('')
offering = df.parse(sheet_name='offering', dtype=str).fillna('')
feature = df.parse(sheet_name='feature', dtype=str).fillna('')
framework = df.parse(sheet_name='framework', dtype=str).fillna('')
teammember = df.parse(sheet_name='teammember', dtype=str).fillna('')
testimonial = df.parse(sheet_name='testimonial', dtype=str).fillna('')
project = df.parse(sheet_name='project', dtype=str).fillna('')
business_category = df.parse(sheet_name='business_category', dtype=str).fillna('')

# New pricing sheets
pricing_section = df.parse(sheet_name='pricing_section', dtype=str).fillna('')
pricing_plan = df.parse(sheet_name='pricing_plan', dtype=str).fillna('')
pricing_feature = df.parse(sheet_name='pricing_feature', dtype=str).fillna('')
pricing_plan_limit = df.parse(sheet_name='pricing_plan_limit', dtype=str).fillna('')

for df_ in [
    sitemetadata, service, marketing, offering, feature,
    framework, teammember, testimonial, project, business_category,
    pricing_section, pricing_plan, pricing_feature, pricing_plan_limit
]:
    obj_cols = df_.select_dtypes(include=['object', 'string']).columns
    df_[obj_cols] = df_[obj_cols].fillna('')

# How to call me
# python manage.py fake_homepage_translated --flush
# python manage.py fake_homepage_translated --generate

bootstrap_icons = [
    'bi-alarm', 'bi-award', 'bi-bell', 'bi-bookmark', 'bi-calendar', 'bi-chat',
]
image_urls = [
    'no-image.jpg'
]


def str_to_bool(value):
    return str(value).strip().lower() in ['1', 'true', 'yes', 'y']


def str_to_decimal(value):
    value = str(value).strip()
    if value == '':
        return None
    return Decimal(value)


def str_to_int(value):
    value = str(value).strip()
    if value == '':
        return None
    return int(value)


def normalize_slug(value):
    return str(value).strip().lower().replace(' ', '-')


def update_translations(model, language_code, **fields):
    model.set_current_language(language_code)
    for field_name, field_value in fields.items():
        if hasattr(model, field_name):
            setattr(model, field_name, field_value)
    model.save()

    model.set_current_language('en')
    model.save()

    display_name = getattr(model, 'name', '')
    print(f'Successfully updated translations: {display_name}')


class Command(BaseCommand):
    help = 'Flush (truncate) or generate fake data for specified models'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Flush (truncate) model tables')
        parser.add_argument('--generate', action='store_true', help='Generate fake data for model tables')
        parser.add_argument('--num-instances', type=int, default=5, help='Number of fake data instances to generate')
        parser.add_argument('--category', action='store_true', help='Generate fake data for model tables')

    def get_image_path(self, image, path):
        folder_path = fr'C:\Users\muhammad.hamoud\Desktop\ng\backend\loading_images\{app}\{path}'

        image_files = [
            os.path.basename(f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]

        filename = 'no-image.jpg'

        for file in image_files:
            if file.startswith(str(image) + "."):
                filename = file
                break

        image_path = os.path.join(folder_path, filename)
        return image_path

    def handle(self, *args, **options):
        flush_models = [
            SiteInformation, SiteInformationAdditional, Marketing, Service, Feature,
            BusinessCategory, Offering, Project, TeamMember, Testimonial, SiteMetaData,
            PricingSection, PricingPlan, PricingFeature, PricingPlanLimit
        ]

        if options['flush']:
            for model in flush_models:
                model._default_manager.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully flushed {model._meta.verbose_name_plural} table.')
                )

        if options['generate']:
            existing_sites = SiteInformation.objects.all().first()

            if existing_sites is None:
                for row in site.itertuples():
                    site_info = SiteInformation(
                        name=row.name,
                        description=row.description,
                        company_name=row.company_name,
                        keywords=row.keywords,
                        license_number=row.license_number,
                        vat_number=row.vat_number,
                        register_number=row.register_number,
                    )
                    site_info.save()

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created SiteInformation: {site_info.name}')
                )
            else:
                site_info = existing_sites
                self.stdout.write(
                    self.style.SUCCESS(
                        'SiteInformation instance already exists. No additional sites were generated.'
                    )
                )

            for row in site.itertuples():
                update_translations(
                    model=site_info,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                )

            for row in sitemetadata.itertuples():
                site_meta_data = SiteMetaData(
                    site=site_info,
                    address=row.address,
                    telephone=row.telephone,
                    mobile=row.mobile,
                    fax=row.fax,
                    email=row.email,
                    website=row.website,
                    sales_email=row.sales_email,
                    technical_email=row.technical_email,
                    accounts_email=row.accounts_email,
                    facebook=row.facebook,
                    twitter=row.twitter,
                    instagram=row.instagram,
                    linkedin=row.linkedin,
                    whatsapp=row.whatsapp,
                    googlemap=row.googlemap,
                )
                site_meta_data.save()

            for row in business_category.itertuples():
                try:
                    model_class = BusinessCategory
                    fake_data = {
                        "site": site_info,
                        "name": row.name,
                        "description": row.description,
                        "image": random.choice(image_urls),
                        "icon": row.icon,
                    }

                    instance = model_class(**fake_data)
                    instance.save()

                    update_translations(
                        model=instance,
                        language_code='ar',
                        name=row.name_ar,
                        description=row.description_ar,
                    )

                    image_path = self.get_image_path(image=row.image, path='business_category')
                    if not image_path.endswith('no-image.jpg'):
                        instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

                except Exception as ex:
                    print(ex)

            for row in project.itertuples():
                model_class = Project
                fake_data = {
                    "site": site_info,
                    "category": BusinessCategory.objects.get(translations__name=row.category),
                    "name": row.name,
                    "description": row.description,
                    "client": row.client,
                    "file": random.choice(image_urls),
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                )

                image_path = self.get_image_path(image=row.image, path='project')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in feature.itertuples():
                model_class = Feature
                fake_data = {
                    "site": site_info,
                    "name": row.name,
                    "description": row.description,
                    "image": random.choice(image_urls),
                    "icon": row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                )

                image_path = self.get_image_path(image=row.image, path='feature')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in framework.itertuples():
                model_class = Framework
                fake_data = {
                    "site": site_info,
                    "name": row.name,
                    "description": row.description,
                    "image": random.choice(image_urls),
                    "icon": row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                )

                image_path = self.get_image_path(image=row.image, path='framework')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in testimonial.itertuples():
                model_class = Testimonial
                fake_data = {
                    "site": site_info,
                    "name": row.name,
                    "description": row.description,
                    "job_title": row.job_title,
                    "company": row.company,
                    "content": row.content,
                    "image": random.choice(image_urls),
                    "icon": row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                    job_title=row.job_title_ar,
                    company=row.company_ar,
                    content=row.content_ar,
                )

            for row in service.itertuples():
                model_class = Service
                fake_data = {
                    "site": site_info,
                    "name": row.name,
                    "description": row.description,
                    "image": random.choice(image_urls),
                    "icon": row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                )

                image_path = self.get_image_path(image=row.image, path='service')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in marketing.itertuples():
                model_class = Marketing
                fake_data = {
                    "site": site_info,
                    "name": row.name,
                    "description": row.description,
                    "image": random.choice(image_urls),
                    "icon": row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                )

                image_path = self.get_image_path(image=row.image, path='marketing')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in teammember.itertuples():
                model_class = TeamMember
                fake_data = {
                    "site": site_info,
                    "name": row.name,
                    "description": row.description,
                    "job_title": row.job_title,
                    "bio": row.bio,
                    "image": random.choice(image_urls),
                    "icon": row.icon,
                    "email": row.email,
                    "phone_number": row.phone_number,
                    "location": row.location,
                    "whatsapp": row.whatsapp,
                    "linkedin": row.linkedin,
                    "twitter": row.twitter,
                    "facebook": row.facebook,
                    "instagram": row.instagram,
                    "github": row.github,
                    "medium": row.medium,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                    job_title=row.job_title_ar,
                    bio=row.bio_ar,
                )

                image_path = self.get_image_path(image=row.image, path='teammember')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in offering.itertuples():
                model_class = Offering
                fake_data = {
                    "site": site_info,
                    "name": row.name,
                    "description": row.description,
                    "category": BusinessCategory.objects.get(translations__name=row.category),
                    "image": random.choice(image_urls),
                    "icon": row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                )

                image_path = self.get_image_path(image=row.image, path='offering')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            # ================================================
            # Pricing Section
            # ================================================
            for row in pricing_section.itertuples():
                model_class = PricingSection
                section_slug = normalize_slug(row.name)

                instance, created = model_class.objects.get_or_create(
                    site=site_info,
                    slug=section_slug,
                    defaults={
                        "site": site_info,
                        "name": row.name,
                        "description": row.description,
                        "image": random.choice(image_urls),
                        "icon": row.icon,
                        "is_published": True,
                    }
                )

                if not created:
                    instance.set_current_language('en')
                    instance.name = row.name
                    instance.description = row.description
                    instance.icon = row.icon
                    instance.is_published = True
                    instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                )

                image_path = self.get_image_path(image=row.image, path='pricing_section')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            # ================================================
            # Pricing Plan
            # ================================================
            for row in pricing_plan.itertuples():
                section_instance = PricingSection.objects.get(translations__name=row.section)
                plan_slug = normalize_slug(row.name)

                instance, created = PricingPlan.objects.get_or_create(
                    section=section_instance,
                    slug=plan_slug,
                    defaults={
                        "section": section_instance,
                        "name": row.name,
                        "description": row.description,
                        "billing_interval": row.billing_interval or 'monthly',
                        "currency": row.currency or 'USD',
                        "price": str_to_decimal(row.price),
                        "compare_at_price": str_to_decimal(row.compare_at_price),
                        "trial_days": str_to_int(row.trial_days) or 0,
                        "setup_fee": str_to_decimal(row.setup_fee),
                        "is_free": str_to_bool(row.is_free),
                        "is_custom_price": str_to_bool(row.is_custom_price),
                        "allow_subscribe": str_to_bool(row.allow_subscribe),
                        "allow_contact_sales": str_to_bool(row.allow_contact_sales),
                        "sort_order": str_to_int(row.sort_order) or 0,
                        "icon": row.icon,
                        "is_published": True,
                    }
                )

                if not created:
                    instance.set_current_language('en')
                    instance.name = row.name
                    instance.description = row.description
                    instance.short_description = row.short_description
                    instance.badge_text = row.badge_text
                    instance.price_label = row.price_label
                    instance.button_text = row.button_text or "Get Started"
                    instance.button_url = row.button_url
                    instance.billing_interval = row.billing_interval or 'monthly'
                    instance.currency = row.currency or 'USD'
                    instance.price = str_to_decimal(row.price)
                    instance.compare_at_price = str_to_decimal(row.compare_at_price)
                    instance.trial_days = str_to_int(row.trial_days) or 0
                    instance.setup_fee = str_to_decimal(row.setup_fee)
                    instance.is_free = str_to_bool(row.is_free)
                    instance.is_custom_price = str_to_bool(row.is_custom_price)
                    instance.allow_subscribe = str_to_bool(row.allow_subscribe)
                    instance.allow_contact_sales = str_to_bool(row.allow_contact_sales)
                    instance.sort_order = str_to_int(row.sort_order) or 0
                    instance.icon = row.icon
                    instance.is_published = True
                    instance.save()
                else:
                    instance.set_current_language('en')
                    instance.short_description = row.short_description
                    instance.badge_text = row.badge_text
                    instance.price_label = row.price_label
                    instance.button_text = row.button_text or "Get Started"
                    instance.button_url = row.button_url
                    instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                    short_description=row.short_description_ar,
                    badge_text=row.badge_text_ar,
                    price_label=row.price_label_ar,
                    button_text=row.button_text_ar,
                    button_url=row.button_url_ar,
                )

                image_path = self.get_image_path(image=row.image, path='pricing_plan')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            # ================================================
            # Pricing Feature
            # ================================================
            for row in pricing_feature.itertuples():
                plan_instance = PricingPlan.objects.get(translations__name=row.plan)
                feature_slug = normalize_slug(row.name)

                instance, created = PricingFeature.objects.get_or_create(
                    plan=plan_instance,
                    slug=feature_slug,
                    defaults={
                        "plan": plan_instance,
                        "name": row.name,
                        "description": row.description,
                        "value_type": row.value_type or 'boolean',
                        "value_boolean": str_to_bool(row.value_boolean),
                        "value_number": str_to_decimal(row.value_number),
                        "sort_order": str_to_int(row.sort_order) or 0,
                        "icon": row.icon,
                        "is_published": True,
                    }
                )

                if not created:
                    instance.set_current_language('en')
                    instance.name = row.name
                    instance.description = row.description
                    instance.value_text = row.value_text if hasattr(row, 'value_text') else ''
                    instance.value_type = row.value_type or 'boolean'
                    instance.value_boolean = str_to_bool(row.value_boolean)
                    instance.value_number = str_to_decimal(row.value_number)
                    instance.sort_order = str_to_int(row.sort_order) or 0
                    instance.icon = row.icon
                    instance.is_published = True
                    instance.save()
                else:
                    instance.set_current_language('en')
                    if hasattr(row, 'value_text'):
                        instance.value_text = row.value_text
                    instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    description=row.description_ar,
                    value_text=row.value_text_ar,
                )

                image_path = self.get_image_path(image=row.image, path='pricing_feature')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            # ================================================
            # Pricing Plan Limit
            # ================================================
            for row in pricing_plan_limit.itertuples():
                plan_instance = PricingPlan.objects.get(translations__name=row.plan)
                limit_slug = normalize_slug(row.name)

                instance, created = PricingPlanLimit.objects.get_or_create(
                    plan=plan_instance,
                    slug=limit_slug,
                    defaults={
                        "plan": plan_instance,
                        "name": row.name,
                        "limit_type": row.limit_type or 'integer',
                        "value_integer": str_to_int(row.value_integer),
                        "value_decimal": str_to_decimal(row.value_decimal),
                        "sort_order": str_to_int(row.sort_order) or 0,
                        "icon": row.icon,
                        "is_published": True,
                    }
                )

                if not created:
                    instance.set_current_language('en')
                    instance.name = row.name
                    instance.unit = row.unit
                    instance.custom_value = row.custom_value if hasattr(row, 'custom_value') else ''
                    instance.limit_type = row.limit_type or 'integer'
                    instance.value_integer = str_to_int(row.value_integer)
                    instance.value_decimal = str_to_decimal(row.value_decimal)
                    instance.sort_order = str_to_int(row.sort_order) or 0
                    instance.icon = row.icon
                    instance.is_published = True
                    instance.save()
                else:
                    instance.set_current_language('en')
                    instance.unit = row.unit
                    if hasattr(row, 'custom_value'):
                        instance.custom_value = row.custom_value
                    instance.save()

                update_translations(
                    model=instance,
                    language_code='ar',
                    name=row.name_ar,
                    unit=row.unit_ar,
                    custom_value=row.custom_value_ar,
                )

                image_path = self.get_image_path(image=row.image, path='pricing_plan_limit')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            def get_random_category():
                categories = BusinessCategory.objects.all()
                if categories:
                    return random.choice(categories)
                return None

            def generate_fake_data(model_class, num_instances):
                for _ in range(num_instances):
                    fake_data = {
                        "site": site_info,
                        "name": fake.company(),
                        "description": fake.text(),
                        "image": random.choice(image_urls),
                        "icon": random.choice(bootstrap_icons),
                    }

                    if model_class == Testimonial:
                        fake_data.update({
                            "job_title": fake.job(),
                            "company": fake.company(),
                            "content": fake.paragraph(),
                        })

                    elif model_class == Offering:
                        offering_category = get_random_category()
                        fake_data.update({
                            "category": offering_category,
                        })

                    elif model_class == Project:
                        project_category = get_random_category()
                        fake_data.update({
                            "category": project_category,
                            "client": fake.company(),
                            "file": "path/to/your/file.pdf",
                            "is_published": fake.boolean(),
                        })

                    elif model_class == TeamMember:
                        fake_data.update({
                            "job_title": fake.job(),
                            "email": fake.email(),
                            "phone_number": fake.phone_number(),
                            "bio": fake.text(),
                        })

                    elif model_class == Testimonial:
                        fake_data.update({
                            "job_title": fake.job(),
                            "company": fake.company(),
                            "content": fake.text(),
                        })

                    instance = model_class(**fake_data)
                    instance.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully created {model_class.__name__}: {instance.name}'
                        )
                    )

            # Example:
            # for model_class in [Marketing, Service, Feature, Offering, Project, TeamMember, Testimonial]:
            #     generate_fake_data(model_class, 5)