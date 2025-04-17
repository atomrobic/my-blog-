from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This makes it an abstract model
class Destination(BaseModel):
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    
    def __str__(self):
        return self.title
class BlogPost(BaseModel):
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=100, choices=[('Adventure', 'Adventure'), ('Culture', 'Culture'), ('Food', 'Food'), ('Nature', 'Nature')])
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="blog_posts")
    author = models.CharField(max_length=100)  # Ensure this field exists
    background_image = models.URLField(blank=True, null=True)  # Support only URL, not file upload
      
    def __str__(self): 
        return f"{self.title} by {self.author}"



      
# Store multiple images for each BlogPost
class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='blog_images/')
    title = models.CharField(max_length=255)  # Title for each image
    description = models.TextField(blank=True, null=True)  # Description for each image
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets date when created
    updated_at = models.DateTimeField(auto_now=True)  # Stores last update time

    def __str__(self):
        return f"Image for {self.blog_post.title} - {self.title}"
  
    

class Comment(models.Model):
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name="comments", null=True, blank=True)  # Allow null
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Add user field
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(BlogImage, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    

