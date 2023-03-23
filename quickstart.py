"""

#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2022-12-01"
openai.api_key = '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'  # os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    engine='text-davinci-003',  # "gpt-35-turbo",
    prompt="<|im_start|>system\nThe system is an AI assistant that helps people find information.\n<|im_end|>\n<|im_start|>user\nDoes Azure OpenAI support customer managed keys?\n<|im_end|>\n<|im_start|>assistant",
    temperature=1,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["<|im_end|>"])

print(response['choices'][0]['text'])

"""

# 经Colab测试 下面的才能运行

#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
openai.api_type = "open_ai" # azure
#openai.api_base = os.getenv("OPENAI_API_BASE") # 电脑环境变量中没有，修改后就基地址就变None了
openai.api_version = "" #试验后发现，这个默认为空不要修改，否则卡住
# InvalidRequestError: Unsupported OpenAI-Version header provided: 2022-12-01. (HINT: you can provide any of the following supported versions: 2020-10-01, 2020-11-07. Alternatively, you can simply omit this header to use the default version associated with your account.)
openai.api_key = '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'  # os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    engine='text-davinci-003',  # "gpt-35-turbo",
    prompt="<|im_start|>system\nThe system is an AI assistant that helps people find information.\n<|im_end|>\n<|im_start|>user\nDoes Azure OpenAI support customer managed keys?\n<|im_end|>\n<|im_start|>assistant",
    temperature=1,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["<|im_end|>"])

print(response['choices'][0]['text'])