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
        # print(doc_category, doc_name)
        markdown += "<font color='info'>" + doc_category + ":</font>" + "[" + doc_name + "](" + "http://aimedocsys.fcsy.fit/media/docs/" + doc_name + ".pdf)\n"
    # print(markdown)
    # markdown = str(markdown)
    send_markdown(markdown=markdown)
    status = wx_send_all_file(msg=markdown)
    if status == "ok":
        context = {
            'status': status,
            'msg': "所有文献推送成功！"
        }
    else:
        context = {
            'status': status,
            'error': "文献推送失败,IP地址未授权！"
        }
    return JsonResponse(context)


def send_looking_file(request):
    file_name = request.GET.get('doc_name')
    try:
        if wx_send_file(media_id=wx_upload_file(file_name)):
            context = {
                'status': 200,
                'msg': file_name + "，文件发送成功。"
            }
        else:
            context = {
                'status': 403,
                'error': file_name + "，文件发送失败，请稍后重试。"
            }
    except Exception as e:
        context = {
            'status': 403,
            'error': file_name + "，文件发送失败，IP地址未授权。"
        }
    finally:
        return JsonResponse(context)
