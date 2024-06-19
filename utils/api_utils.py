import json

import cohere
import dashscope
import jwt
import openai
import reka
import requests
from mistralai.client import MistralClient
from openai import OpenAI, AzureOpenAI, APIError
import anthropic
import time
import os
import google.generativeai as genai
from zhipuai import ZhipuAI
from utils.common_utils import count_tokens, write_jsonl
import yaml
supported_models = [
    # azure
    'gpt-35-turbo-0125', 'gpt-4-turbo-2024-04-09', 'gpt4o-0513',
    # openai
    'gpt-4-0125-preview', 'gpt-4-0613', 'gpt-3.5-turbo-0613',
    # claude
    'claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307',
    'claude-2.1', 'claude-2.0', 'claude-instant-1.2',
    # gemini & palm
    'models/gemini-pro', 'models/gemini-1.5-pro-latest',
    # Yi
    'zero-one-ai/Yi-34B-Chat', 
    # Vicuna
    'lmsys/vicuna-13b-v1.5', 'lmsys/vicuna-7b-v1.5',
    # Llama
    'meta-llama/Llama-2-70b-chat-hf', 'meta-llama/Llama-2-13b-chat-hf', 'meta-llama/Llama-2-7b-chat-hf',
    'meta-llama/Llama-3-70b-chat-hf', 'meta-llama/Meta-Llama-3-8B-Instruct',
    # mistral
    'mistralai/Mistral-7B-Instruct-v0.1', 'mistralai/Mistral-7B-Instruct-v0.2','mistralai/Mixtral-8x7B-Instruct-v0.1',  "mistralai/Mistral-7B-Instruct-v0.3", 
    # qwen
    'Qwen/Qwen1.5-72B-Chat', 'Qwen/Qwen1.5-14B-Chat', 'Qwen/Qwen1.5-7B-Chat', 'Qwen/Qwen2-72B-Instruct', 'Qwen/Qwen2-7B-Instruct',
    # deepseek
    'deepseek-ai/deepseek-llm-67b-chat',
    # openchat
    'openchat/openchat-3.5-1210',
    # Zhipu AI GLM
    'glm-4',
    # Baidu Wenxin
    'wenxin-4',
    # MiniMax
    'minimax-abab6.5-chat',
    # SenseChat
    'SenseChat-5',
    # Baichuan
    'Baichuan2-Turbo-192k',  'baichuan-inc/Baichuan2-7B-Chat', 'baichuan-inc/Baichuan2-13B-Chat', # Baichuan3 api not released yet"
    # Reka AI
    'reka-flash-20240226',
    'reka-core-20240501',
    # Mistral
    'mistral-large-2402',
    # Cohere Command
    'command-r-plus', "CohereForAI/aya-23-8B",
    # Qwen 2.5
    'qwen-max-0428',
    # Phi-3
    'microsoft/Phi-3-small-128k-instruct', 'microsoft/Phi-3-medium-128k-instruct',
    # Sailor
    'sail/Sailor-14B-Chat', 'sail/Sailor-7B-Chat','SeaLLMs/SeaLLM-7B-v2.5',
    # gemma
    "google/gemma-1.1-7b-it",
    # aisingapore
    "aisingapore/sea-lion-7b-instruct",
    ]
open_source_models = ['meta-llama/Meta-Llama-3-8B-Instruct','Qwen/Qwen2-7B-Instruct', 'Qwen/Qwen1.5-14B-Chat', 'Qwen/Qwen1.5-7B-Chat', 'baichuan-inc/Baichuan2-7B-Chat', 'baichuan-inc/Baichuan2-13B-Chat', 'microsoft/Phi-3-small-128k-instruct', 'microsoft/Phi-3-medium-128k-instruct', 'sail/Sailor-14B-Chat', 'sail/Sailor-7B-Chat','SeaLLMs/SeaLLM-7B-v2.5', "CohereForAI/aya-23-8B", "google/gemma-1.1-7b-it", "mistralai/Mistral-7B-Instruct-v0.3", "aisingapore/sea-lion-7b-instruct",]
# API setting constants
API_MAX_RETRY = 5
API_RETRY_SLEEP = 30
API_ERROR_OUTPUT = "$ERROR$"

