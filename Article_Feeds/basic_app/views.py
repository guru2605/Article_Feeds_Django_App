# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from basic_app.forms import UserForm,UserProfileInfoForm,AddArticle,EditProfileForm
from .models import Articles as ArticleModel,UserProfileInfo


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit=False)

            profile.user = user            

            profile.save()


            registered = True

        else:
            print(user_form.errors,profile_form.errors)
            
            

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)

                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'basic_app/login.html', {})


def settings(request):
    user = request.user
    updated = False
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            updated =True
            return render(request,'basic_app/settings.html',{'user_form':user_form,'updated':updated})
       
    else:
        user_form = EditProfileForm(instance = request.user)
        user_profile_info = get_object_or_404(UserProfileInfo,user= request.user)
        phone = user_profile_info.phone
        art_type = user_profile_info.articlecategory
        user_profile_form = UserProfileInfoForm(initial={'phone':phone,'articlecategory':art_type})
        return render(request,'basic_app/settings.html',{'user_form':user_form,'profile_form':user_profile_form,'updated':False})

    


def articles_list(request):
    user = request.user    
    user_ob = UserProfileInfo.objects.get(user=user)
    user_choices=str(user_ob.articlecategory)
    print(user_choices)

    


    # articles = ArticleModel.objects.filter(article_type__contains =user_choices)
    # for article in articles:
    #     print article.article_name
    articles= ArticleModel.objects.all()
    return render(request,'basic_app/article_list.html',{'article_list':articles})



def createpost(request):
    article_form = AddArticle()
    if request.method == 'GET':
        return render(request,'basic_app/article_create.html',{'form':article_form})

    if request.method == 'POST':
        article_form = AddArticle(request.POST)
        if article_form.is_valid():
            article_type = article_form.cleaned_data['article_type']            
            article_name = article_form.cleaned_data['article_name']
            article_body = article_form.cleaned_data['article_body']
            published_by = request.user
            try:
                articleob =ArticleModel(article_type=article_type,article_name=article_name,article_body=article_body,published_by=published_by)
                articleob.save()
                print("SUCESSSSSSSSSSSSSS") 
                return render(request,"basic_app/article_create.html",{'form':article_form,'color':'green','msg':'Article Posted Successfully'})
            except:
                print( "ERROR inserting article")
                return render(request,"basic_app/article_create.html",{'form':article_form,'color':'red','msg':'Article could not be posted'})

   




def edit_post(request):
    # article_form= AddArticle(instance=article)
    updated = False
    if request.method == 'POST':
        article = get_object_or_404(ArticleModel,id=request.POST.get('post_id'))
        article_name = article.article_name
        article_body = article.article_body
        article_type = article.article_type
        article_form = AddArticle(initial={'article_name':article_name,'article_body':article_body,'article_type':article_type})
        return render(request,"basic_app/editpost.html",{'form':article_form,'updated':updated})
    else:
        print( "ERROR loading form")
        return HttpResponse('Error loading form')

def edit_post_submit(request):
    if request.method == 'POST':
        article_form = AddArticle(request.POST)
        if article_form.is_valid():
            article_type = article_form.cleaned_data['article_type']            
            article_name = article_form.cleaned_data['article_name']
            article_body = article_form.cleaned_data['article_body']
            published_by = request.user
            try:
                articleob =ArticleModel(article_type=article_type,article_name=article_name,article_body=article_body,published_by=published_by)
                articleob.save()
                print("SUCESSSSSSSSSSSSSS")
                return render(request,"basic_app/myarticles.html",{'form':article_form,'color':'green','msg':'Article Updated Successfully'})
            except:
                print("ERROR inserting article")
                return render(request,"basic_app/editpost.html",{'form':article_form,'color':'red','msg':'Article could not be Updated'})




def deletepost(request):
    if request.method == 'POST':
        ArticleModel.objects.filter(id=request.POST.get('post_id')).delete()
        print("deleted")
        return HttpResponseRedirect('/basic_app/myarticles')



    









def myarticles(request):
    username = request.user
    articles = ArticleModel.objects.filter(published_by=username)
    return render(request,'basic_app/myarticles.html',{'article_list':articles})


def change_password(request):
    updated = False
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST,user= request.user)
        if form.is_valid():
            form.save()
            updated =True
            update_session_auth_hash(request,form.user)
            args = {'form':form,'updated':updated}
            return render(request,'basic_app/change_password.html',args)

        else:
            return render(request,'basic_app/change_password.html',{'updated':False})
    else:
         form = PasswordChangeForm(user= request.user)
         args = {'form':form}
         return render(request,'basic_app/change_password.html',args)


def like_post(request):
    article = get_object_or_404(ArticleModel,id=request.POST.get('post_id'))    
    article.likes.add(request.user)    
    return HttpResponseRedirect('/basic_app/articles')

def dislike_post(request):
    article = get_object_or_404(ArticleModel,id=request.POST.get('post_id'))    
    article.dislikes.add(request.user)    
    return HttpResponseRedirect('/basic_app/articles')

def block_post(request):
    article = get_object_or_404(ArticleModel,id=request.POST.get('post_id'))    
    article.blocks.add(request.user)    
    return HttpResponseRedirect('/basic_app/articles')






            

