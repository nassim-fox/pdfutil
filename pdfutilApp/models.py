from django.db import models
import datetime




class Log(models.Model) : 
    
    url = models.CharField(max_length=256)
    date = models.DateTimeField(default=datetime.datetime.now)
    
    