'''
这份 agent_tools.py 干了 4 件事：

定义了一组可被 Agent 调用的工具
模拟了一些外部能力，比如天气、用户位置、用户ID、月份
从外部数据文件里读取用户使用记录
给“生成使用报告”这个业务场景提供上下文支撑
'''

import os
import random
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path



rag=RagSummarizeService()
user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]
month_arr = [
    "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
    "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
]
external_data={}


@tool
def rag_summarize(query:str)->str:
    '''
    从向量库里检索最相关的文档，然后总结成一个字符串。
    :param query: 用户的问题
    :return: 模型总结的字符串
    '''
    return rag.rag_summarize(query)
# @tool
# def get_weather(city:str)->str:
#     return f"{city}的天气是晴朗的,温度在25摄氏度左右
def generate_external_data()->None:
    '''
    生成外部数据
    :return: None
    '''
    if not external_data:
        external_data_path=get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"{external_data_path} not exists")

    with open(external_data_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader)  # 跳过表头

        for row in reader:
            '''
            "用户ID","特征","饮食情况","营养摄入","健康对比","时间"
            '''

            user_id = row[0]
            feature = row[1]
            diet = row[2]  # 原 清洁效率 → 饮食情况
            nutrition = row[3]  # 原 耗材 → 营养摄入
            comparison = row[4]  # 对比 → 健康对比
            time = row[5]

            if user_id not in external_data:
                external_data[user_id] = {}

            external_data[user_id][time] = {
                "用户画像": feature,
                "饮食情况": diet,
                "营养摄入": nutrition,
                "健康对比": comparison,
            }


@tool
def fetch_external_data(input_text:str)->str:
    '''
    从外部系统中获取指定用户在指定月份的使用记录。输入格式：user_id,month
    :param input_text: 用户的问题
    :return: 用户使用记录
    :return:
    '''
    try:
        user_id, month = [x.strip() for x in input_text.split(",", 1)]
        return str(external_data[user_id][month])
    except ValueError:
        logger.warning("[fetch_external_data] 输入格式错误，应为：user_id,month")
        return "输入格式错误，请使用：user_id,month"
    except KeyError:
        logger.warning(f"[fetch_external_data] 未能检索到输入 {input_text} 对应的使用记录数据")
        return ""


@tool
def fill_context_for_report(input_text: str) -> str:
    """触发报告生成场景的上下文补全。任意输入即可，例如：report"""
    return "fill_context_for_report已调用"



@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息，并以字符串形式返回。"""
    return f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风1级，AQI21，最近6小时降雨概率极低"


@tool
def get_user_location(input_text: str) -> str:
    """获取用户所在城市名称。输入任意字符串即可。"""
    return random.choice(["深圳", "合肥", "杭州"])


@tool
def get_user_id(input_text: str) -> str:
    """获取用户ID。输入任意字符串即可。"""
    return random.choice(user_ids)


@tool
def get_current_month(input_text: str) -> str:
    """获取当前月份。输入任意字符串即可。"""
    return random.choice(month_arr)
