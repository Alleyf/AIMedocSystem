from django.http import JsonResponse

from medocsys.models import MeDocs
from medocsys.utils.send_msg import send_markdown, wx_upload_file, wx_send_file, wx_send_all_file


def send_all_usr_file(request):
    user_id = request.session["info"].get('id')
    queryset = MeDocs.objects.filter(user_id=user_id).all()
    markdown = ""
    for index, item in enumerate(queryset):
        doc_name = item.name
        doc_category = item.category
        print(doc_category, doc_name)
        markdown += "<font color='info'>" + doc_category + ":</font>" + "[" + doc_name + "](" + "http://amedoc.fcsy.fit/media/docs/" + doc_name + ".pdf)<br>"
    # print(markdown)
    # markdown = str(markdown)
    send_markdown(markdown=markdown)
    status = wx_send_all_file(msg=markdown)
    context = {
        'status': status,
        'msg': "所有文献推送成功！"
    }
    return JsonResponse(context)


def send_looking_file(request):
    try:
        file_name = request.GET.get('doc_name')
        if wx_send_file(media_id=wx_upload_file(file_name)):
            context = {
                'status': 200,
                'msg': file_name + "，文件发送成功。"
            }
        else:
            context = {
                'status': 403,
                'msg': file_name + "，文件发送失败，请稍后重试。"
            }
    except Exception as e:
        context = {
            'status': 403,
            'error': e
        }
    finally:
        return JsonResponse(context)
