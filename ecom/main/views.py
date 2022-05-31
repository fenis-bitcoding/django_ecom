from unicodedata import category
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Banner,Category,Brand,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook
from django.db.models import Max,Min,Count,Avg
from django.template.loader import render_to_string

# Home Page
def home(request):
	banners = Banner.objects.all().order_by('-id')
	data = Product.objects.filter(is_featured=True).order_by('-id')
	return render(request,'index.html',{'data':data,'banners':banners})

# Category
def category_list(request):
	data = Category.objects.all().order_by('-id')
	return render(request,'category_list.html',{'data':data})

# Brand
def brand_list(request):
	data = Brand.objects.all().order_by('-id')
	return render(request,'brand_list.html',{'data':data})

# Product List
def product_list(request):
	total_data=Product.objects.count()
	data = Product.objects.all().order_by('-id')
	min_price=ProductAttribute.objects.aggregate(Min('price'))
	max_price=ProductAttribute.objects.aggregate(Max('price'))
	return render(request,'product_list.html',{'data':data,'total_data':total_data,'min_price':min_price,'max_price':max_price,})

# Product List According to Category
def category_product_list(request,cat_id):
	category = Category.objects.get(id=cat_id)
	data = Product.objects.filter(category=category).order_by('-id')
	return render(request,'category_product_list.html',{'data':data})

# Product List According to Brand
def brand_product_list(request,brand_id):
	brand = Brand.objects.get(id=brand_id)
	data = Product.objects.filter(brand=brand).order_by('-id')	
	return render(request,'category_product_list.html',{'data':data})

# Product Detail
def product_detail(request,slug,id):
	product = Product.objects.get(id=id)
	related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
	return render(request, 'product_detail.html',{'data':product,'related':related_products})

# Search
def search(request):
	q = request.GET['q']
	data = Product.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'search.html',{'data':data})

# Filter Data
def filter_data(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=Product.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(brand__id__in=brands).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
	t=render_to_string('ajax/product-list.html',{'data':allProducts})
	return JsonResponse({'data':t})

# Load More
def load_more_data(request):
	return render(request,'ajax/product-list.html')

# Add to cart
def add_to_cart(request):
	pass
# Cart List Page
def cart_list(request):
	return render(request, 'cart.html')


# Delete Cart Item
def delete_cart_item(request):
	return render(request,'ajax/cart-list.html')

# Delete Cart Item
def update_cart_item(request):
	return render(request,'ajax/cart-list.html')

# Signup Form
def signup(request):
	return render(request, 'registration/signup.html')


# Checkout
def checkout(request):
		return render(request, 'checkout.html')


def payment_done(request):
	return render(request, 'payment-success.html')


def payment_canceled(request):
	return render(request, 'payment-fail.html')


# Save Review
def save_review(request,pid):
	pass

# User Dashboard
def my_dashboard(request):
	return render(request, 'user/dashboard.html')

# My Orders
def my_orders(request):
	return render(request, 'user/orders.html')

# Order Detail
def my_order_items(request,id):
	return render(request, 'user/order-items.html')

# Wishlist
def add_wishlist(request):
	pass

# My Wishlist
def my_wishlist(request):
	return render(request, 'user/wishlist.html')

# My Reviews
def my_reviews(request):
	return render(request, 'user/reviews.html')

# My AddressBook
def my_addressbook(request):
	
	return render(request, 'user/addressbook.html')

# Save addressbook
def save_address(request):
	return render(request, 'user/add-address.html')

# Activate address
def activate_address(request):
	pass
# Edit Profile
def edit_profile(request):
	return render(request, 'user/edit-profile.html')

# Update addressbook
def update_address(request):
	return render(request, 'user/update-address.html')