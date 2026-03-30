import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"



from langchain_core.documents import Document
from langchain_chroma import Chroma
from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger

class VectorStoreService:
    '''
    向量存储服务类：负责存储和检索向量
    '''
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"],
        )
        #文本切分器（最常用、最智能的一种）
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )

    def get_retriever(self):
        '''
            获取检索器
            :param self:
            :return:
        '''
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        '''
            加载文档,从数据文件夹内读取数据文件，转为向量存入向量库
            要计算文件的MD5做去重
            :param self:
            :return:
        '''

        def check_md5_hex(md5_for_check:str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False#创建文件,返回False
            #读取md5文件，看看有没有一样的
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if line.strip()==md5_for_check:
                        return True
                return False

        def save_md5_hex(md5_for_check:str):
            '''
                保存MD5值到文件
                :param md5_for_check: 要保存的MD5值
                :return:
            '''
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check+"\n")

        def get_file_document(read_path:str):
            '''
                获取文件的文档:txt\pdf
                :param read_path: 文件路径
                :return:
            '''
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)

            return []

        # 获取允许的文件路径
        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            # 获取文件的MD5值
            md5_hex = get_file_md5_hex(path)
            # 检查是否重复
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]:文件已存在{path},跳过")
                continue

            try:
                documents: list[Document] = get_file_document(path)

                # 如果文档为空，跳过
                if not documents:
                    logger.warning(f"[加载知识库]:{path}内没有有效文本内容,跳过")
                    continue

                # 把原始文档 → 切成一堆小 Document（适合做 embedding）
                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]:{path}内没有有效文本内容,跳过")
                    continue

                # 分批添加向量到向量库，避免 embedding 接口单次超过 10 条
                batch_size = 10

                for i in range(0, len(split_document), batch_size):
                    batch_docs = split_document[i:i + batch_size]
                    self.vector_store.add_documents(batch_docs)

                # 保存MD5值到文件
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库]:{path}成功")
            except Exception as e:
                logger.error(f"[加载知识库]:{path}失败{e}")
                continue

if __name__ == '__main__':
    vs = VectorStoreService()

    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("烧烤")
    for r in res:
        print(r.page_content)
        print("-"*20)
