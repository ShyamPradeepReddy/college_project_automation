from rest_framework import serializers
from .models import Student,User,Book,BookRequest

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
from rest_framework import serializers
from .models import User,Attendance

class UserSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["name", "roll_number", "department", "branch", "year", "email", "password", "confirmPassword"]

    def validate(self, data):
        if data["password"] != data["confirmPassword"]:
            raise serializers.ValidationError({"confirmPassword": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop("confirmPassword")
        # validated_data.year=int(validated_data.year)  # Remove confirm password field
        user = User.objects.create(**validated_data)
        # validated_data["password"] = make_password(validated_data["password"])
        # user.set_password(validated_data["password"])  # Hash the password
        user.save()
        return user
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
class AllUsers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = "__all__"
class BookRequestSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    student = StudentSerializer()
    class Meta:
        model = BookRequest
        fields = ['id', 'book', 'student', 'requested_at', 'status']
class BookRequestSerializer1(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = BookRequest
        fields = ['id', 'book', 'status']
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'