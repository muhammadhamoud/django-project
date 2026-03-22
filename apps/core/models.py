import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.handle_images import compress_image
from .managers import SoftDeleteManager
import os
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from parler.models import TranslatableModel, TranslatedFields, TranslatedFieldsModel, TranslatedField


def handle_slug(sender, instance, *args, **kwargs):
    try:
        if instance.slug is None or isinstance.slug == "":
            new_slug = slugify(instance.name)
            klass = instance.__class__
            qs = klass.objects.filter(slug__icontains=new_slug).exclude(
                _id=instance._id
            )
            if qs.count() == 0:
                instance.slug = new_slug
            else:
                instance.slug = f"{new_slug}-{qs.count()}"
    except:
        pass


DRY_TRANSLATION = TranslatedFields(
	name=models.CharField(
		max_length=100,
		help_text=_("Enter a name for the content."),
		verbose_name=_("Name"),
		blank=True,
		null=True	
	),
	description=models.TextField(
		blank=True,
		null=True,
		help_text=_("Enter a description for the content."),
		verbose_name=_("Description")
	),
)

DRY_TRANSLATION_UNIQUE = TranslatedFields(
	name=models.CharField(
		max_length=100,
		help_text=_("Enter a name for the content."),
		verbose_name=_("Name"),
		blank=True,
		null=True,
        unique=True	
	),
	description=models.TextField(
		blank=True,
		null=True,
		unique=True,	
		help_text=_("Enter a description for the content."),
		verbose_name=_("Description")
	),
)

def validate_image_extension(value):
	"""Function to validate the image extension"""
	allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.jfif', '.avif']
	ext = os.path.splitext(value.name)[1]
	if str(ext).lower() not in allowed_extensions:
		raise ValidationError(f"Invalid image extension. Allowed extensions are {allowed_extensions}")

def base_image_path(instance, filename):

	# Split the filename and file extension
	name, ext = os.path.splitext(filename)

	# Access the model name
	model_name = str(instance.__class__._meta.model_name).lower()

	# Construct a new filename with the model name and slugified instance name
	try:
		slug = slugify(instance.name)
	except:
		slug = filename

	new_filename = f"{model_name}/{slug}{ext}"

	# # Construct a new filename with the slug and original extension
	# slug = slugify(instance.name)
	# new_filename = f"{slug}{ext}"
	# Construct the upload path
	return f"images/{new_filename}"


def base_file_path_protected(instance, filename):
    # Split the filename and file extension
    name, ext = os.path.splitext(filename)
    # Construct a new filename with the slug and original extension
    slug = slugify(instance.slug)
    new_filename = f"{instance.slug} {ext}"
    # Construct the upload path
    return f"protected/{new_filename}"

def custom_upload_path_html(instance, filename):
    # Define the subdirectory where the file will be stored
    subdirectory = 'downloads'  # Customize this as needed
    # Remove any non-HTML files
    name, ext = os.path.splitext(filename)
    if ext.lower() not in ['.html']:
        raise ValidationError("Only HTML files are allowed.")
    # Define the filename for the uploaded file without the extension
    new_filename = slugify(name)
    # Combine the subdirectory and filename to create the final path
    return os.path.join(subdirectory, new_filename+ext.lower())

def custom_upload_path_rm(instance, filename):
    # Define the subdirectory where the file will be stored
    subdirectory = 'downloads'  # Customize this as needed
    # Remove any non-HTML files
    name, ext = os.path.splitext(filename)
    if ext.lower() not in ['.rm', '.md']:
        raise ValidationError("Only Markdown files are allowed.")
    # Define the filename for the uploaded file without the extension
    new_filename = slugify(name)
    # Combine the subdirectory and filename to create the final path
    return os.path.join(subdirectory, new_filename+ext.lower())

def custom_upload_path(instance, filename):
	# Define the subdirectory where the file will be stored
	subdirectory = 'downloads'  # Customize this as needed
	name, ext = os.path.splitext(filename)
	new_filename = f"{slugify(name)} {ext}"
	# Define the filename for the uploaded file

	# Combine the subdirectory and filename to create the final path
	return os.path.join(subdirectory, new_filename)


class PrimaryKeyUUID(models.Model):
	id = models.UUIDField(
		db_index=True, 
		default=uuid.uuid4, 
		primary_key=True, 
		verbose_name='ID', 
		editable=False, 
		unique=True
	)

	class Meta:
		abstract = True

