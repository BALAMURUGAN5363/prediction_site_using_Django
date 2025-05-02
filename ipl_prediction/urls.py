from django.urls import path
from .views import predict_ipl_score

urlpatterns = [
    path("", predict_ipl_score, name="predict_ipl_score"),  # Handles /ipl_score_predictor/
]