with open('api_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 设置环境变量
for key, value in config.items():
    os.environ[key] = value
vllm_key = os.environ.get("VLLM_API_KEY")
vllm_endpoint = os.environ.get("VLLM_OPENAI_ENDPOINT")
together_api_key = os.environ.get("TOGETHER_API_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
azure_api_gpt35_key = os.environ.get("AZURE_OPENAI_KEY")
azure_api_gpt35_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_api_gpt4_key = os.environ.get("AZURE_OPENAI_KEY_GPT4")
azure_api_gpt4_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT_GPT4")
azure_api_gpt4o_key = os.environ.get("AZURE_OPENAI_KEY_GPT4O")
azure_api_gpt4o_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT_GPT4O")
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY")
WENXIN_API_KEY = os.environ.get("WENXIN_API_KEY")
WENXIN_SECRET_KEY = os.environ.get("WENXIN_SECRET_KEY")
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY")
SENSECHAT_API_KEY = os.environ.get("SENSECHAT_API_KEY")
SENSECHAT_SECRET_KEY = os.environ.get("SENSECHAT_SECRET_KEY")
BAICHUAN_API_KEY = os.environ.get("BAICHUAN_API_KEY")
REKA_API_KEY = os.environ.get("REKA_API_KEY")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def change_system_to_user(conv):
    i = 0
    while i < len(conv):
        if conv[i]['role'] == 'system':
            conv[i]['role'] = 'user'
            # merge two messages together
            if conv[i+1]['role'] == 'user':
                conv[i]['content'] += '\n' + conv[i+1]['content']
                conv.pop(i+1)
            i += 1
        elif conv[i]['role'] == 'assistant' and conv[i+1]['role'] == 'assistant':
            conv[i]['content'] += '\n' + conv[i+1]['content']
            conv.pop(i+1)
            i += 1
        else:
            i += 1
    return conv

import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# openai model
# with openai
def chat_completion_openai(model, conv, temperature, max_tokens=2048, n=1):
    """
    input:
        conv: the message [{'role': 'message'}]
    output:
        if n > 1: [str]
        if n = 1: str
    """
    output = API_ERROR_OUTPUT
    for retry_i in range(API_MAX_RETRY):
        try:
            response = openai_client.chat.completions.create(model=model,
                messages=conv,
                n=n,
                temperature=temperature,
                max_tokens=max_tokens)
            if n == 1:
                output = response.choices[0].message.content
            else:
                output = [response.choices[i].message.content for i in range(n)]
            break
        except openai.OpenAIError as e:
            print(f'{model} encountered error')
            print(type(e), e)
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output


# open source model
# with openai and vllm
def chat_completion_vllm(model, conv, temperature, max_tokens=2048, n=1):
    """
    input:
        conv: the message [{'role': 'message'}]
    output:
        if n > 1: [str]
        if n = 1: str
    """
    output = API_ERROR_OUTPUT
    client = OpenAI(base_url=vllm_endpoint, api_key=vllm_key,)

    for retry_i in range(API_MAX_RETRY):
        try:
            response = client.chat.completions.create(model=model,
                messages=conv,
                n=n,
                temperature=temperature,
                max_tokens=max_tokens)
            if n == 1:
                output = response.choices[0].message.content
            else:
                output = [response.choices[i].message.content for i in range(n)]
            break
        except openai.OpenAIError as e:
            print(f'{model} encountered error')
            print(type(e), e)
            if "This model's maximum context length"  in e.message:
                break
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

# with azure
def chat_completion_azure(model, conv, temperature, max_tokens=2048, n=1):
    if model == 'gpt-35-turbo-0125':
        azure_client = AzureOpenAI(
            azure_endpoint = azure_api_gpt35_endpoint, 
            api_key=azure_api_gpt35_key,  
            api_version="2024-02-15-preview"
            )
    elif model == 'gpt-4-turbo-2024-04-09':
        azure_client = AzureOpenAI(
            azure_endpoint = azure_api_gpt4_endpoint, 
            api_key=azure_api_gpt4_key,  
            api_version="2024-02-15-preview"
            )
    elif "4o" in model:
        model = 'gpt4o-0513'
        azure_client = AzureOpenAI(
            azure_endpoint = azure_api_gpt4o_endpoint, 
            api_key=azure_api_gpt4o_key,  
            api_version="2024-02-15-preview"
            )
    output = API_ERROR_OUTPUT
    price_dict = {
        'gpt4o-0513':{"prompt": 0.005 / 1000, "completion":0.015 / 1000},
        'gpt-4-turbo-2024-04-09':{"prompt": 0.01 / 1000, "completion":0.03 / 1000},
        'gpt-35-turbo-0125':{"prompt": 0.0005 / 1000, "completion":0.0015 / 1000},
    }
    used_prompt = 0
    used_completion = 0
    for retry_i in range(API_MAX_RETRY):
        try:
            response = azure_client.chat.completions.create(model=model,
                messages=conv,
                n=n,
                temperature=temperature,
                max_tokens=max_tokens)
            if n == 1:
                output = response.choices[0].message.content
                used_prompt += response.usage.prompt_tokens
                used_completion += response.usage.completion_tokens
            else:
                output = [response.choices[i].message.content for i in range(n)]
                used_prompt += response.usage.prompt_tokens
                used_completion += response.usage.completion_tokens
            break
        except openai.OpenAIError as e:
            print('conv: ', conv)
            print(type(e), e)
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    price = used_prompt * price_dict[model]["prompt"] + used_completion * price_dict[model]["completion"]
    write_jsonl({"model":model, "used prompt tokens": used_prompt, "used completion tokens": used_completion, "Price": price}, "price.jsonl")
    return output

# open-source models
together_client = openai.OpenAI(
  api_key=together_api_key,
  base_url='https://api.together.xyz/v1',
)
def chat_completion_together(model, conv, temperature, max_tokens=2048, n=1):
    output = API_ERROR_OUTPUT
    for retry_i in range(API_MAX_RETRY):
        try:
            chat_completion = together_client.chat.completions.create(
                messages=conv,
                model=model,
                n=n,
                temperature=temperature,
                max_tokens = max_tokens
            )
            if n == 1:
                output = chat_completion.choices[0].message.content
            else:
                output = [chat_completion.choices[i].message.content for i in range(n)]
            break
        except openai.OpenAIError as e:
            # only happens in this function because Yi and Llama has a limit of 4096 tokens
            if hasattr(e, 'param') and e.param == 'max_tokens':
                # this happens frequently when it is out of context length
                print(f'{model} out of context length')
                raise e
            else:
                print('encountered error: ', e)
                if retry_i == API_MAX_RETRY - 1:
                    raise e
                else:
                    time.sleep(API_RETRY_SLEEP)
    return output

# anthropic
def chat_completion_anthropic(model, conv, temperature, max_tokens, n=1):
    # only supports n=1
    output = API_ERROR_OUTPUT
    for retry_i in range(API_MAX_RETRY):
        try:
            c = anthropic.Anthropic(api_key=anthropic_api_key)
            # only supports user roles
            conv = change_system_to_user(conv)
            response = c.messages.create(
                model=model,
                messages=conv,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            output = response.content[0].text
            break
        except anthropic.APIError as e:
            print(f'{model} encountered error')
            print(type(e), e)
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

# gemini
def chat_completion_gemini(model_name, conv):
    # only supports n=1
    output = API_ERROR_OUTPUT
    for retry_i in range(API_MAX_RETRY):
        try:
            model = genai.GenerativeModel(model_name)
            conv_to_send = []
            # only supports two roles: "user" and "model"
            # format: list of dict {'role': 'user/model', 'parts': [str]}
            for m in conv:
                if m['role'] in ['user', 'system']:
                    if conv_to_send == [] or conv_to_send[-1]['role'] != 'user':
                        conv_to_send.append({'role':'user', 'parts': [m['content']]})
                    else:
                        conv_to_send[-1]['parts'][0] += '\n' + m['content']
                elif m['role'] == 'assistant':
                    conv_to_send.append({'role':'model', 'parts': [m['content']]})
            response = model.generate_content(conv_to_send)
            output = response.candidates[0].content.parts[0].text
            break
        except Exception as e:
            print(f'{model} encountered error')
            print(type(e), e)
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

def chat_completion_glm(model, conv, temperature, max_tokens, n=1):
    assert model in supported_models
    output = API_ERROR_OUTPUT
    for retry_i in range(API_MAX_RETRY):
        try:
            assert n is not None
            client = ZhipuAI(api_key=ZHIPU_API_KEY)
            response = client.chat.completions.create(
                model=model,
                messages=conv,
                max_tokens=max_tokens,
                temperature=temperature
            )
            output = response.choices[0].message.content
            if output.startswith("respond>"):
                output = "<" + output
            break
        except Exception as e:
            print(f'{model} encountered error')
            print(type(e), e)
            if '1301' in str(e):
                # safety filter
                raise APIError(message="safety filter", request=None, body=dict(param="security"))
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

def chat_completion_wenxin(model, conv, temperature, max_tokens, n=1):
    # https://cloud.baidu.com/qianfandev/topic/267840
    assert model in supported_models

    output = API_ERROR_OUTPUT
    for retry_i in range(API_MAX_RETRY):
        try:
            url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={WENXIN_API_KEY}&client_secret={WENXIN_SECRET_KEY}"
            payload = json.dumps("")
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=payload)
            access_token = response.json().get("access_token")

            system_message = ""
            if conv[0]["role"] == "system":
                system_message = conv[0]["content"]
                conv = conv[1:]

            data = dict(messages=conv, temperature=temperature, max_output_tokens=max_tokens)
            if system_message:
                data.update(system=system_message)

            url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token
            payload = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=payload)
            if "max input characters" in str(response.json()) or 'tokens too long' in str(response.json()):
                raise APIError(message="max_tokens exceeded", request=None, body=dict(param="max_tokens"))
            output = response.json()["result"]
            break
        except Exception as e:
            if hasattr(e, 'param') and e.param == 'max_tokens':
                # this happens frequently when it is out of context length
                print(f'{model} out of context length')
                raise e
            else:
                print(f'{model} encountered error')
                print('response: ', response.json())
                print(type(e), e)
                if retry_i == API_MAX_RETRY - 1:
                    raise e
                else:
                    time.sleep(API_RETRY_SLEEP)
    return output

def chat_completion_minimax(model, conv, temperature, max_tokens, n=1):
    # https://www.minimaxi.com/document/guides/chat-model/pro?id=64b79fa3e74cddc5215939f4
    assert model in supported_models
    url = "https://api.minimax.chat/v1/text/chatcompletion_pro"
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + MINIMAX_API_KEY}

    system_message = ""
    if conv[0]["role"] == "system":
        system_message = conv[0]["content"]
        conv = conv[1:]

    messages = []
    for raw in conv:
        if raw["role"] == "user":
            messages.append({"sender_type": "USER", "sender_name": "User", "text": raw["content"]})
        else:
            messages.append({"sender_type": "BOT", "sender_name": "MM智能助理", "text": raw["content"]})

    payload = {
        "bot_setting": [
            {
                "bot_name": "MM智能助理",
                "content": system_message or "MM智能助理是一款由MiniMax自研的，没有调用其他产品的接口的大型语言模型。MiniMax是一家中国科技公司，一直致力于进行大模型相关的研究。",
            }
        ],
        "messages": messages,
        "reply_constraints": {"sender_type": "BOT", "sender_name": "MM智能助理"},
        "model": model.split("minimax-", maxsplit=1)[1],
        "tokens_to_generate": max_tokens,
        "temperature": temperature,
    }

    output = API_ERROR_OUTPUT
    for retry_i in range(API_MAX_RETRY):
        try:
            response = requests.request("POST", url, headers=headers, json=payload)
            output = response.json()["reply"]
            break
        except Exception as e:
            print(f'{model} encountered error')
            print(type(e), e)
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

