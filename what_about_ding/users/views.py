<<<<<<< HEAD
<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
import requests

=======
import requests

>>>>>>> 077b601 (Create : users signin)
import jwt

from django.views import View
from django.http  import JsonResponse

from users.models      import User
from what_about_me.settings import SECRET_KEY, ALGORITHM
from core.social_apis  import Kakao_Token_Error, KakaoAPI

class SigninView(View):
    def get(self, request):
        try:
            access_token     = request.headers.get('Authorization')
            user_information = KakaoAPI(access_token).get_kakao_user_information()
            
            kakao_pk = user_information.get('id')
            email    = user_information.get('kakao_account').get('email')
            nickname = user_information.get('properties').get('nickname')

            user, created = User.objects.get_or_create(kakao_pk=kakao_pk, default = {"email" : email, "name" : nickname})
            
            if not created and not(user.email == email and user.name == nickname):
                user.email, user.name = email, nickname
                user.save()

            authorization = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'message' : 'SUCCESS'},headers = {'Authorization' : authorization}, status = 200)
        
        except Kakao_Token_Error as error:
            return JsonResponse({'message' : error.message}, status = 401)
<<<<<<< HEAD
>>>>>>> e84fc1a (Create : users signin)
=======
>>>>>>> 077b601 (Create : users signin)
