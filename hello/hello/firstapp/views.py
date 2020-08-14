from django.shortcuts import render,redirect,get_object_or_404
from .form import PostForm,SignUp,LoginForm,AddUserForm
# Create your views here.
from .models import Post,Role,Images,Products,Category
from django.contrib.auth import get_user_model
import time
from django.contrib.auth import login,logout
from django.http import HttpResponse,HttpResponseNotFound,FileResponse,HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from django.views import View
from django.views.generic import ListView,DetailView,FormView
from django.views.generic.detail import SingleObjectMixin
from django.template.response import TemplateResponse
import os
import json
import requests
from django.core.paginator import Paginator
from django.core.files import File
from django.core.files.base import ContentFile
from .authen  import MyBackend
from django.views.generic.base import RedirectView,TemplateResponseMixin
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.files.storage import default_storage
import subprocess

#FileUpload
#1.https://docs.djangoproject.com/en/3.0/topics/files/#using-files-in-models
#2.https://docs.djangoproject.com/en/3.0/ref/models/fields/
#3.How to save a file to a model (url :https://docs.djangoproject.com/en/3.0/topics/files/#using-files-in-models)
#4.To send a picture use https://docs.djangoproject.com/en/3.0/ref/request-response/ FileResponse object

#5.1  https://docs.djangoproject.com/en/3.0/ref/forms/api/#using-forms-to-validate-data
#5.1 https://docs.djangoproject.com/en/3.0/ref/forms/validation/

#6.object is a Manager which returns a QuerySet
#7.QuerySet returns  a new instance (User)
#8 https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\static'


def logOut(request):
    logout(request)
    return redirect('/')


class Login(View):
    template_name='login.html'
    form=LoginForm
    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        form=self.form(request.POST)
        if form.is_valid():
             user=MyBackend().authenticate(email=request.POST.get('email'),password=request.POST.get('password'))
             if user is not None:
                login(request,user)
                return redirect('/')
             else:
                form.add_error('email','Неправильный имейл или пароль')
                return render(request,self.template_name,{'form':form})
        else:
             return render(request,self.template_name,{"form":form})


class Home(ListView):
     template_name='home.html'
    
     def paginator(self):
         p=Paginator(Post.objects.all(),4)
         self.posts=p.page(1).object_list

     def get(self,request):
         program=subprocess.Popen('python python.py')
         program.wait()
         self.paginator()
         
         return TemplateResponse(request,self.template_name,{'posts':self.posts})


class SignUp(View):
    template_name='signup.html'

    form_class=SignUp

    def get(self,request):
       
        return render(request,self.template_name)

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
           user=get_user_model().objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'],role=Role.objects.create(update=True,update_all=True,create_posts=True,show_profile_all=True))
           login(request,user)
           return redirect('/auth/dash/'+str(user.id))
        else:    
           return render(request,self.template_name,{'form':form})


class Files(View):
    def get(self,request,folder,filename):
       try:
        response=HttpResponse()

        filepath=os.path.join(BASE_DIR,folder)
         
        filename_p=None

        for root, dirs, files in os.walk(filepath):
                for file in files:
                    if filename in file :
                           filename_p=file


        #Deciding the mime type of file        
        def inter(str1):
            mime={
                 "css":'text/css',
                 "html":"text/html",
                 "jpg":'image/jpg',
                 "png":"image/png",
                 "PNG":"IMAGE/PNG",
                 "js":"text/javascript",
                 "webp":"image/webp"
             }
            return mime[str1]
           
            
        if filename_p :
               response=HttpResponse()
               mode="r"
               if 'image' in request.META['HTTP_ACCEPT']:
                  mode="rb"

               with open(os.path.join(filepath,filename_p),mode) as file_handler:
                  response=HttpResponse()
                  response['Content-Type']=inter(os.path.splitext(filename_p)[1][1:])
                  for line in file_handler:
                       response.write(line)
                  else:
                      return response
            
        else:
            return findFile(request=None,url=request.path_info[request.path_info.index('/public')+len('/public')::])
       except:          
           return findFile(request=None ,url=request.path_info[request.path_info.index('/public')+len('/public')::])




