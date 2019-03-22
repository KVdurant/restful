from django.db import models, IntegrityError # ��ѯʧ��ʱ������Ҫ�õ���ģ��
import subprocess # �������д���
from django.http import Http404 # ����ѯ����ʧ��ʱ����404��Ӧ


class APIQuerysetMinx(object):
    """
    ���ڻ�ȡ��ѯ������ʹ��ʱ��model ���Ժ� queryset ���Ա�����һ��

    :model: ģ����
    :queryet: ��ѯ��
    """
    model = None
    queryset =  None
    
    def get_queryset(self):
        """
        ��ȡ��ѯ�������� model ��������Ĭ�Ϸ������е�ģ�Ͳ�ѯʵ����
        :return: ��ѯ��
        """
        #������Ӧ�����Ƿ񱻴��룬��û�д����׳�����
        assert self.model or self.queryset, 'No queryset found.'
        if self.queryset:
            return self.queryset
        else:
            return self.model.objects.all()
        

class APISingleObjectMixin(APIQuerysetMinx):
    """
        ���ڻ�ȡ��ǰ�����е�ʵ��
    ��lookup_args�� list,�����涨��ѯ�����Ĳ����б�Ĭ��Ϊ['pk','id']
    
    """
    lookup_args = ['pk','id']
    
    def get_object(self):
        """
        ͨ����ѯ lookup_args �еĲ���ֵ�����ص�ǰ����ʵ��������ȡ������ֵʱ����ֹͣ
        ��֮��Ĳ�����ѯ������˳�����Ҫ��
        :return: һ����һ�Ĳ�ѯʵ��
        """
        
        queryset= self.get_queryset() #��ȡ��ѯ��
        for key in self.lookup_args:
            if self.kwargs.get(key):
                id = self.kwargs[key]
                try:
                    instance= queryset.get(id=id) #��ȡ��ǰʵ��
                    return instance #ʵ�����ھͷ���ʵ��
                except models.ObjectDoesNotExist:   #��׽ʵ���������쳣
                    raise Http404('NO object found.')#�׳�404�쳣
        raise Http404('No object found.') #���������в�����δ��׽��ֵ�����׳�404�쳣
    
class APICreateMixin(APIQuerysetMinx):
     """
     API�е�list����
     """
     
     def list(self,fields=None):
         """
                 ���ز�ѯ����Ӧ
        :param fields:��ѯ����ϣ����ʵ�������ֶ�
        :return: JsonResponse
         """
         return self.response(
             queryset=self.get_queryset(),
             fields=fields)
         
     """
     API�е� create����   
     """
     def create(self,create_fields=None):
         """
                    ʹ�ô���Ĳ����б�� POST ֵ�л�ȡ��Ӧ����ֵ���������ֵ����ʵ����
                    �ɹ������򷵻ش����ɹ���Ӧ�����򷵻ش���ʧ����Ӧ��
        :param create_fields: list, ϣ�����������ֶΡ�
                    ��Ϊ None, ��Ĭ��Ϊ POST �ϴ��������ֶΡ�
        :return: JsonResponse
        """
         create_values={}
         if create_fields: #���������ϣ�����������ֶΣ����post�л�ȡÿ��ֵ
             for field in create_fields:
                 create_values[field]=self.request.POST.get(field)
         
         else:
            for key in self.request.POST: #��δ����ϣ���������ֶΣ���Ĭ��ΪPOST�ϴ�
                                          #�ֶζ�Ϊ�����ֶΡ�
                create_values[key]=self.request.POST.get(key);
         queryset = self.get_queryset()#��ȡ��ѯ��
         try:
            instance = queryset.create(**create_values)# ���ò�ѯ��������ʵ��
         except IntegrityError:# ��׽����ʧ���쳣
             return self.response(status='Failed to Create.')# ���ش���ʧ����Ӧ
         return self.response(status='Successfuly Create.')# �����ɹ��򷵻ش����ɹ���Ӧ
     
     

class APIDetailMixin(APISingleObjectMixin):
     """
     API �����в�ѯʵ������
     """
     
     def detail(self, fields=None):
         """
                     ���ص�ǰ�����е�ʵ��
          :param fields:ϣ��������ʵ������Щ�ֶα�ʵ����
          :return: JsonResponse 
         """
         
         return self.response(
             queryset = [self.get_queryset()],
             fields =fields)
         
         
class APIUpateMixin(APISingleObjectMixin):
     """
        API�и���ʵ������
     """
     
     def update(self,update_fields=None):
         
         """
                    ���µ�ǰ������ʵ�������³ɹ��򷵻سɹ���Ӧ�����򣬷��ظ���ʧ����Ӧ��
                    ������ updata_fields �����ֶ��б���ֻ��� PUT �ϴ�ֵ�л�ȡ����б��е��ֶΣ�
                    ����Ĭ��Ϊ���� POST �ϴ�ֵ�����е��ֶΡ�
         :param update_fields: list, ʵ����Ҫ�����µ��ֶ�
         :return: JsonResponse
        """
         instance = self.get_object() # ��ȡ��ǰ�����е�ʵ��
         if not update_fields: #�����ֶθ����б���Ĭ��ΪPUT�ϴ�����������
             update_fields=self.request.PUT.keys() 
         try: # ��������ʵ���ֶ�
             for field in update_fields:
                 update_value =self.request.PUT.get(field)#��PUT�л�ȡֵ
                 setattr(instance, field, update_value) # �����ֶ�
             instance.save() #����ʵ������
         except IntegrityError: # ��׽���´���
             return self.response(status='Faild to update.') #���ظ���ʧ����Ӧ
         return self.response(status='Successfully Upate.')#���ظ��³ɹ�
            
            
     
     
     
                
                
                                          
                                        
                                          
         
        
         
        
         
           
                
        
        



    
        