from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils import timezone
from django.conf import settings
import pytz


class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'date_time', 'instructor', 'available_slots']

    def get_local_time(self, obj):
        request = self.context.get('request')
        user_tz = request.query_params.get('tz') if request else settings.TIME_ZONE
        try:
            tz = pytz.timezone(user_tz)
        except pytz.UnknownTimeZoneError:
            tz = pytz.timezone('Asia/Kolkata')
        return obj.date_time.astimezone(tz).isoformat()


class BookingSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['class_id', 'client_name', 'client_email']

    def validate_class_id(self, value):
        try:
            fitness_class = FitnessClass.objects.get(pk=value)
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError("Class does not exist.")
        if fitness_class.date_time < timezone.now():
            raise serializers.ValidationError("Cannot book past classes.")
        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No slots available.")
        self.context['fitness_class'] = fitness_class
        return value

    def create(self, validated_data):
        validated_data.pop('class_id')
        fitness_class = self.context['fitness_class']
        booking = Booking.objects.create(
            fitness_class=fitness_class,
            **validated_data
        )
        fitness_class.available_slots -= 1
        fitness_class.save()
        return booking
