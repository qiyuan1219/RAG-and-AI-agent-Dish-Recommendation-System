'''
Agent 运行过程中的“中间层控制”
也就是：监控工具调用、模型调用前打日志、根据上下文动态切换 Prompt。
它本质上属于 Agent 的 middleware（中间件）/ hook（钩子）层。


1. monitor_tool

监控每一次工具调用

2. log_before_model

在模型调用前打印日志

3. report_prompt_switch

根据当前上下文，动态切换不同的系统提示词


用户请求
  ↓
Agent开始运行
  ↓
[中间件] 监控工具调用
[中间件] 模型调用前打日志
[中间件] 动态决定这次用哪个Prompt
  ↓
模型/工具继续执行
'''

from typing import Callable

#load_system_prompts()：普通系统提示词
#load_report_prompts()：报告场景专用提示词
from utils.prompt_loader import load_system_prompts, load_report_prompts


'''
wrap_tool_call
包装工具调用
相当于：在真正执行 tool 前后，插入你自己的逻辑

before_model
模型调用前钩子
相当于：在 LLM 真正执行前，让你先做一些事情

dynamic_prompt
动态提示词钩子
相当于：每次模型生成前，不固定写死 Prompt，而是临时决定这次该用哪个 Prompt

AgentState
Agent 当前运行状态
里面通常会有：
消息列表 messages
历史上下文
工具结果等状态信息

ToolCallRequest
工具调用请求对象
里面包含：
工具名
参数
runtime
当前上下文等信息

ModelRequest
模型调用请求对象
用于动态生成 Prompt 时获取：
当前运行时
上下文
状态信息
'''
from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest

'''
ToolMessage：工具调用后的消息对象
Runtime：整个执行过程中的运行时信息
Command：LangGraph 里更高级的流程控制返回值
'''
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command


#不直接执行 tool，而是先经过 monitor_tool 这一层
#monitor_tool -> handler(request) -> 真正的工具函数
@wrap_tool_call
def monitor_tool(
        # 工具调用请求
        request:ToolCallRequest,
        # 工具调用处理函数
        handler:Callable[[ToolCallRequest],ToolMessage|Command]
)->ToolMessage|Command:
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e

@before_model
def log_before_model(
        state: AgentState,          # 整个Agent智能体中的状态记录
        runtime: Runtime,           # 记录了整个执行过程中的上下文信息
):         # 在模型执行前输出日志
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息。")

    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")

    return None


@dynamic_prompt                 # 每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):     # 动态切换提示词
    is_report = request.runtime.context.get("report", False)
    if is_report:               # 是报告生成场景，返回报告生成提示词内容
        return load_report_prompts()

    return load_system_prompts()