from django.dispatch import receiver
from django.db.models.signals import post_save
from django.forms import model_to_dict
from driver.models import activeLogin
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync

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