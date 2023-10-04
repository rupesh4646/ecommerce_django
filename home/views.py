from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *

# Create your views here.
class BaseView(View):
    views = {}
    views['categories'] = Category.objects.all()
    views['brands'] = Brand.objects.all()
    views['siteinfos'] = SiteInfo.objects.all()


class HomeView(BaseView):
    def get(self,request):
        self.views
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['hots'] = Product.objects.filter(labels = 'hot')
        self.views['news'] = Product.objects.filter(labels = 'new')
        self.views['sales'] = Product.objects.filter(labels = 'sale')
        return render(request,'index.html',self.views)


class CategoryView(BaseView):
    def get(self,request,slug):
        self.views
        cat_id = Category.objects.get(slug = slug).id
        self.views['cat_products'] = Product.objects.filter(category_id = cat_id)
        return render(request, 'category.html', self.views)


class BrandView(BaseView):
    def get(self,request,slug):
        self.views
        br_id = Brand.objects.get(slug = slug).id
        self.views['brand_products'] = Product.objects.filter(brand_id = br_id)
        return render(request, 'brand.html', self.views)


class DetailView(BaseView):
    def get(self,request,slug):
        self.views
        self.views['detail_products'] = Product.objects.filter(slug = slug)
        cat_id = Product.objects.get(slug = slug).category_id
        self.views['related_products'] = Product.objects.filter(category_id = cat_id)
        return render(request, 'product-detail.html', self.views)


class SearchView(BaseView):
    def get(self,request):
        self.views
        # if request.method == 'GET':
        #     query = request.GET['search']
        query = request.GET.get('search')
        if query != '':
            self.views['search_products'] = Product.objects.filter(name__icontains = query)
        elif query == ' ':
            return redirect('/')
        else:
            return redirect('/')
        return render(request,'search.html',self.views)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,"This username is already used!")
                return redirect('/signup')
            elif User.objects.filter(email = email).exists():
                messages.error(request, "This email is already exists!")
                return redirect('/signup')
            else:
                User.objects.create_user(
                    username = username,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    password= password
                ).save()
        else:
            messages.error(request, "The passwords do not match!")
            return redirect('/signup')

    return render(request,'signup.html')


class CartView(BaseView):
    def get(self,request):
        username = request.user.username
        self.views['cart_products'] = Cart.objects.filter(name = username, checkout = False)
        return render(request,'cart.html',self.views)