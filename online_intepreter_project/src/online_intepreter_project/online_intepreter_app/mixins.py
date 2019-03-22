from django.db import models, IntegrityError # 查询失败时我们需要用到的模块
import subprocess # 用于运行代码
from django.http import Http404 # 当查询操作失败时返回404响应


class APIQuerysetMinx(object):
    """
    用于获取查询集。在使用时，model 属性和 queryset 属性必有其一。

    :model: 模型类
    :queryet: 查询集
    """
    model = None
    queryset =  None
    
    def get_queryset(self):
        """
        获取查询集。若有 model 参数，则默认返回所有的模型查询实例。
        :return: 查询集
        """
        #检验相应参数是否被传入，若没有传则抛出错误
        assert self.model or self.queryset, 'No queryset found.'
        if self.queryset:
            return self.queryset
        else:
            return self.model.objects.all()
        

class APISingleObjectMixin(APIQuerysetMinx):
    """
        用于获取当前请求中的实例
    ：lookup_args； list,用来规定查询参数的参数列表。默认为['pk','id']
    
    """
    lookup_args = ['pk','id']
    
    def get_object(self):
        """
        通过查询 lookup_args 中的参数值来返回当前请求实例。当获取到参数值时，则停止
        对之后的参数查询。参数顺序很重要。
        :return: 一个单一的查询实例
        """
        
        queryset= self.get_queryset() #获取查询集
        for key in self.lookup_args:
            if self.kwargs.get(key):
                id = self.kwargs[key]
                try:
                    instance= queryset.get(id=id) #获取当前实例
                    return instance #实例存在就返回实例
                except models.ObjectDoesNotExist:   #捕捉实例不存在异常
                    raise Http404('NO object found.')#抛出404异常
        raise Http404('No object found.') #若遍历所有参数都未捕捉到值，则抛出404异常
    
class APICreateMixin(APIQuerysetMinx):
     """
     API中的list操作
     """
     
     def list(self,fields=None):
         """
                 返回查询集响应
        :param fields:查询集中希望被实例化的字段
        :return: JsonResponse
         """
         return self.response(
             queryset=self.get_queryset(),
             fields=fields)
         
     """
     API中的 create操作   
     """
     def create(self,create_fields=None):
         """
                    使用传入的参数列表从 POST 值中获取对应参数值，并用这个值创建实例，
                    成功创建则返回创建成功响应，否则返回创建失败响应。
        :param create_fields: list, 希望被创建的字段。
                    若为 None, 则默认为 POST 上传的所有字段。
        :return: JsonResponse
        """
         create_values={}
         if create_fields: #如果传入了希望被创建的字段，则从post中获取每个值
             for field in create_fields:
                 create_values[field]=self.request.POST.get(field)
         
         else:
            for key in self.request.POST: #若未传入希望被创建字段，则默认为POST上传
                                          #字段都为创建字段。
                create_values[key]=self.request.POST.get(key);
         queryset = self.get_queryset()#获取查询集
         try:
            instance = queryset.create(**create_values)# 利用查询集来创建实例
         except IntegrityError:# 捕捉创建失败异常
             return self.response(status='Failed to Create.')# 返回创建失败响应
         return self.response(status='Successfuly Create.')# 创建成功则返回创建成功响应
     
     

class APIDetailMixin(APISingleObjectMixin):
     """
     API 操作中查询实例操作
     """
     
     def detail(self, fields=None):
         """
                     返回当前请求中的实例
          :param fields:希望被返回实例中那些字段被实例化
          :return: JsonResponse 
         """
         
         return self.response(
             queryset = [self.get_queryset()],
             fields =fields)
         
         
class APIUpateMixin(APISingleObjectMixin):
     """
        API中更新实例操作
     """
     
     def update(self,update_fields=None):
         
         """
                    更新当前请求中实例。更新成功则返回成功响应。否则，返回更新失败响应。
                    若传入 updata_fields 更新字段列表，则只会从 PUT 上传值中获取这个列表中的字段，
                    否则默认为更新 POST 上传值中所有的字段。
         :param update_fields: list, 实例需要被更新的字段
         :return: JsonResponse
        """
         instance = self.get_object() # 获取当前请求中的实例
         if not update_fields: #若无字段更新列表，则默认为PUT上传的所有数据
             update_fields=self.request.PUT.keys() 
         try: # 迭代更新实例字段
             for field in update_fields:
                 update_value =self.request.PUT.get(field)#从PUT中获取值
                 setattr(instance, field, update_value) # 更新字段
             instance.save() #保存实例更新
         except IntegrityError: # 捕捉更新错误
             return self.response(status='Faild to update.') #返回更新失败响应
         return self.response(status='Successfully Upate.')#返回更新成功
            
            
     
     
     
                
                
                                          
                                        
                                          
         
        
         
        
         
           
                
        
        



    
        