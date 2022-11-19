from logging import getLogger
from fastapi import APIRouter
import time

from ml.filtering import abuse_filtering
from ml.inference import loadchat

logging = getLogger(__name__)
router = APIRouter()


# 문자 챗봇
@router.get("/chat_bot")
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

