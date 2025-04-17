# import os
# import django
# import requests
# from django.core.files.base import ContentFile
# from django.core.management.base import BaseCommand
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# # ✅ Set up Django settings module
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
# django.setup()

# # ✅ Import Django models after setting up Django
# from myapp.models import BlogPost, Destination, BlogImage

# class Command(BaseCommand):
#     help = "Scrape images, titles, and descriptions using Selenium and create blog posts"

#     def handle(self, *args, **kwargs):
#         self.stdout.write(self.style.SUCCESS("🚀 Starting Selenium scraping for images, titles & descriptions..."))

#         # **Setup Selenium WebDriver**
#         driver = self.setup_driver()
#         if not driver:
#             return

#         # **List of websites to scrape images & titles from**
#         websites = [
#             {
#                 "url": "https://blogs.malayalam.samayam.com/",
#                 "title_tag": "h3",
#                 "image_tag": "img",
#                 "link_tag": "a",
#                 "description_selector": "longform-block p"  # Updated to a CSS selector
#             }
#         ]

#         # ✅ **Ensure Destination Exists**
#         destination, _ = Destination.objects.get_or_create(location="Kerala")

#         # ✅ **Ensure Media Directory Exists**
#         os.makedirs("media/blog_images", exist_ok=True)

#         for site in websites:
#             self.scrape_website(driver, site, destination)
        
#         driver.quit()
#         self.stdout.write(self.style.SUCCESS("✅ Scraping Completed!"))

#     def setup_driver(self):
#         """Setup and return a Selenium WebDriver instance."""
#         try:
#             options = Options()
#             options.add_argument("--headless")
#             options.add_argument("--disable-gpu")
#             options.add_argument("--no-sandbox")
#             options.add_argument("--disable-dev-shm-usage")
#             driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#             self.stdout.write(self.style.SUCCESS("✅ Selenium WebDriver initialized successfully!"))
#             return driver
#         except Exception as e:
#             self.stderr.write(self.style.ERROR(f"❌ Error initializing WebDriver: {e}"))
#             return None

#     def scrape_website(self, driver, site, destination):
#         """Scrape blog posts from a website."""
#         try:
#             driver.get(site["url"])
#             self.stdout.write(self.style.SUCCESS(f"🔍 Scraping site: {site['url']}"))
            
#             # ✅ Extract Titles
#             titles = [t.text.strip() for t in driver.find_elements(By.TAG_NAME, site["title_tag"]) if t.text.strip()]
#             self.stdout.write(self.style.SUCCESS(f"✅ Found {len(titles)} titles"))

#             # ✅ Extract Links to Blog Detail Pages
#             links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, site["link_tag"]) if a.get_attribute("href")]
#             self.stdout.write(self.style.SUCCESS(f"✅ Found {len(links)} blog detail links"))

#             # ✅ Extract Images
#             image_urls = [img.get_attribute("src") for img in driver.find_elements(By.TAG_NAME, site["image_tag"]) if img.get_attribute("src") and img.get_attribute("src").startswith("http")]
#             self.stdout.write(self.style.SUCCESS(f"✅ Found {len(image_urls)} images"))

#             # ✅ Ensure all lists are of equal length
#             min_length = min(len(titles), len(links), len(image_urls))
#             titles = titles[:min_length]
#             links = links[:min_length]
#             image_urls = image_urls[:min_length]

#             # ✅ Save Data to Django Models
#             self.save_blogs(driver, titles, links, image_urls, destination, site)
#         except Exception as e:
#             self.stderr.write(self.style.ERROR(f"❌ Error accessing website {site['url']}: {e}"))

#     def save_blogs(self, driver, titles, links, image_urls, destination, site):
#         """Save blog posts and images to the database."""
#         for index, (title, link, img_url) in enumerate(zip(titles, links, image_urls)):
#             try:
#                 # Navigate to the blog detail page
#                 driver.get(link)
#                 self.stdout.write(self.style.SUCCESS(f"➡️ Navigating to blog detail page: {link}"))

