from django.urls import path
from . import views


urlpatterns = [
    path('add_user/', views.UserInfoView.as_view(), name='add-user'), # done
    path('user_list/', views.UserInfoView.as_view(), name='user_list'), # done
    path('get_user/<str:id>/', views.GetUserView.as_view(), name='get-user'), # done
    path('update_user/<str:id>/', views.UpdateUserView.as_view(), name='update_user'), # done
    path('delete_user/<str:id>/', views.DeleteUserView.as_view(), name='delete_user'), # done

    path('upload_resume/', views.ResumeUploadView.as_view(), name='upload-resume') #done
]


