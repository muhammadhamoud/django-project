from django.db import models
from core.handle_images import compress_image
from core.models import Extensions
from django.urls import reverse
from core.models import base_image_path, validate_image_extension
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.db import models
# from django.utils.translation import gettext as _
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify

from core.models import BaseContent, DRY_TRANSLATION
	
class SiteInformation(Extensions, TranslatableModel):
	# Site Information Fields
	translations = DRY_TRANSLATION
	slogan = models.CharField(max_length=100, blank=True, null=True)
	company_name = models.CharField(max_length=100, blank=True, null=True)
	keywords = models.CharField(max_length=200, blank=True, null=True)
	license_number = models.CharField(max_length=200, blank=True, null=True)
	vat_number = models.CharField(max_length=200, blank=True, null=True)
	register_number = models.CharField(max_length=200, blank=True, null=True)

	is_featured = models.BooleanField(default=False)
	is_published = models.BooleanField(default=True)

	def __str__(self):
		return str(self.name)
	
	def save(self, *args, **kwargs):
		# self.name = str(self.name).title()
		super(SiteInformation, self).save(*args, **kwargs)

class SiteMetaData(Extensions):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='sitemetadata')
	logo = models.ImageField(
		upload_to='home/',
		validators=[validate_image_extension],
		blank=True,
		null=True,
		help_text=_("Upload Logo image."),
		verbose_name=_("Logo")
	)
	icon = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		help_text=_("Enter an icon for the content."),
		verbose_name=_("Icon")
	)
	# Contact Information Fields
	address = models.TextField(blank=True, null=True)
	telephone = models.CharField(blank=True, null=True, max_length=20)
	mobile = models.CharField(blank=True, null=True, max_length=20)
	fax = models.CharField(blank=True, null=True, max_length=20)
	email = models.EmailField(blank=True, null=True)
	website = models.URLField(blank=True, null=True)
	sales_email = models.EmailField(blank=True, null=True)
	technical_email = models.EmailField(blank=True, null=True)
	accounts_email = models.EmailField(blank=True, null=True)

	# Social Media URLs
	facebook = models.URLField(blank=True, null=True)
	twitter = models.URLField(blank=True, null=True)
	instagram = models.URLField(blank=True, null=True)
	github = models.URLField(blank=True, null=True)
	linkedin = models.URLField(blank=True, null=True)
	whatsapp = models.URLField(blank=True, null=True)
	googlemap = models.URLField(blank=True, null=True)
	youtube = models.URLField(blank=True, null=True)
	medium = models.URLField(blank=True, null=True)
	other_social = models.URLField(blank=True, null=True)

	def __str__(self):
		return str(self.site.name)

class SiteInformationAdditional(Extensions, TranslatableModel):
	site = models.OneToOneField(SiteInformation, on_delete=models.CASCADE, related_name='additional_info')	# Additional Site Information Fields
	translations = TranslatedFields(
		about_us = models.TextField(blank=True, null=True),
		privacy_policy = models.TextField(blank=True, null=True),
		terms_of_service = models.TextField(blank=True, null=True),
		tagline = models.CharField(max_length=200, blank=True, null=True),
	)
	
	def __str__(self):
		return str(self.site.name)
	
	def get_about_url(self):
		return reverse('homepage:about_us')

	def get_privacy_url(self):
		return reverse('homepage:privacy_policy')

	def get_terms_url(self):
		return reverse('homepage:terms_of_service')

