from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo,Articles
from  django.contrib.auth.forms import UserChangeForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta():
        model = User
        fields = ('first_name','last_name','username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    OPTIONS = (
                ("Politics", "Politics"),
                ("SPACE", "SPACE"),
                ("Technology", "Technology"),
                ("CINEMA", "CINEMA"),
                )
    articlecategory = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                             choices=OPTIONS)
    class Meta():
        model = UserProfileInfo
        fields = ('phone','articlecategory')

class AddArticle(forms.ModelForm):
    OPTIONS = (
                ("Politics", "Politics"),
                ("SPACE", "SPACE"),
                ("Technology", "Technology"),
                ("CINEMA", "CINEMA"),
                )
    article_type = forms.ChoiceField(choices=OPTIONS)
    article_body = forms.CharField(widget=forms.Textarea)
    class Meta():
        model = Articles
        fields = ('article_type','article_name','article_body',)


class EditProfileForm(UserChangeForm):
    class Meta():
        model=User
        fields = ('email','first_name','last_name','password',)