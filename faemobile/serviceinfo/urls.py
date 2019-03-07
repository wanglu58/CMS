from django.conf.urls import url
from serviceinfo import views

urlpatterns = [
    url(r"^service/$",views.service),
    url(r"^addservice/$",views.addservice),
    url(r"^addservicepost/$",views.addservicepost),
    url(r"^showinfo/$",views.showinfo),
    url(r"^amendservice/$",views.amendservice),
    url(r"^amendinfo/$",views.amendinfo),
    url(r"^amendservicepost/$",views.amendservicepost),
    url(r"^exportservice/$",views.exportservice)

]