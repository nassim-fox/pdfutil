from rest_framework import serializers
from pdfutilApp.models import Log





class LogSerializer(serializers.HyperlinkedModelSerializer) : 
    
    class Meta : 
        model = Log
        fields = ['url','date']
        


'''

class DataSerializer(serializers.Serializer) : 
    
    url = serializers.TextField()
    im = FileField(blank=True,default='')
    
'''