from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    action_link = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    user_name = models.CharField(max_length=255)
    user_role = models.CharField(max_length=255, help_text="e.g. BVSc Student")
    content = models.TextField()
    avatar_url = models.URLField(blank=True)

class Drug(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True)
    composition = models.TextField(blank=True)
    dosage = models.TextField(blank=True)
    indications = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)

    def __str__(self):
        return self.name

class BookCategory(models.Model):
    name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=20, default="#1e293b")

    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_premium = models.BooleanField(default=False)
    cover_image_url = models.URLField(blank=True)
    pdf_url = models.URLField(blank=True, help_text="Secure link to the ebook PDF")

    def __str__(self):
        return self.title
