from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views #import this


app_name='notes'
urlpatterns = [
    path('', views.notes_view.as_view(), name='notes'),
    path('mynotes/', views.mynotes.as_view(), name='mynotes'),
    path('<int:pk>/',views.detail_view.as_view(), name ='detail'),
    path('new',views.new_notes.as_view(),name='newnote'),
    path('<int:pk>/edit',views.update_notes.as_view(), name ='update'),
    path('<int:pk>/delete',views.deletenotes.as_view(), name ='delete'),
    path('search/',views.search.as_view(), name ='search'),
    path('logout', views.LogoutInterfaceView.as_view(), name='logout'),
    path('login', views.LoginInterfaceView.as_view(), name='login'),
    path('Signup', views.Signup.as_view(), name='Signup'),
    path("<int:pk>/comment", views.comment, name="comments"),
    path("<int:pk>/share", views.grouping, name = "share"),
    path("<int:pk>/remove", views.removing, name = "remove"),
    path("<int:pk>/remove_self", views.remove_self, name = "remove_self"),
    path("password_change", views.change_password, name='change_password'),
    #path('accounts/', include('django.contrib.auth.urls')),

    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

