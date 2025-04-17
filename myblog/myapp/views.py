from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.utils.text import slugify
from .models import Destination, BlogPost, BlogImage,Comment
from .forms import DestinationForm, BlogPostForm, BlogImageForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.files.storage import default_storage

# Define temporary file storage
file_storage = FileSystemStorage(location='media/temp/')




# Signup View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
user = get_user_model()  # Use custom user model

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()
       
        # Check if fields are empty
        if not username or not password1 or not password2:
            messages.error(request, "All fields are required!")
            return redirect("signup")

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        # Create user if all conditions pass
        user = User.objects.create_user(username=username, password=password1)
        print(user)  # ✅ Now the "user" variable is used

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")
    return render(request, "signup.html")

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")

from django.shortcuts import render
def landing_page(request):
    """ Landing page with latest blog posts """
    latest_posts = BlogPost.objects.all().order_by('-created_at')[:16]  # Fetch latest 3 posts
    print("DEBUG: Latest Posts -", latest_posts)  # Debugging output
    return render(request, "landing.html", {"latest_posts": latest_posts})

# =======================
# 🚀 Home Page View
# =======================
def home(request):
    latest_posts = BlogPost.objects.all() # Fetch latest 5 posts
    print(BlogPost)
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
    comments = Comment.objects.filter(image=image)  # Fetch comments related to this image
    
    if request.method == "POST":
        content = request.POST.get('content')
        if content and request.user.is_authenticated:
            Comment.objects.create(
                image=image,
                user=request.user,
                name=request.user.username,  # Use authenticated username
                email=request.user.email,
                content=content,
                post=image.blog_post  # ✅ Pass blog_post_id from BlogImage
            )
            return redirect('image_detail', image_id=image.id)  # Redirect to refresh page

    return render(request, 'blog_details.html', {
        'image': image,
        'related_images': related_images,
        'comments': comments  # Pass the filtered comments
})




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
        new_destination = form_data.get("new_destination", "").strip()

        # ✅ Create a new destination if provided
        if new_destination:
            destination, created = Destination.objects.get_or_create(
                title=new_destination,
                defaults={'slug': new_destination.lower().replace(" ", "-")}
            )
            form_data['destination'] = destination.pk  # Assign ID to form data

        form = BlogPostForm(form_data, request.FILES)  

        if form.is_valid():
            blog_post = form.save()  # ✅ Save Blog Post

            # ✅ Handle multiple image uploads
            images = request.FILES.getlist("images")  # Get multiple images
            print('images')
            titles = request.POST.getlist("image_titles[]")
            descriptions = request.POST.getlist("image_descriptions[]")

            for i in range(len(images)):
                BlogImage.objects.create(
                    blog_post=blog_post,
                    image=images[i],
                    title=titles[i] if i < len(titles) else "",
                    description=descriptions[i] if i < len(descriptions) else "",
                )

            return redirect("home")  # ✅ Redirect to home page

    else:
        form = BlogPostForm()

    return render(request, "create_blog.html", {"form": form})


from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import BlogPost, BlogImage  # Import models

def create_blog_image(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if title and image:
            BlogImage.objects.create(
                blog_post=blog_post,
                title=title,
                description=description,
                image=image
            )
            return redirect(reverse("create_blog_image", kwargs={"post_id": post_id}))

    # Handle GET request (returning form)
    return render(request, "details.html", {"post": blog_post})


