from django.urls import path
from . import views


urlpatterns = [
    path("<int:id>", views.index, name="index"),
    # path("property/<int:id>", views.property, name="index"),
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("view/", views.view, name="view"),
    path("propertyview/<int:id>", views.propertyview, name="view"),
    path('files/', views.file_list, name="file_list"),
    path('upload/', views.upload, name="upload"),
    path('files/upload/', views.file_upload, name="file_upload"),
    path('files/<int:pk>/', views.file_delete, name="file_delete"),
    # path('<str:url>', views.file_encrypt, name="file_encrypt"),
]
