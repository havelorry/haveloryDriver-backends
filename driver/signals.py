from django.dispatch import receiver
from django.db.models.signals import post_save
from django.forms import model_to_dict
from driver.models import activeLogin, Ride,Notification
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync
from driver.views import send_push_message

@receiver(post_save, sender=activeLogin)
def announce_user(instance,**kwargs):
    channel_layer = get_channel_layer()
    group_name = 'driverpool'
    drivers = [model_to_dict(x) for x in list(activeLogin.objects.filter(active='1'))]
    # b = [x  for x in drivers if x.get('active') is True]
    c = [ {**x,'location':json.loads(x.get('location')) } for x in drivers] 
    print('{} send to {} of channel {}'.format(instance,group_name,channel_layer))
    async_to_sync(channel_layer.group_send)(group_name,{
        'type':'user.notification',
        'event':"updatedDrivers",
        'available':c 
    })


@receiver(post_save,sender=Ride)
def announce_rider(instance,**kwargs):
    userId = instance.username_id
    driver_id = instance.driver_id

    userTResult = Notification.objects.get(username=userId)
    driverTResult = Notification.objects.get(username=driver_id)

    if userTResult is not None:
        send_push_message(userTResult.token,"{} ride is {}".format(userId,instance.status))

    if driverTResult is not None:
        send_push_message(driverTResult.token,"{} a ride has been assigned to You see in details".format(instance.driver_id))



