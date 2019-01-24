from django.shortcuts import render, redirect, HttpResponse

from makeiteasy.apps.alipay import AliPay
import json
import time


def get_ali_object():
    """
    沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info

    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2(),接收不到这个请求

    # 验签作用：
    实际上是可以接收到支付成功的请求的，支付宝传递请求成功的响应信息是通过浏览器重定向url中携带的支付成功的参数,传递给后端服务器支付成功的消息
    是不是不安全？如果认为修改重定向的url岂不是可以伪造修改支付成功参数？
    解决办法一：
        这就意味着，后端服务器，在验证是否支付成功，或标记支付状态时的时候必须通过服务器直接与支付宝进行查询， 而不是通过这次响应来判断
        所以，def page2(): 应该增添直接到支付宝服务器
        业务逻辑放在前端来处理的都要小心：如支付状态，修改订单状态
    解决办法二：
        这时候，通过数字签名可以保证信息是否被修改过，详情看 def page2():
    """
    app_id = "2016092500591565"  # APPID （沙箱应用）

    notify_url = "http://localhost:8000/blog/page2/"

    # 支付完成后，跳转的地址。
    # return_url = "http://localhost:8000/blog/page2/"  手动修改支付宝回到商家的url测试验签成功与否
    return_url = "http:///blog/page2/"

    merchant_private_key_path = r"D:\PycharmProject\MakeItEasy\makeiteasy\keys\alipay_sanbox_private_2048.txt"  # 应用私钥
    alipay_public_key_path = r"D:\PycharmProject\MakeItEasy\makeiteasy\keys\alipay_sanbox_public_2048.txt"  # 支付宝公钥

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay


def index(request):
    """
    /blog/index
    """
    context = {}
    return render(request, 'index.html', context)


def page1(request):
    """
    # 根据当前用户的配置，生成URL，并跳转。
    """
    money = float(request.POST.get('money'))

    alipay = get_ali_object()

    # 生成支付的url
    query_params = alipay.direct_pay(
        subject="Test",  # 商品简单描述
        out_trade_no="x2" + str(time.time()),  # 用户购买的商品订单号（每次不一样） 20180301073422891
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
    )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）

    return redirect(pay_url)


def page2(request):
    """
    支付完成后，回到商家的url，携带者支付后的信息
    http://page2/?charset=utf-8&out_trade_no=x21548231642.492832&method=alipay.trade.page.pay.return&total_amount=50.00&sign=bTis6peQpU6N08gzE6Gd91Azk41%2BHsBXWZu7Y4F57R2PrwY%2BbGB5mTr97WjAUH5OKpi0AAEvU6vUUZXBq%2B6uG5tLJzyP1mugJw24yJ8W64Zxe463SwAtxzkM5rkzMneWytS43%2BmW1WwBhQuktOqQWwuwRHiCt4d%2Fpy6R3KMnV3V0cw4j8epSMlasBq%2FSMpmSxPlfGZI2UTVgsgAzbQUbeysnVX7VPuxJJDnXUo2H9aBLA80jqti1hZAFrAvkiVn%2Bz2IQZleWwKg36AlaPbcHXfgNWXGGLmt7bJSrWC9OuemBgMvH8GSrj8eChII4ndbqKL54FKWk1U6eaaVajKJs%2FA%3D%3D&trade_no=2019012322001413590501093271&auth_app_id=2016092500591565&version=1.0&app_id=2016092500591565&sign_type=RSA2&seller_id=2088102177176291&timestamp=2019-01-23+16%3A21%3A59

    {
    "charset":"utf-8",
    "out_trade_no":"x21548231642.492832",
    "method":"alipay.trade.page.pay.return",
    "total_amount":"50.00",
    "sign":"bTis6peQpU6N08gzE6Gd91Azk41%2BHsBXWZu7Y4F57R2PrwY%2BbGB5mTr97WjAUH5OKpi0AAEvU6vUUZXBq%2B6uG5tLJzyP1mugJw24yJ8W64Zxe463SwAtxzkM5rkzMneWytS,""43%2BmW1WwBhQuktOqQWwuwRHiCt4d%2Fpy6R3KMnV3V0cw4j8epSMlasBq%2FSMpmSxPlfGZI2UTVgsgAzbQUbeysnVX7VPuxJJDnXUo2H9aBLA80jqti1hZAFrAvkiVn%2Bz2IQZleWwKg36AlaPbcHXfgNWXGGLmt7bJSrWC9OuemBgMvH8GSrj8eChII4ndbqKL54FKWk1U6eaaVajKJs%2FA%3D%3D,
    "trade_no":"2019012322001413590501093271",
    "auth_app_id":"2016092500591565",
    "version":"1.0",
    "app_id":"2016092500591565",
    "sign_type":"RSA2",
    "seller_id":"2088102177176291",
    "timestamp":"2019-01-23+16%3A21%3A59",
    }

    修改"total_amount":"50.00",  --->  "total_amount":"150.00",后，就会发现status = alipay.verify(post_dict, sign)返回的验签状态为false，
    意味着url被签名的data被修改过，不可信了
    """
    alipay = get_ali_object()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        # post_dict有10key： 9 ，1
        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)  # 验签
        print('------------------开始------------------')
        print('POST验证', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']

        # 修改订单状态
        # models.Order.objects.filter(trade_no=out_trade_no).update(status=2)
        print('------------------结束------------------')
        # 修改订单状态：获取订单号
        return HttpResponse('POST返回')

    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================开始==================')
        print('GET验证', status)
        print('==================结束==================')
        return HttpResponse('支付成功')
