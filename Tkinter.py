import tkinter as tk
from tkinter import ttk

class AppleStyleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Sensor Dashboard")
        self.geometry("420x300")
        self.configure(bg="#e9ecf0")
        self.resizable(True, True)

        self.setup_style()
        self.create_widgets()
        
    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("Card.TFrame", background="white", borderwidth=0, relief="flat")
        style.configure("Title.TLabel", font=("SF Pro Display", 18, "bold"), background="white", foreground="#222")
        style.configure("Info.TLabel", font=("SF Pro Text", 14), background="white", foreground="#555")
        style.configure("Value.TLabel", font=("SF Pro Text", 16, "bold"), background="white")
        style.configure("Bar.Horizontal.TProgressbar", troughcolor="#e0e0e0", borderwidth=0, background="#4f94ef")

    def create_widgets(self):
        # 카드 프레임
        self.card = ttk.Frame(self, style="Card.TFrame", padding=20)
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # 타이틀
        self.title_label = ttk.Label(self.card, text="Smart Sensor", style="Title.TLabel")
        self.title_label.pack(pady=(0, 15))

        # 감지 여부
        self.detect_label = ttk.Label(self.card, text="사람 감지됨: 없음", style="Info.TLabel")
        self.detect_label.pack()

        self.detect_state = ttk.Label(self.card, text="● Not Detected", style="Value.TLabel", foreground="red")
        self.detect_state.pack(pady=(0, 15))

        # 밝기
        self.brightness_label = ttk.Label(self.card, text="LED 밝기", style="Info.TLabel")
        self.brightness_label.pack()

        self.progress = ttk.Progressbar(self.card, style="Bar.Horizontal.TProgressbar", orient="horizontal",
                                        length=250, mode="determinate", maximum=100)
        self.progress.pack(pady=5)

        self.brightness_value = ttk.Label(self.card, text="0%", style="Value.TLabel")
        self.brightness_value.pack()

    def update_ui(self,person_detected:bool,brightness:int):
        # 감지 상태 업데이트
        if person_detected:
            self.detect_label.config(text="사람 감지됨: 있음")
            self.detect_state.config(text="● Detected", foreground="#28a745")  # 초록
        else:
            self.detect_label.config(text="사람 감지됨: 없음")
            self.detect_state.config(text="● Not Detected", foreground="red")

        # 밝기 업데이트
        self.progress['value'] = brightness
        self.brightness_value.config(text=f"{brightness}%")
