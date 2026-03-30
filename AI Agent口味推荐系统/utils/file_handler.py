import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from utils.logger_handler import logger
import hashlib


chunk_size=4096
def get_file_md5_hex(filepath:str):
    '''
    获取文件的MD5值
    :param filepath: 文件路径
    :return: 文件的MD5值:16进制字符串
    '''

    if not os.path.exists(filepath):
        logger.error(f"[md5计算]:文件不存在{filepath}")
        return
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]:{filepath}不是文件")
        return

    #在创建一个 MD5 哈希对象
    md5_obj=hashlib.md5()

    try:
        #文件读取的标准写法（尤其是处理二进制/大模型项目必备）
        #"rb"：以二进制读取模式打开
        with open(filepath,"rb")as f:
            #分块读取文件 + 计算 MD5
            while chunk:=f.read(chunk_size):
                md5_obj.update(chunk)
                """
                chunk = f.read(chunk_size)
                while chunk:

                    md5_obj.update(chunk)
                    chunk = f.read(chunk_size)
                """
            md5_hex=md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"[md5计算]:{filepath}计算md5失败{e}")
        return None

def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    """
    列出指定目录下的所有文件，并筛选出指定类型的文件
    :param path: 目录路径
    :param allowed_types: 允许的文件类型，如：('.jpg', '.png')
    :return: 筛选后的文件列表
    """
    files=[]
    if not os.path.exists(path):
        logger.error(f"[listdir_with_allowed_type]:目录不存在{path}")
        return []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]:{path}不是文件夹")
        return []

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f))

    return tuple(files)

def pdf_loader(filepath: str, passwd=None) -> list[Document]:
    '''
    加载PDF文件
    :param filepath: PDF文件路径
    :param passwd: PDF文件密码
    :return: 加载后的文档列表
    '''
    return PyPDFLoader(filepath, passwd).load()

def txt_loader(filepath: str) -> list[Document]:
    '''
    加载文本文件
    :param filepath: 文本文件路径
    :return: 加载后的文档列表
    '''
    return TextLoader(filepath, encoding="utf-8").load()