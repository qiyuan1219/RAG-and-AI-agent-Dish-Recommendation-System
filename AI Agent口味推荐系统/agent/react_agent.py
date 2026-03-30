'''
这段代码是在封装一个 基于 LangChain 的 ReAct 智能体。
它的作用是：

把大模型、工具、系统提示词组装起来，让模型能够“先思考，再决定调用哪个工具，最后给出答案”。

用户问题
   ↓
ReactAgent.execute_stream()
   ↓
Agent.invoke({"input": query})
   ↓
大模型读取系统提示词 + 工具描述
   ↓
决定是否调用工具
   ↓
工具返回结果
   ↓
大模型整合成最终答案
   ↓
返回 output



'''
"""
新版 ReactAgent（基于 LangChain 新架构）

特点：
- 使用 create_react_agent（替代 initialize_agent）
- 支持自定义 system_prompt
- 兼容工具调用
- 结构清晰，适合后续升级 LangGraph
"""

from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.prompts import PromptTemplate

from model.factory import chat_model
from utils.prompt_loader import load_system_prompts

from agent.tools.agent_tools import (
    rag_summarize,
    get_weather,
    get_user_location,
    get_user_id,
    get_current_month,
    fetch_external_data,
    fill_context_for_report,
)


class ReactAgent:
    def __init__(self):
        # ✅ 工具列表
        self.tools = [
            rag_summarize,
            get_weather,
            get_user_location,
            get_user_id,
            get_current_month,
            fetch_external_data,
            fill_context_for_report,
        ]

        # ✅ 系统提示词
        self.system_prompt = load_system_prompts()

        # ✅ 新版 Prompt（必须包含 agent_scratchpad）
        self.prompt = PromptTemplate.from_template(
            self.system_prompt
            + """


你可以使用以下工具：

{tools}

可用工具名称：
{tool_names}

请根据用户问题选择合适的工具进行回答。

用户问题：
{input}

思考过程：
{agent_scratchpad}

"""
        )

        # ✅ 创建 ReAct Agent
        self.agent = create_react_agent(
            llm=chat_model,
            tools=self.tools,
            prompt=self.prompt,
        )

        # ✅ 执行器（负责运行 Agent）
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def execute_stream(self, query: str):
        """
        执行用户请求（当前为伪流式）
        """

        try:
            result = self.agent_executor.invoke({"input": query})

            # 兼容返回格式
            output = ""
            if isinstance(result, dict):
                output = result.get("output", "")
            else:
                output = str(result)

            if output:
                yield output.strip() + "\n"

        except Exception as e:
            yield f"[ReactAgent Error]: {str(e)}\n"