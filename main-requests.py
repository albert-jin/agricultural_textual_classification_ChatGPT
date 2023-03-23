import requests
import json

# 已在colab上测试 OK

# "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"
def classify_text(sentence, categories):
    """
    使用ChatGPT API对句子进行文本分类。

    参数:
    sentence (str): 需要分类的句子
    categories (list of str): 预定义的类别列表

    返回:
    int: 预测类别在预定义类别列表中的索引，或者返回-1（表示出现错误）
    """

    # 为API请求准备URL、头部和负载
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer <your_api_key>"
    }
    prompt = f"Classify the following sentence into one of the given categories: {categories}\n\nSentence: {sentence}\nCategory: "

    payload = json.dumps({
        "engine": "davinci-codex",
        "prompt": prompt,
        "max_tokens": 10,
        "n": 1,
        "stop": None,
        "temperature": 0.5,
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
        predicted_category = response_data["choices"][0]["text"].strip()
    except KeyError:
        print("Error in parsing API response")
        return -1

    # 返回预测类别在预定义类别列表中的索引
    try:
        index = categories.index(predicted_category)
        return index
    except ValueError:
        print(f"Error: Predicted category '{predicted_category}' not found in the predefined categories")
        return -1


# 示例用法
sentence = "The cat is chasing a ball"
categories = ["Entertainment", "Sports", "Animals", "Technology"]

index = classify_text(sentence, categories)
print(f"Category index: {index}")
