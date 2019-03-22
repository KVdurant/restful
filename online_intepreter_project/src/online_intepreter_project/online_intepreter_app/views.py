#coding=utf-8
from django.views import View  # 引入最基本的类视图
from django.http import JsonResponse # 引入现成的响应类
from django.core.serializers import serialize  # 引入序列化函数
from .models import CodeModel  # 引入 Code 模型，记得加个 `.`  哦。
import json  # 引入 json 库，我们会用它来处理 json 字符串。

# 定义最基本的 API 视图
# 定义最基本的 API 视图
class APIView(View):
    def response(self,
                 queryset=None,
                 fields=None,
                 **kwargs):
        """
        序列化传入的 queryset 或 其他 python 数据类型。返回一个 JsonResponse 。
        :param queryset: 查询集，可以为 None
        :param fields: 查询集中需要序列化的字段，可以为 None
        :param kwargs: 其他需要序列化的关键字参数
        :return: 返回 JsonResponse
        """
        # 根据传入参数序列化查询集，得到序列化之后的 json 字符串
        
        if queryset and fields:
            serialized_data = serialize(format='json', 
                                       queryset=queryset,
                                       fields=fields)
        elif queryset:
            serialized_data = serialize(format='json', 
                                       queryset=queryset)
        else:
            serialized_data=None
        # 这一步很重要，在经过上面的查询步骤之后， serialized_data 已经是一个字符串
        # 我们最终需要把它放入 JsonResponse 中，JsonResponse 只接受 python 数据类型
        # 所以我们需要先把得到的 json 字符串转化为 python 数据结构。
        instances = json.loads(serialized_data) if serialized_data else 'No instance'
        data = {'instances': instances}
        data.update(kwargs)  # 添加其他的字段
        return JsonResponse(data=data)  # 返回响应
        
        
        
        