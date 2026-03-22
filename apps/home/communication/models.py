from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
	name = models.CharField(max_length=250)
	email = models.EmailField()
	phone = models.CharField(max_length=30, blank=True, null=True)
	subject = models.CharField(max_length=250)
	message = models.TextField()
      
	action = models.BooleanField(default=False)
	submission_date = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.email


# "name": "test@test.com"
# "email": "test@test.com"
# "phone": "test@test.com"
# "subject": "test@test.com"
# "message": "test@test.com"