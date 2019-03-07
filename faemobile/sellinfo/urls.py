from django.conf.urls import url
from sellinfo import views

urlpatterns = [
    url(r"^sellweek/$",views.sellweek),
    url(r"^addsellweek/$",views.addsellweekly),
    url(r"^addsellweekpost/$",views.addsellweek),
    url(r"^showinfo/$",views.showinfo),
    url(r"^showpipeline/$",views.showpipeline),
    url(r"^amendsellweek/$",views.amendsellweek),
    url(r"^updateinfo/$",views.updateinfo),
    url(r"^amendinfo/$",views.amendinfo),
    url(r"^exportsellweek/$",views.exportsellweek),
    url(r"^pipeline/$",views.pipeline),
    url(r"^addpipeline/$",views.addpipeline),
    url(r"^addpipelinepost/$",views.addpipelinepost),
    url(r"^amendpipeline/$",views.amendpipeline),
    url(r"^amendinfopipe/$",views.amendinfopipe),
    url(r"^updateinfopipe/$",views.updateinfopipe),
    url(r"^exportpipeline/$",views.exportpipeline),
]