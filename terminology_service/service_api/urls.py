from django.urls import path

from .views import DirectoryView, DirectoryElementView, DirectoryCheckView

app_name = 'service_api'

urlpatterns = [
    path('refbooks/', DirectoryView.as_view(), name="directory-list"),
    path('refbooks/<int:id>/elements', DirectoryElementView.as_view(), name="element"),
    path('refbooks/<int:id>/check_element', DirectoryCheckView.as_view(), name="check"),
]
