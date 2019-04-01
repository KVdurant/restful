#coding:utf-8
from django.db import models

#创建code模型
class CodeModel(models.Model):
    name = models.CharField(max_length=50) #名字最长为50个字符
    code = models.TextField() #这个字段没有文本长度的限制
    
    def __str__(self):
        return 'Code(name={},id={})'.format(self.name,self.id)


