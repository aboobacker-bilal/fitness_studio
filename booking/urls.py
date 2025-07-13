from django.urls import path
from .views import ClassListView, BookingCreateView, BookingListView

urlpatterns = [
    path('classes/', ClassListView.as_view(), name='classes'),
    path('book/', BookingCreateView.as_view(), name='book'),
    path('bookings/', BookingListView.as_view(), name='bookings'),
]
