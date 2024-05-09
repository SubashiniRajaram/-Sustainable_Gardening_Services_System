import datetime
import os
from django.http import JsonResponse
from django.shortcuts import render,redirect
import pyrebase
from django.contrib import auth,messages
from django.views import View
from django.core.mail import send_mail
import logging
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Item
from .models import Fertilizer,tip
from django.conf import settings
import stripe
import requests
from.models import  PlantSpecies,disease,Plant
from embed_video.fields import EmbedVideoField




logger = logging.getLogger(__name__)



    
# Create your views here.
config = {
  'apiKey': "AIzaSyDXPedgFWJ-rZdUHg4whCVMMvbTAuyz3e0",
  'authDomain': "suba-31edf.firebaseapp.com",
  'databaseURL': "https://suba-31edf-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "suba-31edf",
  'storageBucket': "suba-31edf.appspot.com",
  'messagingSenderId': "204798333723",
  'appId': "1:204798333723:web:23a729ad8ec607f4f779be",
  'measurementId': "G-N74BDJ5QFH"
}

firebase = pyrebase.initialize_app(config)
database =firebase.database()
authe= firebase.auth()

session_id=None
username=None

# views.py

from django.shortcuts import render
# import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# def create_payment_intent(request):
#     amount = 1000 
#     try:
#         payment_intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency='usd',
#             payment_method=request.POST.get('payment_method_id'),
#             confirmation_method='manual',
#             confirm=True 
#         )
#         return JsonResponse({'client_secret': payment_intent.client_secret})
#     except stripe.error.StripeError as e:
#         return JsonResponse({'error': str(e)}, status=400)
    

def payment(request):
    overall_total=0
    cart_total=0
    updated_cart_data = database.child("cart_details").child(session_id).get().val()
    for product_id, product_info in  updated_cart_data.items():
      price = product_info['price']
      quantity = product_info['quantity']
      total=int(price)*int(quantity)
      product_info['total']=total
      overall_total=overall_total+total
    cart_total=overall_total
    overall_total=overall_total*100

    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        token = request.POST['stripeToken']
        amount = overall_total
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='inr',
                source=token,
                description='Test Payment'
            )
            return render(request, 'payment.html', {'charge': charge,'cart_data':updated_cart_data,'total':overall_total,'cart_total':cart_total,'success':"Payment Successful! 🌱 Your garden of delights is on the way. Happy planting!"})
        except stripe.error.CardError as e:
            return render(request, 'payment_failed.html', {'error': e})
    else:
        return render(request, 'payment.html', {'publishable_key': settings.STRIPE_PUBLIC_KEY,'cart_data':updated_cart_data,'total':overall_total,'cart_total':cart_total})

def home(request):
    return render(request,'index.html')

def signin(request):
    return render(request,'login1.html')

def signup(request):
    return render(request,'signup1.html')

# def postsignin(request):
#     email = request.POST.get('email')
#     password = request.POST.get('password')
    
#     try:
#         user = authe.sign_in_with_email_and_password(email, password)
#         return render(request, 'products.html')
#     except:
#         messages.error(request, 'Invalid credentials. Please try again.')
#         return render(request, 'login.html') 
    # except authe.AuthError as e:
    #             messages.error(request, f'Authentication error: {e}')

def postsignup(request):
     name = request.POST.get('name')
     email =request.POST.get('email-signup')
     password=request.POST.get('pass-signup')
    #  if len(password)<6:
    #       messages.error(request,"Password must be at least 6 characters long.")
    #       return redirect('signup')
    #  print(password)
     pnum = request.POST.get('pno')
     try:
      user=authe.create_user_with_email_and_password(email,password)
      uid = user['localId']
      data={"name":name,"email":email,"phoneNumber":pnum}
     
      database.child("user-credentials").child(uid).set(data)
      messages.success(request, 'registered successful!')
      return redirect('signin')
     except:
       messages.error(request, 'User email already exists')
       return render(request, 'signup1.html') 
     

