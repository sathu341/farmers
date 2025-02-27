from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import uuid 
import numpy as np
from . models import Farm_table,Prediction,shop,Shopproduct,Cart,NewCart,Payment,Delivery
from django.contrib.sessions.models import Session
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import  tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models 
from keras.preprocessing import  image
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
# import streamlit as st
from PIL import Image
import numpy as np
import tensorflow.keras as keras
import matplotlib.pyplot as plt
import tensorflow_hub as hub

import cv2
import random
import os
from  PIL import Image,ImageTk



# Create your views here.
def index(request):
    products = Shopproduct.objects.all()
    return render(request,'index.html',{'products':products})
def homepage(request):
    return render(request,'home.html')
def videocap(request):
    return render(request, 'camera.html')
def upload(request):
    
    return render(request,'home.html')

def farmer_reg(request):
    if request.method=="POST":
        nam=request.POST.get("name")
        eml=request.POST.get("email")
        cnum=request.POST.get("contact_number")
        pword=request.POST.get("password")
        anum=request.POST.get("adnum")
        obj=Farm_table.objects.create(nam=nam,eml=eml,cnum=cnum,password=pword,anum=anum)
        obj.save()
        return HttpResponse("<h4> Successfully registered</h4> <a href='/login'>Login </a>")
    return render(request,'registration.html')
def farmv(request):
    obj=Farm_table.objects.all()
    return render(request,'framv.html',{'data':obj})

def home(request):
    user=request.session['dusername']
    passw=request.session['dpassword']
    try:
        obj=Farm_table.objects.filter(eml=user,password=passw)#select * from tbl  where username
    except Exception as e:
        print(e)    
           
    return render(request,'home.html')      

def login(request):
    if request.method=="POST":
        user=request.POST.get('eml')
        passw=request.POST.get('passw')
        obj=Farm_table.objects.filter(eml=user,password=passw)#select * from tbl  where username
        
        if obj:
            for l in obj:
                idn=l.id
            request.session['email']=user
            request.session['dpassword']=passw
            request.session['didno']=idn
            return render(request,'home.html')  
        else:
            return render(request,'registration.html',{'msg':"invalid username and password"})  


    return render(request,'registration.html')      
def logout(request):
    request.session['email']=""
    request.session['dpassword']=""
    request.session['didno']=""
    return HttpResponse("Logout to login again <a href='/login'>Login page </a>")    

def prediction(request):
    CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]
    
    # img_batch = np.expand_dims(image, 0)
    
    # predictions = MODEL.predict(img_batch)

    # predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    # confidence = np.max(predictions[0])
    # return {
    #     'class': predicted_class,
    #     'confidence': float(confidence)
    # }
    if request.method=="POST":
        filename=request.FILES.get('pic')
        prdtbl=Prediction.objects.create(frmid=1,prd="not pred",pic=filename)
        if prdtbl:
            prdtbl.save()
            obj=Prediction.objects.filter(pic=filename)
            for  p in obj:
                lc=p.pic
        print(filename)
        name= filename
        image=Image.open(name) 
        image = image.resize((299,299))
        image = np.array(image)
            # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3]
        image = np.expand_dims(image, axis=0)
        image = image/127.5
        image = image - 1.0
        # print(name.index("."))
        # print(name[name.index("."):len(name)])

        model=load_model("D:\potato_farm\potatoes.h5")
        # test_image=image.load_img('D:\potato_farm/testimage/'+str(filename),target_size=(150,150))
        # text_image=image.load_img(str(lc),target_size=(150,150))
        # if text_image.shape[2] == 4: 
        #         text_image = text_image[..., :3]
        
        # test_image=image.img_to_array(test_image)/225
        # test_image=np.expand_dims(test_image,axis=0)
        result=model.predict(image).round(3)
        pred=np.argmax(result)
        print(pred)

        if pred==0:
            # var1.set("Disease:Bacterial leaf")
            msg="Disease:"+CLASS_NAMES[0]    
            
            return render(request,'userpage.html',{'result':msg})

            print("Disease:Bacterial leaf")
        elif pred==1:
            # var1.set("Disease:Brown spot")
            msg="Disease: "+CLASS_NAMES[1]
         
            return render(request,'home.html',{'result':msg})

            print("Disease:",CLASS_NAMES[1])  
        elif pred==3:
            
            print("Disease:",CLASS_NAMES[3]) 
            msg="Disease:"+CLASS_NAMES[3]
           
            return render(request,'home.html',{'result':msg})
        else:
            msg="Input Correct Image"
            
            return render(request,'home.html',{'result':msg})



        print("tensorflow working")
    return render(request,'home.html',{'result':msg})

    

