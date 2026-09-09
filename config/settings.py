import os

from dotenv import load_dotenv


# 加载项目 .env
load_dotenv()


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE")

ALIYUN_BAI_LIAN = os.getenv("ALIYUN_BAI_LIAN")
ALIYUN_API_BASE = os.getenv("ALIYUN_API_BASE")


# 启动时检查必要配置
if not DEEPSEEK_API_KEY:
    raise RuntimeError("缺少环境变量 DEEPSEEK_API_KEY")

if not DEEPSEEK_API_BASE:
    raise RuntimeError("缺少环境变量 DEEPSEEK_API_BASE")

if not ALIYUN_BAI_LIAN:
    raise RuntimeError("缺少环境变量 ALIYUN_BAI_LIAN")

if not ALIYUN_API_BASE:
    raise RuntimeError("缺少环境变量 ALIYUN_API_BASE")