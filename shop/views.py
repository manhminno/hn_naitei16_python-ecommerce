from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelform_factory
from django.shortcuts import redirect, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .utils.constant import LENGTH_PAGE, STATUS_ORDER, FILTER
from shop.models import Item, Order, Product,Category, Size, Comment
from shop.forms import SignUpForm, CommentForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.forms.models import model_to_dict
import re


def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()           
            my_message = _('Successful registration, you can log in now.')
            messages.success(request, my_message)
            
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(request, 'shop/signup.html', {'form': form})

@login_required
def detail_profile(request):
    UserEditForm = modelform_factory(
        get_user_model(), 
        fields=('first_name', 'last_name', 'username', 'phone', 'address'), 
        help_texts = {'username': None}
    )
    form = UserEditForm(instance=request.user)
    if request.method == "POST":
        form = UserEditForm(instance=request.user, data=request.POST or None)
        if form.is_valid():
            form.save()
    return render(request, 'shop/detail-profile.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            my_message = _('Your password was successfully updated. Please log in again!')
            messages.success(request, my_message)
            logout(request)

            return redirect('login')

    else:
        form = PasswordChangeForm(request.user)
    
    for field in form.fields.values():
        field.help_text = None
    
    return render(request, 'shop/change_password.html', {'form': form})

class ShopView(ListView):
    model = Product
    paginate_by = LENGTH_PAGE
    def get_context_data(self, **kwargs):
        query = ""
        product = Product.objects.all()
        if self.request.GET:
            query = self.request.GET.get('sorting', False) 
            if query == FILTER['price low to high']:
                product = product.order_by('price')
            elif query == FILTER['price high to low']:
                product = product.order_by('-price')
        if self.kwargs:
            category = Category.objects.filter(id=self.kwargs['pk']).first()
            product = product.filter(category=category)
        context = super().get_context_data(object_list=product,**kwargs)
        context['data'] = format_data(context['object_list'])
        if query:
            context['filter'] = query
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = []
        category = context['product'].category
        product = Product.objects.filter(category=category)
        context['related_products'] = format_data(product)
        for value in context['product'].image_set.all():
            url = value.url.split('.')
            id =  url[0]
            context['images'].append({'url': 'img/'+ value.url, 'id_img': id})
        context['comment'] = context['product'].comment_set.order_by('-create_at')
        context['all_comment'] = context['product'].comment_set.count()
        context['range'] = range(1, 6)

        return context


def product_search(request):
    query = request.GET.get('search_product', False)
    value_search = re.split("\s", query, flags=re.UNICODE)
    arr_search = []
    for value in value_search:
        if value:
            arr_search.append(value)
    str_search = " ".join(arr_search)
    query = str_search
    results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    page = request.GET.get('page')
    listData = format_data(results)
    if listData:
        paginator = Paginator(listData, LENGTH_PAGE)
        try:
            listData = paginator.page(page)
        except PageNotAnInteger:
            listData = paginator.page(1)
        except EmptyPage:
            listData = paginator.page(1)
    wishlist = None
    return render(
        request,
        'shop/product_list.html',
        {'data': listData, 'wishlist': wishlist , 'query':query}
    )


@login_required
def cart_detail(request):
    try:
        order = Order.objects.get(user = request.user, status = STATUS_ORDER['not_paid'])
        data = order.item_set.select_related('product')
        list_data = []
        total = 0 
        for value in data:
            url = 'img/'+value.product.image_set.first().url
            setattr(value, "url", url)
            setattr(value, "total", value.amount * value.product.price)
            list_data.append(value)
            total = total + value.amount * value.product.price
        return render(request,'shop/cart.html',{'data': list_data, 'total': total, 'user': request.user ,"message": ""})
    except ObjectDoesNotExist:
        message = _("You have not ordered any products yet")
        return render(request,'shop/cart.html',{'message': message})


@login_required
def add_to_cart(request,pk):
    obj, created = Order.objects.get_or_create(user = request.user, status = STATUS_ORDER['not_paid'])
    product = get_object_or_404(Product, id=pk)
    size = get_object_or_404(Size, description=request.POST['size'])
    item, itemCreated = Item.objects.update_or_create(order = obj, product = product, size = size)
    item.amount += int(request.POST['num-product'])
    item.save()
    obj.save()
    return redirect('shop:cart_detail')


@login_required
def remove_cart(request, pk):
    try:
        Item.objects.get(id = pk).delete()
        return redirect('shop:cart_detail')
    except ObjectDoesNotExist:
        message = _("Not found item with ID = {}".format(pk))
        messages.error(request, message)
        return redirect('shop:cart_detail')
    except:
        return redirect('shop:cart_detail')


@login_required
def update_cart(request, pk):
    try:
        item = Item.objects.get(id=pk)
        item.amount = request.POST['num-product']
        item.save()
        return redirect('shop:cart_detail')
    except ObjectDoesNotExist:
        message = _("Not found item with ID = {}".format(pk))
        messages.error(request, message)
        return redirect('shop:cart_detail',err = message)
    except:
        return redirect('shop:cart_detail')


def format_data(data):
    result = []
    for value in data:
        url = 'img/'+value.image_set.first().url
        result.append({'product': value, 'image': value.image_set.first(),'url': url})
    return result


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    listData = format_data(products)

    return render(request, "shop/user_wish_list.html", {"wishlist": listData})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    product.users_wishlist.add(request.user)
    
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def remove_from_wishlist(request, id):
    request.user.user_wishlist.remove(id)

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def add_payment(request):
    try:
        order = get_object_or_404(Order, user = request.user, status = STATUS_ORDER['not_paid'])
        order.create_at = timezone.now()
        order.phone = request.POST['phone']
        order.address = request.POST['address']
        order.status = STATUS_ORDER['waitting']
        order.save()
        return redirect('shop:payment_detail')
    except ObjectDoesNotExist:
        message = _("Not found order with ID = {}").format(pk)
        messages.error(request, message)
        return redirect('shop:payment_detail')


@login_required
def payment_detail(request):
    try:
        orders = Order.objects.filter(user = request.user, status = STATUS_ORDER['waitting'])
        list_order = format_data_order(orders)
        return render(request,'shop/payment.html',{'list_order': list_order, 'tilte_name': _('order waiting for pending'), 'message':"", "title": "WAITING_ORDER"})
    except ObjectDoesNotExist:
        message = _("you have no pending orders")
        return render(request,'shop/cart.html',{'message': message})


@login_required
def cancel_order(request,pk):
    try:
        order = Order.objects.get(id = pk)
        order.status = STATUS_ORDER['cancel']
        order.approve_at = timezone.now()
        order.save()
        return redirect('shop:cancel_order_detail')
    except ObjectDoesNotExist:
        message = _("Not found order with ID = {}").format(pk)
        messages.error(request, message)
        return redirect('shop:cancel_order_detail')
    except:
        return redirect('shop:cancel_order_detail')


@login_required
def cancel_order_detail(request):
    orders = Order.objects.filter(user = request.user, status = STATUS_ORDER['cancel'])
    if orders:
        list_order = format_data_order(orders)
        return render(request,'shop/payment.html',{'list_order': list_order, 'tilte_name': _('order has been canceled'), 'message':"", "title": "CANCELED_ORDER"})
    else:
        message = _("you have no canceled orders")
        return render(request,'shop/payment.html',{'tilte_name': _('order has been canceled'),'message': message})


@login_required
def history_order(request):
    orders = Order.objects.filter(user = request.user, status = STATUS_ORDER['paid'])
    if orders:
        list_order = format_data_order(orders)
        return render(request,'shop/payment.html',{'list_order': list_order, 'tilte_name': _('Purchased orders'), 'message':"", "title": "HISTORY_ORDER"})
    else:
        message = _("you have no Purchase orders")
        return render(request,'shop/payment.html',{'tilte_name': _('Purchased orders'),'message': message})


def format_data_order(orders):
    list_order = []
    for order in orders:
        data = order.item_set.select_related('product')
        list_data = []
        total = 0 
        for value in data:
            url = 'img/'+value.product.image_set.first().url
            setattr(value, "url", url)
            setattr(value, "total", value.amount * value.product.price)
            list_data.append(value)
            total = total + value.amount * value.product.price
        setattr(order, "data", list_data) 
        setattr(order, "total", total) 
        list_order.append(order)
    return list_order


@login_required
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER') 
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.content = form.cleaned_data['content']
            data.rate = form.cleaned_data['rate']
            data.product_id = id
            data.user = request.user
            data.save()
            data_return = model_to_dict(data)
            data_return['user'] = data.user.username
            
            return JsonResponse(data_return)

    return HttpResponseBadRequest({'error':"404"}, content_type='application/json')

@login_required
def deletecomment(request, id):
    cmt = get_object_or_404(Comment, id=id).delete()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])
