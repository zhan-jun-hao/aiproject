1.封装httpxClient
2.成功调用SpringCloud的内部接口, 新增course服务
3.但是现在返回的message为""，原因是因为我们只调用了两次llm，在第二次调用的时候, 没有触发最终答案, 因为大模型知道又要调用一次tools, 所以我们下一步该做Agent Loop
4.封装用户上下文, middleware类比java的Filter进行仿造