# Create your views here.
#Display the 2 videos
def videocap(request):
    return render(request, 'camera.html')


#Every time you call the phone and laptop camera method gets frame
#More info found in camera.py
def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: capture/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#Method for laptop camera
def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
                    #video type
					content_type='multipart/x-mixed-replace; boundary=frame')

#Method for phone camera
def webcam_feed(request):
	return StreamingHttpResponse(gen(IPWebCam()),
                    #video type
					content_type='multipart/x-mixed-replace; boundary=frame')
 #********************************Shop**************************************************************
def shpreg(req):
    if req.method=="POST":
        
     return render(req,'shopbase.html')
def signIn(req):
    return render(req,'') 

def main(request) :
    
    if request.method=="POST":
        file_uploaded=request.FILES.get('pic')
        if file_uploaded is not None :
            image = Image.open(file_uploaded)
            # text_image=image.load_img(image,target_size=(150,150))
            # test_image=image.img_to_array(test_image)/225
            # test_image=np.expand_dims(test_image,axis=0)
       
        # image = cv2.resize(image, (256,256,3))
        # img_batch = np.expand_dims(image, 0) 
            # image = image.resize((299,299))
            # image = np.array(image)
            # for images that has 4 channels, we convert them into 3 channels
            # if image.shape[2] == 4: 
            #     image = image[..., :3]
            # image = np.expand_dims(image, axis=0)
            # image = image/127.5
            # image = image - 1.0
            
        prdtbl=Prediction.objects.create(frmid=1,prd="not pred",pic=file_uploaded)
        if prdtbl:
                prdtbl.save()
                obj=Prediction.objects.filter(pic=file_uploaded)
                for  p in obj:
                    lc=p.pic
            
        
        result, confidence = predict_class(image)
        result2="Disease May Be:"+result
        if result=="Potato__Early_blight":
            df="The spores and mycelia of the pathogen survive in infested plant debris and soil, in infected tubers and in overwintering host crops and weeds. Spores are produced when temperatures are between 41-86 F. (5-30 C.) with alternating periods of wetness and dryness. These spores are then spread through wind, splashing rain, and irrigation water. They gain entry via wounds caused by mechanical injury or insect feeding. Lesions begin to appear 2-3 days after the initial infection. Treatment of early blight includes prevention by planting potato varieties that are resistant to the disease; late maturing are more resistant than early maturing varieties. Avoid overhead irrigation and allow for sufficient aeration between plants to allow the foliage to dry as quickly as possible. Practice a 2-year crop rotation. That is, do not replant potatoes or other crops in this family for 2 years after a potato crop has been harvested. Keep the potato plants healthy and stress free by providing adequate nutrition and sufficient irrigation, especially later in the growing season after flowering when plants are most susceptible to the disease. Only dig the tubers up when they are completely mature to prevent from damaging them. Any damage done at harvest can additionally facilitate the disease. Remove plant debris and weed hosts at the end of the season to mitigate areas where the disease may overwinter.Read more at Gardening Know How: Potato Early Blight Treatment – Managing Potatoes With Early Blight"
        if result=="Potato__Late_blight":
            df="Late blight is controlled by eliminating cull piles and volunteer potatoes, using proper harvesting and storage practices, and applying fungicides when necessary. Air drainage to facilitate the drying of foliage each day is important."    
        if result=="Potato__healthy":
            df=" "    


        return render(request,'home.html',{'result':result2,'confidence':confidence,'ps':df})

