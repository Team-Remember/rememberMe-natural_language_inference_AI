## 챗봇 추론파이프라인
![voice pipeline](https://github.com/Team-Remember/rememberMe-natural_language_train_AI/blob/main/img/nl%20pipeline.png)
- **모델 : Bert**
- **문장 생성 모델**인 lstm이나 GPT등 다양한 모델을 시도해보았으나, **데이터가 부족하여 완전한 문장을 추론하지 못하므로 Bert 모델을 선택**하게 되었습니다.
- 개인별 챗봇 데이터를 추론을 빠르게 하기 위하여 elasticsearch에 챗봇 문자 데이터와 임베딩 데이터를 저장하여 추론시 사용합니다.
- 검색 엔진 elasticsearch를 사용하여 추론시간을 **5초에서 0.5초**로 단축하였습니다.
- **욕설 방지 필터링**을 통하여 입력된 문자가 욕설을 포함할 경우 **onnx runtime 엔진**이 필터처리를 하도록 하였습니다.