#                 # ✅ Extract Description using CSS Selector
#                 try:
#                     WebDriverWait(driver, 5).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, site["description_selector"]))
#                     )
#                     descriptions = [d.text.strip() for d in driver.find_elements(By.CSS_SELECTOR, site["description_selector"]) if d.text.strip()]
#                     description = " ".join(descriptions) if descriptions else "No description available"
#                     print(description)
#                 except Exception:
#                     description = "No description available"

#                 self.stdout.write(self.style.SUCCESS(f"📝 Extracted description: {description}"))

#                 # Download the image
#                 response = requests.get(img_url, stream=True)
#                 if response.status_code == 200:
#                     # ✅ **Create Blog Post**
#                     blog_post = BlogPost.objects.create(
#                         title=title,
#                         content=description,  # Use the scraped description here
#                         category="Nature",
#                         destination=destination,
#                         author="Admin",
#                         background_image=img_url
#                     )

#                     # ✅ **Save Image to BlogPost**
#                     img_name = f"blog_image_{index+1}.jpg"
#                     blog_post.featured_image.save(img_name, ContentFile(response.content), save=True)

#                     # ✅ **Save Blog Image Details**
#                     BlogImage.objects.create(
#                         blog_post=blog_post,
#                         image=img_url,  # Storing the image URL in the model
#                         title=title,  # Using the blog title as the image title
#                         description=description  # Now using the actual scraped description
#                     )

#                     self.stdout.write(self.style.SUCCESS(f"✅ Created BlogPost: {blog_post.title}"))
#                 else:
#                     self.stderr.write(self.style.ERROR(f"❌ Failed to download image: {img_url}"))

#                 # Navigate back to the main page
#                 driver.back()
#                 self.stdout.write(self.style.SUCCESS(f"⬅️ Navigated back to main page"))
#             except Exception as e:
#                 self.stderr.write(self.style.ERROR(f"❌ Error processing blog {title}: {e}"))

# import time
# from django.core.management.base import BaseCommand
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# class Command(BaseCommand):
#     help = "Automate signup and login testing using Selenium"

#     def handle(self, *args, **kwargs):
#         """Run the automation script."""
#         options = Options()
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-gpu")
#         # Uncomment the next line if you want to run headless
#         # options.add_argument("--headless")  

#         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#         try:
#             self.test_signup()
#             self.test_login()
#         finally:
#             self.driver.quit()

#     def open_site(self, url):
#         """Open the specified site."""
#         try:
#             print(f"🔍 Opening site: {url}")
#             self.driver.get(url)
#             time.sleep(2)  # Wait for the page to load
#             print(f"✅ Successfully opened {url}")
#         except Exception as e:
#             print(f"❌ Error opening site {url}: {e}")
#             self.driver.quit()
#             raise SystemExit()

#     def test_signup(self):
#         """Automate the signup process."""
#         self.open_site("http://127.0.0.1:8000/signup/")
#         try:
#             wait = WebDriverWait(self.driver, 10)

#             print("⏳ Locating username field...")
#             username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
#             print("✅ Username field found")
#             username_field.send_keys("makkuuggg")

#             print("⏳ Locating password field...")
#             password1_field = wait.until(EC.presence_of_element_located((By.NAME, "password1")))
#             print("✅ Password field found")
#             password1_field.send_keys("Test@12345")

#             print("⏳ Locating confirm password field...")
#             password2_field = wait.until(EC.presence_of_element_located((By.NAME, "password2")))
#             print("✅ Confirm password field found")
#             password2_field.send_keys("Test@12345")

#             print("⏳ Locating submit button...")
#             submit_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
#             print("✅ Submit button found, clicking it now...")
#             submit_button.click()  

#             print("🔍 Checking for signup success message...")
#             time.sleep(3)  

#             page_source = self.driver.page_source  

#             # Check for a success message or redirection
#             if "Account created successfully!" in page_source or "Welcome!" in page_source:
#                 print("✅ Signup successful!")
#             elif "/login/" in self.driver.current_url:
#                 print("✅ Signup successful, redirected to login page")
#             else:
#                 print("❌ Signup failed: No success message found.")
#                 self.driver.quit()
#                 raise SystemExit()

