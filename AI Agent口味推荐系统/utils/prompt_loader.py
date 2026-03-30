from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

def load_prompt(config_key:str,desc:str)->str:
    try:
        prompt_path=get_abs_path(prompts_conf[config_key])
    except KeyError:
        logger.error(f"[load_prompt] yaml中缺少配置项: {config_key}")
        raise

    try:
        with open(prompt_path,"r",encoding="utf-8")as f:
            return f.read()
    except Exception as e:
        logger.error(f"[load_prompt] 加载{desc}失败: {e}")
        raise


# ================== 对外接口 ==================

def load_system_prompts():
    return load_prompt("main_prompt_path", "系统提示词")


def load_rag_prompts():
    return load_prompt("rag_summarize_prompt_path", "RAG总结提示词")


def load_report_prompts():
    return load_prompt("report_prompt_path", "报告生成提示词")



# if __name__ == '__main__':
#     print(load_report_prompts())