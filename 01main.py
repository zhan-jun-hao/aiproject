from fastapi import FastAPI
from pydantic import BaseModel

# requestDto
class ChatRequest(BaseModel):
    question: str

# responseDto
class ChatResponse(BaseModel):
    answer: str
    code: int

# 容器启动
app = FastAPI()

'''
    1.get接口请求示例
    2.字典返回值自动转换成json
    3.接口文档是 /docs 可以try it out 非常方便
'''
@app.get("/")
def hello():
    return {"message": "Hello FastAPI"}

'''
    post接口请求示例
'''
@app.post("/chat1")
def chat(request: ChatRequest):
    return {
        "answer": f"你问的是：{request.question}"
    }

@app.post("/chat2", response_model=ChatResponse)
def chat(request: ChatRequest):
    return ChatResponse(
        answer=f"你问的是：{request}",
        code=200
    )

# 对应spring的 @Pathvariable
@app.get("/courses/{id}")
def get_course(id: int):
    return {
        "id": id
    }

# Query参数
@app.get("/courses")
def courses(keyword: str, page: int):
    return {
        "keyword": keyword,
        "page": page
    }

