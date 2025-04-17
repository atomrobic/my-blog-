from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp import views

urlpatterns = [
    # 🌍 Landing & Home Pages
    path('landing/', views.landing_page, name='landing_page'),  # Landing Page
    path('home/', views.home, name='home'),  # Home Page

    # 🔐 Authentication URLs
    path('signup/', views.signup_view, name='signup'),  # Signup Page
    path('login/', views.login_view, name='login'),  # Login Page

    # 📝 Blog URLs
    path('blog/<int:pk>/', views.blog_details, name='blog_details'),  # Blog Details Page
    path('blog/create/', views.create_blog_post, name='create_blog_post'),  # Create Blog Post
    path('blog/<int:post_id>/add-image/', views.create_blog_image, name='create_blog_image'),  # Add Image to Blog

    # 📸 Image URLs
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),  # Image Detail Page

    # ⚙️ Admin Panel
    path('admin/', admin.site.urls),  # Admin Dashboard
]

# ✅ Serve Media Files in Debug Mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