def postsignin(request):
    global session_id
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        if email=="admin@gmail.com" :
          return render(request,'admin.html')
        user = authe.sign_in_with_email_and_password(email, password)
        # extract the localId from the user dictionary. 
        session_id = user['localId']
        username = database.child("user-credentials").child(session_id).get().val()['name']

        products =database.child('products').child('plants').child('indoor').shallow().get().val()

        list_products=[]
        for i in products:
            list_products.append(i)
       
        features=[]
        for i in list_products:
            data =database.child('products').child('plants').child('indoor').child(i).get().val()
            features.append(data)
       
        return render(request,'products.html',{'features':features,'username':username})
     
    except:
       messages.error(request, 'Invalid credentials. Please try again.')
       return render(request, 'login1.html') 

def shop(request):
        products =database.child('products').child('plants').child('indoor').shallow().get().val()
  
        list_products=[]
        for i in products:
            list_products.append(i)
       
        features=[]
        for i in list_products:
            data =database.child('products').child('plants').child('indoor').child(i).get().val()
            features.append(data)
        
        username = database.child("user-credentials").child(session_id).get().val()['name']

        return render(request,'products.html',{'features':features,'username':username})
     

 
def show(request,type=None,categorys=None):

    products =database.child('products').child(type).child(categorys).shallow().get().val()
    # print(type)

    features_detail=[]       
    list_products=[]
    for i in products:
            list_products.append(i)
        
    
    
    for i in list_products:
            data =database.child('products').child(type).child(categorys).child(i).get().val()
            features_detail.append(data)
            
    # type_Details.append(type)
    # type_Details.append(categorys)
    # print(type_Details)
    username = database.child("user-credentials").child(session_id).get().val()['name']

    return render(request,'products.html',{'features':features_detail,'username':username})


# def displayproduct(request,name=None,price=None,desc=None,index=None):
#     # index = int(index) 
#     print(index) 
    
#     index = int(index)
       
#     return render(request,'products_detail.html',{'pname':name,'pprice':price,'desc':desc})

# def get_pid_by_name(request):
#     product_name="Jade"
    # Find the product_id (pid) based on the product name
    # result = database.child("products").order_by_child("name").equal_to(product_name).get()
    # print("boooo")
    # for product_id, product_data in result.each():
    #     return product_id

    # If the product name is not found, return None
    # return None
# views.py
def displayproduct(request):
    name = request.GET.get('name', '')
    price = request.GET.get('price', '')
    desc = request.GET.get('desc', '')
    image = request.GET.get('image', '')
    username = database.child("user-credentials").child(session_id).get().val()['name']

    return render(request, 'products_detail.html', {'pname': name, 'pprice': price, 'desc': desc, 'image': image,'username':username})

def showcart(request):
    
    pname = request.GET.get('name')
    pprice = request.GET.get('price')
    quantity = request.GET.get('quantity')
    image=request.GET.get('image')
    # Check if the product is already in the cart
    cart_ref = database.child("cart_details").child(session_id)
    cart_data = cart_ref.get().val()

    # if cart_data:
    #     for key, product in cart_data.items():
    #         if product.get('product_name') == pname:
                # Update the quantity if the product is already in the cart
                # new_quantity = int(product['quantity']) + int(quantity)
                # database.child("cart_details").child(session_id).child(key).update({'quantity': str(new_quantity)})
                # break
    # else:
    cart=database.child("cart_details").child(session_id).push({'product_name': pname ,'price':pprice,'quantity':quantity,'image':image})
    print(cart)
    # Fetch the updated cart data
    overall_total=0
    updated_cart_data = database.child("cart_details").child(session_id).get().val()
    if updated_cart_data:
     for product_id, product_info in  updated_cart_data.items():
      price = product_info['price']
      quantity = product_info['quantity']
      total=int(price)*int(quantity)
      product_info['total']=total
      overall_total=overall_total+total
    #   priceList.append(total)
    username = database.child("user-credentials").child(session_id).get().val()['name']
     
    return render(request, 'shoping-cart.html', {'cart_data': updated_cart_data,'totalprice':overall_total,'username':username})

   

def showCart(request):
    cartdata = database.child("cart_details").child(session_id).get().val()
    overall_total=0
    if cartdata:
      for product_id, product_info in cartdata.items():
       price = product_info['price']
       quantity = product_info['quantity']
       total=int(price)*int(quantity)
       product_info['total']=total
       overall_total=overall_total+total
    #   priceList.append(total)
    #   print(cartdata.items()) 
    # print("hii")
    print(cartdata)
    username = database.child("user-credentials").child(session_id).get().val()['name']

    return render(request, 'shoping-cart.html', {'cart_data':cartdata,'totalprice':overall_total,'username':username})


