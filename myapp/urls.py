from django.urls import path
from .import views
from myproject.settings import DEBUG,MEDIA_URL,MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('search',views.serach,name='search'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('news',views.news,name='news'),
    # path('another',views.another,name='another')

]

if DEBUG:
    urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT,)