#         except Exception as e:
#             print(f"❌ Signup failed: {e}")
#             self.driver.quit()
#             raise SystemExit()

#     def test_login(self):
#         """Automate the login process."""
#         self.open_site("http://127.0.0.1:8000/login/")  
#         try:
#             wait = WebDriverWait(self.driver, 5)

#             print("⏳ Locating username field...")
#             username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
#             print("✅ Username field found")
#             username_field.send_keys("makkuuggg")

#             print("⏳ Locating password field...")
#             password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
#             print("✅ Password field found")
#             password_field.send_keys("Test@12345")

#             print("⏳ Locating submit button...")
#             submit_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
#             print("✅ Submit button found, clicking it now...")
#             submit_button.click()

#             print("🔍 Checking for login success...")
#             time.sleep(3)

#             # Check for successful login by verifying the presence of a "Logout" link
#             if "Logout" in self.driver.page_source:
#                 print("✅ Login successful")
#             else:
#                 print("❌ Login failed: No logout link found.")
#                 self.driver.quit()
#                 raise SystemExit()

#         except Exception as e:
#             print(f"❌ Login failed: {e}")
#             self.driver.quit()
#             raise SystemExit()


# from myapp.models import BlogPost, BlogImage, Destination  # Ensure correct import
# import time
# import requests
# from django.core.management.base import BaseCommand
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from django.core.files.base import ContentFile


# from myapp.models import BlogPost, BlogImage, Destination  # Ensure correct import
# import time
# import requests
# from django.core.management.base import BaseCommand
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from django.core.files.base import ContentFile


# class Command(BaseCommand):
#     help = "Automate signup, login, blog scraping, and blog creation testing using Selenium"

#     def handle(self, *args, **kwargs):
#         """Run the automation script."""
#         options = Options()
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-gpu")
#         # options.add_argument("--headless")  # Uncomment for headless mode

#         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#         try:
#             self.test_signup()
#             self.test_login()
#             self.scrape_and_create_blog()
#         finally:
#             self.driver.quit()

#     def open_site(self, url):
#         """Open the specified site."""
#         try:
#             print(f"🔍 Opening site: {url}")
#             self.driver.get(url)
#             time.sleep(2)  # Wait for the page to load
#             print(f"✅ Successfully opened {url}")
#         except Exception as e:
#             print(f"❌ Error opening site {url}: {e}")
#             self.driver.quit()
#             raise SystemExit()

#     def test_signup(self):
#         """Automate the signup process."""
#         self.open_site("http://127.0.0.1:8000/signup/")
#         try:
#             wait = WebDriverWait(self.driver, 10)

#             username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
#             username_field.send_keys("auecfoi")

#             password1_field = wait.until(EC.presence_of_element_located((By.NAME, "password1")))
#             password1_field.send_keys("Test@12345")

#             password2_field = wait.until(EC.presence_of_element_located((By.NAME, "password2")))
#             password2_field.send_keys("Test@12345")

#             submit_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
#             submit_button.click()

#             time.sleep(3)
#             if "Account created successfully!" in self.driver.page_source or "/login/" in self.driver.current_url:
#                 print("✅ Signup successful!")
#             else:
#                 print("❌ Signup failed")
#                 self.driver.quit()
#                 raise SystemExit()

#         except Exception as e:
#             print(f"❌ Signup failed: {e}")
#             self.driver.quit()
#             raise SystemExit()

#     def test_login(self):
#         """Automate the login process."""
#         self.open_site("http://127.0.0.1:8000/login/")
#         try:
#             wait = WebDriverWait(self.driver, 5)

#             username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
#             username_field.send_keys("auecfoi")

#             password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
#             password_field.send_keys("Test@12345")

#             submit_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
#             submit_button.click()

#             time.sleep(3)
#             if "Logout" in self.driver.page_source:
#                 print("✅ Login successful")
#             else:
#                 print("❌ Login failed")
#                 self.driver.quit()
#                 raise SystemExit()