def chat_completion_sensechat(model, conv, temperature, max_tokens, n=1):
    # https://platform.sensenova.cn/doc?path=/model/llm/GeneralLLM.md
    assert model in supported_models

    headers = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "iss": SENSECHAT_API_KEY,
        "exp": int(time.time()) + 1800,  # 填写您期望的有效时间，此处示例代表当前时间+30分钟
        "nbf": int(time.time()) - 5  # 填写您期望的生效时间，此处示例代表当前时间-5秒
    }
    access_token = jwt.encode(payload, SENSECHAT_SECRET_KEY, headers=headers)

    # If the assistant generated an empty response, remove it and merge the user requests
    if len(conv) > 2 and conv[-2] == {'role': 'assistant', 'content': ''} and conv[-1]["role"] == "user":
        conv[-3]["content"] = conv[-3]["content"] + "\n" + conv[-1]["content"]
        conv = conv[:-2]
    conv = [raw for raw in conv if raw != {'role': 'assistant', 'content': ''}]

    data = dict(model=model, messages=conv, temperature=temperature, max_new_tokens=max_tokens, n=n)
    url = "https://api.sensenova.cn/v1/llm/chat-completions"
    payload = json.dumps(data)
    headers = {'Content-Type': 'application/json', "Authorization": "Bearer " + access_token}

    output = API_ERROR_OUTPUT
    for retry_i in range(API_MAX_RETRY):
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            output = response.json()["data"]["choices"][0]["message"]
            break
        except Exception as e:
            print(f'{model} encountered error: ', e)
            print('response.json(): ', response.json())
            if response.json()['error']['code']==18:
                # safety filter
                raise APIError(message="safety filter", request=None, body=dict(param="security"))
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

