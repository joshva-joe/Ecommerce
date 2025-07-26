from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from adm.form import CustomUserForm
from .models import *
from django.http import JsonResponse

def landing(request):
    return render(request, 'landing.html')

def adminsignup(request):
    if request.method == 'POST':
        selected_role = request.POST.get('role')
        form = CustomUserForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            role_instance = Role.objects.filter(role=selected_role).first()
            user_role.objects.create(user_id=new_user, role_id=role_instance)

            if selected_role == 'customer':
                customers.objects.create(customer_name=new_user.username, email=new_user.email)

            if selected_role == 'seller':
                return redirect('/selleradd')

            return redirect('/adminlogin')

    return render(request, 'adminsignup.html')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)

            if authenticated_user.is_superuser:
                return redirect('/admin')

            user_role_entry = user_role.objects.filter(user_id=authenticated_user.id).first()
            if user_role_entry:
                role_id = user_role_entry.role_id.id

                if role_id == 3:
                    return redirect('/seller/profile/')
                elif role_id == 2:
                    return redirect('/customer')

        messages.error(request, "Invalid login credentials.")
        return redirect('/adminlogin')

    return render(request, 'adminlogin.html')

def selleradddata(request):
    if request.method == 'POST':
        seller_username = request.POST.get('seller_name')
        seller_email = request.POST.get('seller_email')
        seller_user = User.objects.filter(username=seller_username).first()

        if not seller_user:
            messages.error(request, "User not found. Please sign up first.")
            return redirect('/adminsignup')

        if selleradd.objects.filter(sellername=seller_user).exists():
            messages.warning(request, "Seller already exists.")
            return redirect('/selleradd')

        selleradd.objects.create(
            sellername=seller_user,
            email=seller_email,
            shopname=request.POST.get('shop_name'),
            phonenumber=request.POST.get('seller_phone'),
            location=request.POST.get('location'),
            profile=request.FILES.get('profile')
        )
        messages.success(request, "Seller profile created successfully.")
        return redirect('/adminlogin')

    return render(request, 'selleradd.html')

def seller_profile(request):
    current_user = request.user
    seller_profile_data = selleradd.objects.filter(sellername=current_user).first()
    seller_products = addproduct.objects.filter(sellername=current_user)

    return render(request, 'seller.html', {
        'seller': current_user,
        'seller_profile': seller_profile_data,
        'products': seller_products
    })

def productadd(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if addproduct.objects.filter(product_id=product_id).exists():
            messages.error(request, "Product ID already exists.")
            return redirect('/addproduct')

        addproduct.objects.create(
            sellername=request.user,
            product_name=request.POST.get('product_name'),
            product_id=product_id,
            category=request.POST.get('category'),
            price=request.POST.get('price'),
            stock=request.POST.get('stock'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        messages.success(request, "Product added successfully.")
        return redirect('/seller/profile/')

    return render(request, 'addproduct.html')

def edit_product(request, product_id):
    product = get_object_or_404(addproduct, product_id=product_id, sellername=request.user)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name', product.product_name)
        product.category = request.POST.get('category', product.category)
        product.price = request.POST.get('price', product.price)
        product.stock = request.POST.get('stock', product.stock)
        product.description = request.POST.get('description', product.description)

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect('/seller/profile/')

    return render(request, 'editproduct.html', {'product': product})

def delete_product(request, product_id):
    product_to_delete = get_object_or_404(addproduct, product_id=product_id, sellername=request.user)
    product_to_delete.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('/seller/profile/')

def customer(request):
    product_list = addproduct.objects.all()
    return render(request, 'customer.html', {'products': product_list})

def admin(request):
    return render(request, 'adminpage.html', {
        'product': addproduct.objects.count(),
        'customer': customers.objects.count(),
        'sellers': selleradd.objects.count(),
        'orders': orderlist.objects.count()
    })

def products(request):
    all_products = addproduct.objects.all()
    return render(request, "productshow.html", {'products': all_products})

def sellers(request):
    all_sellers = selleradd.objects.all()
    return render(request, "sellershow.html", {'sellers': all_sellers})

def customershow(request):
    all_customers = customers.objects.all()
    return render(request, "customershow.html", {'customers': all_customers})

def admindelete_product(request, product_id):
    product_to_delete = addproduct.objects.filter(product_id=product_id).first()
    if product_to_delete:
        product_to_delete.delete()
        messages.success(request, "Product deleted by admin.")
    return redirect('/products')

def admindelete_seller(request, sellername):
    if request.method == 'POST':
        seller = get_object_or_404(selleradd, sellername_id=sellername)
        seller.delete()
        messages.success(request, "Seller deleted successfully.")
        return redirect('/sellers')

def admindelete_customer(request, customer_name):
    if request.method == 'POST':
        customers.objects.filter(customer_name=customer_name).delete()
        User.objects.filter(username=customer_name).delete()
        messages.success(request, "Customer deleted successfully.")
        return redirect('/customers')

def admindelete_orders(request, product_id):
    if request.method == 'POST':
        orderlist.objects.filter(product_id=product_id).delete()
        messages.success(request, "Order deleted successfully.")
        return redirect('/orders')

def buyproduct(request, product_id):
    selected_product = get_object_or_404(addproduct, product_id=product_id)
    return render(request, 'buyproduct.html', {'product': selected_product})

def productorder(request, product_id):
    product = get_object_or_404(addproduct, product_id=product_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity.")
            return redirect('buy_product', product_id=product_id)

        if quantity > product.stock:
            messages.error(request, "Not enough stock available.")
            return redirect('buy_product', product_id=product_id)

        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_number = request.POST.get('customer_number')
        address = request.POST.get('address')

        # seller_profile = selleradd.objects.filter(sellername=product.sellername).first()
        # if not seller_profile:
        #     messages.error(request, "Order placed")
        #     return redirect('/buy_product', product_id=product_id)

        # orderlist.objects.create(
        #     product_name=product.product_name,
        #     product_id=product.product_id,
        #     sellername=product.sellername.username,
        #     shopname=seller_profile.shopname,
        #     customer_name=customer_name,
        #     customer_email=customer_email,
        #     customer_number=customer_number,
        #     delivery_address=address
        # )

        product.stock -= quantity
        product.save()

        messages.success(request, "Order Placed")
        return redirect('/customer?order=success')

    return redirect('buy_product', product_id=product_id)

def ordershow(request):
    order_list = orderlist.objects.all()
    return render(request, 'ordershow.html', {'orders': order_list})