class Marketing(TranslatableModel, BaseContent):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='marketings')
	translations = DRY_TRANSLATION
	
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('homepage:marketing-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)
		# Update the slug using the name field
		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(Marketing, self).save(*args, **kwargs)
	
class Service(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='services')
	translations = DRY_TRANSLATION
	
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('homepage:service-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)
		# Update the slug using the name field
		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(Service, self).save(*args, **kwargs)

class Feature(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='features')
	translations = DRY_TRANSLATION
	
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('homepage:feature-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)
		# Update the slug using the name field
		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(Feature, self).save(*args, **kwargs)

class Framework(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='frameworks')
	translations = DRY_TRANSLATION
	
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('homepage:framework-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)
		# Update the slug using the name field
		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)

		super(Framework, self).save(*args, **kwargs)

class BusinessCategory(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='product_categories')
	translations = DRY_TRANSLATION
	
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('homepage:product-category-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)
		# Update the slug using the name field
		# self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(BusinessCategory, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'Business Categories'
    
class Offering(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='offerings')
	translations = DRY_TRANSLATION
	category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('homepage:offering-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)
		# Update the slug using the name field
		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(Offering, self).save(*args, **kwargs)

	@property
	def image_url(self):
		try:
			url = self.image.url
		except:
			url = ""
		return url

class Project(BaseContent, TranslatableModel):
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='projects')
	translations = DRY_TRANSLATION
	category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
	client = models.CharField(max_length=256, blank=True, null=True)
	file = models.FileField(blank=True, null=True)
	# is_published = models.BooleanField(default=False)

	def __str__(self):
		return str(self.name)
	
	def get_absolute_url(self):
		return reverse('homepage:project-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):

		if self.image and self.image.name:
			self.image = compress_image(self.image)

		# Update the slug using the name field
		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(Project, self).save(*args, **kwargs)

class MenuItem(BaseContent, TranslatableModel):
	site = models.ForeignKey(
		SiteInformation,
		on_delete=models.CASCADE,
		related_name='menu_items'
	)

	translations = DRY_TRANSLATION

	parent = models.ForeignKey(
		'self',
		on_delete=models.CASCADE,
		related_name='children',
		blank=True,
		null=True
	)

	url = models.CharField(
		max_length=300,
		blank=True,
		null=True,
		help_text=_("Direct URL or anchor like /en/#services"),
		verbose_name=_("URL")
	)

	route_name = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		help_text=_("Optional Django route name like home or service-detail"),
		verbose_name=_("Route Name")
	)

	icon = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		help_text=_("FontAwesome icon class."),
		verbose_name=_("Icon")
	)

	anchor = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		help_text=_("Optional anchor like services or projects"),
		verbose_name=_("Anchor")
	)

	open_in_new_tab = models.BooleanField(default=False)
	is_dropdown = models.BooleanField(default=False)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order', '-modified']

	def __str__(self):
		return str(self.name)

	def get_absolute_url(self):
		if self.url:
			return self.url

		if self.route_name:
			try:
				base_url = reverse(self.route_name)
				if self.anchor:
					return f"{base_url}#{self.anchor}"
				return base_url
			except:
				pass

		if self.anchor:
			try:
				return f"{reverse('')}#{self.anchor}"
			except:
				return f"#{self.anchor}"

		return "#"

class TeamMember(BaseContent, TranslatableModel):
	# Personal Information
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='teammembers')
	
	translations = TranslatedFields(
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
		job_title = models.CharField(max_length=100, blank=True, null=True),
		bio = models.TextField(blank=True, null=True),
	)
	
	email = models.EmailField(blank=True, null=True)
	phone_number = models.CharField(max_length=20, blank=True, null=True)
	location = models.CharField(max_length=256, blank=True, null=True)

	# Social Media Profiles (optional)
	whatsapp = models.URLField(blank=True, null=True)
	linkedin = models.URLField(blank=True, null=True)
	twitter = models.URLField(blank=True, null=True)
	facebook = models.URLField(blank=True, null=True)
	instagram = models.URLField(blank=True, null=True)
	github = models.URLField(blank=True, null=True)
	medium = models.URLField(blank=True, null=True)

	def __str__(self):
		return f"{self.name or ''}"
	
	def get_absolute_url(self):
		return reverse('homepage:teammember-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)

		# Update the slug using the name field
		self.name = str(self.name).title()
		# self.slug = slugify(self.name)
		super(TeamMember, self).save(*args, **kwargs)
	
class Testimonial(BaseContent, TranslatableModel):
	translations = TranslatedFields(
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
		job_title = models.CharField(max_length=100, blank=True, null=True),
		company = models.CharField(max_length=100, blank=True, null=True),
		content = models.TextField(blank=True, null=True),
	)
	site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='testimonials')
	
	def __str__(self):
		return f"{str(self.name)}"
	
	def get_absolute_url(self):
		return reverse('homepage:testimonial-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)
			
		# Update the slug using the name field
		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(Testimonial, self).save(*args, **kwargs)


# ================================================
# Pricings
# ================================================
class PricingSection(TranslatableModel, BaseContent):
	"""
	Main pricing section for a site.
	Example: 'Pricing', 'Plans', 'Choose Your Plan'
	"""
	site = models.ForeignKey(
		'SiteInformation',
		on_delete=models.CASCADE,
		related_name='pricing_sections'
	)
	translations = DRY_TRANSLATION

	class Meta:
		verbose_name = "Pricing Section"
		verbose_name_plural = "Pricing Sections"
		ordering = ['-created']

	def __str__(self):
		return f"{str(self.name)}"

	def get_absolute_url(self):
		return reverse('homepage:pricing-detail', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)
		
		# name = self.safe_translation_getter('name', any_language=True)
		# if name:
		# 	self.name = str(name).title()

		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(PricingSection, self).save(*args, **kwargs)


class PricingPlan(TranslatableModel, BaseContent):
	"""
	Actual plan card like:
	Free / Starter / Pro / Enterprise
	"""
	BILLING_INTERVAL_CHOICES = (
		('free', 'Free'),
		('monthly', 'Monthly'),
		('quarterly', 'Quarterly'),
		('yearly', 'Yearly'),
		('one_time', 'One Time'),
		('custom', 'Custom'),
	)

	CURRENCY_CHOICES = (
		('USD', 'USD'),
		('EUR', 'EUR'),
		('GBP', 'GBP'),
		('AED', 'AED'),
		('SAR', 'SAR'),
	)

	section = models.ForeignKey(
		PricingSection,
		on_delete=models.CASCADE,
		related_name='plans'
	)

	translations = TranslatedFields(
		name=models.CharField(max_length=255),
		short_description=models.CharField(max_length=300, blank=True, null=True),
		description=models.TextField(blank=True, null=True),
		badge_text=models.CharField(max_length=100, blank=True, null=True),
		price_label=models.CharField(
			max_length=100,
			blank=True,
			null=True,
			help_text="Examples: Per Month, Per User / Month, Contact Us"
		),
		button_text=models.CharField(max_length=100, default="Get Started"),
		button_url=models.CharField(max_length=500, blank=True, null=True),
	)

	billing_interval = models.CharField(
		max_length=20,
		choices=BILLING_INTERVAL_CHOICES,
		default='monthly'
	)

	currency = models.CharField(
		max_length=10,
		choices=CURRENCY_CHOICES,
		default='USD'
	)

	price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		blank=True,
		null=True,
		help_text="Leave empty for Contact Us / Custom pricing"
	)

	compare_at_price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		blank=True,
		null=True,
		help_text="Optional old price for discounts"
	)

	trial_days = models.PositiveIntegerField(default=0)
	setup_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	is_popular = models.BooleanField(default=False)
	is_free = models.BooleanField(default=False)
	is_custom_price = models.BooleanField(
		default=False,
		help_text="Enable for enterprise or contact-sales plans"
	)

	allow_subscribe = models.BooleanField(default=True)
	allow_contact_sales = models.BooleanField(default=False)
	sort_order = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = "Pricing Plan"
		verbose_name_plural = "Pricing Plans"
		ordering = ['sort_order', 'id']

	def __str__(self):
		return f"{str(self.name)}"

	def get_absolute_url(self):
		return reverse('homepage:pricing-plan-detail', args=[str(self.slug)])

	@property
	def final_price_display(self):
		if self.is_free:
			return "Free"
		if self.is_custom_price or self.billing_interval == 'custom' or self.price is None:
			return "Contact Us"
		return f"{self.price}"

	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)

		if self.is_free:
			self.price = 0
			self.billing_interval = 'free'

		if self.is_custom_price:
			self.price = None
			
		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(PricingPlan, self).save(*args, **kwargs)


