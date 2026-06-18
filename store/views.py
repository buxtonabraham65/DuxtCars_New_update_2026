from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse,HttpResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder

from django.core.mail import send_mail
from .forms import *
from django.forms import modelformset_factory
from django.conf import settings

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()

    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category=category)

    context = {
        'products': products,
        'cartItems': cartItems
    }

    return render(request, 'store/store.html', context)

from django.shortcuts import render, redirect
from django.core.mail import send_mail

from django.http import JsonResponse

def submit_interest(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        product_id = request.POST.get('product_id')
        message = request.POST.get('message')
        price = request.POST.get('price')
        
        # Create email content
        subject = f"Interest in Car ID {product_id}"
        email_message = f"Name: {name}\nEmail: {email}\nPrice: {price}\nMessage: {message}"
        
        # Send email
        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['buxtoncars2'],  # Replace with your email
                fail_silently=False,
            )
            return JsonResponse({'message': 'Our team will contact you soon. Thank you!'}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'Failed to submit your interest.'}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)


def home(request):
	return render(request, 'store/home.html')


def rent(request):
    rents = Rent.objects.all()  # Fetch all rentals from the database
    context = {'rents': rents}
    return render(request, 'store/rent.html', context)


def car_maintenance(request):

    return render(request, 'store/car_maintenance.html')




#SELL
def submit_sell_interest(request):
    if request.method == 'POST':
        # Get form data
        car_model = request.POST.get('carModel')
        seller_name = request.POST.get('sellerName')
        seller_contact = request.POST.get('sellerContact')
        car_details = request.POST.get('carDetails')

        # Email content
        subject = f"New Sell Interest from Sell Page"
        email_message = f"""
        Name: {seller_name}
        Contact Info: {seller_contact}
        Car Model: {car_model}
        Car Details: {car_details}
        This form was submitted from the sell.html page.
        """
        
        # Send the email
        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],  # Your email address
            fail_silently=False,
        )

        # Redirect or render a success message
        return render(request, 'store/success.html', {'message': 'Our team will contact you soon. Thank you!'})
    else:
        return redirect('store')


def sell(request):
    # Your view logic here
    return render(request, 'store/sell.html')


def privacy(request):
	return render(request, 'store/privacy.html')

def termsandcondition(request):
	return render(request, 'store/termsandcondition.html')

def disclaimer(request):
	return render(request, 'store/disclaimer.html')

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

#Buy

# views.py
def submit_interest(request):
    if request.method == 'POST':
        # Get form data
        product_id = request.POST.get('product_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Email content
        subject = f"New Interest in Car ID {product_id} from Buy Page"
        email_message = f"""
        Name: {name}
        Email: {email}
        Car ID: {product_id}
        Message: {message}
        This form was submitted from the buy.html page.
        """
        
        # Send the email
        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],  # Your email address
            fail_silently=False,
        )
        
        # Redirect or render a success message
        return render(request, 'store/success.html', {'message': 'Our team will contact you soon. Thank you!'})
    else:
        return redirect('store')



#Rent forms
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

def submit_rent_interest(request):
    if request.method == 'POST':
        # Get form data
        rent_car_id = request.POST.get('rentCarId')
        renter_name = request.POST.get('renterName')
        renter_contact = request.POST.get('renterContact')
        rent_duration = request.POST.get('rentDuration')

        # Email content
        subject = f"New Rent Interest in Car ID {rent_car_id} from Rent Page"
        email_message = f"""
        Name: {renter_name}
        Contact Info: {renter_contact}
        Car ID: {rent_car_id}
        Duration of Rent (in days): {rent_duration}
        This form was submitted from the rent.html page.
        """
        
        # Send the email
        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],  # Your email address
            fail_silently=False,
        )

        # Redirect or render a success message
        return render(request, 'store/success.html', {'message': 'Our team will contact you soon. Thank you!'})
    else:
        return redirect('store')


# homepage forms views.py



def contact_form_submit(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Create email content
        subject = f"New Contact Form Submission from {name}"
        email_message = f"""
        You have received a new message from your website contact form.
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """
        
        # Send the email to your Gmail account
        try:
            send_mail(
                subject,
                email_message,
                'buxtoncars2',  # Your Gmail account
                ['buxtoncars2'],  # Recipient email(s)
                fail_silently=False,
            )
            return HttpResponse("Form submission successful!")
        except Exception as e:
            return HttpResponse(f"Failed to send email: {e}")

    return render(request, 'your_template.html')  # Update this to your form's template





def contact_form_submit(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        
        # Construct the message body
        email_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
        
        # Send the email
        send_mail(
            'New Contact Form Submission',  # Subject
            email_message,  # Message
            settings.DEFAULT_FROM_EMAIL,  # From email (set in settings.py)
            ['buxtoncars2@gmail.com'],  # To email (change to your Gmail)
        )
        
        return redirect('home')  # Replace 'success_page' with your success page URL name
    
    return render(request, 'contact.html')



def success_view(request):
    return render(request, 'success.html')


#Views for multiple images to be accessd when none clicks on the view button on buy.html
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()
    return render(request, 'store/product_detail.html', {'product': product, 'images': images})



#FOR RENT
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Rent

def rent_list(request):
    products = Rent.objects.all()
    return render(request, 'rent_list.html', {'rents': rents})

from django.shortcuts import render, get_object_or_404
from .models import Rent, RentImage

def rent_detail(request, rent_id):
    # Fetch the rent object
    rent = get_object_or_404(Rent, id=rent_id)

    # Fetch related images for the rent
    images = RentImage.objects.filter(rent=rent)  # Assuming RentImage has a ForeignKey to Rent

    return render(request, 'store/rent_detail.html', {'rent': rent, 'images': images})



#END


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Email content
        subject = 'New Signup for Exclusive Offers'
        message = f'Name: {name}\nEmail: {email}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['your-email@gmail.com']  # Replace with your email

        send_mail(subject, message, from_email, recipient_list)
        return redirect('success')  # Redirect to a success page
    return render(request, 'signup_form.html')


def add_to_wishlist(request):

    if request.method == 'POST':

        product_id = request.POST.get('product_id')

        product = Product.objects.get(id=product_id)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        return JsonResponse({
            'success': True,
            'created': created
        })

    return JsonResponse({
        'success': False
    })



	