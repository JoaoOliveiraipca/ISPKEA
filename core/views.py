from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from core.models import Product, Category, CartOrderItems, CartOrder, Wishlist,ProductImages, Address, ProductReview
from django.db.models import Count, Avg
from core.forms import ProductReviewForm
from django.contrib import messages
from django.template.loader import render_to_string

# Create your views here.

def index(request):
    products = Product.objects.filter(featured = True).order_by("-id")

    context = {
        "products": products #key : object
    }
    return render(request, 'core/index.html', context)


def product_list_view(request):
     products = Product.objects.filter().order_by("-id")

     context = {
        "products": products #key : object
    }
     
     return render(request, 'core/product-list.html', context)
    
def category_list_view(request):
     categories = Category.objects.all()

     context = {
        "categories": categories  #key : object
    }
     
     return render(request, 'core/category-list.html', context)
    
def category_product_list_view(request, cid):
     category = Category.objects.get(cid=cid)
     products = Product.objects.filter(category=category)

     context = {
          "category":category,
          "products":products
     }

     return render(request, "core/category-product-list.html", context)

def product_detail_view(request, pid):
     
     product = Product.objects.get(pid=pid)
     p_images = product.p_images.all()

     #Getting all reviews
     reviews = ProductReview.objects.filter(product=product)

     #Getting average reviews
     average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

     #product revire form
     review_form = ProductReviewForm()

     context = {
          "product":product,
          "p_images":p_images,
          "reviews":reviews,
          "review_form":review_form,
          "average_rating": average_rating
     }

     return render(request, "core/product-detail.html", context)

def add_review(request, pid):
     product = Product.objects.get(pid=pid)
     user = request.user

     review = ProductReview.objects.create(
          user= user,
          product= product,
          review = request.POST['review'],
          rating = request.POST['rating'],
     )

     context = {
          'user': user.username,
          'review': request.POST['review'],
          'rating': request.POST['rating'],
     }

     average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

     return JsonResponse(
          {
          'bool': True,
          'context': context,
          'avg_reviews': average_reviews
          }
     )


def add_to_cart(request):
     cart_product = {}

     cart_product[str(request.GET['id'])] ={
          'title':request.GET['title'],
          'qty':request.GET['qty'],
          'price':request.GET['price'],
          'image':request.GET['image'],
          'pid':request.GET['pid'],
     }

     if 'cart_data_obj' in request.session:
          if str(request.GET['id']) in request.session['cart_data_obj']:
               cart_data = request.session['cart_data_obj']
               cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
               cart_data.update(cart_data)
               request.session['cart_data_obj'] = cart_data
          else:
               cart_data = request.session['cart_data_obj']
               cart_data.update(cart_product)
               request.session['cart_data_obj'] = cart_data
     
     else:
          request.session['cart_data_obj'] = cart_product
     return JsonResponse({"data":request.session['cart_data_obj'],'totalcartItems':len(request.session['cart_data_obj'])})


def cart_view(request):
     cart_total_amount = 0
     if 'cart_data_obj' in request.session:

          for product_id, item in request.session['cart_data_obj'].items():
               cart_total_amount += int(item['qty']) * float(item['price'])
          return render(request,"core/cart.html", {"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
     else:
          messages.warning(request, "Não tem nada no carrinho")
          return redirect("core:index")
     

def delete_item_from_cart(request):
     product_id = str(request.GET['id'])
     if 'cart_data_obj' in request.session:
          if product_id in request.session['cart_data_obj']:
               cart_data = request.session['cart_data_obj']
               del request.session['cart_data_obj'][product_id]
               request.session['cart_data_obj'] = cart_data
    
     cart_total_amount = 0
     if 'cart_data_obj' in request.session:

          for product_id, item in request.session['cart_data_obj'].items():
               cart_total_amount += int(item['qty']) * float(item['price'])

     context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount} )

     return JsonResponse({"data": context, 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})  


def update_cart(request):
     product_id = str(request.GET['id'])
     product_qty = request.GET['qty']

     if 'cart_data_obj' in request.session:
          if product_id in request.session['cart_data_obj']:
               cart_data = request.session['cart_data_obj']
               cart_data[str(request.GET['id'])]['qty'] = product_qty
               request.session['cart_data_obj'] = cart_data
    
     cart_total_amount = 0
     if 'cart_data_obj' in request.session:

          for product_id, item in request.session['cart_data_obj'].items():
               cart_total_amount += int(item['qty']) * float(item['price'])

     context = render_to_string("core/async/cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount} )

     return JsonResponse({"data": context, 'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})



def checkout_view(request):
         
     cart_total_amount = 0
     if 'cart_data_obj' in request.session:

          for product_id, item in request.session['cart_data_obj'].items():
               cart_total_amount += int(item['qty']) * float(item['price'])

          return render(request,"core/checkout.html", {"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})


def place_order(request):
         
     cart_total_amount = 0
     total_amount = 0
     if 'cart_data_obj' in request.session:
          
          order = CartOrder.objects.create(
               user = request.user,
               price=total_amount
          )

          for product_id, item in request.session['cart_data_obj'].items():
               cart_total_amount += int(item['qty']) * float(item['price'])

               items=CartOrderItems.objects.create(
                    order=order,
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=float(item['qty']) * float(item['price'])
               )

          JsonResponse({"cart_data":request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
          return redirect("core:index") 
     

def about_us_view(request):
     
     return render(request, 'core/about-us.html')