def update_cart(request):
    if request.method == 'GET':
        print("update cart is called")
        
        product_name = request.GET.get('name', '')
        product_price = request.GET.get('price', '')
        quantity = request.GET.get('quantity', '')
        key = request.GET.get('key', '')

        try:
           
                quantity = int(quantity)

               
                print("i am executing")
                database.child("cart_details").child(session_id).child(key).update({'quantity': quantity})

                # Return a JSON response indicating success
                return JsonResponse({'status': 'success'})
            # else:
                # Return a JSON response indicating invalid parameters
                # return JsonResponse({'status': 'failure', 'message': 'Invalid parameters'})

        except Exception as e:
            # Handle exceptions (e.g., Firebase errors) and return a JSON response indicating failure
            return JsonResponse({'status': 'failure', 'message': str(e)})

    # Return a JSON response indicating failure if the request method is not GET
    return JsonResponse({'status': 'failure', 'message': 'Invalid request method'})

def remove_from_cart(request):
    if request.method == 'GET':
        key = request.GET.get('key', '')
        database.child("cart_details").child(session_id).child(key).remove()
        print("deleted")
      
    return redirect('cart') 


def T_service(request):
    username = database.child("user-credentials").child(session_id).get().val()['name']

    return render(request,'terrace-gardening.html',{'username':username})

def terrace_details(request):
    username = database.child("user-credentials").child(session_id).get().val()['name']

    return render(request,'terrace-details.html')

def terrace_form(request):
    email=request.POST.get('email')
    pno=request.POST.get('phone')
    address=request.POST.get('address')
    type=request.POST.get('GardeningType')
    area=request.POST.get('terraceSize')
    date=request.POST.get('datepicker')
    time=request.POST.get('timepicker')

    price=int(area)*100
    materials=price/2
    labor=price/4
    
    data={'email':email,'phone':pno,'address':address,'type':type,'area':area,'date':date,'time':time}
    # database.child("services").child("Terrace_Gardening").child(session_id).push(data)
    return render(request,"Service_confirmation.html",{'estimate':price,'data':data,'materials':materials,'labor':labor})

import smtplib




def terrace_save(request):
    email = request.POST.get('email')
    pno = request.POST.get('phone')
    address = request.POST.get('address')
    type = request.POST.get('type')
    area = request.POST.get('terrace_size')
    date=request.POST.get('datepicker')
    time=request.POST.get('timepicker')
    data = {'email': email, 'phone': pno, 'address': address, 'type': type, 'area': area,'summary':'Customer location details ,the place has good water facility and sunlight exposure,Customer preferences were discussed, emphasizing a mix of flowers, herbs, and vegetables ,Plans were made for efficient watering systems and proper drainage solutions.Suitable plant varieties were recommended based on terrace conditions and space availability,the estimated budget is Rs.50000',}
    database.child("services").child("Terrace_Gardening").child(session_id).push(data)
    data=database.child("services").child("Terrace_Gardening").child(session_id).get().val()
    keys = list(data.keys())

    key = keys[0]
    print(key)

    database.child("services").child("Terrace_Gardening").child(session_id).child(key).child("status").set({'Site Assessment': 'completed','Design and Planning': 'ongoing', 'Material Selection and Procurement':'upcoming','Installation':'upcoming'})

    try:
        subject = 'Service confirmation'
        message = f'Thank you for booking our service. Your booking is scheduled for {date} at {time}.Our team member,Roshini, will be visiting the site for a site visit. Here are the details:\n\nName: Roshini\n\nPhone: 9942552425.\n\n Happy Gardening'
        from_email = 'subavachu@gmail.com'
        recipient_list = [email]

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.content_subtype = "html"

        # Attach image
        image_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'gardener.jpg')
        with open(image_path, 'rb') as f:
            email.attach('image.jpg', f.read(), 'image/jpeg')

        email.send()
        email_sent = True
    except Exception as e:
        print(f"Error sending email: {e}")
        email_sent = False

    return render(request, "Service_confirmation.html",{'data': data,  'email_sent': email_sent})

