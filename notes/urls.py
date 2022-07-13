from django.urls import path

from . import views
app_name='notes'
urlpatterns = [
    path('', views.notes_view.as_view(), name='notes'),
    path('<int:pk>/',views.detail_view.as_view(), name ='detail'),
    path('new',views.new_notes.as_view(),name='newnote'),
    path('<int:pk>/edit',views.update_notes.as_view(), name ='update'),

]