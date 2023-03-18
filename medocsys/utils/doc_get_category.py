import openai
import time
import re
import cohere

# 在环境变量中设置OpenAI API密钥
import requests

openai.api_key = "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"
cohere_api_key = "AmyM4HOivElEHEo7Pd3AbYIBwtFUBMqjOPKhtxNy"


def get_context(prompt: str) -> str:
    """
    :param prompt: 要输入的提示
    :return: 获取到的结果
    """
    try:
        co = cohere.Client(cohere_api_key)
        question = "请判断文章标题为'" + prompt + "'是医学中[内科，外科，儿科，妇产科，骨科，影像科，其他]中的哪个领域，用这是医学中的...领域来回答"
        response = co.generate(
            model='command-xlarge-nightly',
            # model='medium',
            prompt=question,
            max_tokens=100,
            temperature=0.7,
            stop_sequences=["--"]
        )
        context = response.generations[0].text
        return context
    except Exception as e:
        print(e)


# 提问代码
def get_category(title: str) -> str:
    # 你的问题
    try:
        question = "请判断文本'" + title + "'是医学中[内科，外科，儿科，妇产科，骨科，影像科，其他]中的哪个领域，用这是医学中的...领域来回答"
        prompt = question
        # print(prompt)
        # 调用 ChatGPT 接口
        model_engine = "text-davinci-003"
        create = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None,
                                          temperature=0.5, )
        completion = create

        response = completion.choices[0].text
        # print(response)
        rule = r'这是医学中的(.*?)领域'
        category = re.findall(rule, response)[0].strip()
        return category
    except Exception as e:
        print(e)


def get_category_api(title: str):
    url = "https://chat.openai.run/wp-json/ai-chatbot/v1/chat"
    question = "请判断文本'" + title + "'是医学中[内科，外科，儿科，妇产科，骨科，影像科，其他]中的哪个领域，用这是医学中的...领域来回答"
    formdata = {
        "env": "chatbot",
        "session": "6415bb36147c3",
        "prompt": "像 AI 助手一样交谈。 要友好，有创意。\n\nAI: 你好！有什么我可以帮助您的吗？openai.wiki\nUser: 免费的chatgpt接口有哪些？\nAI: ",
        "context": "像 AI 助手一样交谈。 要友好，有创意。",
        "messages": [
            {
                "id": "0f6jovcjjiej",
                "role": "assistant",
                "content": "你好！有什么我可以帮助您的吗？openai.wiki",
                "who": "AI: ",
                "html": "你好！有什么我可以帮助您的吗？openai.wiki"
            },
            {
                "id": "lnr7nxcmcol",
                "role": "user",
                "content": "question",
                "who": "User: ",
                "html": "question"
            }
        ],
        "rawInput": question,
        "userName": "<div class=\"mwai-avatar mwai-svg\"><img src=\"https://chat.openai.run/wp-content/plugins/ai-engine-pro//images/avatar-user.svg\" /></div>",
        "aiName": "<div class=\"mwai-avatar mwai-svg\"><img src=\"https://chat.openai.run/wp-content/plugins/ai-engine-pro//images/avatar-ai.svg\" /></div>",
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,
        "maxTokens": 1024,
        "maxResults": 1,
        "apiKey": "",
        "embeddingsIndex": "",
        "stop": "",
        "clientId": "3xfuimltudo"
    }
    headers = {
        'origin': "https://chat.openai.run",
        'Accept': 'application/json, text/plain, */*',
        'user-agent': "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        # 罪大恶极的参数:
        'content-type': "application/json",
    }

    res = requests.post(url=url, data=formdata, headers=headers).text
    print(type(res), res)
    return res


if __name__ == '__main__':
    title = "高果糖饮食与代谢综合征研究进展"
    start = time.time()
    response = get_context(prompt=title)
    # response = get_category_api(title)
    end = time.time()
    # print("标题是：" + title)
    print(response, len(response))
    # print("耗时", end - start)