def status(request):
         service=request.POST.get('service')
         user_id=request.POST.get('user_id')
         key=request.POST.get('service_id')
        
         print(service)
         if service == 'terrace_gardening':
          step1=request.POST.get('site')
          step2=request.POST.get('design')
          step3=request.POST.get('material')
          step4=request.POST.get('installation')
          database.child("services").child("Terrace_Gardening").child(user_id).child(key).child("status").set({'Site Assessment': step1,'Design and Planning': step2, 'Material Selection and Procurement':step3,'Installation':step4})

         elif service == 'maintenance':
          step1=request.POST.get('msite')
          step2=request.POST.get('plan')
          step3=request.POST.get('visit')
          database.child("services").child("Garden_Maintainence").child(user_id).child(key).child("status").set({'Site Assessment': step1,'Maintenance Planning': step2, 'Maintenance visit':step3})

         else:
          step1=request.POST.get('site')
          step2=request.POST.get('design')
          step3=request.POST.get('material')
          step4=request.POST.get('installation')
          database.child("services").child("Landscaping").child(user_id).child(key).child("status").set({'Site Assessment': step1,'Design and Planning': step2, 'Material Selection and Procurement':step3,'Installation':step4})

         return render(request,'admin.html')

def view_summary(request,service_type=None):
 summary= database.child("services").child(service_type).child(session_id).get().val()
 if summary != None:  
   for key,value in summary.items():
    if 'summary' in value:
        summary = value['summary']     
   status =  database.child("services").child(service_type).child(session_id).child(key).child("status").get().val()
   print(status)
   if service_type=="Terrace_Gardening" or service_type=="Landscaping":
    step1=status['Site Assessment']
    step2=status['Design and Planning']
    step3=status['Material Selection and Procurement']
    step4=status['Installation']
    return render(request,'summary.html',{'summary':summary,'service_name':service_type,'step1':step1,'step2':step2,'step3':step3,'step4':step4})
   elif service_type=="Garden_Maintainence":
    step1=status['Site Assessment']
    step2=status['Maintenance Planning']
    step3=status['Maintenance visit']
    return render(request,'summary.html',{'summary':summary,'service_name':service_type,'step1':step1,'step2':step2,'step3':step3})
 else:
   return render(request,'summary.html',{'summary':"site visit not yet done summary will be updated after your site Assessment ",'service_name':service_type})

def update_summary(request):
    service_type=request.POST.get('service')
    user_id=request.POST.get('user_id')
    key=request.POST.get('service_id')
    summarys=request.POST.get('summary')
    print(service_type)
    print(user_id)
    database.child("services").child(service_type).child(user_id).child(key).update({'summary':summarys})
    return render(request,'admin.html')

def maintainence(request):
    return render(request,'maintainence.html')

def maintainence_detail(request):
    return render(request,'maintainence_detail.html')

def maintainence_confirm(request):
    email = request.POST.get('email')
    pno = request.POST.get('phone')
    address = request.POST.get('address')
    desc=request.POST.get('desc')
    area=request.POST.get('terraceSize')
    date=request.POST.get('datepicker')
    time=request.POST.get('timepicker')
    frequency=request.POST.get('frequency')
    selected_services = request.POST.getlist('services[]')
    print(selected_services)
    price = len(selected_services) * 1000 * (int(area) / 100)
    data={'email':email,'phone':pno,'address':address,'desc':type,'area':area,'date':date,'time':time,'frequency':frequency}
    # database.child("services").child("Terrace_Gardening").child(session_id).push(data)
    return render(request,"maintainence_confirm.html",{'estimate':price,'data':data,'selected_service':selected_services})

