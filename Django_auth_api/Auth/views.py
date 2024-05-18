from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializer import *
from .renderers import customRenderers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
# Create your views here.
class Registration_API(APIView):
    renderer_classes = [customRenderers]
    def post(self,request,format=None):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({"MSG":"Given user data is created.","token":token},status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":serializer.error_messages},status=status.HTTP_400_BAD_REQUEST)

    # renderer_classes = [customRenderers]  
    # permission_classes=[IsAuthenticated]
    # def get(self,request,format=None):
    #     serialize = AuthSerializer(request.user)
    #     return Response(serialize.data,status=status.HTTP_302_FOUND)
        # id = pk
        # if id is not None:
        #     try:
        #         data = MyUser.objects.get(id=id)
        #         serializer = AuthSerializer(data)
        #         return Response(serializer.data,status=status.HTTP_302_FOUND)
        #     except:
        #         return Response("Invalid Id",status=status.HTTP_404_NOT_FOUND)
        # else:
        #     data = MyUser.objects.all()
        #     serializer = AuthSerializer(data,many=True)
        #     return Response(serializer.data,status=status.HTTP_207_MULTI_STATUS)
    # renderer_classes = [customRenderers]  
    # permission_classes=[IsAuthenticated]
    # def patch(self,request,format=None):
    #     data = request.data
    #     try:
    #         withtransaction=MyUser.objects.get(id=data.get('id'))
    #         print(withtransaction)
    #         serializer = AuthSerializer(withtransaction,data=data,partial=True)
    #         if serializer.is_valid():
    #            serializer.save()
    #            return Response(serializer.data,status=status.HTTP_201_CREATED)
    #         else:
    #             return Response({"Error":serializer.error_messages},status=status.HTTP_400_BAD_REQUEST)
    #     except:
    #         return Response("This User does not exist.",status=status.HTTP_400_BAD_REQUEST)

    # renderer_classes = [customRenderers]  
    # permission_classes=[IsAuthenticated]
    # def delete(self,request,pk=None,format=None):
    #     id = pk
    #     try:
    #         data = MyUser.objects.get(pk=id)
    #         data.delete()
    #         return Response(f"The student record has been deleted successfully.")
    #     except Exception as e:
    #         return Response(str(e))

class Login_API(APIView):
    renderer_classes = [customRenderers]
    def post(self,request,format=None):
        seri_data = LoginSerializer(data=request.data)
        if seri_data.is_valid(raise_exception=True):
            email = request.data['email']
            password = request.data['password']
            usr = authenticate(email=email,password=password)
            if usr is not None :
                token = get_tokens_for_user(usr)
                return Response({'msg':"Login successfully","token":token},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'errors':{'non_field_errors':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
            
class ChangePassword(APIView):
    #permission_classes = (IsAdminOrReadOnly,)
    renderer_classes = [customRenderers]
    permission_classes=[IsAuthenticated]
    def put(self,request,format=None):
        serializer = PasswordChangeSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Password changed Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendEmailToResetPassword(APIView):
    renderer_classes = [customRenderers]
    def post(self,request,format=None):
        serializer = SendEmailToResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"msg":'Password reset link send on your registered email address'},status=status.HTTP_200_OK)
    
class resetPassword(APIView):
    # renderer_classes = [customRenderers]
    def post(self,request,uuid,token,format=None):
        serializer = ResetPassword(data=request.data,context={'uuid':uuid,'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({"msg":"Password reset successfully"},status=status.HTTP_200_OK)


class UserView(APIView):
    renderer_classes = [customRenderers]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer = GetUserdataSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_302_FOUND)

    renderer_classes = [customRenderers]
    permission_classes=[IsAuthenticated]
    def patch(self,request,format=None):
        data = request.data
        try:
            user_data = MyUser.objects.get(id=data.get('id'))
            serializer = GetUserdataSerializer(data=user_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                message = "Profile update successfully."
                return Response({'msg':message},serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors':{'non_field_errors':[str(e)]}},status=status.HTTP_400_BAD_REQUEST)

    renderer_classes=[customRenderers]
    permission_classes=[IsAuthenticated]   
    def delete(self,request):
        try:
            user_data = MyUser.objects.get(id=request.data.get('id'))
            user_data.delete()
            return Response({'msg':'User deleted successfully.'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors':{'non_field_errors':[str(e)]}},status=status.HTTP_400_BAD_REQUEST)
