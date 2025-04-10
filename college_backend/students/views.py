import random
import smtplib
from email.mime.text import MIMEText
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import User
from .serializers import UserSerializer,BookSerializer,AllUsers,BookRequestSerializer,BookRequestSerializer1,AttendanceSerializer


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from .models import User,Book,BookRequest
from .utils import generate_otp, send_otp_email
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import random
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import threading

from datetime import date
import cv2
import os
import numpy as np
from rest_framework.response import Response
from django.http import JsonResponse
from deepface import DeepFace
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()  # Use the existing User model

FACES_DIR = os.path.join(settings.MEDIA_ROOT, "faces")  # Face images directory


from django.db.models import Q
import django.db.models as models
from django.shortcuts import render, redirect, get_object_or_404

# students/views.py
from django.http import JsonResponse
from django.db.models import Q
from .models import Book  # Make sure you import your model

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Attendance, User


@api_view(['GET'])
def attendance_today(request):
    dept = request.GET.get('department')
    branch = request.GET.get('branch')

    today = date.today()
    records = Attendance.objects.filter(date=today)

    if dept:
        records = records.filter(department=dept)
    if branch:
        records = records.filter(branch=branch)

    records = records.order_by('roll_number')
    serializer = AttendanceSerializer(records, many=True)
    print(serializer)
    return Response(serializer.data)
@api_view(['GET'])
def get_attendance_list(request):
    today = date.today()
    department = request.GET.get('department')
    branch = request.GET.get('branch')

    students = User.objects.all()

    if department:
        students = students.filter(department=department)
    if branch:
        students = students.filter(branch=branch)

    # Get student IDs who are present today
    present_ids = Attendance.objects.filter(date=today).values_list('student__id', flat=True)

    student_data = []
    for student in students.order_by('roll_number'):
        student_data.append({
            "name": student.name,
            "roll_number": student.roll_number,
            "department": student.department,
            "branch": student.branch,
            "status": "Present" if student.id in present_ids else "Absent"
        })

    return Response(student_data)

@csrf_exempt
def get_students(request):
    if request.method == "POST":
        data = json.loads(request.body)
        department = data.get("department")
        branch = data.get("branch")

        users = User.objects.filter(department=department, branch=branch)
        result = [
            {
                "roll_number": user.roll_number,
                "full_name": user.name,
                "department": user.department,
                "branch": user.branch,
            }
            for user in users
        ]
        return JsonResponse(result, safe=False)

@api_view(['POST'])
def mark_attendance(request):
    serializer = AttendanceSerializer(data=request.data)
    print(serializer)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Attendance recorded'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookStatusView(APIView):
    def get(self, request, roll_number):
        try:
            user = User.objects.get(roll_number=roll_number)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        book_requests = BookRequest.objects.filter(student=user)
        # print(book_requests)
        serializer = BookRequestSerializer1(book_requests, many=True)
        # print(serializer.id)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UpdateRequestView(APIView):
    def post(self, request):
        request_id = request.data.get('request_id')
        action = request.data.get('action')  # "accept" or "reject"

        try:
            req = BookRequest.objects.get(id=request_id)
        except BookRequest.DoesNotExist:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            req.status = 'accepted'
        elif action == 'reject':
            req.status = 'rejected'
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        req.save()
        return Response({'message': f'Request {action}ed'}, status=status.HTTP_200_OK)


class PendingRequestsView(APIView):
    def get(self, request):
        pending = BookRequest.objects.filter(status='pending')
        data = [{
            'id': r.id,
            'student_roll': r.student.roll_number,
            'student_name': r.student.name,
            'book_name': r.book.book_name,
            'requested_at': r.requested_at,
        } for r in pending]
        return Response(data)

