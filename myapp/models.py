from django.db import models  # Default Django auth user (for feedback)

# Custom user model (not using Django's AbstractUser here)
class CustomUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg')

    def __str__(self):
        return self.username
    
class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use your custom user modela
    rating = models.IntegerField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Rating: {self.rating} - {self.message[:30]}'


# Team Member model for About Us or Team section
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='team/')
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# Services model for dynamic service listing
class Service(models.Model):
    ICON_CHOICES = [
        ("bi-bar-chart-line", "Bar Chart"),
        ("bi-briefcase", "Briefcase"),
        ("bi-cash-coin", "Cash Coin"),
        ("bi-people", "People"),
        ("bi-laptop", "Laptop"),
        ("bi-megaphone", "Megaphone"),
    ]

    title = models.CharField(max_length=200)
    short_description = models.TextField()
    features = models.TextField(help_text="Separate each feature with a comma")
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    detail_url = models.URLField(default="#", help_text="Link to service detail page")

    def feature_list(self):
        return [f.strip() for f in self.features.split(",") if f.strip()]

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ConsultationRequest(models.Model):
    name    = models.CharField(max_length=100)
    email   = models.EmailField()
    phone   = models.CharField(max_length=20, blank=True)
    service = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.name} {self.service}"



from django.db import models

class PricingPlan(models.Model):
    PLAN_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES)
    is_popular = models.BooleanField(default=False)
    features = models.TextField(help_text="Separate features with semicolons")

    def get_features_list(self):
        return [feature.strip() for feature in self.features.split(';') if feature.strip()]

    def __str__(self):
        return f"{self.title} - {self.plan_type}"
