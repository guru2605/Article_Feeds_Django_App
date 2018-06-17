from django.conf.urls import url
from basic_app import views

# SET THE NAMESPACE!
app_name = 'basic_app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^settings/$',views.settings,name="settings"),
    url(r'^articles/$',views.articles_list,name="articles"),
    url(r'^createpost/$',views.createpost,name="createarticle"),
    url(r'^deletepost/$',views.deletepost,name="deletepost"),
    url(r'^myarticles/$',views.myarticles,name="myarticles"),
    url(r'^password/$',views.change_password,name="change_password"),
    url(r'^like/',views.like_post,name="like_post"),
    url(r'^dislike/',views.dislike_post,name="dislike_post"),
    url(r'^block/',views.block_post,name="block_post"),

    url(r'^editpost/$',views.edit_post,name="editpost"),
    url(r'^edit_post_submit/$',views.edit_post_submit,name="editpostsubmit")



    
]