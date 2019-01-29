from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from CMS.views import *

urlpatterns = [
      path('users/', ListUsersView.as_view(), name='list_users'),
      path('user/add/', CreateUserView.as_view(), name='add_user'),
      path('user/<int:pk>/edit/', UpdateUserView.as_view(), name='update_user'),
      path('user/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),

      path('', ListSurveyView.as_view(), name='list_surveys'),
      path('add/', CreateSurveyView.as_view(), name='add_survey'),
      path('<int:pk>/edit/', UpdateSurveyView.as_view(), name='update_survey'),
      path('<int:pk>/delete/', DeleteSurveyView.as_view(), name='delete_survey'),
      path('<int:pk>/detail/', DetailSurveyView.as_view(), name='survey_detail'),

      path('type/', ListApplicationMasterTypesView.as_view(), name='list_master_types'),
      path('type/add/', CreateApplicationMasterTypeView.as_view(), name='add_master_type'),
      path('type/<int:pk>/edit/', UpdateApplicationMasterTypeView.as_view(), name='update_master_type'),
      path('type/<int:pk>/delete/', DeleteApplicationMasterTypeView.as_view(), name='delete_master_type'),

      path('download/', survey_export_csv, name='download_surveys'),
      path('upload/', ImportDataView.as_view(), name='upload_surveys'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)