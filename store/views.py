from django.forms import BaseModelForm

from django.http import HttpResponse

from django.shortcuts import render,redirect,get_object_or_404

from store.forms import SignUpForm,SignInForm,UserProfileForm,ProjectForm,PasswordResetForm

from django.urls import reverse_lazy

from django.contrib.auth import authenticate,logout,login

from django.views.generic import View,FormView,CreateView,TemplateView

from store.models import UserProfile,Project,WishListItem,Order

from django.contrib import messages

from django.db.models import Sum

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from django.core.mail import send_mail

from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

from store.decorators import signin_required

from django.contrib.auth.models import User

from decouple import config

from twilio.rest import Client

decs=[signin_required,never_cache]

def send_text_message():
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    messaging_service_sid='MGf6cbeb77420eb2770cd2b66be77db8f8',
    body='You have completed purchase from Codesphere',
    to='+919048444482',
)
    print(message.sid)
    

def send_email():

    send_mail(
    "Codehub Project Download",
    "You have completed your purchase of project",
    "nihasansin25@gmail.com",
    ["sr4sarath18@gmail.com"],
    fail_silently=False,
)


class SignUpVIew(CreateView):

    template_name="register.html"

    form_class=SignUpForm

    success_url=reverse_lazy("signin")

    # def get(self,request,*args,**kwargs):

    #     form_instance=self.form_class()

    #     return render(request,self.template_name,{"form":form_instance})

    # def post(self,request,*args,**kwargs):

    #     form_instance=self.form_class(request.POST)

    #     if form_instance.is_valid:

    #         form_instance.save()

    #         print("account created")

    #         return redirect("signin")

    #     else:

    #         return render(request,self.template_name,{"form":form_instance})
@method_decorator(decs,name="dispatch")
class IndexView(View):

    template_name="index.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.all().exclude(developer=request.user)

        return render(request,self.template_name,{"data":qs})


class SignInView(FormView):

    template_name="login.html"

    form_class=SignInForm

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("index")
        
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class LogoutView(View):
    
    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")

@method_decorator(decs,name="dispatch")
class UserProfileEditView(View):

    template_name="profile_edit.html"

    form_class=UserProfileForm

    def get(self,request,*args,**kwargs):

        # profile_object=UserProfile.objects.get(owner=request.user)

        user_profile_instance=request.user.profile

        form_instance=self.form_class(instance=user_profile_instance)

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=self.form_class(request.POST,instance=user_profile_instance,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("index")

        return render(request,self.template_name,{"form":form_instance})


@method_decorator(decs,name="dispatch")
class ProjectCreateView(View):

    template_name='project_add.html'

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.developer=request.user

            form_instance.save()

            return redirect("index")
        
        return render(request,self.template_name,{"form":form_instance})


@method_decorator(decs,name="dispatch")
class MyProjectListView(View):

    template_name="myproject.html"

    def get(self,request,*args,**kwargs):

        qs=Project.objects.filter(developer=request.user)

        return render(request,self.template_name,{"data":qs})


@method_decorator(decs,name="dispatch")
class ProjectUpdateView(View):

    template_name="project_update.html"

    form_class=ProjectForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=Project.objects.get(id=id)

        form_instance=self.form_class(instance=project_object)

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=Project.objects.get(id=id)

        form_instance=self.form_class(request.POST,instance=project_object,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("my-work")

        return render(request,self.template_name,{"form":form_instance})


@method_decorator(decs,name="dispatch")
class ProjectDetailView(View):

    template_name="project_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Project.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})

@method_decorator(decs,name="dispatch")
class AddWishListItemView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        project_object=get_object_or_404(Project,id=id)

        try:

            request.user.basket.basket_item.create(project_object=project_object)

            print("wish list item added")

            messages.success(request,"added successfully to wishlist")

        except Exception as e:

            messages.error(request,"failed")
    

        return redirect("index")
        

@method_decorator(decs,name="dispatch")
class MyWishListView(View):

    template_name="mywishlist.html"

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_item.filter(is_order_placed=False)  

        total=qs.values("project_object").aggregate(total=Sum("project_object__price")).get("total")     

        print("totall",total)     

        return render(request,self.template_name,{"data":qs,"total":total})


@method_decorator(decs,name="dispatch")
class WishListItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        WishListItem.objects.get(id=id).delete()

        return redirect("my-wishlist")

import razorpay

@method_decorator(decs,name="dispatch")
class CheckOutView(View):

    template_name="checkout.html"

    def get(self,request,*args,**kwargs):

        #razorpay authentication
        KEY_ID=config('KEY_ID')

        KEY_SECRET=config('KEY_SECRET')

        # authentication
        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        # order create in razorpay
        wish_list_total=request.user.basket.basket_item.filter(is_order_placed=False).values("project_object").aggregate(total=Sum("project_object__price")).get("total")

        data={ "amount":wish_list_total*100, "currency":"INR", "receipt":"order_rcptid_code_hub" }

        payment=client.order.create(data=data)

        order_id=payment.get("id")

        order_object=Order.objects.create(order_id=order_id,customer=request.user)

        wishlist_items=request.user.basket.basket_item.filter(is_order_placed=False)

        for wi in wishlist_items:

            order_object.wishlist_item_objects.add(wi)

            wi.is_order_placed=True

            wi.save()

        data={
            "key_id":KEY_ID,
            "amount":wish_list_total,
            "order_id":order_id
        }
            
        

        return render(request,self.template_name,data)

# @method_decorator(decs,name="dispatch")
@method_decorator(csrf_exempt,name='dispatch')
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        KEY_ID=config('KEY_ID')

        KEY_SECRET=config('KEY_SECRET')

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        try:

            client.utility.verify_payment_signature(request.POST)

            order_id=request.POST.get("razorpay_order_id")

            Order.objects.filter(order_id=order_id).update(is_paid=True)

            send_email()

            send_text_message()

            print("success")

        except:

            print("failed")


        return redirect('orders')

@method_decorator(decs,name="dispatch")
class MyordersView(View):

    template_name="myorders.html"

    def get(self,request,*args,**kwargs):

        qs=Order.objects.filter(customer=request.user)

        return render(request,self.template_name,{"data":qs})

@method_decorator(decs,name="dispatch")
class PasswordResestView(View):

    template_name="password_reset.html"

    form_class=PasswordResetForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            username=form_instance.cleaned_data.get("username")

            email=form_instance.cleaned_data.get("email")

            password1=form_instance.cleaned_data.get("password1")

            password2=form_instance.cleaned_data.get("password2")

            print(username,email,password1,password2)

            try:
                assert password1==password2,"password mismatch"

                user_object=User.objects.get(username=username,email=email)

                user_object.set_password(password2)

                user_object.save()

                return redirect('signin')

            except Exception as e:

                messages.error(request,f"{e}")

                return render(request,self.template_name,{"form":form_instance})

        return render(request,self.template_name,{"form":form_instance})



        





        