def predict_class(image) :
   
    classifier_model = keras.models.load_model(r'final_model.h5', compile = False)

    shape = ((256,256,3))
    model = keras.Sequential([hub.KerasLayer(classifier_model, input_shape = shape)])     # ye bhi kaam kar raha he
    # test_image = image.resize((256, 256))
    
    # if text_image.shape[2]==4:
    #     text_image=text_image[...,:3]
    # test_image = keras.preprocessing.image.img_to_array(test_image)
    # test_image /= 255.0
    # test_image = np.expand_dims(test_image, axis = 0)
    image = image.resize((256,256))
    image = np.array(image)
            # for images that has 4 channels, we convert them into 3 channels
    if image.shape[2] == 4: 
            image = image[..., :3]
    image = np.expand_dims(image, axis=0)
    image = image/127.5
    image = image - 1.0
    class_name = ['Potato__Early_blight', 'Potato__Late_blight', 'Potato__healthy']

    prediction = model.predict(image)
    confidence = round(100 * (np.max(prediction[0])), 2)
    final_pred = class_name[np.argmax(prediction)]
    return final_pred, confidence
from .models import Product, Cart, Order, Delivery
from django.contrib import messages
from django.utils import timezone
#farmersProduct
def farmersaddProduct(request):
    if request.method == "POST":
        pname = request.POST.get("pname")
        cat = request.POST.get("cat")
        price=request.POST.get("price")
        qty = request.POST.get("qty")
        image=request.FILES.get('image')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        image4=request.FILES.get('image4')
        stock=request.POST.get('stock')
        description=request.POST.get('description')
        farmers=get_object_or_404(Farm_table,id=request.session.get('didno'))
        Product.objects.create(
            name=pname,
            cat=cat, 
            qty=qty,
            stock=stock,
            price=price,
            description=description,
            image=image,
            image2=image2,
            image3=image3,
            image4=image4,
            farmer=farmers,
        )
        return redirect("farmersaddProduct") 
    return render(request,'farmers/addproducts.html')
def farmesproduct_list(request):
    products =Product.objects.all()
    return render(request, "farmers/productlist.html", {"products": products})
def farmerproduct_byid(req,prdid):
    products=get_object_or_404(Product,id=prdid)
    return render(req,'farmers/product_details.html',{'products':products})
#addproduct 
def addproduct(request):
    if request.method == "POST":
        pname = request.POST.get("pname")
        cat = request.POST.get("cat")
        brand = request.POST.get("brand")
        price = request.POST.get("price")
        qty = request.POST.get("qty")
        image=request.FILES.get('image')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        image4=request.FILES.get('image4')
        stock=request.POST.get('stock')
        description=request.POST.get('description')
        shops=get_object_or_404(shop,id=request.session.get('shopid'))
        Shopproduct.objects.create(
            pname=pname,
            cat=cat,
            brand=brand,
            price=price,
            qty=qty,
            stock=stock,
            description=description,
            image=image,
            image2=image2,
            image3=image3,
            image4=image4,
            shop=shops
        )
        return redirect("addproduct") 
    return render(request,'shop/addproduct.html')

# shop register 
def shopregister(req):
    if req.method=="POST":
        shopname=req.POST.get('shopname')
        email=req.POST.get('email')
        password=req.POST.get('password')
        location=req.POST.get('location')
        contact=req.POST.get('contact')
        check=shop.objects.filter(email=email).first()
        if check:
             return render(req,'shop/shopregister.html',{'msg':'email already existing'})
        
        result=shop.objects.create(
            shname=shopname,email=email,passw=password,location=location,contact=contact
        )
        if result:
            return render(req,'shop/login.html',{'msg':'register success login here'})
        else:
            return render(req,'shop/shopregister.html',{'msg':'register wend wrong'})
    return render(req,'shop/shopregister.html',{'msg':''})
#shop login  
def shoplogin(req):
    if req.method=="POST":
        email=req.POST.get('email')
        password=req.POST.get('password')
        result=shop.objects.filter(email=email,passw=password).first()
        if result:
            req.session['shopid']=result.id
            
            return redirect('shophome')
    return render(req,'shop/login.html',{'msg':''})
#shoppage 
def shophome(req):
    shop=req.session.get('shop')
    return render(req,'shopbase.html',{'shop':shop})

# Show all products
def product_list(request):
    products = Shopproduct.objects.all()
    return render(request, "shop/product_list.html", {"products": products})
