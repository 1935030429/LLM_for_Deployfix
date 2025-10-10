import os
def FindAllYamlData() -> str:
    """在_config文件夹下找到所有yaml文件数据，然后送给大模型解析   此函数参数为空，返回包含所有yaml文件拼接的字符串
       params: void
       return str
    """
    yamls = []
    if not os.path.exists('_config'):
            raise FileNotFoundError(f"目录 _config 不存在")
    
    for root, _, files in os.walk('_config'):
        for file in files:
            if file.endswith((".yaml", ".yml")):
                file_path = os.path.join(root, file)
                file_name =os.path.basename(file_path)
                with open(file_path, "r") as f:
                    yaml_data = f.read()
                data = {
                    "yaml_name": file_name,
                    "yaml_content": yaml_data
                }
                parsed_data = data
                if parsed_data:
                    yamls.append(parsed_data)

    structured_parts = ["# 集群YAML文件结构化文本（所有文件关联信息）"]

    # 遍历每个「文件名-内容」字典，添加到字符串
    for idx, yaml_dict in enumerate(yamls, 1):
        yaml_name = yaml_dict["yaml_name"]
        yaml_content = yaml_dict["yaml_content"]

        # 每个文件的格式：序号 + 文件名 + 分隔线 + YAML内容
        structured_parts.append(f"## {idx}. 文件：{yaml_name}")
        structured_parts.append(f"--- 文件名分隔线 ---")
        structured_parts.append(f"YAML内容：\n{yaml_content}")
        structured_parts.append(f"--- 结束分隔线 ---\n")

    # 合并所有部分为最终字符串
    return "\n".join(structured_parts)