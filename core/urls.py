from django.urls import path
from core.views import about_us_view, place_order, checkout_view, update_cart, delete_item_from_cart, cart_view, add_to_cart, add_review, index, product_list_view, product_detail_view, category_list_view,category_product_list_view

app_name = "core"

urlpatterns = [

    # Homepage
    path("", index, name="index"),
    path("products/", product_list_view, name="product_list"),
    path("products/<pid>/", product_detail_view, name="product_detail"),
    path("about-us/", about_us_view, name="about_us"),

    # Category
    path("category/", category_list_view, name="category_list"),
    path("category/<cid>/", category_product_list_view, name="category_product_list"),

    #add review
    path("add-review/<pid>", add_review, name="add-review"),
    #add to cart
    path("add-to-cart", add_to_cart, name="add-to-cart"),
    
    #cartview
    path("cart/", cart_view, name="cart"),

    #detele item from cart
    path("delete-from-cart", delete_item_from_cart, name="delete-from-cart"),

    #update cart
    path("update-cart", update_cart, name="update-cart"),

    #checkout cart
    path("checkout/", checkout_view, name="checkout"),

    #place order
    path("place-order", place_order, name="place_order"),
]
