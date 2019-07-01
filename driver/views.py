from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializations import ProfileDetailSerializer,ProfileSerializer,ActiveLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Driver,activeLogin,AppSetting
from rest_framework import generics
from .vincenty import vincenty_inverse
# Create your views here.

class DriverPofile(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
           raise_exception=True 
    def post(self,request,format=None):
        print ("inside post method")
        profile_serializer=ProfileSerializer(data=request.data)
        if profile_serializer.is_valid(raise_exception=True):
            user=profile_serializer.save()
            if user:
                token = Token.objects.create(user=user)
                print("token created",token)
            profile_detail_serializer=ProfileDetailSerializer(data=request.data)
            
            if profile_detail_serializer.is_valid(raise_exception=True):
                
                profile_detail_serializer.save()
                return Response({"massage":"saved successfully"})
        return Response("done")

    def get(self,request,format=None):
        username=request.query_params.get("username")
        print(username)
        #user=User.objects.get(username=username)
        user = self.get_object(username)
        if user==None:
            return Response({"error":"User does not exist"})
        else:    
            username1=Driver.objects.get(username=username)
            print(username1)
            detail_serilaizer=ProfileDetailSerializer(username1)
            serializer=ProfileSerializer(user)
            serializer.data['address']=detail_serilaizer['address']
            print (serializer.data)
            return Response({"username":detail_serilaizer.data['username'],"email":serializer.data['email'],"first_name":serializer.data['first_name'],"last_name":serializer.data['last_name'],"address":detail_serilaizer.data['address'],"mobile":detail_serilaizer.data['mobile'],"vehicle_number":detail_serilaizer.data['vehicle_number'],"locations":detail_serilaizer.data['locations'],"age":detail_serilaizer.data['age']})    
    def put(self,request,format=None):
        user_detail=User.objects.get(username=request.data.get('username'))
        update_serializer=ProfileSerializer(instance=user_detail,data=request.data,partial=True)
        if update_serializer.is_valid(raise_exception=True):
            print ("updation done1")
            update_serializer.save()
            driver_detail=Driver.objects.get(username=request.data.get('username'))

            profile_detail_serializer=ProfileDetailSerializer(instance=driver_detail,data=request.data,partial=True)
            if profile_detail_serializer.is_valid(raise_exception=True):
                print ("updation done2")
                profile_detail_serializer.save()
                return Response({"massage":"Profile update successfully","status":status.HTTP_200_OK})
        return Response({"massage":"Something went wrong","status":status.HTTP_400_BAD_REQUEST})
    
    def delete(self, request, format=None):
        username=request.query_params.get("username")

        event = self.get_object(username)
        if event==None:
            return Response({"error":"User does not exist"})
        else:
            event.delete()
            return Response({"massage":"Deletion successfully","status":status.HTTP_204_NO_CONTENT})
            
     
class Login(APIView):
    def post(self,request,format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
       
        return Response({"massage":"Login Successfully","token":token.key})
    #def get(self,request,format=None):

class ActiveLogin(APIView):
    def post(self,request,format=None):
        print ("inside post method")
        active_serializer=ActiveLoginSerializer(data=request.data)
        if active_serializer.is_valid(raise_exception=True):
            active_serializer.save()
            return Response({"massage":"activation successfully"})
        else:
            return Response({"massage":"activatiion failed"})    

    def put(self,request):
        active_user=activeLogin.objects.get(username=request.data.get('username'))
        active_login_serializer=ActiveLoginSerializer(instance=active_user,data=request.data,partial=True)    
        if active_login_serializer.is_valid(raise_exception=True):
            active_login_serializer.save()
            return Response({"massage":"Updation done successfully","status":status.HTTP_200_OK})
        return Response({'massage':"Some thing went wrong","status":status.HTTP_400_BAD_REQUEST})    
    
def cvt(loc):
    import json
    temp = loc.get('username_id')
    driver = Driver.objects.get(username=temp)
    
    return {
        **loc,
        'workers':driver.__dict__.get('workers'),
    }


def level_1(loc,coords):
    import json
    _coords = json.loads(loc.get('location'))
    _flt_x = float(
        _coords.get('x')
    )

    _flt_y = float(
        _coords.get('y')
    )


    _flt2_x = float(
        coords[0]
    )

    _flt2_y = float(
        coords[1]
    )    

    _distance = vincenty_inverse([
        _flt2_x,
        _flt2_y
    ],[
       _flt_x,
       _flt_y 
    ])

    return {
        **loc,
        'location':json.loads(loc.get('location')),
        'distance':_distance.km,
        'display':_distance.km <= 108 and loc.get('status') == 'available' 
    }


class ActiveDrivers(APIView):
    
    
    def get(self, request, format=None):
        from django.http import JsonResponse
        
        if not (request.GET.__contains__('lat') and request.GET.__contains__('lng')):
            return JsonResponse({
                'message':'Missing required params'
            })

        lat = request.GET.__getitem__('lat')
        lng = request.GET.__getitem__('lng')    

        
        active = activeLogin.objects.filter(active=1)
        bc = list(active.values())
        mc = [ level_1(x,[lat,lng]) for x in bc]
        dk = [cvt(x) for x in mc if x.get('display') is True]
        
        return JsonResponse(
            dk,
            safe=False
        )    




class RideCreationView(APIView):
    pass




def calculate(request, incl=False):
    basePrice = AppSetting.objects.get(name="BASE_PRICE").value
    
    print(request.POST)

    if incl:
        pass
    else:
        pass

class FareCalculation(APIView):
    def get(sef ,request, format=None):
        try:
            includeDriverDistance = AppSetting.objects.get(name="INCLUDE_DRIVER_DISTANCE").value

            if includeDriverDistance is 0:
                calculate(request,incl=False)
            else:
                calculate(request,incl=True)

        except :
            print('Loading failed')
            





