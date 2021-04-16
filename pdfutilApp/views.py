from django.shortcuts import render
from rest_framework import viewsets, permissions, views
from .serializers import LogSerializer
from .models import Log
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
import os 
from PIL import Image
from wsgiref.util import FileWrapper
from django.http import HttpResponse



class LogViewSet(viewsets.ModelViewSet) : 
    
    '''
        API for Logs, create, edit and view
    '''

    queryset = Log.objects.all().order_by('-date')
    serializer_class = LogSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        im = request.data['file']
        
        
        
        folder = '/static/ims'

        img_save_path = folder+'/'+filename
        with open(img_save_path, 'wb+') as f:
            for chunk in im.chunks():
                f.write(chunk)
        
        print(filename)
        

        return Response(status=204)


class ImageToPdfView(views.APIView) : 
    
    def get(self,request,filename) : 
        
        
        folder = '/static/ims'

        img_save_path = folder+'/'+filename
        pdfpath = os.path.splitext('/static/ims/'+filename)[0]+'.pdf'

        image1 = Image.open(r'/static/ims/'+filename)
        im1 = image1.convert('RGB')
        im1.save(pdfpath)
        
        short_report = open(pdfpath, 'rb')
        response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')
        return response