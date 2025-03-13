from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.utils.text import slugify
from .models import Destination, BlogPost, BlogImage
from .forms import DestinationForm, BlogPostForm, BlogImageForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.files.storage import default_storage

# Define temporary file storage
file_storage = FileSystemStorage(location='media/temp/')



User = get_user_model()  # Use custom user model

# Signup View
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password1)
                messages.success(request, "Account created successfully! Please log in.")
                return redirect("login")
            else:
                messages.error(request, "Username already exists!")
        else:
            messages.error(request, "Passwords do not match!")

    return render(request, "signup.html")

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")



# =======================
# 🚀 Home Page View
# =======================
def home(request):
    latest_posts = BlogPost.objects.order_by('-created_at')[:10]  # Fetch latest 5 posts
    recent_posts = BlogPost.objects.order_by('-created_at')[:3]  # Fetch recent 3 posts for sidebar
    return render(request, 'home.html', {'latest_posts': latest_posts, 'recent_posts': recent_posts})


# =======================
# 📝 Blog Details View
# =======================
def blog_details(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'details.html', {'post': post})
# ======================
# 📸 Image Detail View
# =======================
def image_detail(request, image_id):
    image = get_object_or_404(BlogImage, id=image_id)
    related_images = BlogImage.objects.exclude(id=image_id)[:4]  # Fetch 4 related images
    
    return render(request, 'blog_details.html', {'image': image, 'related_images': related_images})

# =======================
# ✍️ Create Blog Post
# =======================
from django.shortcuts import render, redirect
from .models import Destination
from .forms import BlogPostForm

from django.shortcuts import render, redirect
from .models import Destination, BlogPost
from .forms import BlogPostForm


# def create_blog_post(request):
#     if request.method == "POST":
#         form_data = request.POST.copy()  # Make a mutable copy of POST data

#         # Check if a new destination was added via text input
#         new_destination = form_data.get("new_destination", "").strip()
#         if new_destination:
#             # Create a new Destination if it does not exist
#             destination, created = Destination.objects.get_or_create(
#                 title=new_destination,
#                 defaults={'slug': new_destination.lower().replace(" ", "-")}
#             )

#             # Assign the newly created destination ID to the form data
#             form_data['destination'] = destination.pk  

#         form = BlogPostForm(form_data, request.FILES)  # Pass updated form data

#         if form.is_valid():
#             form.save()
#             return redirect("home")  # Redirect on success

#     else:
#         form = BlogPostForm()

#     return render(request, "create_blog.html", {"form": form})
def create_blog_post(request):
    if request.method == "POST":
        form_data = request.POST.copy()  # Make a mutable copy

        # Check if user entered a new destination
        new_destination = form_data.get("new_destination", "").strip()
        if new_destination:
            destination, created = Destination.objects.get_or_create(
                title=new_destination,
                defaults={'slug': new_destination.lower().replace(" ", "-")}
            )
            form_data['destination'] = destination.pk  # Assign ID to form data

        form = BlogPostForm(form_data, request.FILES)  

        if form.is_valid():
            form.save()
            return redirect("home")  

    else:
        form = BlogPostForm()

    return render(request, "create_blog.html", {"form": form})