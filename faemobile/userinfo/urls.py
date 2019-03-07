from django.conf.urls import url
from userinfo import views

urlpatterns = [
    url(r"^login/$", views.login_),
    url(r"^loginin/$", views.loginin),
    url(r"^register/$", views.register_),
    url(r"^logout/$", views.logout),
    url(r"^registerin/$", views.registerin),
    url(r"^changepwd/$", views.changepwd),
    url(r"^change_pwd/$", views.change_pwd)
]