def product_byid(req,prdid):
    products=get_object_or_404(Shopproduct,id=prdid)
    return render(req,'shop/product_details.html',{'products':products})
# Add product to cart
def add_to_cart(request, product_id):
    print("Product ID:", product_id)
    
    # Debug session value
    didno = request.session.get('didno')
    if not didno:
        return HttpResponse("User session ID missing", status=400)

    print("Session ID (didno):", didno)
    
    products = get_object_or_404(Shopproduct, id=product_id)

    # Ensure the user exists
    try:
        users = Farm_table.objects.get(id=didno)
        print("user",users.id)
        print(users.nam)
    except Farm_table.DoesNotExist:
        return HttpResponse("User does not exist", status=400)

    # Create cart entry
    NewCart.objects.create(
        user=users,product=products
    )
   
    return redirect("cart")
        

    
    

# View cart

def cart_view(request):
    user=get_object_or_404(Farm_table,id=request.session.get('didno'))
    cart_items = NewCart.objects.filter(user=user)
    total_price=sum(float(item.total_price()) for item in cart_items)
    print(total_price)
    return render(request, "shop/cart.html", {"cart_items": cart_items, "total_price": total_price})

# Remove from cart

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(NewCart, id=cart_id)
    cart_item.delete()
    messages.success(request, "Removed from cart.")
    return redirect("cart")

# Place Order

def place_order(request):
    users = get_object_or_404(Farm_table, id=request.session.get('didno'))  # Ensure Farm_table user exists

    cart_items = NewCart.objects.filter(user=users)
    
    if not cart_items.exists():  # Check if cart is empty
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")

    total_amount = sum(float(item.total_price()) for item in cart_items)  # Calculate total price
    
    # Create order
    order = Order.objects.create(user=users, total_amount=total_amount)

    # Set cart items to the order correctly
    order.cart_items.add(*cart_items)  # Pass QuerySet directly, not .first()
    
    # Clear cart after order placement
    cart_items.delete()

    messages.success(request, "Order placed successfully!")
    return redirect("order_list")

def update_cart_quantity(request, item_id, action):
    cart_item = get_object_or_404(NewCart, id=item_id)

    if action == "increase":
        qty=int(cart_item.quantity)+1

    elif action == "decrease" and cart_item.quantity > 1:
       
       qty=int(cart_item.quantity)-1
    

    print("quantity",qty)
    cart_item.quantity=qty

    
    cart_item.save()
    print(cart_item.total_price())
    return JsonResponse({"success": True, "new_quantity": cart_item.quantity, "total_price": cart_item.total_price()})
# View all orders

def order_list(request):
    users = get_object_or_404(Farm_table, id=request.session.get('didno'))
    orders = Order.objects.select_related('user').filter(user=users)
    return render(request, "shop/orders.html", {"orders": orders})
from datetime import datetime, timedelta
# Payment Processing (Dummy)
def payment_page(request):
    current_date = datetime.today()

# Add 7 days
    future_date = current_date + timedelta(days=7)
    print("payment")
    user =get_object_or_404(Farm_table,id=request.session.get('didno'))

    # Get the latest order for the user (assuming one order at a time)
    order = Order.objects.filter(user=user, status="Pending").last()

    if not order:
        messages.warning(request, "No pending orders found.")
        return redirect("cart")

    if request.method == "POST":
        payment_method ="card"

        # Generate a fake transaction ID
        transaction_id = str(uuid.uuid4())

        # Create a payment record
        payment = Payment.objects.create(
            order=order,
            user=user,
            amount=order.total_amount,
            method=payment_method,
            transaction_id=transaction_id,
            status="Success",  # Assuming success for simplicity
        )

        # Update order status
        order.status = "Completed"
        order.save()
        delivery=Delivery.objects.create(
            order=order,
            delivery_address=request.POST.get("address"),
            estimated_time =future_date + "10:00"

        )   
        delivery.save()
        messages.success(request, "Payment successful!")
        return redirect("order_list")

    return render(request, "shop/payment.html", {"order": order})

def payment_view(request):
    messages.success(request, "Payment successful! Your order is being processed.")
    return redirect("order_list")