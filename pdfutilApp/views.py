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
from pdf2image import convert_from_path, convert_from_bytes
import zipfile
import shutil




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
        
        
        print(os.listdir()) 
        
        folder = 'pdfutilApp/static/ims'    

        img_save_path = folder+'/'+filename
        with open(img_save_path, 'wb+') as f:
            for chunk in im.chunks():
                f.write(chunk)
        
        print(filename)
        

        return Response(status=204)


class ImageToPdfView(views.APIView) : 
    
    def get(self,request,filename) : 
        
        
        folder = 'pdfutilApp/static/ims'

        img_save_path = folder+'/'+filename
        pdfpath = os.path.splitext('pdfutilApp/static/ims/'+filename)[0]+'.pdf'

        image1 = Image.open(r'pdfutilApp/static/ims/'+filename)
        im1 = image1.convert('RGB')
        im1.save(pdfpath)
        
        short_report = open(pdfpath, 'rb')
        response = HttpResponse(FileWrapper(short_report), content_type='application/pdf')
        return response
    
class PdfToImageView(views.APIView) : 
    
    def get(self,request,filename) : 

        file = os.path.splitext(filename)[0]
        
        images = convert_from_path('pdfutilApp/static/ims/'+filename)#,fmt='jpeg')
      
        dir_name = 'pdfutilApp/static/ims/'+file
        
        os.mkdir(dir_name)
      
        i = 0 
        for im in images :
            im.save('pdfutilApp/static/ims/'+file+"/{}".format(i)+'.jpeg',"JPEG")
            i += 1 
            
        shutil.make_archive('pdfutilApp/static/ims/'+file, 'zip', dir_name)
        
        # delete the dir
        shutil.rmtree(dir_name) 
        
        zippath = 'pdfutilApp/static/ims/'+file+'.zip'
        
        f = open(zippath, 'rb')

        response = HttpResponse(f, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename='+zippath
        
        #delete files
        os.remove(zippath)
        os.remove('pdfutilApp/static/ims/'+filename)
        
        return response
        
        
        
    