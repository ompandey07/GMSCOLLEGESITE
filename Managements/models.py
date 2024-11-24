from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class VisitorContactModel (models.Model):
    Fullname = models.CharField(max_length=50 , null=True)
    Email = models.CharField(max_length=50 , null=True)
    PhoneNumber = models.CharField(max_length=50 , null=True)
    Message = models.CharField(max_length=50 , null=True)




class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('important', 'Important'),
        ('event', 'Event'),
        ('academic', 'Academic'),
        ('administrative', 'Administrative'),
        ('scholarship', 'Scholarship'),
        ('hackathon', 'Hackathon'),
        ('workshop', 'Workshop'),
        ('holiday', 'Holiday'),
    ]

    CATEGORY_COLORS = {
        'important': 'indigo',
        'event': 'pink',
        'academic': 'green',
        'administrative': 'yellow',
        'scholarship': 'blue',
        'hackathon': 'purple',
        'workshop': 'cyan',
        'holiday': 'red',
    }

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=False, blank=False)
    image = models.ImageField(upload_to='Notices/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_category_color(self):
        return self.CATEGORY_COLORS.get(self.category, 'gray')
    
    def get_nepali_date(self):
        return self.created_at.strftime('%Y-%m-%d')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Notice - {self.category}"




class Gallery(models.Model):
    title = models.CharField(max_length=200,null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='gallery/',null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('gallery_detail_view', kwargs={'pk': self.pk})

    def get_nepali_date(self):
        return self.created_at.strftime('%Y-%m-%d')

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Galleries'

    def __str__(self):
        return self.title

