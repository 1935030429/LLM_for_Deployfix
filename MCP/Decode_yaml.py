import yaml
def Decode_yaml(file_path: str) -> str:
    """解析YAML文件，得到app, pod, node之间的依赖关系"""
    
    try:
        content = ""
        with open(file_path, "r+", encoding="ignores") as f:
            content = f.read()
        data = yaml.safe_load(content)

        res = {"metadata": data.metadata, }
        
    except Exception as e:
        raise e