def maintainence_save(request):
    email = request.POST.get('email')
    pno = request.POST.get('phone')
    address = request.POST.get('address')
    desc=request.POST.get('desc')
    area=request.POST.get('terraceSize')
    date=request.POST.get('datepicker')
    time=request.POST.get('timepicker')
    frequency=request.POST.get('frequency')
    selected_services = request.POST.getlist('selected_services')
    print(selected_services)
    data={'email':email,'phone':pno,'address':address,'desc':desc,'area':area,'date':date,'time':time,'frequency':frequency,'services':selected_services,'summary':'During the garden maintenance meeting, an in-depth evaluation of the garden\'s condition was conducted, pinpointing areas requiring attention such as overgrown foliage and weed proliferation. Following this assessment, a detailed maintenance strategy was devised, outlining specific tasks including lawn mowing, plant trimming, weed eradication, and mulching. The customer expressed satisfaction with the proposed plan, particularly commending its emphasis on sustainable gardening practices'}
    database.child("services").child("Garden_Maintainence").child(session_id).push(data)
    data=database.child("services").child("Garden_Maintainence").child(session_id).get().val()
    keys = list(data.keys())

    key = keys[0]
    print(key)

    database.child("services").child("Garden_Maintainence").child(session_id).child(key).child("status").set({'Site Assessment': 'completed','Maintenance Planning': 'ongoing', 'Maintenance visit':'upcoming'})

    try:
        subject = 'Service confirmation'
        message = f'Thank you for booking our service. Your booking is scheduled for {date} at {time}. \n\nOur team member,Roshini, will be visiting the site for a site visit. Here are the details:\n\nName: Roshini\n\nPhone: 9942552425.\n\n Happy Gardening'
        from_email = 'subavachu@gmail.com'
        recipient_list = [email]

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.content_subtype = "html"

        # Attach image
        image_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'gardener.jpg')
        with open(image_path, 'rb') as f:
            email.attach('image.jpg', f.read(), 'image/jpeg')

        email.send()
        email_sent = True
    except Exception as e:
        print(f"Error sending email: {e}")
        email_sent = False


    return render(request,'maintainence_confirm.html',{'data':data,'email_sent': email_sent})

def landscape(request):
    return render(request,'landscape.html')

def landscape_details(request):
    return render(request,'landscape_info.html')

def landscape_confirm(request):
    email = request.POST.get('email')
    pno = request.POST.get('phone')
    address = request.POST.get('address')
    desc=request.POST.get('desc')
    area=request.POST.get('terraceSize')
    date=request.POST.get('datepicker')
    time=request.POST.get('timepicker')
    selected_services = request.POST.get('service-type')
    print(selected_services)
    data={'email':email,'phone':pno,'address':address,'desc':desc,'area':area,'date':date,'time':time,'services':selected_services,'estimate':10000}

    return render(request,'landscape_confirm.html',{'data':data})


def landscape_save(request):
    email = request.POST.get('email')
    pno = request.POST.get('phone')
    address = request.POST.get('address')
    desc=request.POST.get('desc')
    area=request.POST.get('terraceSize')
    date=request.POST.get('datepicker')
    time=request.POST.get('timepicker')
    selected_services = request.POST.get('service-type')
    print(selected_services)
    data={'email':email,'phone':pno,'address':address,'desc':desc,'area':area,'date':date,'time':time,'services':selected_services,'estimate':10000,'summary':'During the site visit, the landscape team surveyed the outdoor area, noting its dimensions, existing vegetation, soil quality, and any unique features such as slopes or existing hardscapes. Discussions with the customer provided insight into their desired aesthetic, functional requirements, and preferences for specific plant species or landscape elements. Preliminary design ideas, including potential garden layouts, hardscape features, and plant selections, were presented and discussed. Additionally, the team provided initial estimates regarding project costs and outlined a tentative timeline for project completion, ensuring alignment with the customer\'s expectations and budget constraints'}
    database.child("services").child("Landscaping").child(session_id).push(data)
    data=database.child("services").child("Landscaping").child(session_id).get().val()
    keys = list(data.keys())

    key = keys[0]
    print(key)

    database.child("services").child("Landscaping").child(session_id).child(key).child("status").set({'Site Assessment': 'completed','Design and Planning': 'ongoing', 'Material Selection and Procurement':'upcoming','Installation':'upcoming'})

    try:
        subject = 'Service confirmation'
        message = f'Thank you for booking our service. Your booking is scheduled for {date} at {time}. \n\nOur team member,Roshini, will be visiting the site for a site visit. Here are the details:\n\nName: Roshini\n\nPhone: 9942552425.\n\n Happy Gardening'
        from_email = 'subavachu@gmail.com'
        recipient_list = [email]

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.content_subtype = "html"

        # Attach image
        image_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'gardener.jpg')
        with open(image_path, 'rb') as f:
            email.attach('image.jpg', f.read(), 'image/jpeg')

        email.send()
        email_sent = True
    except Exception as e:
        print(f"Error sending email: {e}")
        email_sent = False


    return render(request,'landscape_confirm.html',{'data':data,'email_sent': email_sent})



