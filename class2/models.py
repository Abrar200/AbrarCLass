from pyexpat import model
from django.contrib.auth.models import User
from django.core.checks.messages import CheckMessage
from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.conf import settings


YEAR_IN_SCHOOL_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('University 1st Year', 'University 1st Year'),
    ('University 2nd Year', 'University 2nd Year'),
    ('University 3rd Year', 'University 3rd Year'),
    ('University 4th Year', 'University 4th Year'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length = 100)
    grade = models.CharField(max_length=100, choices= YEAR_IN_SCHOOL_CHOICES)
    bio = models.TextField(max_length=300)

    def __str__(self):
        return f'{self.user.username} Profile'



class Course(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/class/instructor_pics', null=True)
    instructor = models.CharField(max_length=100)
    instructor_image = models.ImageField(upload_to='static/class/instructor_pics', null=True)
    enrolled_students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_students', blank=True)

    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=300, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 285 or img.width > 201:
            output_size = (285, 201)
            img.thumbnail(output_size)
            img.save(self.image.path)

        img2 = Image.open(self.instructor_image.path)

        if img2.height > 40 or img2.width > 40:
            output_size = (40, 40)
            img2.thumbnail(output_size)
            img2.save(self.instructor_image.path)



class Class(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='static/class/class_videos',null=True,
validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name='classes')


def __str__(self):
    return self.title






