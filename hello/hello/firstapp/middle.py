from  django.http  import HttpResponseForbidden,HttpResponseRedirect

#1.https://docs.djangoproject.com/en/3.0/topics/http/middleware/
#2.https://django-book.readthedocs.io/en/latest/chapter17.html

class MiddleWareAuth(object):
     def __init__(self, get_response):
        self.get_response = get_response

     def __call__(self, request):
        reponse=self.get_response(request)
        if('.woff2' in request.path or '.woff' in request.path):
             return HttpResponseForbidden()
        return reponse

    
     def process_view(self,request, view_func, view_args, view_kwargs):

         if '/auth' in str(request.path_info):
                 if not request.user.is_authenticated:
                     return HttpResponseRedirect('/login')
                 else:
                     if str(request.user.id)==str(view_kwargs.get('id')):
                         return None
                     else:
                        if request.user.has_perm('show_profile_all'):
                                 return None
                         
                        return HttpResponseRedirect('/')
         else:
             return None
     
     def proccess_response(self, request,response):
             return response
             
     def process_template_response(self,request, response):
         if 'product/'in str(request.path_info) :
             response.context_data['styles']=['https://liga-a.ru/portfolio/rus-partners/css/style.min.css']
             response.context_data['scripts']=['/public/script/ajax.js']
         elif'auth' in str(request.path_info):
             response.context_data['scripts']=['/public/script/admin.js',"/public/script/ajax.js"]
         else:
             response.context_data['scripts']=['/public/script/search.js']
         response.context_data['getattr']=getattr
         return response
