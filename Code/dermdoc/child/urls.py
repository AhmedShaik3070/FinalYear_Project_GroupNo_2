from django.urls import path
from .views import get_all_children,get_children_by_user,child
urlpatterns = [
    path('my-child/',get_children_by_user,name='child_by_adder'),
    path('child/<int:pk>',child,name="post_child"),
    path('childer/',get_all_children,name='all_children'),
]
