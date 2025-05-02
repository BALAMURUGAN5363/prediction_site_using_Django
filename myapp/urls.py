from django.contrib import admin
from django.urls import path, include

handle404 = 'myapp.views.custom_page_error'

urlpatterns = [
    path("blog/", include("blog.urls")),
    path('admin/', admin.site.urls),
    path("diabetes_predictor/", include("diabetes_predictor.urls")),
    path("ipl_prediction/", include("ipl_prediction.urls")),
    path("car_price_prediction/", include("car_price_prediction.urls")),
]



