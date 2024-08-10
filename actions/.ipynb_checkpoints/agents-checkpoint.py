from http import HTTPStatus
from actions.logger import logger
import dashscope

dashscope.api_key = "xxxxxxxxxxxxx"

def call_llm_api(content):
    messages = [{'role': 'user', 'content': content}]
    responses = dashscope.Generation.call(
        "qwen2-7b-instruct",
        messages=messages,
        result_format='message',  # set the result to be "message" format.
        stream=True,  # set streaming output
        incremental_output=True  # get streaming output incrementally
    )
    
    response_content = ""  # 初始化一个空字符串来收集输出
    
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            output_text = response.output.choices[0]['message']['content']
            response_content += output_text  # 将内容追加到response_content中
        else:
            error_message = (
                'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message)
            )
            logger.error(error_message)  # 记录错误信息到日志
            print(error_message)
    
    # logger.info(f"API call completed with content: {response_content}")  # 记录成功信息到日志
    return response_content  # 返回生成的内容

def call_llm_for_menu(user_message: str) -> str:
    prompt = f"""
    用户请求查看餐馆的菜单。以下是用户的输入:
    "{user_message}"

    请生成餐馆的菜单，菜单内容应包括以下菜品：
    - 扬州炒饭
    - 鸡蛋炒饭
    - 牛肉面
    - 炸酱面
    - 宫保鸡丁
    - 麻婆豆腐
    - 鱼香茄子
    - 红烧肉
    - 凉拌黄瓜
    - 皮蛋豆腐
    - 夫妻肺片
    - 酸辣汤
    - 冬瓜排骨汤
    - 番茄蛋花汤
    - 春卷
    - 小笼包
    - 生煎包
    - 绿豆汤
    - 豆浆
    - 酸梅汤

    直接返回生成的菜单内容作为结果。
    """
    response = call_llm_api(prompt)
    return response  # 假设API返回的菜单文本在'text'字段中

# def call_llm_for_intent(user_message: str) -> dict:
#     # 提供意图示例来提高识别准确率
#     examples = """
#     示例1:
#     用户输入: "请给我看看菜单"
#     意图: "request_menu" （解释: 用户请求查看菜单，如: "请给我看看菜单", "我想看看今天有什么菜", "可以给我菜单吗"）

#     示例2:
#     用户输入: "我要点一份宫保鸡丁"
#     意图: "order_food" （解释: 用户请求订餐，如: "我要点一份宫保鸡丁", "来两份麻婆豆腐", "点三份扬州炒饭"）

#     示例3:
#     用户输入: "确认订单"
#     意图: "confirm_order" （解释: 用户想确认他们的订单，如: "确认订单", "订单信息对吗", "请确认我的订单"）

#     示例4:
#     用户输入: "请告诉我你们的营业时间"
#     意图: "provide_info" （解释: 用户请求一般信息，如: "请告诉我你们的营业时间", "你们的招牌菜是什么", "餐馆的位置在哪里"）
#     """

#     prompt = f"""
#     请帮我分析以下用户的输入，并识别其意图。意图只能是以下之一：
#     - request_menu （用户请求查看菜单）
#     - order_food （用户请求订餐）
#     - confirm_order （用户想确认订单）
#     - provide_info （用户请求一般信息）

#     {examples}

#     用户输入: "{user_message}"

#     如果无法识别用户的意图，请返回 "unknown" 作为意图。

#     请以以下结构化格式返回结果：
#     {{
#       "intent": "意图的名称，必须是 'request_menu', 'order_food', 'confirm_order', 'provide_info' 之一，或者 'unknown'",
#       "confidence": "意图识别的置信度（0到1之间的小数）",
#       "reason": "选择该意图的原因"
#     }}
#     """
    
#     return call_llm_api(prompt)


