from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import requests
import uvicorn
import json
from typing import Dict, Any
from AppLogger import AppLogger

app = FastAPI(title="Ollama中间转发服务", description="在Client和Ollama之间转发请求和响应")

# 配置Ollama服务地址
OLLAMA_BASE_URL = "http://localhost:11434"

# 日志打印 只支持一次会话
logger = AppLogger()

# message计数器
message_num = 0

@app.post("/api/chat")
async def chat_proxy(request: Request):
    """
    转发聊天请求到Ollama服务，并返回响应
    支持普通请求和流式请求两种模式
    """
    # 声明全局变量
    global message_num
    # 获取客户端请求数据
    client_data = await request.json()

    logger.log("\ncline请求：\n")
    if 'messages' in client_data:
        for i in range(message_num, len(client_data['messages'])):
            role = client_data['messages'][i]['role']
            content = client_data['messages'][i]['content']
            logger.log(f"{role}:\n{content}\n")
        message_num = len(client_data['messages'])

    logger.log("\n模型返回：\n")
    logger.log("\nassistant：\n")
    # 构建Ollama请求
    ollama_url = f"{OLLAMA_BASE_URL}/api/chat"
    headers = {"Content-Type": "application/json"}
    
    # 判断是否为流式请求
    is_stream = client_data.get("stream", False)
    
    try:
        message_num = message_num + 1
        if is_stream:
            # 流式响应处理
            return StreamingResponse(
                _stream_generator(ollama_url, headers, client_data),
                media_type="text/event-stream"
            )
        else:
            # 普通响应处理
            response = requests.post(ollama_url, headers=headers, json=client_data)
            return Response(content=response.content, status_code=response.status_code)
            
    except Exception as e:
        return {"error": str(e)}, 500

def _stream_generator(url: str, headers: Dict[str, str], data: Dict[str, Any]):
    """
    生成流式响应内容
    """
    try:
        with requests.post(url, headers=headers, json=data, stream=True) as response:
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    # 处理SSE格式数据
                    # 解析JSON
                    chunk = json.loads(line)
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        logger.log(content)
                    yield line.decode('utf-8') + "\n"
                    
    except Exception as e:
        # 错误处理，返回错误信息
        error_msg = json.dumps({"error": str(e)})
        yield f"data: {error_msg}\n\n"



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)