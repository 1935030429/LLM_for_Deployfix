#from transformers import AutoModelForCausalLM

from ChatApi import ChatModel
import logging
from MCP.filecontrol import FileEx
from OpenAi import OpenAi

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

fileCon = FileEx(logger=logger, dir_path="_config")

model_list = ["", 'Qwen/Qwen3-235B-A22B-Instruct-2507', "Qwen/Qwen3-Next-80B-A3B-Thinking", "deepseek-ai/DeepSeek-V3.1-Terminus","Qwen/Qwen3-Coder-480B-A35B-Instruct"]
chat = ChatModel(model_list[0])
prompt = fileCon.yamls_parse()
chat.build_prompt(prompt)

if __name__ == '__main__':
    #userinput = input('用户输入：')
    
        OpenAi()._output(chat.history)
        # res = chat.createChat()
        # output = res.choices[0].message.content
        # print(output)
        # -------
        # for chunk in res:
        #     print(chunk.choices[0].delta.content, end="", flush=True)
        #     print("\n")