def call_llm_for_intent(user_message: str) -> dict:
    # 提供意图示例来提高识别准确率
    examples = """
    示例1:
    用户输入: "请给我看看菜单"
    意图: request_menu （解释: 用户请求查看菜单，如: "请给我看看菜单", "我想看看今天有什么菜", "可以给我菜单吗"）

    示例2:
    用户输入: "我要点一份宫保鸡丁"
    意图: order_food （解释: 用户请求订餐，如: "我要点一份宫保鸡丁", "来两份麻婆豆腐", "点三份扬州炒饭"）

    示例3:
    用户输入: "确认订单"
    意图: confirm_order （解释: 用户想确认他们的订单，如: "确认订单", "订单信息对吗", "请确认我的订单"）

    示例4:
    用户输入: "请告诉我你们的营业时间"
    意图: provide_info （解释: 用户请求一般信息，如: "请告诉我你们的营业时间", "你们的招牌菜是什么", "餐馆的位置在哪里"）
    """

    prompt = f"""
    请帮我分析以下用户的输入，并识别其意图。意图只能是以下之一：
    - request_menu （用户请求查看菜单）
    - order_food （用户请求订餐）
    - confirm_order （用户想确认订单）
    - provide_info （用户请求一般信息）

    {examples}

    如果无法识别用户的意图，请返回 "unknown" 作为意图。

    用户输入: "{user_message}"
    意图: "意图的名称，必须是 'request_menu', 'order_food', 'confirm_order', 'provide_info' 之一，或者 'unknown'"
    """
    
    return call_llm_api(prompt)


def call_llm_for_detailed_info(user_message: str) -> dict:
    prompt = f"""
    用户正在询问有关餐馆的一些常规信息，如营业时间、地点或特色菜。以下是用户的具体问题:
    "{user_message}"

    请根据已知的餐馆信息提供一个适当的回答。

    如果您无法确认信息或不清楚答案，请简单地回答“对不起，我无法提供该信息。”。
    """
    return call_llm_api(prompt)

def call_llm_for_order(user_message: str) -> dict:
    prompt = f"""
    用户想要订餐，请帮我分析以下输入，并识别用户想点的菜品及其数量。可选择的菜品包括：
    - 扬州炒饭
    - 鸡蛋炒饭
    - 牛肉面
    - 炸酱面
    - 宫保鸡丁
    - 麻婆豆腐
    - 鱼香茄子
    - 红烧肉
    - 凉拌黄瓜
    - 皮蛋豆腐
    - 夫妻肺片
    - 酸辣汤
    - 冬瓜排骨汤
    - 番茄蛋花汤
    - 春卷
    - 小笼包
    - 生煎包
    - 绿豆汤
    - 豆浆
    - 酸梅汤

    用户输入: "{user_message}"

    请生成用户选择的菜品名称，只输出菜品名称。
    如果无法识别，请回复"对不起，我不确定您的订单。请再说一遍？"
    """
    return call_llm_api(prompt)


# def call_llm_for_order(user_message: str) -> dict:
#     prompt = f"""
#     用户想要订餐，请帮我分析以下输入，并识别用户想点的菜品及其数量。可选择的菜品包括：
#     - 扬州炒饭
#     - 鸡蛋炒饭
#     - 牛肉面
#     - 炸酱面
#     - 宫保鸡丁
#     - 麻婆豆腐
#     - 鱼香茄子
#     - 红烧肉
#     - 凉拌黄瓜
#     - 皮蛋豆腐
#     - 夫妻肺片
#     - 酸辣汤
#     - 冬瓜排骨汤
#     - 番茄蛋花汤
#     - 春卷
#     - 小笼包
#     - 生煎包
#     - 绿豆汤
#     - 豆浆
#     - 酸梅汤

#     用户输入: "{user_message}"

#     请以以下结构化格式返回结果：
#     {{
#       "dish": "用户选择的菜品名称",
#       "quantity": "用户选择的数量",
#       "confidence": "识别结果的置信度（0到1之间的小数）",
#       "reason": "选择该菜品和数量的原因"
#     }}
#     如果无法识别，请返回：
#     {{
#       "dish": null,
#       "quantity": null,
#       "confidence": 0,
#       "reason": "无法理解用户的订餐请求"
#     }}
#     """
#     return call_llm_api(prompt)


def call_llm_for_confirmation(dish: str, quantity: str) -> dict:
    prompt = f"""
    用户已完成订餐，请帮我确认以下信息。用户点了以下菜品：
    - 菜品: "{dish}"
    - 数量: "{quantity}"

    请生成一条友好的确认消息，询问用户是否确认该订单。
    如果信息不完整或您无法确认订单，请回复"对不起，我无法确认您的订单信息。"
    """
    return call_llm_api(prompt)
