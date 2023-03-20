from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework import permissions

# import pdfminer
# from pdfminer.high_level import extract_text
import nltk
import re
import os, io
import spacy
from nltk.corpus import stopwords
from spacy.matcher import Matcher
import pdfplumber
from pdfminer.high_level import extract_text
from io import BytesIO

from .serializers import FileSerializer, ResumeDataSerializer
from .models import User, Resume_Data
from .utils import extract_name, extract_email, extract_entities, extract_phone_number, extract_skills, extract_text_from_pdf


# Create your views here.

class ResumeUploadView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    parser_class = (FileUploadParser)

    def post(self, request):

        file_serializer = FileSerializer(data = request.data)

        if file_serializer.is_valid():
            file_serializer.save(user = request.user)

            # RESUME PARSING

            file = request.FILES['file']
            file_text = extract_text_from_pdf(file)


            name = extract_name(file_text)
            phone_number = extract_phone_number(file_text)
            email = extract_email(file_text)
            skills = extract_skills(file_text)
            entities = extract_entities(file_text)
            experience = entities.get('INTERNSHIPS', 'null')
            education = entities.get('EDUCATION', 'null')
            projects = entities.get('PROJECTS', 'null')
            achievements = entities.get('AWARDS AND ACHIEVEMENTS', 'null')
            position_of_responsiblity = entities.get('POSITION OF RESPONSIBILITY', 'null')
            extra_curricular = entities.get('EXTRA CURRICULAR', 'null')

            new = Resume_Data(
                name = name,
                phone_number=phone_number,
                email=email,
                education = str(education),
                projects = str(projects),
                achievements = str(achievements),
                skills = str(skills),
                experience = str(experience),
                position_of_responsibility = str(position_of_responsiblity),
                extra_curricular = str(extra_curricular)
            )

            new = new.__dict__

            resume_data_serializer = ResumeDataSerializer(data = new)

            print('data: ' ,new['education'])
            if resume_data_serializer.is_valid():
                resume_data_serializer.save(user = request.user)
                return Response({
                    'message' : 'resume parsed successfully',
                    'data' : resume_data_serializer.data
                }, status = status.HTTP_201_CREATED)
            else:
                return Response({
                    'data' : resume_data_serializer.errors
                }, status = status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'error' : file_serializer.errors
        })


class UserInfoView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    #  ___________ Add user data _______________

    def post(self, request):

        serializer = ResumeDataSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response({
                'message' : 'User info added successfully',
                'status' : 'success',
                'user' : serializer.data
            },
            status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors)

    # ___________ Get all users_______________

    def get(self, request):

        users = list(Resume_Data.objects.all())

        if not users:
            return Response({
                'message' : 'No user found',
                'status' : 'failure',
            },
            status = status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeDataSerializer(users, many=True)


         
        return Response({
                'message' : 'All users fetched successfully',
                'status' : 'success',
                'users' : [{
                    'id' : x['id'],
                    'user' : x['user']
                } for x in serializer.data]
            },
            status=status.HTTP_200_OK
            )    

    
class UpdateUserView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    # ___________ Update a user_______________

    def patch(self, request, id):

        user = Resume_Data.objects.filter(id = id).first()

        if not user:
            return Response({
                'message' : 'No user found',
                'status' : 'failure'
            },
            status = status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeDataSerializer(data = request.data, instance = user, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : 'User udpated successfully',
                'status' : 'success',
                'updated_user' : {
                'id' : serializer.data['id'],
                'user' : serializer.data['user']
            }
            },
            status = status.HTTP_200_OK
            )
        

    # ___________ Get a user_______________

class GetUserView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):

        user = Resume_Data.objects.filter(id = id).first()

        if not user:
            return Response({
                'error' : 'no user found',
                'status' : 'failure',
            }, 
            status = status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeDataSerializer(user)
            
        return Response({
            'message' : 'user found',
            'status' : 'success',
            'user' : {
                'id' : serializer.data['id'],
                'user' : serializer.data['user']
            }
        }, 
        status = status.HTTP_200_OK
        )

    # ___________ Delete a user_______________

class DeleteUserView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):

        user = Resume_Data.objects.filter(id = id).first()
    
        if not user:
            return Response({
                'error' : 'no user found',
                'status' : 'failure',
            }, 
            status = status.HTTP_404_NOT_FOUND
            )

        user.delete()

        return Response({
            'message' : 'user deleted successfully',
            'status' : 'success',
        })




        

        
            













    


