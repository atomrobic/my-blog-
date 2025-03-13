from django.contrib import admin
from django.urls import path
from myapp.views import home, blog_details, image_detail, create_blog_post,signup_view,login_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin Panel
    path('', home, name='home'),  # Home page
    path('blogs/<int:pk>/', blog_details, name='blog_details'),  # Individual blog post
    path('image/<int:image_id>/', image_detail, name='image_detail'),  # Image detail page
    path('blog/create/', create_blog_post, name='create_blog_post'),  # Create blog post
    
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
