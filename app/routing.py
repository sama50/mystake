from django.urls import path
from app.patti_consumers import PattiConsumers

websocket_urlpatterns =[

    path('ws/patti/',PattiConsumers.as_asgi())
]

# ## celery -A kingobet worker --pool=solo -l info
