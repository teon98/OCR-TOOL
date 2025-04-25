import cv2
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 한글 경로 대응
def load_image_with_pil(image_path):
    pil_image = Image.open(image_path).convert("RGB")
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def draw_korean_text(img, text, position, font_path="C:/Windows/Fonts/malgun.ttf", font_size=20, color=(0, 0, 255)):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

image_path = "../documents/직원대출신청서_5개모음집_pages-to-jpg-0001.jpg"
img = load_image_with_pil(image_path)
img_display = img.copy()
temp_display = img.copy()

boxes = []  # 드래그된 박스 리스트
start_point = None
is_drawing = False

window_name = "Draw Box and Label Field (Press ESC to Save and Exit)"

def mouse_callback(event, x, y, flags, param):
    global start_point, is_drawing, temp_display, img_display

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        is_drawing = True
        print(f"📍 시작점: ({x}, {y})")

    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing:
            temp_display = img_display.copy()
            overlay = temp_display.copy()
            cv2.rectangle(overlay, start_point, (x, y), (255, 255, 153), -1)  # 하늘색 채우기
            alpha = 0.4
            cv2.addWeighted(overlay, alpha, temp_display, 1 - alpha, 0, temp_display)
            cv2.rectangle(temp_display, start_point, (x, y), (255, 0, 0), 2)  # 파란색 테두리

    elif event == cv2.EVENT_LBUTTONUP:
        if start_point:
            end_point = (x, y)
            is_drawing = False
            print(f"✅ 종료점: ({x}, {y})")
            x1, y1 = start_point
            x2, y2 = end_point

            # 네모 박스 네 꼭짓점 직접 지정
            top_left = (x1, y1)
            top_right = (x2, y1)
            bottom_left = (x1, y2)
            bottom_right = (x2, y2)

            field_name = input("Field name: ").strip()
            if field_name:
                boxes.append({
                    "field": field_name,
                    "box": {
                        "top_left": top_left,
                        "top_right": top_right,
                        "bottom_left": bottom_left,
                        "bottom_right": bottom_right
                    }
                })
                cv2.rectangle(img_display, top_left, bottom_right, (0, 255, 0), 2)
                img_display = draw_korean_text(img_display, field_name, (top_left[0], top_left[1] - 25))
            start_point = None
            temp_display = img_display.copy()

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)       # 창 조절 가능하게
cv2.resizeWindow(window_name, 1280, 900)              # 기본 크기 지정
cv2.setMouseCallback(window_name, mouse_callback)

while True:
    cv2.imshow(window_name, temp_display)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

field_template = {
    item["field"]: item["box"] for item in boxes
}

with open("field_template_boxes.json", "w", encoding="utf-8") as f:
    json.dump(field_template, f, ensure_ascii=False, indent=2)

print("\n✅ 박스 템플릿 저장 완료! (field_template_boxes.json)")
print(json.dumps(field_template, ensure_ascii=False, indent=2))
