from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='notes'
urlpatterns = [
    path('', views.notes_view.as_view(), name='notes'),
    path('<int:pk>/',views.detail_view.as_view(), name ='detail'),
    path('new',views.new_notes.as_view(),name='newnote'),
    path('<int:pk>/edit',views.update_notes.as_view(), name ='update'),
    path('logout', views.LogoutInterfaceView.as_view(), name='logout'),
    path('login', views.LoginInterfaceView.as_view(), name='login'),
    path('Signup', views.Signup.as_view(), name='Signup'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)