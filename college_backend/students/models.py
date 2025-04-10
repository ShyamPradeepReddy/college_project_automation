from django.db import models
import os

def face_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]  # Get file extension (jpg, png, etc.)
    new_filename = f"{instance.roll_number}.{ext}"  # Rename file as roll_number
    return os.path.join("faces/", new_filename)
def book_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]  # Get file extension (jpg, png, etc.)
    sanitized_book_name = instance.book_name.replace(" ", "_")  # Replace spaces with underscores
    new_filename = f"{sanitized_book_name}.{ext}"  # Format filename as book_name.extension
    return os.path.join("books/", new_filename)

class User(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128,default="hi")  # Store hashed password
    # confirm_password = models.CharField(max_length=128)  # Store hashed password
    is_verified = models.BooleanField(default=False)
    face_image = models.ImageField(upload_to=face_image_upload_path)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    no_of_pages = models.IntegerField()
    no_of_books = models.IntegerField()
    book_image = models.ImageField(upload_to=book_image_upload_path)

    def __str__(self):
        return self.book_name
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class BookRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def book_id(self):
        return self.book.id

    def __str__(self):
        return f"{self.student.roll_number} → {self.book.book_name} ({self.status})"
    
class Attendance(models.Model):
    roll_number = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    faculty_updated = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

    def __str__(self):
        return f"{self.roll_number} - {self.date} - {self.status}"