def chat_completion_baichuan(model, conv, temperature, max_tokens, n=1):
    # https://platform.baichuan-ai.com/docs/api
    url = "https://api.baichuan-ai.com/v1/chat/completions"
    assert n == 1

    data = {
        "model": model,
        "messages": conv,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    json_data = json.dumps(data)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + BAICHUAN_API_KEY}

    output = API_ERROR_OUTPUT
    for retry_i in range(API_MAX_RETRY):
        try:
            response = requests.post(url, data=json_data, headers=headers)
            output = response.json()["choices"][0]["message"]["content"]
            break
        except Exception as e:
            print(f'{model} encountered error')
            print(type(e), e)
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

def chat_completion_reka(model, conv, temperature, max_tokens, n=1):
    # https://docs.reka.ai
    reka.API_KEY = REKA_API_KEY
    assert n == 1

    output = API_ERROR_OUTPUT
    messages = []
    for raw in change_system_to_user(conv):
        if raw["role"] == "user":
            messages.append(dict(type="human", text=raw["content"]))
        else:
            messages.append(dict(type="model", text=raw["content"]))

    for retry_i in range(API_MAX_RETRY):
        try:
            response = reka.chat(model_name=model, conversation_history=messages,
                                 temperature=temperature, request_output_len=max_tokens)
            output = response["text"]
            break
        except Exception as e:
            print(f'{model} encountered error')
            print(type(e), e)
            print('original conv: ', [c['role'] for c in change_system_to_user(conv)])
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

