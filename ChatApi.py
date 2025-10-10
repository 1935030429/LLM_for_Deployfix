from openai import OpenAI

class ChatModel():
    def __init__(self, modelname: str):
        self.modelname = modelname
        self.client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key='ms-0fedd531-837c-41a2-8502-d3d975912425', # ModelScope Token
        )
        self.history = []
    
    def build_prompt(self, parsed_yaml: str) -> str:
        """构建提示词（包含论文错误类型定义，确保模型输出符合要求）"""
        # 论文中定义的常见错误类型（用于引导模型识别）
        paper_error_types = """
        1. 约束冲突（如：appA requires appB，appB requires HPN，appA excludes HPN）；
        2. 无效标签（如：nodeSelector引用不存在的标签，拼写错误）；
        3. 语法错误（如：YAML缩进错误、关键字拼写错误）；
        4. 循环依赖（如：appA requires appB，appB requires appA）；
        5. 约束冗余（如：重复定义相同的affinity规则）。
        """
        
        # 提示词模板（明确输出格式：错误类型、位置、修复方法）
        prompt = f"""
        你是针对于k8s与apache集群架构的配置错误检测专家。
        请分析以下Kubernetes YAML配置的解析结果，完成3件事：
        1. 识别错误类型（参考错误类型：{paper_error_types}）；
        2. 定位错误位置（文件路径+行号，优先使用line_mapping中的行号）；
        3. 提供修复方法（优先保留高优先级应用约束，删除冲突的低优先级约束；或修正无效标签）。

        注意：需结合 Kubernetes 调度逻辑（如 nodeAffinity、podAffinity 生效规则），优先保障高优先级应用（若配置中存在 priorityClassName）的可用性。

        若检测到错误,输出“#Error#”
        输出格式要求（要求描述为json格式）：
        - 错误类型：[具体错误类型，如约束冲突]
        - 错误位置：[文件路径：行号，如_config/app1.yaml：15]
        - 错误原因：[简要说明错误根源]
        - 修复方法：[如删除appA的excludes HPN约束]
        - 修复后的yaml文件: [按照修复方案修改的yaml文件内容]

        若未检测到错误，请输出“#NoError#：未检测到定义的部署错误”。

        接下来，我将给出相应的若干关联的yaml文件
        """
        #prompt = "请提取出yaml文件中所有的依赖关系作为Json格式输出"
        self.history.append({
                    'role': 'system',
                    'content': prompt
                })
        self.history.append({
            'role': 'user',
            'content': "yaml配置为：{}".format(parsed_yaml)
        })

    def createChat(self):
        response = self.client.chat.completions.create(
            model=self.modelname,
            messages=self.history,
            stream=False
        )
        return response