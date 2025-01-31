from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy



app_name = 'account'
urlpatterns = [
    path('register/', views.RegisterView, name='register_url'),
    path('', views.DashView, name='dash_url'),

    path('login/', auth_views.LoginView.as_view(template_name='account/login.html', 
        extra_context={'source':'login'}), 
        name='login_url'),

    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), 
                                                    name='logout_url'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='account/PassChange.html', 
        success_url=reverse_lazy('account:pass_change_done_url')), 
        name='pass_change_url'),

    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='account/PassChangeDone.html',),
        name= 'pass_change_done_url'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/PassReset.html',
        success_url=reverse_lazy('account:pass_reset_complete_url'),
        email_template_name='account/ResetEmail.html'),
        name='pass_reset_url'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/PassResetComplete.html'),
        name='pass_reset_complete_url'),
    
    path('password_reset_confirm/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(
        template_name='account/PassResetConfirm.html',
        success_url = reverse_lazy('account:pass_reset_done_url')), 
        name='pass_reset_confirm_url'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/PassResetDone.html'),
        name='pass_reset_done_url'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate_url'),
    path('edit_info/<username>/', views.EditInfo, name='edit_info_url'),
    path('users_list/', views.ListProfilesView, name='profiles_list_url'),
    path('follow_user/', views.follow_user, name='follow_user_url'),
    path('userdetail/<int:id>/', views.ProfileDetail, name='user_detail_url'),

]

