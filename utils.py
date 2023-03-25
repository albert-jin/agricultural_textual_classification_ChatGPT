import requests
import json
from typing import List
from config import api_key, choices, temperature, string_similar, max_tokens
import Levenshtein


def parser_classification(predicted_category: str, _categories: List[str]):
    """
    1. 大小写合并 2.检测是否相同 3. 检测是否包含 4. 检测相似度 (string_similar) 5. 意外取-1
    :param predicted_category: ChatGPT预测的答案
    :param _categories: 类别集合
    :return:
    """
    try:
        _categories = [cat.lower() for cat in _categories]
        predicted_category = predicted_category.lower()
        if predicted_category in _categories:
            return _categories.index(predicted_category)
        else:
            for i, cate in enumerate(_categories):
                if cate in predicted_category:
                    return i
            if string_similar:
                ratios = [Levenshtein.ratio(predicted_category, category) for category in _categories]
                return ratios.index(max(ratios))
        raise Exception("no category matched with answer")
    except Exception as e:
        print(f"Error: {e.args}")
        return -1


def classify_text_davinci(sentence, categories, prompt_template, model_type="text-davinci-003"):
    """
    使用ChatGPT API对句子进行文本分类。

    参数:
    sentence (str): 需要分类的句子
    categories (list of str): 预定义的类别列表
    model_type (str):  可选模型类型 from ["text-davinci-001","text-davinci-002","text-davinci-003"]
    choices: 返回的随机可能数量
    返回:
    int: 预测类别在预定义类别列表中的索引，或者返回-1（出现错误）
    """

    # 为API请求准备URL、头部和负载
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }
    # prompt = f"Classify the following sentence into one of the given categories: {categories}\n\nSentence: {sentence}\nCategory: "
    # DEFAULT: "Classify the following sentence into one of the given categories: {}\n\nSentence: {}\nCategory: "
    prompt = prompt_template.format(categories, sentence)

    payload = json.dumps({
        "model": model_type,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "n": choices,
        "stop": None,
        "temperature": temperature,
    })

    try:
        # 向API发出请求并获取响应
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return -1

    # 解析API响应并提取预测类标签
    try:
        response_data = response.json()
        # print(json.dumps(response_data))
        predicted_category = response_data["choices"][0]["text"].strip()
    except KeyError:
        print("Error in parsing API response")
        return -1

    # 返回预测类别在预定义类别列表中的索引
    return parser_classification(predicted_category, categories)


def classify_text_turbo(sentences, categories, prompt_template):
    """
    使用ChatGPT API对句子进行文本分类。

    参数:
    sentence (str): 需要分类的句子
    categories (list of str): 预定义的类别列表
    choices: 返回的随机可能数量
    返回:
    int: 预测类别在预定义类别列表中的索引，或者返回-1（表示出现错误）
    """

    # 为API请求准备URL、头部和负载
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    # DEFAULT: "Classify the following sentence into one of the given categories: {}\n\nSentence: {}\nCategory: "
    # messages = [{"role": "user", "content": f"Classify the following sentence into one of the given categories: "
    #              f"{categories}\n\nSentence: {sentence}\nCategory: "} for sentence in sentences]
    messages = [{"role": "user", "content": prompt_template.format(categories, sentence)} for sentence in sentences]

    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": max_tokens,
        "n": choices,
        "stop": None,
        "temperature": temperature,
    })

    try:
        # 向API发出请求并获取响应
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return -1

    # 解析API响应并提取预测类标签
    try:
        response_data = response.json()
        # print(json.dumps(response_data))
        predicted_category = response_data["choices"][0]["message"]["content"].strip()
    except KeyError:
        print("Error in parsing API response")
        return -1

    # 返回预测类别在预定义类别列表中的索引
    return parser_classification(predicted_category, categories)


def get_answer_davinci(sentence, categories, prompt_template, model_type="text-davinci-003"):
    """ classify_text_davinci 不同在于 只获取chatGPT的输出 """
    # 为API请求准备URL、头部和负载
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
    }
    # prompt = f"Classify the following sentence into one of the given categories: {categories}\n\nSentence: {sentence}\nCategory: "
    # DEFAULT: "Classify the following sentence into one of the given categories: {}\n\nSentence: {}\nCategory: "
    prompt = prompt_template.format(categories, sentence)
    payload = json.dumps({
        "model": model_type,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "n": choices,
        "stop": None,
        "temperature": temperature,
    })
    try:
        # 向API发出请求并获取响应
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []

    # 解析API响应并提取预测类标签
    try:
        response_data = response.json()
        # print(json.dumps(response_data))
        predicted_answer = [response_data["choices"][i]["text"].strip() for i in range(choices)]
        return predicted_answer
    except KeyError:
        print("Error in parsing API response")
        return []


def get_answer_turbo(sentences, categories, prompt_template):
    """ classify_text_turbo 不同在于 只获取chatGPT的输出 """
    # 为API请求准备URL、头部和负载
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    # DEFAULT: "Classify the following sentence into one of the given categories: {}\n\nSentence: {}\nCategory: "
    # messages = [{"role": "user", "content": f"Classify the following sentence into one of the given categories: "
    #              f"{categories}\n\nSentence: {sentence}\nCategory: "} for sentence in sentences]
    messages = [{"role": "user", "content": prompt_template.format(categories, sentence)} for sentence in sentences]

    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": max_tokens,
        "n": choices,
        "stop": None,
        "temperature": temperature,
    })

    try:
        # 向API发出请求并获取响应
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []

    # 解析API响应并提取预测类标签
    try:
        response_data = response.json()
        # print(json.dumps(response_data))
        predicted_answer = [response_data["choices"][i]["message"]["content"].strip() for i in range(choices)]
        return predicted_answer
    except KeyError:
        print("Error in parsing API response")
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
