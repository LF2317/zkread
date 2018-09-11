# 封装购物车合并函数
import pickle
import base64
from django_redis import get_redis_connection


def merge_cookie_cart_to_redis(request, user, response):
    """合并cookie中购物车数据到redis中"""
    # 获取cookie中的购物车数据
    cookie_cart = request.COOKIES.get('cart') # None

    if cookie_cart is None:
        return

    # 解析cookie中购物车数据
    # {
    #     '<sku_id>': {
    #         'count': '<count>',
    #         'selected': '<selected>'
    #     },
    #     ...
    # }
    cart_dict = pickle.loads(base64.b64decode(cookie_cart))  # {}

    if not cart_dict:
        return

    # 对数据进行处理

    # 获取向redis购物车中合并加入的商品的id和数量count
    # {
    #     '<sku_id>': '<count>',
    #     ...
    # }
    cart = {}

    # 获取向redis购物车添加勾选商品id
    redis_selected_add = []

    # 获取从redis购物车移除勾选商品id
    redis_selected_remove = []

    for sku_id, count_selected in cart_dict.items():
        # 保存cookie购物车中对应商品的id和数量count
        cart[sku_id] = count_selected['count']

        # 判断cookie中该商品是否被选中
        if count_selected['selected']:
            # 勾选
            redis_selected_add.append(sku_id)
        else:
            # 不勾选
            redis_selected_remove.append(sku_id)

    # 执行合并
    redis_conn = get_redis_connection('cart')
    pl = redis_conn.pipeline()

    # 合并购物车中商品id和对应数量
    cart_key = 'cart_%s' % user.id
    # hmset: 一次向hash中添加多个属性和值，如果属性已存在，值直接进行覆盖，如果属性不存在，新建属性和值
    pl.hmset(cart_key, cart)

    # 合并购物车中商品勾选状态 set
    cart_selected_key = 'cart_selected_%s' % user.id

    if redis_selected_add:
        pl.sadd(cart_selected_key, *redis_selected_add)

    if redis_selected_remove:
        pl.srem(cart_selected_key, *redis_selected_remove)

    pl.execute()

    # 删除cookie购物车数据
    response.delete_cookie('cart')









