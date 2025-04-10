from django.urls import path
from .views import SendOTPView, VerifyOTPView, RegisterUserView, FaceUploadView,send_otp,verify_otp,Hello,LoginView,add_book,get_books,UserProfileView,recognize_face,search_books,admin_book_requests,update_request_status,handle_request_action,admin_requests_list,BookView,RegisterBookView,PendingRequestsView,UpdateRequestView,BookStatusView,get_students,mark_attendance,attendance_today
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path("students/",)
    path("send-otp/", send_otp, name="send-otp"),
    path("verify-otp/", verify_otp, name="verify-otp"),
    path("myupload/", FaceUploadView.as_view(), name="myupload"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("upload-face/", Hello.as_view(), name="upload-face"),
    path("login/", LoginView.as_view(), name="login"),
    path("user-profile/<str:roll_number>/", UserProfileView.as_view(), name="user-profile"),
    path("add-book/", add_book, name="add_book"),
    path("books/", get_books, name="get_books"),
    path("get-students/", get_students, name="get_students"),
    path("mark-attendance/", mark_attendance, name="mark_attendance"),
    path("recognize-face/", recognize_face, name="recognize_face"),
    path('search-books', search_books, name='search-books'),
     path('book-details/<int:book_id>/', BookView.as_view(), name='book_details'),
     path('attendance-today/', attendance_today, name='attendance_today'),
     path('register-book/', RegisterBookView.as_view(), name='register-book'),
     path('pending-requests/', PendingRequestsView.as_view(), name='pending-requests'),
     path('update-request/', UpdateRequestView.as_view(), name='update-request'),
     path('book-status/<str:roll_number>/', BookStatusView.as_view(), name='book-status'),
     path('admin/requests/', admin_book_requests, name='admin-book-requests'),
    #  path('attendance-summary/<str:roll_number>/', get_attendance_summary),

    path('admin/requests/<int:request_id>/<str:action>/', update_request_status, name='update-request-status'),
    path('api/admin/requests/', admin_requests_list),
    path('api/admin/requests/<int:request_id>/<str:action>/', handle_request_action),
    # path('bujji/<int:id>/')
    # path("start-attendance/", start_face_recognition, name="start-attendance"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
