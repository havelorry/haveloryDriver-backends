from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializations import ProfileDetailSerializer,ProfileSerializer,ActiveLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Driver,activeLogin,AppSetting,Ride
from rest_framework import generics
from .vincenty import vincenty_inverse
from rest_framework.parsers import JSONParser
from .serializations import RideSerializer
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
import requests
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
                return Response({"massage":"saved successfully","details":profile_detail_serializer.data})
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
            print(detail_serilaizer.data['id'])
            serializer=ProfileSerializer(user)
            serializer.data['address']=detail_serilaizer['address']
            #serializer.data['id']=detail_serilaizer.data['id']

            print (serializer.data)
            return Response({"id":detail_serilaizer.data['id'],"username":detail_serilaizer.data['username'],"email":serializer.data['email'],"first_name":serializer.data['first_name'],"last_name":serializer.data['last_name'],"address":detail_serilaizer.data['address'],"mobile":detail_serilaizer.data['mobile'],"vehicle_number":detail_serilaizer.data['vehicle_number'],"locations":detail_serilaizer.data['locations'],"age":detail_serilaizer.data['age']})    
   
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
        else:
            token, _ = Token.objects.get_or_create(user=user)
            driver=Driver.objects.get(username=user)
            print(driver.id)
            return Response({"massage":"Login Successfully","token":token.key,"driverId":driver.id})
    #def get(self,request,format=None):

class ActiveLogin(APIView):
    def get_object(self, username):
        try:
            return activeLogin.objects.get(username=username)
        except activeLogin.DoesNotExist:
           raise_exception=True 
    def post(self,request,format=None):
        print ("inside post method")
        active_user=self.get_object(request.data.get('username'))
        if active_user==None:
            print("inisde if")
            active_serializer=ActiveLoginSerializer(data=request.data)
            if active_serializer.is_valid(raise_exception=True):
                active_serializer.save()
                print("save successfully")
                return Response({"massage":"activation successfully","status":status.HTTP_200_OK})
        else:
            
            active_login_serializer=ActiveLoginSerializer(instance=active_user,data=request.data,partial=True)    
            if active_login_serializer.is_valid(raise_exception=True):
                active_login_serializer.save()
                return Response({"massage":"Updation done successfully","status":status.HTTP_200_OK})
        return Response({'massage':"Some thing went wrong","status":status.HTTP_400_BAD_REQUEST})
        # active_serializer=ActiveLoginSerializer(data=request.data)
        # if active_serializer.is_valid(raise_exception=True):
        #     active_serializer.save()
        #     return Response({"massage":"activation successfully"})
        # else:
        #     return Response({"massage":"activatiion failed"})    

    def put(self,request):
        active_user=self.get_object(request.data.get('username'))
        if active_user==None:
            print("inisde if")
            active_serializer=ActiveLoginSerializer(data=request.data)
            if active_serializer.is_valid(raise_exception=True):
                active_serializer.save()
                print("save successfully")
                return Response({"massage":"activation successfully","status":status.HTTP_200_OK})
        else:
            
            active_login_serializer=ActiveLoginSerializer(instance=active_user,data=request.data,partial=True)    
            if active_login_serializer.is_valid(raise_exception=True):
                active_login_serializer.save()
                return Response({"massage":"Updation done successfully","status":status.HTTP_200_OK})
        return Response({'massage':"Some thing went wrong","status":status.HTTP_400_BAD_REQUEST})
        # active_user=activeLogin.objects.get(username=request.data.get('username'))
        # active_login_serializer=ActiveLoginSerializer(instance=active_user,data=request.data,partial=True)    
        # if active_login_serializer.is_valid(raise_exception=True):
        #     active_login_serializer.save()
        #     return Response({"massage":"Updation done successfully","status":status.HTTP_200_OK})
        # return Response({'massage':"Some thing went wrong","status":status.HTTP_400_BAD_REQUEST})    
    
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



class GenericModel(object):
    def __init__(self, *args,**kwargs):
        for field in args:
            setattr(self,field,kwargs[field])


class RideCreationView(APIView):

    def get(self,request,format=None):
        
        queryset = Ride.objects.all()
        data = [ x.toJson() for x in list(queryset)]        
        return JsonResponse(data, safe=False)

    def post(self,request, format=None):
        z = RideSerializer(data = request.data)
        
        if Ride.objects.create(**request.data):
            return Response({'message':'Ride created succesfully','status':'ok'})
        else:
            return Response({'message':'Ride creation Error','status':False})    

    def put(self, request):
        _id = request.data.get('id')
        status = request.data.get('status')
        ride = Ride.objects.filter(
            Q(id= _id),
        )

        results = list(ride)

        if len(results) ==1:
            r = results[0]
            r.status = status
            print(r.save())
            return JsonResponse({'message':'Ride updated successfully', 'status':True})
        
        return JsonResponse({'message':'updation failed', 'status':False})
        

def add_driver(obj):
    driver = Driver.objects.get(username=obj.get('driver_id'))
    return {
        **obj,
        'driver':model_to_dict(driver)
    }
def add_user(obj):
    payload = {'id': obj.get('customer_id')}
    r = requests.get('https://havelorryapp.herokuapp.com/api/customer/', params=payload)
    print("Data=",r.text)

    #driver = Driver.objects.get( id=obj.get('driver_id'))
    return {
        **obj,
        'customer':r.text
    }

class RideHistory(APIView):
    def get(self,request,format=None):
        
        A = 'all'
        D ='driver'
        C = 'customer'

        print(request.GET['by'])
        if not isinstance(int(request.GET['identifier']),int):
            return JsonResponse({'message':'wrong format'}, status=400)

        if request.GET['by'] == D:
            print("if")
            
            return JsonResponse( [ add_user(x.toJson()) for x in list(Ride.objects.filter(Q(driver_id=request.GET['identifier'])))], safe=False)
        else:
            return JsonResponse( [ add_driver(x.toJson())  for x in list(Ride.objects.filter(Q(customer_id=request.GET['identifier'])))], safe=False)
        
        return JsonResponse([], safe=False)


@api_view(['GET'])
def getEarnings(request):
    earnings = Ride.get_driver_earnings(request.GET['driver'])
    print(earnings)
    return JsonResponse(earnings, safe=False)