class PricingFeature(TranslatableModel, BaseContent):
	"""
	Feature rows under each plan.
	Example:
	- Unlimited Reports
	- Email Support
	- Advanced Analytics
	"""
	VALUE_TYPE_CHOICES = (
		('text', 'Text'),
		('boolean', 'Boolean'),
		('number', 'Number'),
	)

	plan = models.ForeignKey(
		PricingPlan,
		on_delete=models.CASCADE,
		related_name='features'
	)

	translations = TranslatedFields(
		name=models.CharField(max_length=255),
		description=models.CharField(max_length=300, blank=True, null=True),
		value_text=models.CharField(max_length=255, blank=True, null=True),
	)

	value_type = models.CharField(max_length=20, choices=VALUE_TYPE_CHOICES, default='boolean')
	value_boolean = models.BooleanField(default=True)
	value_number = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	sort_order = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = "Pricing Feature"
		verbose_name_plural = "Pricing Features"
		ordering = ['sort_order', 'id']

	def __str__(self):
		return f"{str(self.name)}"

	@property
	def display_value(self):
		if self.value_type == 'boolean':
			return self.value_boolean
		if self.value_type == 'number':
			return self.value_number
		return self.safe_translation_getter('value_text', any_language=True)

	def get_absolute_url(self):
		return reverse('homepage:pricing-features', args=[str(self.slug)])
	
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)

		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(PricingFeature, self).save(*args, **kwargs)


