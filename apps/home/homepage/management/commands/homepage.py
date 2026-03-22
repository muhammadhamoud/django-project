from django.core.management.base import BaseCommand

from homepage.models import (
    SiteInformation, SiteInformationAdditional, SiteMetaData, Marketing, Service, Feature, 
    BusinessCategory, Offering, Project, TeamMember, Testimonial, Framework
)
from faker import Faker
fake = Faker()

import pandas as pd
import os
from django.conf import settings
from pathlib import Path

app = 'roinsight'
current_path = Path(__file__).resolve().parent.parent.parent
df = pd.ExcelFile(os.path.join(current_path, "fixtures", f"{app}.xlsx"))

site = df.parse(sheet_name='site')
sitemetadata = df.parse(sheet_name='sitemetadata')
service = df.parse(sheet_name='service')
marketing = df.parse(sheet_name='marketing')
offering = df.parse(sheet_name='offering')
feature = df.parse(sheet_name='feature')
framework = df.parse(sheet_name='framework')
teammember = df.parse(sheet_name='teammember')
testimonial = df.parse(sheet_name='testimonial')
project = df.parse(sheet_name='project')
business_category = df.parse(sheet_name='business_category')

print(business_category)

# sitemetadata.fillna('', inplace=True)
# service.fillna('', inplace=True)
# marketing.fillna('', inplace=True)
# offering.fillna('', inplace=True)
# feature.fillna('', inplace=True)
# framework.fillna('', inplace=True)
# teammember.fillna('', inplace=True)
# testimonial.fillna('', inplace=True)
# project.fillna('', inplace=True)
# business_category.fillna('', inplace=True)

for df_ in [
    sitemetadata, service, marketing, offering, feature,
    framework, teammember, testimonial, project, business_category
]:
    obj_cols = df_.select_dtypes(include=['object', 'string']).columns
    df_[obj_cols] = df_[obj_cols].fillna('')

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

# print(service)

# How to call me
# python manage.py fake_homepage_translated --flush 

# List of Bootstrap icon names
import random
bootstrap_icons = [
    'bi-alarm', 'bi-award', 'bi-bell', 'bi-bookmark', 'bi-calendar', 'bi-chat',  # Add more icons as needed
]
image_urls = [
    'no-image.jpg'
]

def update_translations(model, name, description, language_code, *args, **kwargs):
    # Ensure you set the language for which you want to update the translations
    model.set_current_language(language_code)

    # Update the translation fields with the provided data
    model.name = name
    model.description = description

    # Save the translation instance
    model.save()

    # Make sure to set the current language back to the original language
    model.set_current_language('en')  # Replace 'en' with your original language code
    model.save()

    print(f'Successfully created: {model.name}')


