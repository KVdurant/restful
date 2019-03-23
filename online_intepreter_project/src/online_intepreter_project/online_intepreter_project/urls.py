"""online_intepreter_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# �������ǵ� URL ������ã�����ֱ�ӽ�������õ������ URL �ϡ�

from django.conf.urls import url, include  # ������Ҫ�õ������ú���
# include �������������� URL ���á����������Ǹ�·���ַ�����Ҳ�����Ǹ� url �����б�

from online_intepreter_app.views import APICodeView, APIRunCodeView, home, js, css  # �������ǵ���ͼ����
from django.views.decorators.csrf import csrf_exempt  # ͬ���ģ����ǲ���Ҫʹ�� csrf ���ܡ�

# ע����������� csrf_exempt ���÷�����ͽ�����Ϊװ����ʹ�õ�Ч����һ����

# ��ͨ�ļ��ϲ��� API
generic_code_view = csrf_exempt(APICodeView.as_view(method_map={'get': 'list',
                                                                'post': 'create'}))  # �����Զ���� method_map ����
# ���ĳ������Ĳ��� API
detail_code_view = csrf_exempt(APICodeView.as_view(method_map={'get': 'detail',
                                                               'put': 'update',
                                                               'delete': 'remove'}))
# ���д������ API
run_code_view = csrf_exempt(APIRunCodeView.as_view())
# Code Ӧ�� API ����
code_api = [
    url(r'^$', generic_code_view, name='generic_code'),  # ���ϲ���
    url(r'^(?P<pk>\d*)/$', detail_code_view, name='detail_code'),  # ����ĳ���ض�����
    url(r'^run/$', run_code_view, name='run_code'),  # ���д���
    url(r'^run/(?P<pk>\d*)/$', run_code_view, name='run_specific_code')  # �����ض�����
]
api_v1 = [url('^codes/', include(code_api))]  # API �� v1 �汾
api_versions = [url(r'^v1/', include(api_v1))]  # API �İ汾������� URL
urlpatterns = [
    url(r'^api/', include(api_versions)),  # API ���� URL
    url(r'^$', home, name='index'),  # ��ҳ��ͼ
    url(r'^js/(?P<filename>.*\.js)$', js, name='js'),  # ���� js �ļ����ǵã����û�� /
    url(r'^css/(?P<filename>.*\.css)$', css, name='css')  # ���� css �ļ����ǵã����û�� /
]
