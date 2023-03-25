"""
基于 utils.py 的 OpenAI 工具包 实现
"""

import openai
from config import api_key, choices, temperature, max_tokens
from utils import parser_classification
openai.api_key = api_key


def classify_text_davinci(sentence, categories, prompt_template, model_type="text-davinci-003"):
    prompt = prompt_template.format(categories, sentence)

    try:
        # 向API发出请求并获取响应
        response = openai.Completion.create(
            engine=model_type,  # gpt-3.5-turbo是目前最好的模型
            prompt=prompt,
            max_tokens=max_tokens,
            n=choices,
            stop=None,
            temperature=temperature,
        )
    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return -1

    # 解析API响应并提取预测类标签
    try:
        # print(json.dumps(response))
        predicted_category = response["choices"][0]["text"].strip()
    except KeyError as e:
        print(f"Error in parsing API response: {e}")
        return -1

    # 返回预测类别在预定义类别列表中的索引
    return parser_classification(predicted_category, categories)


def classify_text_turbo(sentences, categories, prompt_template):
    messages = [{"role": "user", "content": prompt_template.format(categories, sentence)} for sentence in sentences]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 使用gpt-3.5-turbo，这是目前最好的模型 # gpt-3.5-turbo
            messages=messages,
            max_tokens=max_tokens,
            n=choices,
            stop=None,
            temperature=temperature,
        )
    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return -1

    # 解析API响应并提取预测类标签
    try:
        # print(json.dumps(response))
        predicted_category = response["choices"][0]["message"]["content"].strip()
    except KeyError as e:
        print(f"Error in parsing API response: {e}")
        return -1

    # 返回预测类别在预定义类别列表中的索引
    return parser_classification(predicted_category, categories)


def get_answer_davinci(sentence, categories, prompt_template, model_type="text-davinci-003"):
    prompt = prompt_template.format(categories, sentence)

    try:
        # 向API发出请求并获取响应
        response = openai.Completion.create(
            engine=model_type,  # gpt-3.5-turbo是目前最好的模型
            prompt=prompt,
            max_tokens=max_tokens,
            n=choices,
            stop=None,
            temperature=temperature,
        )
    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return []

    # 解析API响应并提取预测类标签
    try:
        # print(json.dumps(response_data))
        predicted_answer = [response["choices"][i]["text"].strip() for i in range(choices)]
        return predicted_answer
    except KeyError as e:
        print(f"Error in parsing API response: {e}")
        return []


def get_answer_turbo(sentences, categories, prompt_template):
    messages = [{"role": "user", "content": prompt_template.format(categories, sentence)} for sentence in sentences]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 使用gpt-3.5-turbo，这是目前最好的模型 # gpt-3.5-turbo
            messages=messages,
            max_tokens=max_tokens,
            n=choices,
            stop=None,
            temperature=temperature,
        )
    except openai.OpenAIError as e:
        print(f"Error during API request: {e}")
        return []

    # 解析API响应并提取预测类标签
    try:
        # print(json.dumps(response))
        predicted_answer = [response["choices"][i]["message"]["content"].strip() for i in range(choices)]
        return predicted_answer
    except KeyError as e:
        print(f"Error in parsing API response: {e}")
        return []


if __name__ == '__main__':
    # 示例用法
    sentence = "The cat is chasing a ball"
    categories = ["Entertainment", "Sports", "Animals", "Technology"]
    template = "Classify the following sentence into one of the given categories: {}\n\nSentence: {}\nCategory: "
    answers = get_answer_davinci(sentence, categories, template)
    print('answers: ', answers)
    index = classify_text_davinci(sentence, categories, template)
    print(f"classify_text_davinci test: Category index: {index}")

    # 示例用法
    sentences = ["The cat is chasing a ball", "The phone is with a windows system."]
    # categories = ["Entertainment", "Sports", "Animals", "Technology"]
    answers = get_answer_turbo(sentences, categories, template)
    print('answers: ', answers)
    index = classify_text_turbo(sentences, categories, template)
    print(f"classify_text_turbo test: Category index: {index}")
