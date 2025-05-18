# LLMAgent 学习
## LangChain
学习连接：[https://www.langchain.com/langchain](https://www.langchain.com/langchain)
- 简单学习怎么使用其与模型交互
- 怎么进行历史交互
- 使用模板交互
## MCP开发学习
学习连接：[https://modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)
- MCP 客户端
- MCP 服务端

在Cline之间增加代理服务器截取之间的交流信息，之间通过xml文件去调用mpc服务器

### MCP Server开发学习
## MCP 客户端
> 类似cline工具，负责与mcp server和大模型沟通，规定沟通交流的方式
## MCP 服务端
> 实现具体功能，供MCP 客户端调用，客户端通过咨询大模型确定调用哪些工具和参数

：代码不做具体实现了，大致原理是这样
