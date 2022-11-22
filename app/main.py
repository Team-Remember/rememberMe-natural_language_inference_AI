from fastapi import APIRouter, FastAPI
import time

from filtering import abuse_filtering
from inference import loadchat
app = FastAPI()


# 문자 챗봇
@app.get("/chat_bot")
def chatbot(memberId: int, weId: int, chatRequest: str = ''):
    print('memberId', memberId, 'weId', weId, "request,", chatRequest)
    start = time.time()

    # 욕설방지 필터링
    abuse_filter = abuse_filtering(chatRequest, 0)
    print("None 이야?", abuse_filter)

    # 욕설이 포함되었을 때 return
    if abuse_filter is not None:
        return {"response": abuse_filter, "filter": 1}

    # chatbot
    load_chat_response = loadchat(memberId, weId, chatRequest)
    sentence = load_chat_response['return_sentence']
    print(sentence)
    filtering = load_chat_response['filtering']

    if filtering == 1:
        return {"response": sentence, "filter": 1}

    chat = time.time()
    print('chat 시간', chat - start)
    return {"response": sentence, "filter": 0}


# uvicorn app.main:app --reload --host=0.0.0.0 --port=8002