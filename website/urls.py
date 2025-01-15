from django.urls import path
from website.views import HomeView, FaqView, PropertyView, PropertyDetailView, ContactView

urlpatterns = [path("", HomeView.as_view(), name="home_page"),
               path("catalog/", PropertyView.as_view(), name="properties_page"),
               path("catalog/<int:pk>", PropertyDetailView.as_view(), name="property_details_page"),
               path("faq/", FaqView.as_view(), name="faq_page"),
               path("contacts/", ContactView.as_view(), name="contacts_page"),
               ]