def blog(request):
   blog_data=database.child("post").get().val()
   return render(request,'blog.html',{'data':blog_data})

def post_detail(request,id):
      post_content=database.child("post").child(id).get().val()
      # print(post_content['title'])
      length=0
      comment_data=database.child("comments").child(id).get().val()
      if comment_data is not None:
         length = len(comment_data)
      data={'title':post_content['title'],'content':post_content['content'],'date':post_content['date'],'time':post_content['time'],'id':id,'image':post_content['image']}
      return render(request,'post_detail.html',{'content':data,'comment_data':comment_data,'count':length})

def add_post(request):
        url = request.POST.get('url')
        title = request.POST.get('title')
        content = request.POST.get('content')
        current_date = datetime.date.today().strftime('%d-%m-%Y')
        current_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        
        data = {'title': title, 'content': content, 'date': current_date, 'time': current_time,'image':url,'session_id':session_id}
        # Assuming `database` is some Firebase database object
        data = database.child('post').push(data)
        print(session_id)
        blog_data=database.child("post").get().val()
        return render(request,'blog.html',{'data':blog_data})

def add_comment(request,id):
   pid =request.POST.get('id')
   comment=request.POST.get('comment')
   database.child('comments').child(pid).push({'comment':comment})
   post_content=database.child("post").child(id).get().val()
      # print(post_content['title'])
   comment_data=database.child("comments").child(id).get().val()
   length=len(comment_data)
   data={'title':post_content['title'],'content':post_content['content'],'date':post_content['date'],'time':post_content['time'],'id':id,'image':post_content['image']}
   return render(request,'post_detail.html',{'content':data,'comment_data':comment_data,'count':length})

def mypost(request):
    try:
        posts = database.child("post").order_by_child("session_id").equal_to(session_id).get()
        
        # Extract the JSON data from the PyreResponse object
        posts_data = posts.val()
        
        # Ensure that posts_data is not None before returning
        if posts_data:
            print(posts_data)
            return render(request,'mypost.html',{'posts':posts_data})
        else:
            # Handle case where no posts are found for the session ID
            return HttpResponse("No posts available", status=404)
    except Exception as e:
        print("Error fetching posts:", e)
        return HttpResponse("Error fetching posts: " + str(e), status=500)

def edit_post(request,id):
      post_content=database.child("post").child(id).get().val()

      return render(request,'post_edit.html',{'content':post_content})

def save_edit(request,id):
      title=request.POST.get('title')
      content=request.POST.get('content')
      database.child('post').child(id).update({'title':title,'content':content})
      blog_data=database.child("post").get().val()
      return render(request,'blog.html',{'data':blog_data})

def delete(request,id):
    return render(request,'delete.html',{'id':id})
def delete_post(request,id):
       database.child('post').child(id).remove()
       view2_url = reverse('blog')  # Replace 'view2_name' with the name of the view2
       return redirect(view2_url)


def tutorial_category(request,type=None):
    data = Fertilizer.objects.filter(type=type)
    print(data)
    return render(request,'fertlizer_tutorial.html',{'obj':data})

def tips_category(request,type=None):
    data = tip.objects.filter(type=type)
    print(data)
    return render(request,'tips.html',{'obj':data})

def gardening_category(request,type=None):
    data = Item.objects.filter(type=type)
    print(data)
    return render(request,'video.html',{'obj':data})



def video(request):
    obj=Item.objects.all()
    return render(request,'video.html',{'obj':obj})

def fertilizer_making(request):
    obj=Fertilizer.objects.all()
    return render(request,'fertlizer_tutorial.html',{'obj':obj})

def tips(request):
    obj=tip.objects.all()
    return render(request,'tips.html',{'obj':obj})

def tutorial(request):
    return render(request,'tutorial.html')

def get_speciesdb(request):
    species_data = PlantSpecies.objects.all()[:5]

    return render(request, 'species_list.html', {'species_list': species_data})

