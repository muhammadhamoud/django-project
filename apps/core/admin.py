from django.contrib import admin

# Define the get_prepopulated_fields method for all inline classes
def get_prepopulated_fields(self, request, obj=None):
    return {'slug': ('name',)}