class BaseContent(models.Model):
     
	slug = models.SlugField(
		# unique=True,
		blank=True,
		null=True,
		help_text=_("Enter a slug for the content."),
		verbose_name=_("Slug")
	)
	image = models.ImageField(
		upload_to=base_image_path,
		validators=[validate_image_extension],
		blank=True,
		null=True,
		help_text=_("Upload an image for the content."),
		verbose_name=_("Image"),
	)
	icon = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		help_text=_("Enter an icon for the content."),
		verbose_name=_("Icon")
	)
	
	is_featured = models.BooleanField(default=False)
	is_published = models.BooleanField(default=True)

	created = models.DateTimeField(
		auto_now_add=True,
		db_index=True,
		help_text=_("The date and time when the content was created."),
		verbose_name=_("Created")
	)
	modified = models.DateTimeField(
		auto_now=True,
		help_text=_("The date and time when the content was last modified."),
		verbose_name=_("Modified")
	)
    
	class Meta:
		abstract = True
		ordering = ['-modified']
          
	def save(self, *args, **kwargs):
		
		# Check if the image field is not None and has a file associated with it
		if self.image and not self.image.name:
			self.image = compress_image(self.image)
		
		# Update the slug using the name field
		# self.slug = slugify(self.name)
		super(BaseContent, self).save(*args, **kwargs)
            
	@property
	def image_url(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url


class BaseContentOld(models.Model):

	name = models.CharField(
		max_length=100,
		help_text=_("Enter a name for the content."),
		verbose_name=_("Name")
	)
	slug = models.SlugField(
		# unique=True,
		blank=True,
		null=True,
		help_text=_("Enter a slug for the content."),
		verbose_name=_("Slug")
	)
	description = models.TextField(
		blank=True,
		null=True,
		help_text=_("Enter a description for the content."),
		verbose_name=_("Description")
	)
	image = models.ImageField(
		upload_to=base_image_path,
		validators=[validate_image_extension],
		blank=True,
		null=True,
		help_text=_("Upload an image for the content."),
		verbose_name=_("Image")
	)
	icon = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		help_text=_("Enter an icon for the content."),
		verbose_name=_("Icon")
	)
	created = models.DateTimeField(
		auto_now_add=True,
		db_index=True,
		help_text=_("The date and time when the content was created."),
		verbose_name=_("Created")
	)
	modified = models.DateTimeField(
		auto_now=True,
		help_text=_("The date and time when the content was last modified."),
		verbose_name=_("Modified")
	)
    
	class Meta:
		abstract = True
		ordering = ['-modified', 'name']
		

	def save(self, *args, **kwargs):
		# Update the slug using the name field
		self.image = compress_image(self.image)
		self.slug = slugify(self.name)
		super(BaseContent, self).save(*args, **kwargs)

class TimeStampedModel(models.Model):
    # id = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, verbose_name='ID', editable=False, unique=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Extensions(models.Model):
    """ Best practice for lookup field url instead pk or slug """
    # uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ModelExtensions(models.Model):
    """ Best practice for lookup field url instead pk or slug """
    id = models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, verbose_name='ID', editable=False, unique=True)
    # uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100,
        help_text=_('Enter a name.'),
        verbose_name=_('Name'),
    )
    description = models.TextField(
        help_text=_('Enter a description.'),
        verbose_name=_('Description'),
        blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UUIDModel(models.Model):
    """ 
    Best practice for lookup field url instead pk or slug.
    for security
    """
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

class IncrementingIntegerField(models.BigIntegerField):
    # Used as confirmation number
    def __init__(self, start_value=10000, *args, **kwargs):
        kwargs['editable'] = False  # The field should not be edited manually
        kwargs['unique'] = True  # Ensure uniqueness of values
        kwargs['default'] = start_value  # Set the default value to the starting value
        super(IncrementingIntegerField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if add and self.default:
            # Calculate and set the next unique value
            value = self.get_next_value(model_instance)
            setattr(model_instance, self.attname, value)
            return value
        return super(IncrementingIntegerField, self).pre_save(model_instance, add)

    def get_next_value(self, model_instance):
        # Find the maximum value currently in the database
        max_value = type(model_instance)._default_manager.aggregate(
            max_value=models.Max(self.attname)
        )['max_value'] or 10000
        # Calculate the next unique value by incrementing the maximum value
        return max_value + 1


class RentalBaseModel(models.Model):
    id = models.UUIDField(
		db_index=True, 
		default=uuid.uuid4, 
		primary_key=True, 
		verbose_name='ID', 
		editable=False, 
		unique=True
	)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
