from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Student
from .serializers import StudentSerializer


class StudentListCreateAPIView(APIView):
    """List all students or create a new one"""


    @swagger_auto_schema(
        operation_description="Get all students",
        responses={200: StudentSerializer(many=True)}
    )
    def get(self, request):
        students = Student.objects.all()
        return Response(StudentSerializer(students, many=True).data)

    @swagger_auto_schema(
        operation_description="Create a new student",
        request_body=StudentSerializer,
        responses={201: StudentSerializer()}
    )
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentRetrieveUpdateDeleteAPIView(APIView):
    """Retrieve, update, or delete a student by ID"""

    def get_object(self, pk):
        return Student.objects.filter(pk=pk).first()

    def handle_not_found(self):
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Retrieve a student by ID",
        responses={200: StudentSerializer()}
    )
    def get(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return self.handle_not_found()
        return Response(StudentSerializer(student).data)

    @swagger_auto_schema(
        operation_description="Update a student by ID",
        request_body=StudentSerializer,
        responses={200: StudentSerializer()}
    )
    def put(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return self.handle_not_found()
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a student by ID",
        responses={204: 'No content'}
    )
    def delete(self, request, pk):
        student = self.get_object(pk)
        if not student:
            return self.handle_not_found()
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