#         except Exception as e:
#             print(f"❌ Login failed: {e}")
#             self.driver.quit()
#             raise SystemExit()

#     def scrape_and_create_blog(self):
#         """Scrape blog posts from an external site and create them in Django."""
#         external_blog_url = "https://www.ctvnews.ca/"
#         self.open_site(external_blog_url)

#         try:
#             wait = WebDriverWait(self.driver, 10)

#             # Scrape titles, links, images, and descriptions
#             titles = [t.text.strip() for t in self.driver.find_elements(By.TAG_NAME, "h2") if t.text.strip()]
#             links = [a.get_attribute("href") for a in self.driver.find_elements(By.TAG_NAME, "a") if a.get_attribute("href")]
#             image_urls = [img.get_attribute("src") for img in self.driver.find_elements(By.TAG_NAME, "img") if img.get_attribute("src")]
#             descriptions = [p.text.strip() for p in self.driver.find_elements(By.TAG_NAME, "p") if p.text.strip()]

#             # Debugging: Print scraped data
#             print(f"Titles: {titles}")
#             print(f"Links: {links}")
#             print(f"Image URLs: {image_urls}")
#             print(f"Descriptions: {descriptions}")

#             # Ensure all lists have the same length
#             min_length = min(len(titles), len(links), len(image_urls), len(descriptions))
#             titles, links, image_urls, descriptions = descriptions, links[:min_length], image_urls[:min_length], descriptions[:min_length]

#             # Save the data
#             self.save_blogs(titles, links, image_urls, descriptions)

#         except Exception as e:
#             print(f"❌ Blog scraping failed: {e}")
#             self.driver.quit()
#             raise SystemExit()

#     def save_blogs(self, titles, links, image_urls, descriptions):
#         """Save the scraped blogs in Django."""
#         for title, link, image_url, description in zip(titles, links, image_urls, descriptions):
#             try:
#                 content = f"{description}\n\n"
#                 self.create_blog_in_django(title, content, image_url, description)
#             except Exception as e:
#                 print(f"⚠️ Failed to save blog '{title}': {e}")

#     def create_blog_in_django(self, title, content, image_url, description):
#         """Create a blog post directly in the Django database and save its image."""
#         try:
#             # Validate image URL
#             response = requests.get(image_url)
#             if response.status_code != 200:
#                 print(f"⚠️ Invalid image URL: {image_url}")
#                 return

#             # Get or create a Destination object
#             destination = Destination.objects.first()
#             if not destination:
#                 print("❌ No destination found. Creating a default one.")
#                 destination = Destination.objects.create(name="Default Destination")

#             # Create the BlogPost
#             blog_post = BlogPost.objects.create(
#                 title=title,
#                 content=content,
#                 category="Scraped",
#                 author="Admin",
#                 background_image=image_url,
#                 destination=destination
#             )

#             # Save Image to BlogPost
#             img_name = f"blog_image_{blog_post.id}.jpg"
#             blog_post.featured_image.save(img_name, ContentFile(response.content), save=True)

#             # Save Blog Image Details
#             BlogImage.objects.create(
#                 blog_post=blog_post,
#                 image=image_url,
#                 title=title,
#                 description=description
#             )

#             print(f"✅ Blog '{title}' created successfully with image!")

#         except Exception as e:
#             print(f"❌ Failed to create blog: {e}")


import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from myapp.models import BlogPost, BlogImage, Destination

# Set your API Keys (store these securely, don't hardcode in production)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "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")

