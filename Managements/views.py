from django.shortcuts import render , redirect , get_object_or_404
from .models import VisitorContactModel , Notice , Gallery
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone




                                                                            #? Websites Views



                                                                            
#! Home Page View
def home_page_view(request):
    notices = Notice.objects.filter(is_active=True).order_by('-created_at')[:3]  
    galleries = Gallery.objects.filter(is_active=True).order_by('-created_at')[:3]  
    
    if request.method == 'POST':
        Fullname = request.POST.get('first_name')
        Email = request.POST.get('email_address')
        PhoneNumber = request.POST.get('phone_number')
        Message = request.POST.get('message')

        Data = VisitorContactModel(Fullname=Fullname, Email=Email, PhoneNumber=PhoneNumber, Message=Message)
        Data.save()
        return redirect('home_page_view')    
    
    context = {
        'notices': notices,
        'galleries' : galleries
    }
    return render(request, 'Website/index.html', context)





#! About Page View
def about_page_view (request):
    return render(request , 'Website/about.html')



#! contact_page_view
def contact_page_view (request):
    return render(request , 'Website/contact.html')



# ! courses_page_view
def courses_page_view (request):
    return render(request , 'Website/Courses.html')



# ! Gallery_page_view
def Gallery_page_view (request):
    galleries = Gallery.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'galleries': galleries
    }
    return render(request, 'Website/Gallery.html', context)



# ! Deyailed_Gallery_page_view
def Detailed_Gallery_page_view (request , gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id, is_active=True)
    context = {
        'gallery': gallery
    }
    return render(request, 'Website/DetailedGallery.html', context)


# ! Notices_page_view
def Notices_page_view (request):
    notices = Notice.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'notices': notices
    }
    return render(request , 'Website/Notices.html' , context)




#! Websites Views End



                                                                    #! < ----------------------------------------> #




                                                                            # ? Authentication Views


#! Register View 
# @login_required
def register_page_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('Email')  
        password = request.POST.get('password')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register_page_view')
        
        # Create new user
        user = User.objects.create_user(
            username=email,  
            email=email,
            password=password,
            first_name=name
        )
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('register_page_view')
    
    return render(request, 'Controls/Register.html')





#! Login View
def login_page_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user (using email as username)
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('admin_pannel_view')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login_page_view')
    
    return render(request, 'Controls/Login.html')

@login_required(login_url='login_page_view')




#! Lgout View
def logout_view(request):
    logout(request)
    return redirect('login_page_view')





                                                                                # ? Admin Panel View

#! Admin Panel View
@login_required
def admin_pannel_view(request):
    # Get notices based on user role
    if request.user.is_superuser or request.user.is_staff:
        notices = Notice.objects.all().order_by('-created_at')
        galleries = Gallery.objects.all().order_by('-created_at')
    else:
        notices = Notice.objects.filter(created_by=request.user).order_by('-created_at')
        galleries = Gallery.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'VisitorContactData': VisitorContactModel.objects.all(),
        'notices': notices,
        'galleries': galleries,
        'user': request.user
    }
    return render(request, 'Controls/AdminPanel.html', context)





                                                                    #?   Handling Notice Section Views



#! Create Notice View
@login_required
def create_notice_view(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # Only validate category
        if not category:
            messages.error(request, 'Category is required')
            return redirect('create_notice_view')

        try:
            notice = Notice.objects.create(
                category=category,
                title=title if title else None,
                description=description if description else None,
                created_by=request.user
            )
            if image:
                notice.image = image
                notice.save()
            messages.success(request, 'Notice created successfully')
            return redirect('create_notice_view')
        except Exception as e:
            messages.error(request, f'Error creating notice: {str(e)}')
            return redirect('create_notice_view')

    context = {
        'notice': None,
        'CATEGORY_CHOICES': Notice.CATEGORY_CHOICES,
    }
    return render(request, 'Controls/UploadNotice.html', context)




# Update Notice View
@login_required
def update_notice_view(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    
    if not (request.user.is_superuser or request.user.is_staff) and notice.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this notice')
        return redirect('admin_pannel_view')
    
    if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        image_clear = request.POST.get('image-clear') == 'true'

        # Only validate category
        if not category:
            messages.error(request, 'Category is required')
            return redirect('update_notice_view', notice_id=notice_id)

        try:
            notice.category = category
            notice.title = title if title else None
            notice.description = description if description else None
            
            # Handle image
            if image_clear:
                notice.image.delete(save=False)
                notice.image = None
            elif image:
                if notice.image:
                    notice.image.delete(save=False)
                notice.image = image
            
            notice.save()
            messages.success(request, 'Notice updated successfully')
            return redirect('admin_pannel_view')
        except Exception as e:
            messages.error(request, f'Error updating notice: {str(e)}')
            return redirect('update_notice_view', notice_id=notice_id)

    context = {
        'notice': notice,
        'CATEGORY_CHOICES': Notice.CATEGORY_CHOICES,
        'is_update': True
    }
    return render(request, 'Controls/UploadNotice.html', context)



def notice_detail_view(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    context = {
        'notice': notice
    }
    return render(request, 'Website/DetailedNotice.html', context)





#! Delete Notice View
@login_required
def delete_notice_view(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    
    # Check if user has permission to delete this notice
    if not (request.user.is_superuser or request.user.is_staff) and notice.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this notice')
        return redirect('admin_pannel_view')
        
    try:
        notice.delete()
        messages.success(request, 'Notice deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting notice: {str(e)}')
    return redirect('admin_pannel_view')







                                                            #?   Handling Gallery Section Views
#! Create Gallery View
@login_required
def create_gallery_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not all([title, description, image]):
            messages.error(request, 'All fields are required')
            return redirect('create_gallery_view')

        try:
            Gallery.objects.create(
                title=title,
                description=description,
                image=image,
                created_by=request.user
            )
            messages.success(request, 'Gallery image uploaded successfully')
            return redirect('create_gallery_view')
        except Exception as e:
            messages.error(request, f'Error uploading image: {str(e)}')
            return redirect('create_gallery_view')
    context = {
        'is_update': False
    }
    return render(request, 'Controls/UploadGallery.html' , context)







#! Update Gallery View
@login_required
def update_gallery_view(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    
    if not (request.user.is_superuser or request.user.is_staff) and gallery.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this gallery item')
        return redirect('admin_pannel_view')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not all([title, description]):
            messages.error(request, 'Title and description are required')
            return redirect('update_gallery_view', gallery_id=gallery_id)

        try:
            gallery.title = title
            gallery.description = description
            if image:
                gallery.image = image
            gallery.save()
            messages.success(request, 'Gallery item updated successfully')
            return redirect('admin_pannel_view')
        except Exception as e:
            messages.error(request, f'Error updating gallery item: {str(e)}')
            return redirect('update_gallery_view', gallery_id=gallery_id)

    context = {
        'gallery': gallery,
        'user': request.user,
        'is_update': True
    }
    return render(request, 'Controls/UploadGallery.html', context)






#! Delete Gallery View
@login_required
def delete_gallery_view(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    
    if not (request.user.is_superuser or request.user.is_staff) and gallery.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this gallery item')
        return redirect('admin_pannel_view')

    try:
        gallery.delete()
        messages.success(request, 'Gallery item deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting gallery item: {str(e)}')
    return redirect('admin_pannel_view')

#! Control Views End