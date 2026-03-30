"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
def print_prompt(prompt):
    '''
    打印提示词
    :param prompt: 提示词对象
    :param prompt:
    :return:
    '''
    print("="*20)
    print(prompt.to_string())
    print("-"*20)
    return prompt

class RagSummarizeService(object):
    '''
    总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
    '''

    '''
    初始化总结服务类,
    vector_store: 向量数据库服务类对象
    retriever: 向量数据库检索器对象
    prompt_text: 提示词文本
    prompt_template: 提示词模板对象
    model: 模型对象
    chain: 链对象
    '''
    def __init__(self):
        self.vector_store=VectorStoreService()
        self.retriever=self.vector_store.get_retriever()
        #把你写好的 Prompt 模板 → 转换成可动态填充的模板对象
        self.prompt_text=load_rag_prompts()
        self.prompt_template=PromptTemplate.from_template(self.prompt_text)
        # prompt = self.prompt_template.format(
        #     context=context,
        #     question=query
        # )
        self.model=chat_model
        self.chain=self.prompt_template|print_prompt|self.model|StrOutputParser()


        #输入用户问题 → 从向量库里找最相关的文档 → 返回文档列表
    def retriever_docs(self,query:str)->list[Document]:
        '''
            检索器取回相关文档
            :param self: 总结服务类对象
            :param query: 用户问题
            :return: 相关文档列表
        '''
        return self.retriever.invoke(query)

    def rag_summarize(self,query:str)->str:
        '''
            RAG基本流程
            :param self: 总结服务类对象
            :param query: 用户问题
            :return: 模型回答
        '''
        context_docs=self.retriever_docs(query)# 检索器取回相关文档
        context=""
        counter=0# 记录已处理的文档数量

        for doc in context_docs:
            counter+=1
            context +=f"【参考资料{counter}】: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"

            return self.chain.invoke(
                {
                    "input":query,
                    "context":context,
                }
            )


# if __name__ == '__main__':
#     rag = RagSummarizeService()
#
#     print(rag.rag_summarize("小户型适合哪些扫地机器人"))