class BlogScraper:
    def __init__(self):
        # Initialize the Selenium WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def open_site(self, url):
        """Open the specified URL using Selenium."""
        self.driver.get(url)
        self.driver.maximize_window()  # Optional: Maximize the browser window
        print(f"✅ Opened site: {url}")

    def close_site(self):
        """Close the Selenium WebDriver."""
        if self.driver:
            self.driver.quit()
            print("✅ Closed the browser.")

    def scrape_and_create_blog(self):
        """Scrape blog posts and enhance with AI-generated content."""
        external_blog_url = "https://www.ctvnews.ca/"
        try:
            # Open the website
            self.open_site(external_blog_url)

            wait = WebDriverWait(self.driver, 10)

            # Scrape blog data
            titles = [t.text.strip() for t in self.driver.find_elements(By.TAG_NAME, "h2") if t.text.strip()]
            links = [a.get_attribute("href") for a in self.driver.find_elements(By.TAG_NAME, "a") if a.get_attribute("href")]
            image_urls = [img.get_attribute("src") for img in self.driver.find_elements(By.TAG_NAME, "img") if img.get_attribute("src")]
            descriptions = [p.text.strip() for p in self.driver.find_elements(By.TAG_NAME, "p") if p.text.strip()]

            # Debugging: Print scraped data
            print(f"Titles: {titles}")
            print(f"Links: {links}")
            print(f"Image URLs: {image_urls}")
            print(f"Descriptions: {descriptions}")

            # Ensure lists have the same length
            min_length = min(len(titles), len(links), len(image_urls), len(descriptions))
            titles, links, image_urls, descriptions = titles[:min_length], links[:min_length], image_urls[:min_length], descriptions[:min_length]

            # Enhance content with AI
            enhanced_descriptions = [self.get_ai_enhanced_content(desc) for desc in descriptions]

            # Save the data
            self.save_blogs(titles, links, image_urls, enhanced_descriptions)

        except Exception as e:
            print(f"❌ Blog scraping failed: {e}")
        finally:
            # Close the browser
            self.close_site()
    
    def get_ai_enhanced_content(self, original_content):
        """Generate unique blog content using DeepSeek AI."""
        prompt = f"Enhance this news summary with unique insights and a compelling introduction:\n\n{original_content}"

        try:
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a professional blogger."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 200,
            }

            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                response_data = response.json()
                print("🔍 DeepSeek API Response:", response_data)  # Debugging
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                print(f"⚠️ DeepSeek API call failed: {response.status_code}, {response.text}")
                return original_content  # Fallback

        except Exception as e:
            print(f"⚠️ DeepSeek API call failed: {e}")
            return original_content  # Fallback
    def save_blogs(self, titles, links, image_urls, descriptions):
        """Save the AI-enhanced blogs in Django."""
        for title, link, image_url, description in zip(titles, links, image_urls, descriptions):
            try:
                content = f"{description}\n\n"
                self.create_blog_in_django(title, content, image_url, description)
            except Exception as e:
                print(f"⚠️ Failed to save blog '{title}': {e}")

    def create_blog_in_django(self, title, content, image_url, description):
        """Create a blog post directly in the Django database and save its image."""
        try:
            response = requests.get(image_url)
            if response.status_code != 200:
                print(f"⚠️ Invalid image URL: {image_url}")
                return

            # Get or create a Destination object
            destination = Destination.objects.first()
            if not destination:
                print("❌ No destination found. Creating a default one.")
                destination = Destination.objects.create(name="Default Destination")

            # Create the BlogPost
            blog_post = BlogPost.objects.create(
                title=title,
                content=content,
                category="AI-Enhanced",
                author="Admin",
                background_image=image_url,
                destination=destination
            )

            # Save Image to BlogPost
            img_name = f"blog_image_{blog_post.id}.jpg"
            blog_post.featured_image.save(img_name, ContentFile(response.content), save=True)

            # Save Blog Image Details
            BlogImage.objects.create(
                blog_post=blog_post,
                image=image_url,
                title=title,
                description=description
            )

            print(f"✅ Blog '{title}' created successfully with AI-enhanced content!")

        except Exception as e:
            print(f"❌ Failed to create blog: {e}")


class Command(BaseCommand):
    help = "Automates blog scraping and creation."

    def handle(self, *args, **options):
        self.stdout.write("Starting blog scraping process...")
        try:
            scraper = BlogScraper()  # Initialize your scraper
            scraper.scrape_and_create_blog()  # Run the scraping logic
            self.stdout.write(self.style.SUCCESS("✅ Blog scraping completed successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ An error occurred: {e}"))