class PricingPlanLimit(TranslatableModel, BaseContent):
	"""
	Numeric usage limits per plan.
	Example:
	- Users: 10
	- Properties: 5
	- Reports / month: 100
	"""
	LIMIT_TYPE_CHOICES = (
		('integer', 'Integer'),
		('decimal', 'Decimal'),
		('unlimited', 'Unlimited'),
		('custom', 'Custom'),
	)

	plan = models.ForeignKey(
		PricingPlan,
		on_delete=models.CASCADE,
		related_name='limits'
	)

	translations = TranslatedFields(
		name=models.CharField(max_length=255),
		unit=models.CharField(max_length=100, blank=True, null=True),
		custom_value=models.CharField(max_length=255, blank=True, null=True),
	)

	limit_type = models.CharField(max_length=20, choices=LIMIT_TYPE_CHOICES, default='integer')
	value_integer = models.PositiveIntegerField(blank=True, null=True)
	value_decimal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	sort_order = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = "Pricing Plan Limit"
		verbose_name_plural = "Pricing Plan Limits"
		ordering = ['sort_order', 'id']

	def __str__(self):
		return str(self.safe_translation_getter('name', any_language=True) or "Plan Limit")

	@property
	def display_limit(self):
		if self.limit_type == 'unlimited':
			return "Unlimited"
		if self.limit_type == 'decimal':
			return self.value_decimal
		if self.limit_type == 'custom':
			return self.safe_translation_getter('custom_value', any_language=True)
		return self.value_integer
 
	def save(self, *args, **kwargs):
		if self.image and self.image.name:
			self.image = compress_image(self.image)

		self.name = str(self.name).title()
		if not self.id:
			self.slug = slugify(self.name)
		super(PricingPlanLimit, self).save(*args, **kwargs)




"""
Front-End Developer
Back-End Developer
Full-Stack Developer
Web Developer
UI/UX Designer
Web Application Developer
E-commerce Developer
Mobile App Developer
CMS Developer
Web Security Specialist
Web Accessibility Specialist
DevOps Engineer
Web Project Manager
Web Content Writer/Copywriter
Web Quality Assurance (QA) Tester

Data Scientist
Machine Learning Engineer
Data Analyst
Business Analyst
Data Engineer
Statistical Analyst
Quantitative Analyst (Quant)
Data Science Manager
Machine Learning Researcher
Data Science Consultant
Data Visualization Specialist
Natural Language Processing (NLP) Engineer
Computer Vision Engineer
AI Ethicist
Predictive Modeler
Healthcare Data Analyst

"""