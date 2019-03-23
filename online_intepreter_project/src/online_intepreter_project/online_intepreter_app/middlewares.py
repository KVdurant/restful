from django.http import QueryDict
def put_middleware(get_response):
    def middleware(request):
        if request.method == 'PUT':  # 如果是 PUT 请求
            setattr(request, 'PUT', QueryDict(request.body))  # 给请求设置 PUT 属性，这样我们就可以在视图函数中访问这个属性了
            # request.body 是请求的主体。我们知道请求有请求头，那请求的主体就是
            # request.body 了。当然，你一定还会问，为什么这样就可以访问 PUT 请求的相关
            # 数据了呢？这涉及到了 http 协议的知识，这里就不展开了，有兴趣的同学可以自行查阅资料
        response = get_response(request)  # 使用 get_response 返回响应
        return response  # 返回响应

    return middleware  # 返回核心的中间件处理函数
