from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    ROLES = (
        ('Mentor', 'Mentor'),
        ('Student', 'Student'),
        ('Parent', 'Parent'),
    )
    username = None
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(('email address'), unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Mentor(models.Model):
    mentor_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    area_of_expertise = models.CharField(max_length=255)
    userpic = models.CharField(max_length=255,
                               default='https://i.imgur.com/0ndtScF.png')

    def __str__(self):
        return f'{self.user_id} ({self.area_of_expertise} mentor)'


class Parent(models.Model):
    parent_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    userpic = models.CharField(max_length=255, blank=True,
                               default='https://i.imgur.com/0ndtScF.png')

    def __str__(self):
        return f'{self.user_id}'


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=timezone.now)
    interests = models.TextField()
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL,
                               null=True, blank=True)
    userpic = models.CharField(max_length=255, blank=True,
                               default='https://i.imgur.com/0ndtScF.png')

    def __str__(self):
        return f'{self.user_id}'


class Relationship(models.Model):
    relationship_id = models.AutoField(primary_key=True)
    mentor_id = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.mentor_id.user_id}|{self.student_id.user_id}'


class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Resource(models.Model):
    name = models.CharField(max_length=60)
    url = models.CharField(max_length=255)
    about = models.TextField()
    img = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a User Profile instance when a new Custom User is created.
    """
    print(f"User role: {instance.role}")
    if created:
        if instance.role == 'Student':
            Student.objects.create(user_id=instance)
        elif instance.role == 'Parent':
            Parent.objects.create(user_id=instance)
        elif instance.role == 'Mentor':
            Mentor.objects.create(user_id=instance)
