from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from  django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from .models import Post,Category
error_messages_email={
            'required':"Введите имейл", 
            'invalid':"Имейл недействительный",
            'max_length':"Слишком большой имейл",
            'min_length':"Слишком короткий имейл"
}

password_errors={
            'max_length':"Слишком длинный пароль",
            'min_length':"Слишком короткий пароль"
 }

def user_exists(value):
      if get_user_model().objects.filter(email=value).exists():
            raise  ValidationError(
            _('Имейл %(value)s уже используется'),
            params={'value': value},
        )



def validate_email(value):
      try:
            email= EmailValidator()
            email(value)
            return True
      except:
            return False


class PostForm(forms.Form):

      title=forms.CharField(max_length=50,min_length=10,error_messages={
            "required":"Заголовок не может быть пустым ",
            'max_length':"Слишком большой заголовок",
            'min_length':"Слишком короткий заголовок"
          
      })
      content=forms.CharField(max_length=600,min_length=10,
      error_messages={
            "required":"Содержание не может быть пустым ",

            'max_length':"Слишком большое содержание ",
            'min_length':"Слишком короткое содержание"
          
      })
      pictures= forms.ImageField(error_messages={
            "required":"Картинка не может быть пустой ",

            'invalid_extension':'Что-то не так с изображение '
      },widget=forms.ClearableFileInput(attrs={'multiple': True}))

      select=forms.ChoiceField(choices=(('furnish','Мебель'),('services',"Услуги"),('cars',"Автомобили")),error_messages={
            "invalid_choice":"Товар или услуга может иметь лишь одну категорию",
            "required":"Выбирите категорию"
      })
      def clean(self):
            cleaned_data = super().clean()
            title=cleaned_data['title']
            if Post.objects.filter(title=title):
                   self.add_error("title","Такой пост уже существует")
            

class  SignUp(forms.Form):
      username=forms.CharField(max_length=30,min_length=4,error_messages={
            'required':'Ваше имя некорректно'
      })
      password=forms.CharField(max_length=21,min_length=5,error_messages=password_errors)
      email=forms.EmailField(max_length=20,min_length=5,error_messages=error_messages_email,validators=[user_exists,validate_email])

      def clean_username(self):
            data=self.cleaned_data['username']
            if get_user_model().objects.filter(username=data).exists():
                  raise forms.ValidationError(_("Ваше имя уже занято"))
            return data
              
    
class  LoginForm(forms.Form):
      email=forms.EmailField(max_length=30,min_length=4,error_messages=error_messages_email)
      password=forms.CharField(max_length=20,min_length=4,error_messages=password_errors)



class AddUserForm(forms.Form):
      
      email=forms.EmailField(max_length=30,min_length=4,error_messages=error_messages_email)
      password=forms.CharField(max_length=20,min_length=4,error_messages=password_errors)
      username=forms.CharField(max_length=20,min_length=4,error_messages={
             'required':'Ваше имя некорректно',
             'max_length':"Слишком большое  имя ",
             'min_length':"Слишком короткое имя"
      })

      def clean(self):
            cleaned_data = super().clean()
            email = cleaned_data.get("email")
            username = cleaned_data.get("username")
            if get_user_model().objects.filter(email=email).exists() or get_user_model().objects.filter(username=username).exists() :
                   self.add_error('email','Пользователь с таким именем или почтой уже существует ')
                   
          