from django.contrib import admin
from .models import BlogPost, Destination, Comment, UserProfile, BlogImage

# Inline model for multiple images inside BlogPost
class BlogImageInline(admin.TabularInline):  
    model = BlogImage
    extra = 3  # Show 3 empty image fields by default
    fields = ('image', 'title', 'description')  # Only display these fields

# Destination Model Admin
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('location', 'description')
    search_fields = ('location',)
    ordering = ('location',)

# BlogPost Model Admin
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'destination', 'created_at')
    search_fields = ('title', 'author', 'category')
    list_filter = ('category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    inlines = [BlogImageInline]  # Attach BlogImage inline

# Comment Model Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at')
    search_fields = ('name', 'email', 'content')
    ordering = ('-created_at',)

# UserProfile Model Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

# BlogImage Model Admin (Separate Registration)
@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'title', 'image')
    search_fields = ('title', 'blog_post__title')
