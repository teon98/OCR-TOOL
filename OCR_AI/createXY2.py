import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import json

# === 설정 ===
image_path = "../documents/직원대출신청서_5개모음집_pages-to-jpg-0001.jpg"
img = Image.open(image_path)
boxes = []  # 저장될 필드 정보
start_x = start_y = 0
rect_id = None

# === 이벤트 핸들러 ===
def on_mouse_down(event):
    global start_x, start_y, rect_id
    start_x, start_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y,
                                      outline='blue', width=2, fill='#CCEEFF', stipple='gray50')

def on_mouse_drag(event):
    if rect_id:
        curr_x, curr_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        canvas.coords(rect_id, start_x, start_y, curr_x, curr_y)

def on_mouse_up(event):
    global rect_id
    end_x, end_y = canvas.canvasx(event.x), canvas.canvasy(event.y)

    field = simpledialog.askstring("필드명 입력", "이 박스의 필드명은?")
    if field:
        box = {
            "top_left": [int(start_x), int(start_y)],
            "top_right": [int(end_x), int(start_y)],
            "bottom_left": [int(start_x), int(end_y)],
            "bottom_right": [int(end_x), int(end_y)]
        }
        boxes.append({"field": field, "box": box})
        canvas.create_text(start_x + 5, start_y - 10, text=field, anchor="nw", fill="red")

    rect_id = None

# === 저장 ===
def save_json():
    if not boxes:
        print("❌ 저장할 박스가 없음")
        return
    output = {item['field']: item['box'] for item in boxes}
    with open("field_template_boxes.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("✅ field_template_boxes.json 저장 완료!")

# === Tkinter 기본 설정 ===
root = tk.Tk()
root.title("📐 OCR 필드 지정기 (Tkinter with Scroll)")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

canvas = tk.Canvas(frame, width=1000, height=800, bg='white', scrollregion=(0, 0, img.width, img.height))
canvas.pack(side="left", fill="both", expand=True)

hbar = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
hbar.pack(side="bottom", fill="x")
vbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
vbar.pack(side="right", fill="y")
canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

img_tk = ImageTk.PhotoImage(img)
canvas.create_image(0, 0, anchor="nw", image=img_tk)

canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)

save_btn = tk.Button(root, text="💾 JSON 저장하기", command=save_json)
save_btn.pack(pady=10)

root.mainloop()