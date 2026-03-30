import yaml
from utils.path_tool import get_abs_path

def load_yaml_config(config_name:str,encoding:str="utf-8"):
    # 获取配置文件路径
    config_path = get_abs_path(f"config/{config_name}.yml")

    with open(config_path,"r",encoding=encoding) as f:
        return yaml.load(f,Loader=yaml.FullLoader)

# ================== 具体配置 ==================
rag_conf = load_yaml_config("rag")
chroma_conf = load_yaml_config("chroma")
prompts_conf = load_yaml_config("prompts")
agent_conf = load_yaml_config("agent")