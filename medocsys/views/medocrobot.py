import openai
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.gzip import gzip_page


@gzip_page
@csrf_exempt
def chat(request):
    # 设置API密钥
    question = request.POST.get("question")
    print(question)
    openai.api_key = "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"
    # 设置问题和上下文
    # question = "What is the meaning of life?"
    # context = "The meaning of life is a philosophical question concerning the significance of life or existence in general."
    # 调用GPT-3生成答案
    response = openai.Completion.create(
        # engine="davinci",
        engine="text-davinci-003",
        prompt=question,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # 输出答案
    answer = response.choices[0].text.strip()
    context = {
        "status": 200,
        "answer": answer
    }
    # print(answer)
    return JsonResponse(context)
