# OCR-TOOL 조사

## 1) GPT 4o Multimodal 사용
- OpenAI 4o model.ipynb: GPT 4o 멀티모달 자체 사용 (✅손글씨 인식률 좋음)
- LangChain + LangSmith.ipynb: LangChain Prompt 사용(1회 요청당 7원 소요)
- Agent 확장성 있음

## 2) EasyOCR
- EasyOCR.ipynb (⚠️손글씨 인식률 중간)
- createXY2.py: tkinter로 field 영역 좌표 추출 -> 관리자가 field 영역 지정 시 EasyOCR에서 추출된 box 좌표값으로 자동 field 지정 가능

## 3) PaddleOCR (중국 모델)
- PaddleOCR.ipynb (⚠️손글씨 인식률 중간, 개인적으로 EasyOCR 보다 안좋음)
- createXY2.py로 추출한 field area로 field 자동 맵핑 가능