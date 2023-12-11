from core.models import Product, Category, CartOrderItems, CartOrder, Wishlist,ProductImages, Address, ProductReview
from userauths.models import User

def default(request):
    categories = Category.objects.all()
    user = User.username
    
    return{
        'categories':categories,
         'user':user,
    }