class RegisterBookView(APIView):
    def post(self, request):
        book_id = request.data.get('book_id')
        roll_number = request.data.get('roll_number')
        print(book_id)
        print(roll_number)

        try:
            student = User.objects.get(roll_number=roll_number)
            book = Book.objects.get(id=book_id)
        except (User.DoesNotExist, Book.DoesNotExist):
            return Response({'error': 'Invalid student or book'}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent duplicate requests
        existing_request = BookRequest.objects.filter(student=student, book=book, status='pending').first()
        if existing_request:
            return Response({'message': 'Request already exists'}, status=status.HTTP_409_CONFLICT)

        BookRequest.objects.create(student=student, book=book)
        return Response({'message': 'Request submitted'}, status=status.HTTP_201_CREATED)
class BookView(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
def admin_requests_list(request):
    requests = BookRequest.objects.all().order_by('-requested_at')
    serializer = BookRequestSerializer(requests, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def handle_request_action(request, request_id, action):
    try:
        req = BookRequest.objects.get(id=request_id)
    except BookRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

    if req.status != 'pending':
        return Response({"error": "Request already processed"}, status=status.HTTP_400_BAD_REQUEST)

    if action == 'accept':
        req.status = 'accepted'
    elif action == 'reject':
        req.status = 'rejected'
    else:
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    req.save()
    return Response({"message": f"Request {action}ed successfully"})

def admin_book_requests(request):
    requests = BookRequest.objects.select_related('book', 'student__user').order_by('-requested_at')
    return render(request, 'admin_requests.html', {'requests': requests})

def update_request_status(request, request_id, action):
    req = get_object_or_404(BookRequest, id=request_id)
    if action == 'accept':
        req.status = 'accepted'
    elif action == 'reject':
        req.status = 'rejected'
    req.save()
    return redirect('admin-book-requests')
def register_book(request):
    data = json.loads(request.body)
    book_id = data['book_id']
    roll_number = data['roll_number']

    book = Book.objects.get(id=book_id)
    BookRequest.objects.create(book=book, roll_number=roll_number, status='Pending')
    return JsonResponse({'message': 'Request sent'})

def search_books(request):
    query = request.GET.get('query', '')
    # Fetch all matching books based on book name or author
    books = Book.objects.filter(
        Q(book_name__istartswith=query) | Q(author__istartswith=query)
    ).values('id','book_name', 'author', 'field', 'no_of_pages')
    # Return all matching books in JSON format
    # for book in books:
        # print(book.id)
    data = [
        {
            "id":book['id'],
            "name": book['book_name'],
            "author": book['author'],
            "field": book['field'],
            "pages": book['no_of_pages']
        }
        for book in books
    ]
    return JsonResponse(data, safe=False)

def get_registered_faces():
    users = User.objects.exclude(profile_photo="")  # Get users with profile photos
    face_db = {user.roll_number: os.path.join(FACES_DIR, user.profile_photo.name) for user in users}
    return face_db

# Recognize face from live camera
def recognize_face(request):
    face_db = get_registered_faces()
    
    cap = cv2.VideoCapture(0)  # Open camera
    if not cap.isOpened():
        return JsonResponse({"error": "Camera not found"}, status=500)
    
    recognized_user = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save captured frame temporarily
        temp_image_path = os.path.join(settings.MEDIA_ROOT, "temp.jpg")
        cv2.imwrite(temp_image_path, frame)

        # Compare with registered faces
        for roll_number, face_path in face_db.items():
            try:
                result = DeepFace.verify(img1_path=temp_image_path, img2_path=face_path, model_name="VGG-Face", enforce_detection=False)
                if result["verified"]:
                    user = User.objects.get(roll_number=roll_number)
                    recognized_user = {
                        "roll_number": user.roll_number,
                        "name": user.username,
                        "department": user.department,
                        "year": user.year,
                        "profile_photo": user.profile_photo.url
                    }
                    break  # Stop after first match
            except Exception as e:
                continue  # Skip errors

        if recognized_user:
            break  # Stop recognition once a user is found

    cap.release()
    cv2.destroyAllWindows()

    if recognized_user:
        return JsonResponse({"recognized_user": recognized_user})
    else:
        return JsonResponse({"message": "No user recognized"}, status=404)

# from .face_recognition import recognize_face
otp_storage = {}  # Temporary storage for OTPs



class LoginView(APIView):
    def post(self, request):
        email_or_roll = request.data.get("email_or_roll")
        password = request.data.get("password")
        print(email_or_roll)
        print(password)
        # Find user by email or roll number
        user = User.objects.filter(email=email_or_roll).first() or User.objects.filter(roll_number=email_or_roll).first()
        print(user.password)
        if user and password==user.password:  # Checking hashed password
            return Response({
                "message": "Login Successful",
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(["POST"])
@permission_classes([AllowAny])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    print(serializer)
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Book added successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    serializer
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    def get(self, request, roll_number):
        user = User.objects.filter(roll_number=roll_number).first()
        print("User details ra",user)
        serializer=AllUsers(user)
        print(FACES_DIR)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(["POST"])
def send_otp(request):
    email = request.data.get("email")
    fors=request.data.get("for")
    print(email)
    print(fors)
    message=""
    subject=""
    print(fors)
    otp = random.randint(100000, 999999)
    otp_storage[email] = otp
    print(fors=="register")
    if User.objects.filter(email=email).exists():
        if fors=="reset_password":
            subject="Password Reset OTP"
            message = f"Dear User,\n\nYour OTP to Reset Password at AITS Tirupati, is: {otp}\n\nThis OTP is valid for [5 or 10] minutes. Please do not share it with anyone.\n\nIf you did not request this, please ignore this email.\n\nBest regards,\nYour developer Pradeep from AITS Titupati"
        return Response({"EMail Already registered try to login"},status=400)
    elif fors=="register":
        subject="Email Verification OTP"
        message = f"Dear User,\n\nYour OTP for registration at AITS Tirupati, is: {otp}\n\nThis OTP is valid for [5 or 10] minutes. Please do not share it with anyone.\n\nIf you did not request this, please ignore this email.\n\nBest regards,\nYour developer Pradeep from AITS Titupati"
    if not email:
        return Response({"error": "Email is required"}, status=400)


    try:
        send_mail(
            subject=subject,
            message=message,
            from_email="your-email@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"OTP sent successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=500)  # Log exact error

@csrf_exempt
def verify_otp(request):
    """Verifies the OTP entered by the user"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            otp = int(data.get("otp"))
            print(data)
            print(email)
            print(otp)
            print(otp_storage[email])
            if otp==otp_storage[email]:
                print("OK Of otp")
            else:
                print("Godd bye!")
            # if not email or not otp:
            #     return JsonResponse({"message": "Email and OTP are required"}, status=400)

            # Check if OTP matches
            if email in otp_storage and otp_storage[email] == otp:
                del otp_storage[email]  # Remove OTP after successful verification
                return JsonResponse({"message": "OTP verified successfully"}, status=200)
            else:
                return JsonResponse({"message": "Invalid OTP came"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid request format"}, status=400)

    return JsonResponse({"message": "Invalid request"}, status=400)

otp_storage = {}
def send_email_otp(email, otp):
    subject = "Your OTP for Registration"
    message = f"Your OTP for registration is: {otp}\n\nDo not share this with anyone."
    
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_HOST_USER
    msg["To"] = email

    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")

        otp = random.randint(100000, 999999)
        otp_storage[email] = otp

        if send_email_otp(email, otp):
            return Response({"message": "OTP sent successfully!"})
        return Response({"error": "Failed to send OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user_otp = int(request.data.get("otp"))

        if otp_storage.get(email) == user_otp:
            return Response({"message": "OTP verified!"})
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User

class Hello(APIView):
    def hi(self,request):
        print(request.data)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        roll_number = request.data.get("roll_number")
        file = request.FILES.get("face_image")

        user = get_object_or_404(User, roll_number=roll_number)
        file_name = f"faces/{roll_number}.jpg"

        if file:
            user.face_image.save(file_name, file, save=True)
            return Response({"message": "Face image uploaded successfully!"})
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserView(APIView):
    def post(self, request):
        # print(User.objects.email)
        # Check if roll_number or email already exists
        if User.objects.filter(roll_number=request.data.get("roll_number")).exists():
            return Response({"error": "Roll number already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=request.data.get("email")).exists():
            return Response({"error": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        print("Hello world")
        # Validate and save user
        serializer = UserSerializer(data=request.data)
        print(serializer)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FaceUploadView(APIView):
    def post(self, request):
        roll_number = request.data.get("roll_number")
        face_image = request.FILES.get("face_image")

        try:
            user = User.objects.get(roll_number=roll_number)
            user.face_image = face_image
            user.save()
            return Response({"message": "Face image uploaded successfully!"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
