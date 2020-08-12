from cart.cart import Cart
from django.urls import reverse
from mshop import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from registration.forms import User
from shop.forms import OrderForm
from shop.models import Product, Category, Order, OrderItem
from paypal.standard.forms import PayPalPaymentsForm


def index(request, cat_id=0):
    all_categories = Category.objects.all()
    all_products = None
    if cat_id is not '':
        if int(cat_id) > 0:
            print(cat_id)
            try:
                category = Category.objects.get(id=cat_id)
            except:
                category = None

            if category is not None:
                all_products = Product.objects.filter(category=category)
    if all_products is None:
        all_products = Product.objects.all().order_by('sku')

    paginator = Paginator(all_products, 4)
    pages = paginator.page_range
    p = request.GET.get('p')
    try:
        products = paginator.page(p)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'index.html', locals())


def product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        product = None
    return render(request, 'product.html', locals())


@login_required
def cart(request):
    all_categories = Category.objects.all()
    cart = Cart(request)
    return render(request, 'cart.html', locals())


def add_to_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product, product.price, quantity)
    return redirect('/')


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('/cart/')


def order(request):
    all_categories = Category.objects.all()
    cart = Cart(request)
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        new_order = Order(user=user)
        form = OrderForm(request.POST, instance=new_order)
        if form.is_valid():
            order = form.save()
            email_messaages = "你的购物内容如下:\n"
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item.product,
                                         price=item.product.price,
                                         quantity=item.quantity)
                email_messaages += "\n" + "商品: {}, {}元, {}件".format(item.product, item.product.price, item.quantity)
            email_messaages += "\n以上共计{}元\nhttp://fanggaoshang.cn感谢你的订购!".format(cart.summary())
            cart.clear()
            messages.add_message(request, messages.INFO, '订单已保存,我们会尽快处理')
            send_mail("感谢你的订购",
                      email_messaages,
                      "迷你小电商<fangyingdon@163.com>",
                      [request.user.email], )
            send_mail("有人订购了产品",
                      email_messaages,
                      "迷你小电商<fangyingdon@163.com>",
                      ['fangyingdon@163.com'], )
            return redirect('/myorders/')
    else:
        form = OrderForm()

    return render(request, 'order.html', locals())


@login_required()
def my_orders(request):
    all_categories = Category.objects.all()
    orders = Order.objects.filter(user=request.user)
    return render(request, "myorders.html", locals())


@csrf_exempt
def payment(request, order_id):
    all_categories = Category.objects.all()
    try:
        order = Order.objects.get(id=order_id)
    except:
        messages.add_message(request, messages.WARNING, '订单编号错误, 无法处理付款')
        return redirect('/myorders/')
    all_order_items = OrderItem.objects.filter(order=order)
    items = list()
    total = 0
    for order_item in all_order_items:
        t = dict()
        t['name'] = order_item.product.name
        t['price'] = order_item.product.price
        t['quantity'] = order_item.quantity
        t['subtotal'] = order_item.product.price * order_item.quantity
        total += order_item.product.price
        items.append(t)
        host = request.get_host()
        paypal_dict = {
            "business": settings.PAYPAL_REVEIVER_EMAIL,
            "amount": total,
            "item_name": "迷你小电商货品编号:{}".format(order_id),
            "invoice": "invoice-{}".format(order_id),
            "currency_code": "USD",
            "notify_url": "http://{}{}".format(host, reverse('paypal-ipn')),
            "return_url": "http://{}/done/".format(host),
            "cancel_return": "http://{}/canceled/".format(host),
        }

    # print(items)
    # for i in items:
    #     print(i.name)

    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment.html', locals())


@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html', locals())


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_canceled.html', locals())


# def pay(request):
#     # 此时alipay 对象的创建放在了 settings 中
#     subject = "身高168, 体重100斤, 肤色皙白, 活好"
#     from mshop.settings import alipay
#     order_string = alipay.api_alipay_trade_wap_pay(
#         out_trade_no="20161112",
#         total_amount=0.01,
#         subject=subject,
#         return_url="https://example.com",
#         notify_url="https://example.com/notify"  # 可选, 不填则使用默认notify url
#     )
#     # 这里alipay的网关可能会有变动
#     return redirect('https://openapi.alipaydev.com/gateway.do?' + order_string)
