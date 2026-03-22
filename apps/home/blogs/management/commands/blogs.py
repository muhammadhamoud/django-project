
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from blogs.models import *
from faker import Faker
fake = Faker()

import pandas as pd
import os
from django.conf import settings

def get_data_list():
    xl = pd.ExcelFile(os.path.join(Path(__file__).resolve().parent.parent.parent, "fixtures", "blogs.xlsx"))

    data_list = {}
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name=sheet_name)
        df.fillna('', inplace=True)
        data_list[sheet_name] = df
        print(sheet_name)
        exec('{} = df'.format(sheet_name))
    
    return data_list

data_list = get_data_list()


class Command(BaseCommand):
    help = 'Flush (truncate) or generate fake data for specified models'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Flush (truncate) model tables')
        parser.add_argument('--generate', action='store_true', help='Generate fake data for model tables')
        parser.add_argument('--models', nargs='+', type=str, help='Specify models to operate on')

    def handle(self, *args, **options):
        if options['flush'] and options['generate']:
            raise CommandError("Cannot flush and generate data at the same time.")

        if not options['flush'] and not options['generate']:
            raise CommandError("Please specify either --flush or --generate.")

        if options['flush']:
            if options['models']:
                self.flush_data(options['models'])
            else:
                self.flush_all_models()
        elif options['generate']:
            if options['models']:
                self.generate_data(options['models'])
            else:
                self.generate_all_models()

    def flush_data(self, models):
        for model_name in models:
            try:
                model = apps.get_model(self.get_app_name(), model_name)
                model.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f"Successfully flushed data for {model_name}."))
            except LookupError:
                self.stdout.write(self.style.ERROR(f"Model {model_name} not found."))

    def flush_all_models(self):
        for model in apps.get_app_config(self.get_app_name()).get_models():
            try:
                model._default_manager.all().delete()
                self.stdout.write(self.style.SUCCESS(f"Successfully flushed data for {model._meta.verbose_name_plural}."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to flush data for {model._meta.verbose_name_plural}: {e}"))

    def generate_all_models(self):
        pass

    def generate_data(self, models):
        for model_name in models:
            try:
                model = apps.get_model(self.get_app_name(), model_name)
                print(model_name, model)
                self.load_data_into_model(model_name, data_list[model_name])
                self.stdout.write(self.style.SUCCESS(f"Successfully generated data for {model_name}."))
            except LookupError:
                self.stdout.write(self.style.ERROR(f"Model {model_name} not found."))

    def load_data_into_model_dfterr(self, model_name, df):
        try:
            model = apps.get_model(self.get_app_name(), model_name)
            for index, row in df.iterrows():
                model_instance = model()
                for column in df.columns:
                    if hasattr(model_instance, column):
                        if column == 'tag' or column == 'attribute':
                            # Handle Many-to-Many relationships
                            m2m_field = getattr(model_instance, column)
                            values = row[column].split(',')  # Assuming multiple values are separated by commas
                            for value in values:
                                # Assuming your Tag and Attribute models have a 'name' field
                                try:
                                    related_model = apps.get_model(self.get_app_name(), column.capitalize()).objects.get(name=value)
                                    m2m_field.add(related_model)  # Use add() method to add related model
                                except related_model.DoesNotExist:
                                    self.stdout.write(self.style.ERROR(f"Related instance {value} does not exist for {column.capitalize()}."))

                        else:
                            setattr(model_instance, column, row[column])
                        # if column == 'tag' or column == 'attribute':
                        #     # Handle Many-to-Many relationships
                        #     m2m_field = getattr(model_instance, column)
                        #     values = row[column].split(',')  # Assuming multiple values are separated by commas
                        #     for value in values:
                        #         # Assuming your Tag and Attribute models have a 'name' field
                        #         try:
                        #             related_model = apps.get_model(self.get_app_name(), column.capitalize()).objects.get(name=value)
                        #             m2m_field.add(related_model)
                        #         except related_model.DoesNotExist:
                        #             self.stdout.write(self.style.ERROR(f"Related instance {value} does not exist for {column.capitalize()}."))

                        # else:
                        #     setattr(model_instance, column, row[column])

                try:
                    model_instance.save()

                    self.update_translations(
                        model=model_instance, 
                        name=row.name_ar, 
                        description=row.description_ar, 
                        language_code='ar'
                    )

                    image_path = self.get_image_path(image=row.image, path=model_name)
                    if image_path is not None:
                        if not image_path.endswith('no-image.jpg'):
                            model_instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

                    self.stdout.write(self.style.SUCCESS(f"Successfully loaded data for {model_name}."))
                except AttributeError as e:
                    self.stdout.write(self.style.ERROR(f"Error while saving data for {model_name}: {e}"))
        except LookupError:
            self.stdout.write(self.style.ERROR(f"Model {model_name} not found."))

            
    def load_data_into_model(self, model_name, df):
        try:
            model = apps.get_model(self.get_app_name(), model_name)
            # model.objects.all().delete()  # Clear existing data
            for index, row in df.iterrows():
                model_instance = model()
                for column in df.columns:
                    setattr(model_instance, column, row[column])
                model_instance.save()

                self.update_translations(
                    model=model_instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )

                image_path = self.get_image_path(image=row.image, path=model_name)
                if image_path is not None:
                    if not image_path.endswith('no-image.jpg'):
                        model_instance.image.save(os.path.basename(image_path), open(image_path, 'rb'))

            self.stdout.write(self.style.SUCCESS(f"Successfully loaded data for {model_name}."))
        
        except LookupError:
            self.stdout.write(self.style.ERROR(f"Model {model_name} not found."))    


    def get_app_name(self):
        # Custom method to get the current app name based on your project structure.
        # You might need to modify this to fit your project's structure.
        return "categories"  # Replace with the actual app name
    
    def get_image_path(self, image, path):
        try:
            # Change this to the path of your folder containing random images
            folder_path = fr'C:\Backup\ng\backend\api\loading_images\hamouds\{path}'
            # print(image)
            # Get a list of file names in the specified folder
            image_files = [os.path.basename(f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            # Check if the image name exists in the list of files
            filename = 'no-image.jpg'
            if isinstance(image, (int, float)):
                image = str(int(image))

            for file in image_files:
                if file.startswith(str(image) + "." ):
                    filename = file
                    break

            image_path = os.path.join(folder_path, filename)
            
            return image_path
        except Exception as ex:
            # print(ex)
            return None
    

    def update_translations(self, model, name, description, language_code, *args, **kwargs):
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


# dataframes = [blogcategory, blogtag, post, blogimage] #, favoritepost, like, comment, bloguser]
# models = [BlogCategory, BlogTag, Post, BlogImage] #, FavoritePost, Like, Comment, BlogUser]

# for model_class in models:
    
#     # Construct the dataframe variable name from the model class name
#     dataframe_variable_name = model_class.__name__.lower()

#     # Assuming the dataframe variable is in the global namespace, retrieve it
#     data_frame = globals()[dataframe_variable_name]
#     # print(data_frame)
#     data_frame.fillna('', inplace=True)


# def update_translations(model, name, description, language_code, *args, **kwargs):
#     # Ensure you set the language for which you want to update the translations
#     model.set_current_language(language_code)

#     # Update the translation fields with the provided data
#     model.name = name
#     model.description = description

#     # Save the translation instance
#     model.save()

#     # Make sure to set the current language back to the original language
#     model.set_current_language('en')  # Replace 'en' with your original language code
#     model.save()

#     print(f'Successfully created: {model.name}')


# class Command(BaseCommand):
#     help = 'Flush (truncate) or generate fake data for specified models'

#     def add_arguments(self, parser):
#         parser.add_argument('--flush', action='store_true', help='Flush (truncate) model tables')
#         parser.add_argument('--generate', action='store_true', help='Generate fake data for model tables')

#     def handle(self, *args, **options):

#         flush_models = models

#         if options['flush']:
#             # Flush (truncate) the tables for specified models
#             for model in flush_models:
#                 model._default_manager.all().delete()
#                 self.stdout.write(self.style.SUCCESS(f'Successfully flushed {model._meta.verbose_name_plural} table.'))

#         if options['generate']:
#             for model in models:
#                 # load_data_and_translations(model_class=model)
