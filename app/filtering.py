import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np
import os

USE_GPU = os.getenv('USE_GPU', 0)
if USE_GPU == 0:
    ep = ['CPUExecutionProvider']
else:
    ep = ['CUDAExecutionProvider', 'CPUExecutionProvider']

model_name = 'beomi/kcbert-base'
tokenizer = AutoTokenizer.from_pretrained(model_name)
unsmile_labels = ['여성/가족', '남성', '성소수자', '인종/국적', '연령', '지역', '종교', '기타 혐오', '악플/욕설', 'clean']
abuse_filter = ort.InferenceSession('../models/abuse_filtering_model.onnx', providers=ep)


def abuse_filtering(text, text_or_voice):
    encoded_input = tokenizer(text, return_tensors='pt')
    encoded_input = {name: np.atleast_2d(value) for name, value in encoded_input.items()}

    inference = abuse_filter.run(None, encoded_input)[0][0]
    inference_max = inference.max()
    inference_max_index = inference.argmax(0)
    print(inference_max, inference_max_index)
    if inference_max > 1.03 and inference_max_index < 9 and text_or_voice == 0:
        return unsmile_labels[inference_max_index] + '에 대한 내용이 담겨있습니다. 다른 문장을 입력해주세요!'
    elif inference_max > 1.03 and inference_max_index < 9 and text_or_voice == 1:
        return unsmile_labels[inference_max_index] + '에 대한 내용이 담겨있습니다. 다른 문장을 말씀해주세요!'
    return None

