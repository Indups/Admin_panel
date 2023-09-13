from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('login',views.handlelogin,name='handlelogin'),
    path('logout',views.handlelogout,name='handlelogout'),
    path('signup',views.handlesignup,name='handlesignup'),
    path('adminlogin',views.handleadminlogin,name='handleadminlogin'),
    path('adminpanel',views.adminpanel,name='adminpanel'),
    path('userlist',views.userlist,name='userlist'),
    path('adminlogout',views.handleadminlogout,name='handleadminlogout'),
    path('adduser',views.adduser,name='adduser'),
    path('update/<id>',views.update,name='update'),
    path('delete/<int:id>',views.delete,name='delete'),
    # path('deleteconfirm/<id>',views.deleteconfirm,name='deleteconfirm'),
    path('search',views.handlesearch,name='handlesearch'),
]