class Dash(LoginRequiredMixin,ListView,UserPassesTestMixin):
    login_url="/login"
    redirect_field_name = '/'
    template_name="admin/dashboard.html"
    content1={
        'create_post':{},
        'mes':[]
    }   
    context_object_name='posts' 
    def get(self,request,*args,**kw):
        return super().get(request, *args, **kw)
      
    def test_func(self):
        if self.request.user==self.request.user.id:
           return True
        else:
           return self.request.user.has_perm('show_profile_all')


    def post(self,request,*args,**kw):

        form=PostForm(request.POST,request.FILES)
        files=request.FILES.getlist('pictures')
        
        if form.is_valid():
            data=""
            for f in files: 
                path = default_storage.save('pictures/'+f.name, f)
                data=data+path+","                         

            select_can={"furnish":False,"cars":False,"services":False}
            categ=Category()

            for key in select_can :
                    if request.POST['select']==key:
                        setattr(categ,key,True)
                    else:
                        setattr(categ,key,False)
           
        
            post =Post(title=request.POST.get('title'),users=request.user,content=request.POST.get('content'),time="2020-03-19")
            post.save()
            image=Images.objects.create(post=post,images=data)
            post.image1=image
            categ.post=post
            categ.save()
            post.category1=categ
            post.save()
            self.content1['mes'].append('Пост сохранён ')

        self.content1["create_post"]=form.errors
        return super().get(request, *args, **kw)
      
    def get_queryset(self):
        return Post.objects.all().exclude(id=self.kwargs['id'])
    
    def get_context_data(self, **kwargs):
        user=get_object_or_404(get_user_model(),id=self.kwargs['id'])
        for key in super().get_context_data(**kwargs):
            self.content1[key]=super().get_context_data(**kwargs)[key]

        self.content1['user']=user
        self.content1['my_posts']=Post.objects.filter(users=user)
        self.content1['pokupki']=Products.objects.filter(user=user).all()
        if self.request.user.has_perm('show_profile_all'):
            self.content1['users']=get_user_model().objects.all()[:5]
        return self.content1
   

class DataNews(View) :
    def get(self,request,*args,**kwargs):
        from bs4 import BeautifulSoup
        
        request=requests.get('https://rozetka.com.ua/ua/news-articles-promotions/')
        soup = BeautifulSoup(request.text, 'lxml')
        images=soup.find_all('div',class_="nap-tile-i-image responsive-img")
        data=list()
        for line in images:
            li=list()
            if  line.contents[0].has_attr('data_src'):
                li.append(line.contents[0]['data_src'])
            else:
                li.append(line.contents[0]['src'])
            li.append(line.contents[0]['title'])
            data.append(li)        
        return HttpResponse(json.dumps(data))

def findFile(request,url=None,*args):
  try:
    path='https://liga-a.ru/portfolio/rus-partners'
    if request is not None :
       path+=str(request.path_info)
    else:
       path+=url
    headers=[
    'cache-control: max-age=0',
	'upgrade-insecure-requests: 1',
	'user-agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
	'sec-fetch-user: ?1',
	'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
	'x-compress: null',
	'sec-fetch-site: none',
	'sec-fetch-mode: navigate',
	'accept-encoding: deflate, br',
	'accept-language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    "Access-Control-Allow-Origin: *"
    ]
    newheader=dict()
    
    

    for line in headers:
         parts=line.split(':')
         newheader[parts[0]]=parts[1].strip()


    def inter(str1):
        mime={
                 "css":'text/css',
                 "jpg":'image/jpg',
                 "jpeg":"image/jpeg",
                 "png":"image/png",
                 "PNG":"IMAGE/PNG",
                 'svg':"image/svg+xml"
        }
        if str1 in mime:
            return mime[str1]
        else:
            return False
               

              
    req=requests.get(path,headers=newheader,timeout=2)
    response=HttpResponse()

    m1=inter(os.path.splitext(path)[1][1:])

    
    if m1:
        response['Content-Type']=m1
        
        for c in req.iter_content():
           response.write(c)
        else:
           return response
    else:
        return response
  except:
    import sys

    print(sys.exc_info())
    return HttpResponseNotFound()
    



