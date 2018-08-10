from django.shortcuts import render,HttpResponse,redirect
from app01 import models
import uuid

from utils.pay import AliPay


def index(request):
    """
    购买页面
    :param request:
    :return:
    """
    goods = models.Goods.objects.all()
    return render(request, 'index.html', locals())


def buy(request,pk):
    #  0. 判读要购买的商品是否存在
    good_obj = models.Goods.objects.get(id=pk)
    if not good_obj:
        return HttpResponse('商品不存在')
    #  1. 创建订单
    no = str(uuid.uuid4())
    orders_obj = models.Orders.objects.create(no=no,good=good_obj)
    print("order",orders_obj)
    #  2. 根据支付宝SDK生成跳转链接
    alipay = AliPay(
        # 配置APPID
        appid="2016091800538549",
        app_notify_url="http://118.25.231.23:8899/check_order/",  # POST,发送支付状态信息
        return_url="http://118.25.231.23:8899/index/",  # GET,将用户浏览器地址重定向回原网站
        # 配置私钥
        app_private_key_path="keys/key_private.txt",
        # 配置公钥
        alipay_public_key_path="keys/key_public.txt",
        debug=True,  # 默认True测试环境、False正式环境
    )

    query_params = alipay.direct_pay(

        subject=good_obj.title,  # 商品简单描述
        out_trade_no=no,  # 商户订单号
        total_amount=good_obj.price,  # 交易金额(单位: 元 保留俩位小数)
    )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)

    return redirect(pay_url)


def check_order(request):
    if request.method == "POST":
        alipay = AliPay(
            # 配置APPID
            appid="2016091800538549",
            app_notify_url="http://118.25.231.23:8899/check_order/",  # POST,发送支付状态信息
            return_url="http://118.25.231.23:8899/index/",  # GET,将用户浏览器地址重定向回原网站
            # 配置私钥
            app_private_key_path="keys/key_private.txt",
            # 配置公钥
            alipay_public_key_path="keys/key_public.txt",
            debug=True,  # 默认True测试环境、False正式环境
        )
        from urllib.parse import parse_qs
        # 获取POST请求体中的数据
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        # 判断订单是否支付成功
        if status:
            # 支付成功，获取订单号将订单状态更新
            # 获取订单编号
            out_trade_no = post_dict['out_trade_no']
            models.Orders.objects.filter(no=out_trade_no).update(status=1)
            # 固定的返回格式
            return HttpResponse('success')
        else:
            return HttpResponse('支持失败')
    else:
        return HttpResponse("仅支持POST请求")
    pass