def plant_moredetails(request,id=None):
            api_key = "sk-iXP665cf240720ea44202"
        

            api_endpoint = f"https://perenual.com/api/species/details/{id}?key={api_key}"

        # Send a GET request to the API endpoint
            response = requests.get(api_endpoint)
            if response.status_code == 200:
        # Convert the JSON response to a Python dictionary
              data = response.json()
              print(data)
            else:
              print(f"Error: Unable to fetch data from API for plant ID {id}" )
            # return HttpResponse("success")
            return render(request,'more.html',{'data':data})
 

def get_disease_db(request):

    disease_data = disease.objects.all()[:7]
    print(disease_data)

    return render(request, 'disease_list.html', {'disease_list': disease_data})

def info_hub(request):
    return render(request,'infohub.html')


def search_plant(request):
    api_key = "sk-iXP665cf240720ea44202"

    name=request.POST.get('search_species')
    print(name)
    url = f"https://perenual.com/api/species-list?key={api_key}&q={name}"
    response = requests.get(url)
    
    # Check if the API call was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data)
      
        # Pass the data to the template

        return render(request, 'search.html', {'species_list': data})
    else:
        # If the API call was not successful, return an error message
        return render(request, 'error.html', {'error_message': 'Error: Unable to fetch species list'})
    
def search_disease(request):
    api_key = "sk-iXP665cf240720ea44202"
    name=request.POST.get('search_disease')
    print(name)
    url = f" https://perenual.com/api/pest-disease-list?key={api_key}&q={name}"
    response = requests.get(url)
    
    # Check if the API call was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data)
        # paginator = Paginator(data['data'], 10)  # Show 10 items per page
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)
        # Pass the data to the template
        # return render(request, 's_d.html', {'page_obj': page_obj})

        return render(request, 'search_disease.html', {'disease_list': data})
    else:
        # If the API call was not successful, return an error message
        return render(request, 'error.html', {'error_message': 'Error: Unable to fetch species list'})

def search_guide(request):
    api_key = "sk-iXP665cf240720ea44202"
    name=request.POST.get('search_guide')
    print(name)
    url = f" https://perenual.com/api/species-care-guide-list?key={api_key}&q={name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        return render(request, 'search_guide.html', {'guide_list': data})
    else:
        return render(request, 'error.html', {'error_message': 'Error: Unable to fetch species list'})
    
def plants_guide(request):
     api_key = "sk-iXP665cf240720ea44202"
     guide_data = []
     try:
        page_number = 1
        while len(guide_data) < 4:
            url = f"https://perenual.com/api/species-care-guide-list?key={api_key}&page={page_number}"
            headers = {}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            page_guide_data = response.json().get('data', [])  # Access the list of disease from the JSON response
            guide_data.extend(page_guide_data)  # Append the disease data from the current page to the list
            page_number += 1

            # Break the loop if no more disease data is returned
            if not page_guide_data:
                break

        # Slice the list to ensure exactly 100 disease are returned
        guide_data =guide_data[:3]

        # Pass the disease list data to the template
        return render(request, 'guide.html', {'guide_list': guide_data})

     except requests.exceptions.RequestException as e:
        # Handle request exceptions
        return render(request, 'error.html', {'error_message': f'Failed to fetch disease list: {str(e)}'})
    
def results(request):
    matchs=[]
    str_to_boolean={'True':True,'False':False}
    sun=['Both']
    sugg_values_str = request.GET.getlist('sugg')
    print("Values passed in the URL:", sugg_values_str)
    
    sugg_values_str = ','.join(sugg_values_str)
    
    sugg_values = sugg_values_str.split(',')
    
    carelevel=sugg_values[0]
    sunlight=sugg_values[1]
    type=sugg_values[2]
    watering=sugg_values[3]
    flower=sugg_values[4]
    fruit=sugg_values[5]
    pet=sugg_values[6]
     
    indoor=str_to_boolean.get(type)
    flowering=str_to_boolean.get(flower)
    fruits=str_to_boolean.get(fruit)
    pets=str_to_boolean.get(pet)
    print(carelevel,watering,indoor,flowering,fruits,pets)
    sun.append(sunlight)
    print(pets)
    data = Plant.objects.filter(watering=watering,carelevel=carelevel,flowering=flowering,fruits=fruits,indoor=indoor,sunlight__in=sun)
 
    if pets==True :
     data=data.filter(pets=False)

    for value in data:
      print(value.id)
      matchs.append(value)
    return render(request,'results.html',{'data':matchs})
    
