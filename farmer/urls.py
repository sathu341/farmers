from django.urls import path
from .import views
from .views import product_list, add_to_cart, cart_view, remove_from_cart, place_order, order_list, payment_view,shopregister,shoplogin,shophome,addproduct,product_byid,update_cart_quantity,payment_page,farmersaddProduct
from .views import farmesproduct_list,farmerproduct_byid,farmeradd_to_cart,report_detail,product_list_all,logout
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('registration', views.farmer_reg),
    path('logout', views.logout),
     path('home', views.homepage),
     path('prediction',views.prediction),
    path('videocap',views.videocap),
    path('shpreg',views.shpreg),
    path('main',views.main),
    path('shopregister',shopregister,name="shopregister"),
    path('shoplogin',shoplogin,name="shoplogin"),
    path('shophome',shophome,name="shophome"),
    path('addproduct',addproduct,name="addproduct"),
   # #display both cameras
   #  path('', views.index, name='index'),

    #access the laptop camera
    path('video_feed', views.video_feed, name='video_feed'),

    #access the phone camera
    path('webcam_feed', views.webcam_feed, name='webcam_feed'),
    path('upload',views.upload),
     path("cart/", cart_view, name="cart"),
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:cart_id>/", remove_from_cart, name="remove_from_cart"),
    path("order/place/", place_order, name="place_order"),
    path("orders/", order_list, name="order_list"),
    path("payment_view/", payment_view, name="payment_view"),
    path("product_list", product_list, name="product_list"),
    path('product_list_all',product_list_all,name="product_list_all"),
    path('product_byid/<int:prdid>/',product_byid,name="product_byid"),
    path('update-cart/<int:item_id>/<str:action>/', update_cart_quantity, name='update_cart_quantity'),
     path('payments/', payment_page, name='payment_page'),
     path("farmersaddproduct",farmersaddProduct,name="farmersaddProduct"),
     path("farmersproductlist",farmesproduct_list,name="farmesproductlist"),
     path("farmerproduct_byid/<int:prdid>",farmerproduct_byid,name="farmerproduct_byid"),
     path("farmeradd_to_cart/<int:product_id>/",farmeradd_to_cart,name="farmeradd_to_cart"),
     path("report_detail",report_detail,name="report_detail"),
     path('logout',logout,name='logout')
   
]