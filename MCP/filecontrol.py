import logging
from typing import Optional, List
import os

class FileEx():
    def __init__(self, logger: logging.Logger, dir_path: str):
        self.logger = logger
        self.yamls: List = []
        self.dir_path = dir_path

    def yamls_parse(self) -> str:
        self.parse_yamls(self.dir_path)
        return self._list_to_formatted_str()

    def _list_to_formatted_str(self) -> str:
        if not self.yamls:
            return "无有效YAML文件可转换"

        # 构建结构化字符串（带清晰格式）
        structured_parts = ["# 集群YAML文件结构化文本（所有文件关联信息）"]

        # 遍历每个「文件名-内容」字典，添加到字符串
        for idx, yaml_dict in enumerate(self.yamls, 1):
            yaml_name = yaml_dict["yaml_name"]
            yaml_content = yaml_dict["yaml_content"]

            # 每个文件的格式：序号 + 文件名 + 分隔线 + YAML内容
            structured_parts.append(f"## {idx}. 文件：{yaml_name}")
            structured_parts.append(f"--- 文件名分隔线 ---")
            structured_parts.append(f"YAML内容：\n{yaml_content}")
            structured_parts.append(f"--- 结束分隔线 ---\n")

        # 合并所有部分为最终字符串
        return "\n".join(structured_parts)

    def _parse_single_yaml(self, file_path: str) -> dict:
        """解析单个YAML文件，提取关键配置和行号"""
        try:
            with open(file_path, "r") as f:
                yaml_data = f.read()
            
            file_name =os.path.basename(file_path)
            return {
                "yaml_name": file_name,
                "yaml_content": yaml_data
            }
        except PermissionError:
            self.logger.error(f"权限不足，无法读取文件：{file_path}")
            return None
        except Exception as e:
            self.logger.error(f"处理文件失败：{file_path}，错误：{str(e)}")
            return None

    
    def _find_config_line(self, yaml_lines: List[str], keyword: str) -> int:
        """查找关键字在YAML中的行号（从1开始）"""
        for line_num, line in enumerate(yaml_lines, 1):
            if line.strip().startswith(keyword):
                return line_num
        return -1  # 未找到

    def parse_yamls(self, yaml_dir: str) -> List[dict]:
        """解析_config目录下所有YAML文件，建立集群级关联数据"""
        if not os.path.exists(yaml_dir):
            self.logger.error(f"YAML目录不存在：{yaml_dir}")
            raise FileNotFoundError(f"目录 {yaml_dir} 不存在")

        # 第一步：批量解析所有YAML文件
        for root, _, files in os.walk(yaml_dir):
            for file in files:
                if file.endswith((".yaml", ".yml")):
                    file_path = os.path.join(root, file)
                    parsed_data = self._parse_single_yaml(file_path)
                    if parsed_data:
                        self.yamls.append(parsed_data)