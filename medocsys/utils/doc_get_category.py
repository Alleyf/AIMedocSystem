import openai
import time
import re

# 在环境变量中设置OpenAI API密钥
openai.api_key = "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"


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


if __name__ == '__main__':
    title = "高果糖饮食与代谢综合征研究进展"
    start = time.time()
    response = get_category(title)
    end = time.time()
    # print("标题是：" + title)
    print(response, len(response))
    # print("耗时", end - start)
