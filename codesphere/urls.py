"""
URL configuration for codesphere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpVIew.as_view(),name='signup'),
    path('',views.SignInView.as_view(),name='signin'),
    path('index/',views.IndexView.as_view(),name='index'),
    path('logout/',views.LogoutView.as_view(),name='signout'),
    path('profile/change',views.UserProfileEditView.as_view(),name='profile-edit'),
    path('project/add',views.ProjectCreateView.as_view(),name='project-add'),
    path('mywork/all',views.MyProjectListView.as_view(),name='my-work'),
    path('project/<int:pk>/update',views.ProjectUpdateView.as_view(),name='project-update'),
    path('project/<int:pk>/detail/',views.ProjectDetailView.as_view(),name='project-detail'),
    path('project/<int:pk>/wishlist',views.AddWishListItemView.as_view(),name='wish-list'),
    path('mywishlist',views.MyWishListView.as_view(),name='my-wishlist'),
    path('mywishlist/<int:pk>/delete',views.WishListItemDeleteView.as_view(),name='wishlist-delete'),
    path('checkout/',views.CheckOutView.as_view(),name='checkout'),
    path('payment/verify/',views.PaymentVerificationView.as_view(),name='payment-verification'),
    path('orders/all/',views.MyordersView.as_view(),name='orders'),
    path('reset/password',views.PasswordResestView.as_view(),name='reset-password'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
