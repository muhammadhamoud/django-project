from rest_framework import serializers
from communication.models import Subscriber, Contact

class SubscriberSerializer(serializers.ModelSerializer):
    # is_subscribed = serializers.BooleanField(default=True)
    # email = serializers.EmailField(.normalize_email(email.lower()))

    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'is_subscribed']

    def validate_email(self, value):
        subscriber = Subscriber.objects.filter(email=value).first()
        if subscriber:
            subscriber.is_subscribed = True
            subscriber.save()
            raise serializers.ValidationError("You have been resubscribed successfully.")
        return value
    

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
