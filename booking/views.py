from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
import logging

logger = logging.getLogger(__name__)


class ClassListView(generics.ListAPIView):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        upcoming = self.queryset.filter(date_time__gte=timezone.now())
        logger.info(
            f"{len(upcoming)} upcoming classes fetched at {timezone.now()}"
        )
        return upcoming

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fitness_class = serializer.context['fitness_class']

        if Booking.objects.filter(
                fitness_class=fitness_class,
                client_email=serializer.validated_data['client_email']
        ).exists():
            return Response(
                {"error": "You have already booked this class"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = serializer.save()
        logger.info(f"New booking created: {booking}")

        return Response(
            {
                "message": "Booking successful",
                "booking_id": booking.id,
                "available_slots": booking.fitness_class.available_slots
            },
            status=status.HTTP_201_CREATED
        )


class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email:
            logger.info(f"Booking list requested for {email}")
            return Booking.objects.filter(client_email=email)
        logger.warning("Booking list requested without email")
        return Booking.objects.none()

    def list(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        if not email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().list(request, *args, **kwargs)
