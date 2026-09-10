# 技术栈
fastapi + langchain
# 架构方式
1.与微服务SpringCloudAlibaba配合, 此服务也相当于一个微服务
2.对于内部调用，如Tools：使用httpx.client进行请求, 由于内部鉴权的存在, 需要手动把internal密钥放进请求头进行验证