class DeleteUser(UserPassesTestMixin,SingleObjectMixin,View):
      model=get_user_model()
      def test_func(self):
          return self.request.user.has_perm('delete_users')
      def get(self,request,*args,**kwards):
          get_object_or_404(get_user_model(), id=kwards['pk']).delete()
          return redirect('/auth/dash/'+str(request.user.id))
 
           

class AddUser(FormView,UserPassesTestMixin):
    success_url="/"
    form_class=AddUserForm
    template_name="admin/dashboard.html"
    
    def form_valid(self,form):
        if not request.META['HTTP_REFERER'].find('http://127.0.0.1:8000/auth/dash/'):
            return HttpResponseNotFound()

        select=self.request.POST.getlist('role')
        can=('update_all', 'update','create_posts','show_profile_all')
        role=Role()        
        for action in can:
            if action in select:
                setattr(role,action,True)
            else:
                setattr(role,action,False)
        else:
            role.save()
                   
        newuser=get_user_model().objects.create(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['email'],
            role=role
        )
        return HttpResponse(json.dumps({"message":"Юзер добавлен."}).encode('utf8'))


    def form_invalid(self,form):
        return HttpResponse(json.dumps(form.errors,ensure_ascii=False).encode('utf8'))

    def test_func(self):
        return self.request.user.has_perm('add_users')


class Product(SingleObjectMixin, ListView):
    paginate_by=3
    template_name='product.html'
    

    def get(self, request, *args, **kwargs):
        print(request.user.id)
        self.object = self.get_object(queryset=Post.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_post'] = self.object
        return context

    def get_queryset(self):
        return Post.objects.exclude(id=self.object.id)



class Order(ListView,SingleObjectMixin):
      context_object_name="other_posts"
      
      
      def get(self,request,*args,**kwar):
          count=request.GET.get('count')
          if not count :
              return HttpResponseForbidden()

          if count.isdigit() and request.user.is_authenticated:
              pro=Products.objects.get(user=request.user,product=Post.objects.get(id=kwar['pk']))
              pro.count_of=count
              pro.save()
              return HttpResponse(json.dumps('{"status":"changed","counter":${count}}'))
          else:
              return HttpResponse()


      def post(self, request,*args, **kwargs):
          counter=request.POST.get('count')
          if request.user.is_authenticated and counter.isdigit(): 
             post=get_object_or_404(Post,id=kwargs['pk'])
             product=Products.objects.filter(product=post).first()
             print(product)
             if product:
                 if product.user==request.user:
                        product.count_of+=int(counter)
                        product.save()
                        counter=product.count_of
             else:
                product=Products(user=request.user,product=post,count_of=counter)
                product.save()
             return HttpResponse(json.dumps({"status":"added",'counter':counter}))
          else:
             return HttpResponse(json.dumps({"status":"forbidden"}))

     

class ShowCategory(ListView):
    context_object_name="posts"
    paginate_by=10
    template_name="category.html"
    page_kwarg='p'
    def get(self,request,*args,**kw):
        if not  kw['p']:
                kw['p']=1
        return super().get(request,*args,**kw)  

    def get_queryset(self):
        cat=self.kwargs['category']
        source=None
        if cat == 'furnish':
               source=Post.objects.filter(category1__furnish=True)
        return source

    

class Cat(ListView,UserPassesTestMixin):


    def post(self,request,*args,**kw):
       string=json.loads(request.body)['string']
       if string:
           bytitle=Post.objects.filter(title__contains=string).values('id','users_id','title','content')[:5]
           byauthor=Post.objects.filter(users__username__contains=string).values('id','users_id','title','content')[:5]
           bycontent=Post.objects.filter(content__contains=string).values('id','users_id','title','content')[:5]
           for result in (bytitle,byauthor,bycontent):
               if result:
                   return HttpResponse(repr(list(result)),content_type="application/json;charset=utf-8")
       return HttpResponseForbidden()
