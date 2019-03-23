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
    
class APIListMixin(APIQuerysetMinx):
     
     def list(self,fields=None):
         """
                 ���ز�ѯ����Ӧ
        :param fields:��ѯ����ϣ����ʵ�������ֶ�
        :return: JsonResponse
         """
         return self.response(
             queryset=self.get_queryset(),
             fields=fields)
         
class APICreateMixin(APIQuerysetMinx):  
    
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
         
         
class APIUpdateMixin(APISingleObjectMixin):
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
     

class APIDeleteMixin(APISingleObjectMixin):
         """
         API ɾ��ʵ������
         """
         def remove(self):
             """
                             ɾ����ǰ�����е�ʵ����ɾ���ɹ��򷵻�ɾ���ɹ���Ӧ��
             :return: JsonResponse
             """
             
             instance = self.get_object() #��ȡ��ǰʵ��
             instance.delete() # ɾ��ʵ��
             return self.response(status='Successfully Delete')  #����ɾ���ɹ�


class APIRunCodeMixin(object):
    """
            ���д������
    """
    def run_code(self, code):
        """
                    ���������Ĵ��룬������ִ�н��
        :param code: str, ��Ҫ�����еĴ���
        :return: str, ���н��
        """
        try:
            output = subprocess.check_output(['python', '-c', code], # ���д���
                                             stderr=subprocess.STDOUT, # �ض��������������ӽ���
                                             universal_newlines=True, # ������ִ�н��ת��Ϊ�ַ���
                                             timeout=30) # �趨ִ�г�ʱʱ��
        except subprocess.CalledProcessError as e: # ��׽ִ��ʧ���쳣
            output = e.output # ��ȡ�ӽ��̱�����Ϣ
        except subprocess.TimeoutExpired as e: # ��׽��ʱ�쳣
            output = '\r\n'.join(['Time Out!', e.output]) # ��ȡ�ӽ��̱�����������г�ʱ��ʾ
        return output # ����ִ�н��
    
class APIMethodMapMixin(object):
    """
         �����󷽷�ӳ�䵽����������
    :method_map: dict, ����ӳ���ֵ䡣
         �罫 get ����ӳ�䵽 list ��������ֵ��Ϊ {'get':'list'}
    """
    
    method_map = {}
    def __init__(self,*args,**kwargs):
        """
                  ӳ�����󷽷�����Ӵ�������Ĺؼ��ֲ�����Ѱ�� method_map ����������ֵΪ dict���͡�Ѱ�Ҷ�Ӧ����ֵ��
                  ���������Ժʹ��������ͬʱ������ method_map �����Դ������Ϊ׼��
        :param args: �����λ�ò���
        :param kwargs: ����Ĺؼ��ֲ���
        """
        method_map=kwargs['method_map'] if kwargs.get('method_map',None) \
                                        else self.method_map # ��ȡ method_map ����
        for request_method, mapped_method in method_map.items(): # ����ӳ�䷽��
            mapped_method = getattr(self, mapped_method) # ��ȡ��ӳ�䷽��
            method_proxy = self.view_proxy(mapped_method) # ���ö�Ӧ��ͼ����
            setattr(self, request_method, method_proxy) # ����ͼ����ӳ�䵽��ͼ��������
        super(APIMethodMapMixin,self).__init__(*args,**kwargs) # ִ�������������ʼ��

    def view_proxy(self, mapped_method):
        """
                    ����ӳ�䷽������������մ�����ͼ����������������
        :param mapped_method: �������ӳ�䷽��
        :return: function, ������ͼ������
        """
        def view(*args, **kwargs):
            """
                            ��ͼ�Ĵ�����
            :param args: ������ͼ������λ�ò���
            :param kwargs: ������ͼ�����Ĺؼ��ֲ���
            :return: ����ִ�б�ӳ�䷽��
            """
            return mapped_method() # ����ִ�д�����
        return view # ���ش�����ͼ


    

     
     
     
                
                
                                          
                                        
                                          
         
        
         
        
         
           
                
        
        



    
        