class Command(BaseCommand):
    help = 'Flush (truncate) or generate fake data for specified models'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Flush (truncate) model tables')
        parser.add_argument('--generate', action='store_true', help='Generate fake data for model tables')
        parser.add_argument('--num-instances', type=int, default=5, help='Number of fake data instances to generate')
        parser.add_argument('--category', action='store_true', help='Generate fake data for model tables')

    def get_image_path(self, image, path):
        # Change this to the path of your folder containing random images
        folder_path = fr'C:\Users\muhammad.hamoud\Desktop\ng\backend\loading_images\{app}\{path}'
        
        # Get a list of file names in the specified folder
        image_files = [os.path.basename(f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        # Check if the image name exists in the list of files
        filename = 'no-image.jpg'
        
        for file in image_files:
            if file.startswith(str(image) + "." ):
                filename = file
                break

        image_path = os.path.join(folder_path, filename)
        
        return image_path

    def handle(self, *args, **options):

        flush_models = [
            SiteInformation, SiteInformationAdditional, Marketing, Service, Feature,
            BusinessCategory, Offering, Project, TeamMember, Testimonial, SiteMetaData
        ]

        if options['flush']:
            # Flush (truncate) the tables for specified models
            for model in flush_models:
                model._default_manager.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully flushed {model._meta.verbose_name_plural} table.'))

        if options['generate']:
            # Check if there are existing SiteInformation instances
            existing_sites = SiteInformation.objects.all().first()
            # print(existing_sites)

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
                self.stdout.write(self.style.SUCCESS(f'Successfully created SiteInformation: {site_info.name}'))
            
            else:
                site_info = existing_sites
                self.stdout.write(self.style.SUCCESS('SiteInformation instance already exists. No additional sites were generated.'))

            for row in site.itertuples():
                update_translations(
                    model=site_info, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
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

            # siteinformationadditional = SiteInformationAdditional(
            #     site=site_info,
            #     about_us=fake.paragraph(),
            #     privacy_policy=fake.paragraph(),
            #     terms_of_service=fake.paragraph(),
            # )
            # siteinformationadditional.save()
            
            for row in business_category.itertuples():
                try:
                    model_class = BusinessCategory
                    fake_data = {
                        "site": site_info,
                        'name': row.name,
                        'description': row.description,
                        'image': random.choice(image_urls),
                        'icon': row.icon,
                    }

                    instance = model_class(**fake_data)
                    instance.save()

                    update_translations(
                        model=instance, 
                        name=row.name_ar, 
                        description=row.description_ar, 
                        language_code='ar'
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
                    'category': BusinessCategory.objects.get(translations__name=row.category),
                    'name': row.name,
                    'description': row.description,
                    'client': row.client,
                    'file': random.choice(image_urls),
                 }
                # Offering_category = get_random_category()
                # fake_data.update({
                #     'category': Offering_category,
                # })

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )
                image_path = self.get_image_path(image=row.image, path='project')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in feature.itertuples():
                model_class = Feature
                fake_data = {
                    "site": site_info,
                    'name': row.name,
                    'description': row.description,
                    'image': random.choice(image_urls),
                    'icon': row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )

                image_path = self.get_image_path(image=row.image, path='feature')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))                

            for row in framework.itertuples():
                model_class = Framework
                fake_data = {
                    "site": site_info,
                    'name': row.name,
                    'description': row.description,
                    'image': random.choice(image_urls),
                    'icon': row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )

                image_path = self.get_image_path(image=row.image, path='framework')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in testimonial.itertuples():
                model_class = Testimonial
                fake_data = {
                    "site": site_info,
                    'name': row.name,
                    'description': row.description,
                    'job_title': row.job_title,
                    'company': row.company,
                    'content': row.content,
                    'image': random.choice(image_urls),
                    'icon': row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    job_title= row.job_title_ar,
                    company= row.company_ar,
                    content= row.content_ar,

                    language_code='ar'
                )

            for row in service.itertuples():
                model_class = Service
                fake_data = {
                    "site": site_info,
                    'name': row.name,
                    'description': row.description,
                    'image': random.choice(image_urls),
                    'icon': row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )
                image_path = self.get_image_path(image=row.image, path='service')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in marketing.itertuples():
                model_class = Marketing
                fake_data = {
                    "site": site_info,
                    'name': row.name,
                    'description': row.description,
                    'image': random.choice(image_urls),
                    'icon': row.icon,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )

                image_path = self.get_image_path(image=row.image, path='marketing')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in teammember.itertuples():
                model_class = TeamMember
                fake_data = {
                    "site": site_info,
                    'name': row.name,
                    'description': row.description,
                    'job_title': row.job_title,
                    'bio': row.bio,
                    'image': random.choice(image_urls),
                    'icon': row.icon,
                    'email': row.email,
                    'phone_number': row.phone_number,
                    'location': row.location,
                    'whatsapp': row.whatsapp,
                    'linkedin': row.linkedin,
                    'twitter': row.twitter,
                    'facebook': row.facebook,
                    'instagram': row.instagram,
                    'github': row.github,
                    'medium': row.medium,
                }

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar,
                    # TODO fix this
                    job_title=row.job_title_ar,
                    bio=row.bio_ar,
                    language_code='ar'
                )
                image_path = self.get_image_path(image=row.image, path='teammember')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            for row in offering.itertuples():
                model_class = Offering
                fake_data = {
                    "site": site_info,
                    'name': row.name,
                    'description': row.description,
                    'category': BusinessCategory.objects.get(translations__name=row.category),
                    'image': random.choice(image_urls),
                    'icon': row.icon,
                }
                # Offering_category = get_random_category()
                # fake_data.update({
                #     'category': Offering_category,
                # })

                instance = model_class(**fake_data)
                instance.save()

                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )
                image_path = self.get_image_path(image=row.image, path='offering')
                if not image_path.endswith('no-image.jpg'):
                    instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            # # Offering_category = BusinessCategory(
            # #     site=site_info,
            # #     name=fake.word(),
            # #     description=fake.text(),
            # # )
            # # Offering_category.save()

            def get_random_category():
                # Get a list of existing BusinessCategory objects
                categories = BusinessCategory.objects.all()
                if categories:
                    # Randomly select a category from the list
                    return random.choice(categories)
                else:
                    # If no categories exist, return None
                    return None

          

            def generate_fake_data(model_class, num_instances):
                for _ in range(num_instances):
                    fake_data = {
                        "site": site_info,
                        'name': fake.company(),
                        'description': fake.text(),
                        'image': random.choice(image_urls),
                        'icon': random.choice(bootstrap_icons),
                    }

                    if model_class == Testimonial:
                        fake_data.update({
                            'job_title': fake.job(),
                            'company': fake.company(),
                            'content': fake.paragraph(),
                        })

                    elif model_class == Offering: 
                        Offering_category = get_random_category() 
                        fake_data.update({
                            'category': Offering_category,
                        })
                    
                    elif model_class == Project:
                        Offering_category = get_random_category()
                        fake_data.update({
                            'category': Offering_category,
                            'client': fake.company(),
                            'file': "path/to/your/file.pdf",
                            'is_published': fake.boolean(),
                        })
                    
                    elif model_class == TeamMember:
                        fake_data.update({
                        'job_title': fake.job(),
                        'email': fake.email(),
                        'phone_number': fake.phone_number(),
                        'bio': fake.text()
                    })
                    
                    elif model_class == Testimonial:
                        fake_data.update({
                        'job_title': fake.job(),
                        'company': fake.company(),
                        'content': fake.text()
                    })
                   
                    instance = model_class(**fake_data)
                    instance.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully created {model_class.__name__}: {instance.name}'))

            # for model_class in [Marketing, Service, Feature, Offering, Project, TeamMember, Testimonial]:
            #     # Example usage for generating Testimonial instances
            #     generate_fake_data(model_class, 5)
                    
