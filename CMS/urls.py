from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from CMS.views import *

urlpatterns = [
      path('', ListSurveyView.as_view(), name='list_surveys'),
      path('add/', CreateSurveyView.as_view(), name='add_survey'),
      path('<int:pk>/edit/', UpdateSurveyView.as_view(), name='update_survey'),
      path('<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_survey'),

      path('download/', survey_export_csv, name='download_surveys'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)