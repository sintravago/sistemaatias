from django.urls import include, path
from .views import EmailUpdate, EmailDoneView

registration_patterns = ([
    path('accounts/email_change/', EmailUpdate.as_view(), name="email_form"),
    path('accounts/email_done/', EmailDoneView.as_view(), name="email_done"),
], 'registration')

urlpatterns = [
    path('', include(registration_patterns)),
]