from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    # Олимпиады и комментарии
    path('olympiad/<int:pk>/', views.olympiad_detail, name='olympiad_detail'),
    path('olympiad/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('report-comment/<int:pk>/', views.report_comment, name='report_comment'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),

    # Обращения и онлайн
    path('support/', views.support_center, name='support_center'),
    path('online-ping/', views.online_ping, name='online_ping'),

    # Страницы документов
    path('agreement/', views.agreement_view, name='agreement'),
    path('cookies/', views.cookies_view, name='cookies_policy'),

    # Настройки темы
    path('settings/', views.settings_view, name='settings'),

    # Страницы админки
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('login-admin/', views.login_admin, name='login_admin'),
    path('logout-admin/', views.logout_admin, name='logout_admin'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('excel-instruction/', views.excel_instruction, name='excel_instruction'),
]
