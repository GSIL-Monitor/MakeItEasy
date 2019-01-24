from django.conf.urls import url, include


from makeiteasy.apps.blog import views


urlpatterns = [
    url(r'^index/', views.index),
    url(r'^page1/', views.page1),
    url(r'^page2/', views.page2),

]