def quiz(request):
    return render(request,'quiz.html')

def suggestion_home(request):
    return render(request,'suggestion_home.html')

def update_plant_data(request):
    api_key = "sk-iXP665cf240720ea44202"

    # Loop through plant IDs from 1 to 10
    for plant_id in range(2405,2455,5):
        # Replace the placeholder in the API endpoint with the current plant ID
        api_endpoint = f"https://perenual.com/api/species/details/{plant_id}?key={api_key}"

        # Send a GET request to the API endpoint
        response = requests.get(api_endpoint)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Convert the JSON response to a Python dictionary
            api_response = response.json()

            # Get the plant instance from the database based on the ID
            plant_instance = Plant.objects.get(id=api_response['id'])

            # Update the image field with the new URL from the API response
            plant_instance.image = api_response['default_image']['original_url']

            # Save the updated plant instance to the database
            plant_instance.save()
        else:
            print(f"Error: Unable to fetch data from API for plant ID {plant_id}. Status code: {response.status_code}")

    return HttpResponse('success')

def spcalculator(request):
    return render(request,'plant_space.html')
def mcalculator(request):
    return render(request,'mulch.html')
def scalculator(request):
    return render(request,'calculator.html')
def space_details(request):
    return render(request,'space.html')

def sell(request):
    return render(request,'sell.html')

def addwaste(request):
    pno=request.POST.get('phone')
    address=request.POST.get('address')
    type=request.POST.get('type')
    quantity=request.POST.get('quantity')
    # price=request.POST.get('price')
    image=request.POST.get('url')
    username = database.child("user-credentials").child(session_id).get().val()['name']
    print(pno,address,type,quantity,image,username)
    data={'name':username,'contactnumber':pno,'address':address,'type':type,'quantity':quantity,'image':image}
    print(data)
    database.child("Garden_Waste").child(session_id).push(data)
    return render(request,'sell.html',{'message':"added successfully for donation"})

def buy(request):
    donate=database.child("Garden_Waste").get().val()
    print(donate)

    return render(request,'buy.html',{'data':donate})

def donation(request):
    mydonations=database.child("Garden_Waste").child(session_id).get().val()
    print(mydonations)
    return render(request,'mydonations.html',{'data':mydonations})

def updatedonation(request,key=None):
    quantity=request.POST.get('quantity')
    database.child("Garden_Waste").child(session_id).child(key).update({'quantity':quantity})
    print(quantity)
    return redirect(reverse('mydonations'))

def deletedonation(request):
    #  query parameter
    delete_id = request.GET.get('key')
    database.child("Garden_Waste").child(session_id).child( delete_id).remove()
    return redirect(reverse('mydonations'))

    
def cancel_booking(request,service_type=None):
   print("Service type:", service_type)
   print("Session ID:", session_id)

   if database.child("services").child(service_type).child(session_id).get().val() is not None:
    booking = database.child("services").child(service_type).child(session_id).remove()
    print("Booking:", booking)

    if booking is None:
        if service_type == 'Terrace_Gardening':
            return render(request, 'terrace-gardening.html', {'msg': "Booking cancelled successfully"})
        elif service_type == 'Landscaping':
            return render(request, 'landscape.html', {'msg': "Booking cancelled successfully"})
        else:
            return render(request, 'maintainence.html', {'msg': "Booking cancelled successfully"})
    else:
       if service_type == 'Terrace_Gardening':
            return render(request, 'terrace-gardening.html', {'msg': "No Booking Found"})
       elif service_type == 'Landscaping':
            return render(request, 'landscape.html', {'msg': "No Booking Found"})
       else:
            return render(request, 'maintainence.html', {'msg': "No Booking Found"})
   else:
       if service_type == 'Terrace_Gardening':
            return render(request, 'terrace-gardening.html', {'msg': "No Booking Found"})
       elif service_type == 'Landscaping':
            return render(request, 'landscape.html', {'msg': "No Booking Found"})
       else:
            return render(request, 'maintainence.html', {'msg': "No Booking Found"})
