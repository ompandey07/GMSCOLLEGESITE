from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    
    # Websites Urls
    path('', views.home_page_view, name='home_page_view'),
    path('contact_page_view/', views.contact_page_view, name='contact_page_view'),
    path('courses_page_view/', views.courses_page_view, name='courses_page_view'),
    path('Gallery_page_view/', views.Gallery_page_view, name='Gallery_page_view'),
    path('gallery/<int:gallery_id>/', views.Detailed_Gallery_page_view, name='Detailed_Gallery_page_view'),
    path('Notices_page_view/', views.Notices_page_view, name='Notices_page_view'),
    path('about_page_view/', views.about_page_view, name='about_page_view'),









                        #! < ------------------------------------> #


    #  Content Urls 

    # Auths
    path('admin_pannel_view/', views.admin_pannel_view, name='admin_pannel_view'),
    path('login_page_view/', views.login_page_view, name='login_page_view'),
    path('register_page_view/', views.register_page_view, name='register_page_view'),
    path('logout/', views.logout_view, name='logout_view'),


    # Uploads
    path('create_notice_view/', views.create_notice_view, name='create_notice_view'),
    path('update-notice/<int:notice_id>/', views.update_notice_view, name='update_notice_view'),
    path('delete-notice/<int:notice_id>/', views.delete_notice_view, name='delete_notice_view'),



    # Create new gallery item
    path('gallery/create/', views.create_gallery_view, name='create_gallery_view'),
    
    # Update existing gallery item
    path('gallery/update/<int:gallery_id>/', views.update_gallery_view, name='update_gallery_view'),
    
    # Delete gallery item
    path('gallery/delete/<int:gallery_id>/', views.delete_gallery_view, name='delete_gallery_view'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
