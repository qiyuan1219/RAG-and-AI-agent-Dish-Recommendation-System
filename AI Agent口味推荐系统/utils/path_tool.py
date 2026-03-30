import os

def get_project_root()->str:
    '''
    获取项目根目录
    :return: 项目根目录
    '''
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    '''
    # 当前文件绝对路径
    current_file_abs_path=os.path.abspath(__file__)
    # 当前文件所在目录
    current_dir=os.path.dirname(current_file_abs_path)
    # 项目根目录
    project_root=os.path.dirname(current_dir)
    
    return project_root
    '''

def get_abs_path(relative_path:str)->str:
    """
        传递相对路径，得到绝对路径
        :param relative_path: 相对领
        :return: 绝对路径
    """
    return os.path.join(get_project_root(),relative_path)


'''
if __name__ == '__main__':
    print(get_abs_path("config/config.txt"))
#D:\Project_Package\PythonProject\AI Agent口味推荐系统\config/config.txt
'''
