from django.urls import path

from .views import GoogleSocialAuthView

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
    # path('facebook/', FacebookSocialAuthView.as_view()),
    # path('twitter/', TwitterSocialAuthView.as_view()),


]