def chat_completion_mistral(model, conv, temperature, max_tokens, n=1):
    # https://docs.mistral.ai/getting-started/quickstart/
    client = MistralClient(api_key=MISTRAL_API_KEY)
    output = API_ERROR_OUTPUT
    
    # If the assistant generated an empty response, remove it and merge the user requests
    if len(conv) > 2 and conv[-2] == {'role': 'assistant', 'content': ''} and conv[-1]["role"] == "user":
        conv[-3]["content"] = conv[-3]["content"] + "\n" + conv[-1]["content"]
        conv = conv[:-2]
    conv = [raw for raw in conv if raw != {'role': 'assistant', 'content': ''}]

    for retry_i in range(API_MAX_RETRY):
        try:
            response = client.chat(
                model=model,
                messages=conv,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            output = response.choices[0].message.content
            break
        except Exception as e:
            print(f'{model} encountered error')
            print(type(e), e)
            print('conv: ', conv)
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

def chat_completion_cohere(model, conv, temperature, max_tokens, n=1):
    # https://docs.cohere.com/docs/chat-api
    client = cohere.Client(COHERE_API_KEY)
    output = API_ERROR_OUTPUT
    messages = []
    for raw in conv:
        if raw["role"] == "user":
            messages.append(dict(role="USER", message=raw["content"]))
        elif raw["role"] == "system":
            messages.append(dict(role="SYSTEM", message=raw["content"]))
        else:
            messages.append(dict(role="CHATBOT", message=raw["content"]))

    prompt = messages.pop()["message"]
    for retry_i in range(API_MAX_RETRY):
        try:
            response = client.chat(
                model=model,
                message=prompt,
                chat_history=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            output = response.text
            break
        except Exception as e:
            print(f'{model} encountered error')
            print(type(e), e)
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

def chat_completion_qwen_max(model, conv, temperature, max_tokens, n=1):
    # https://help.aliyun.com/zh/dashscope/developer-reference/quick-start
    output = API_ERROR_OUTPUT

    for retry_i in range(API_MAX_RETRY):
        try:
            response = dashscope.Generation.call(
                dashscope.Generation.Models.qwen_turbo,
                messages=conv,
                result_format='message',  # 将返回结果格式设置为 message
            )
            output = response.output.choices[0].message.content
            break
        except Exception as e:
            print(f'{model} encountered error')
            print(type(e), e)
            if retry_i == API_MAX_RETRY - 1:
                raise e
            else:
                time.sleep(API_RETRY_SLEEP)
    return output

# map to api_utils
# please put all api calling functions here
def generate_response(model, conv, temperature = 0.1, max_tokens = 400, n = 1, model_name = None):
    if model_name is None:
        name = model.model_name
    else:
        name = model_name

    if name in supported_models:
        output = ""
        if name in open_source_models:
            output = chat_completion_vllm(name, conv, temperature = temperature, max_tokens = max_tokens, n = n)
        elif name in ['gpt-35-turbo-0125', 'gpt-4-turbo-2024-04-09', 'gpt4o-0513']:
            output = chat_completion_azure(name, conv, temperature = temperature, max_tokens = max_tokens, n = n)
        elif 'gpt' in name:
            output = chat_completion_openai(name, conv, temperature = temperature, max_tokens = max_tokens, n = n)
        elif 'claude' in name: # only support n = 1
            output = chat_completion_anthropic(name, conv, temperature = temperature, max_tokens = max_tokens, n = n)
        elif name in ['models/gemini-pro', 'models/gemini-1.5-pro-latest']:
            # only support n = 1
            output = chat_completion_gemini(name, conv)
        elif "glm" in name:
            output = chat_completion_glm(name, conv, temperature = temperature, max_tokens = max_tokens, n = n)
        elif "wenxin" in name:
            output = chat_completion_wenxin(name, conv, temperature=temperature, max_tokens=max_tokens, n=n)
        elif "minimax" in name:
            output = chat_completion_minimax(name, conv, temperature=temperature, max_tokens=max_tokens, n=n)
        elif "sensechat" in name.lower():
            output = chat_completion_sensechat(name, conv, temperature=temperature, max_tokens=max_tokens, n=n)
        elif "baichuan" in name.lower():
            output = chat_completion_baichuan(name, conv, temperature=temperature, max_tokens=max_tokens, n=n)
        elif "reka" in name.lower():
            output = chat_completion_reka(name, conv, temperature=temperature, max_tokens=max_tokens, n=n)
        elif "mistral-large" in name.lower():
            output = chat_completion_mistral(name, conv, temperature=temperature, max_tokens=max_tokens, n=n)
        elif "command" in name.lower():
            output = chat_completion_cohere(name, conv, temperature=temperature, max_tokens=max_tokens, n=n)
        elif "qwen-max" in name.lower():
            output = chat_completion_qwen_max(name, conv, temperature=temperature, max_tokens=max_tokens, n=n)
        elif name in supported_models:
            output = chat_completion_together(name, conv, temperature = temperature, max_tokens = max_tokens, n = n)
        if n == 1: #debate scenarios
            # truncate output to only max_tokens
            tokens = count_tokens(output)
            output = output if tokens == 0 else output[:int(len(output) / tokens * max_tokens)]
        return output
    else:
        raise ValueError(f"Unsupported model: {model}")