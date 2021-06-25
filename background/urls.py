from django.urls import path
from background import views as background_views
from login import views as login_views

app_name = 'background'
urlpatterns = [
    path('group/', background_views.group, name="group"),
    path('main/', background_views.main_page, name="main"),
    path('group_create/', background_views.group_create),
    path('paper_create/', background_views.paper_insert),
    path('note_create/', background_views.note_create),
    path('group_list.html/', background_views.group, name="group_list"),
    path('note_list.html/', background_views.note, name="note_list"),
    path('paper_list.html/', background_views.paper, name="paper_list"),
    path('main_page.html/', background_views.main_page),
    path('paper_detail.html/<paper_id>/', background_views.paper_detail, name="paper_detail"),
    path('group_detail.html/<group_id>/', background_views.group_detail, name="group_detail"),
    path('note_detail.html/<note_id>/', background_views.note_detail, name="note_detail"),
    path('<filename>/', background_views.getPage),
    path('note_form/<paper_id>/', background_views.note_form),
    path('add_number/<group_id>/<user_id>/', background_views.add_number),
    path('info_delete/<kind>/<group_id>/', background_views.info_delete),
    #   个人待办事项处理
    path('task/add/<content>/', background_views.task_add),
    path('task/delete/<task_id>/', background_views.task_delete),
    path('task/toggle/<task_id>/', background_views.task_toggle)
]
