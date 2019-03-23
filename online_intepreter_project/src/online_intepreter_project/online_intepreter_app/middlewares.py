from django.http import QueryDict
def put_middleware(get_response):
    def middleware(request):
        if request.method == 'PUT':  # ����� PUT ����
            setattr(request, 'PUT', QueryDict(request.body))  # ���������� PUT ���ԣ��������ǾͿ�������ͼ�����з������������
            # request.body ����������塣����֪������������ͷ����������������
            # request.body �ˡ���Ȼ����һ�������ʣ�Ϊʲô�����Ϳ��Է��� PUT ��������
            # �������أ����漰���� http Э���֪ʶ������Ͳ�չ���ˣ�����Ȥ��ͬѧ�������в�������
        response = get_response(request)  # ʹ�� get_response ������Ӧ
        return response  # ������Ӧ

    return middleware  # ���غ��ĵ��м��������
