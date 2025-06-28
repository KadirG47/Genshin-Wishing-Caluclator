import tkinter as tk
from tkinter import ttk
import json
import os

NAVY = "#203A56"
BTN_BG = "#28446A"
BTN_FG = "#FFD700"
BTN_BG_ACTIVE = "#345B89"
OFFWHITE = "#E5E5E5"
TITLE_FONT = ("Cinzel", 36, "bold")
LABEL_FONT = ("Segoe UI", 18)
BTN_FONT = ("Segoe UI", 16, "bold")
DROPDOWN_FONT = ("Segoe UI", 20)

DATA_DIR = os.path.join(os.path.expanduser("~"), ".genshin_wish_data")
os.makedirs(DATA_DIR, exist_ok=True)

def user_file(username):
    return os.path.join(DATA_DIR, f"{username}.json")

def default_data():
    return {
        "Limited": {"5star_pity": 0, "won_5050": False, "guaranteed": False},
        "Weapon": {"5star_pity": 0, "fate_points": 0},
        "Standard": {"5star_pity": 0}
    }

def load_data(username):
    path = user_file(username)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default_data()

def save_data(username, data):
    path = user_file(username)
    with open(path, "w") as f:
        json.dump(data, f)

class WishCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genshin Wish Calculator")
        self.geometry("900x650")  # Bigger window
        self.resizable(False, False)
        self.configure(bg=NAVY)
        self.username = "default_user"
        self.data = load_data(self.username)
        self.banner = tk.StringVar(value="Limited")
        self.notification_label = None
        self._5050_dialog_open = False
        self._create_widgets()
        self._show_banner()
        self._apply_genshin_style()

    def _create_widgets(self):
        top_frame = tk.Frame(self, bg=NAVY)
        top_frame.pack(fill="x", pady=(24, 0))

        try:
            import tkinter.font as tkFont
            genshin_font = tkFont.Font(family="Cinzel", size=36, weight="bold")
        except Exception:
            genshin_font = ("Segoe UI", 36, "bold")
        self.title_label = tk.Label(
            top_frame, text="Genshin Wish Calculator", bg=NAVY, fg=BTN_FG, font=genshin_font
        )
        self.title_label.pack(side="left", padx=40)

        banner_selector = ttk.Combobox(
            top_frame, values=["Limited", "Weapon", "Standard"],
            state="readonly", textvariable=self.banner, font=DROPDOWN_FONT, width=18
        )
        banner_selector.pack(side="right", padx=60, ipadx=20, ipady=10, pady=10)
        banner_selector.bind("<<ComboboxSelected>>", lambda e: self._show_banner())

        self.content = tk.Frame(self, bg=NAVY)
        self.content.pack(fill="both", expand=True, pady=(40, 20))

        self.banner_frames = {}
        for banner in ["Limited", "Weapon", "Standard"]:
            frame = tk.Frame(self.content, bg=NAVY)
            self.banner_frames[banner] = frame

            tk.Label(frame, text="5★ Pity:", font=LABEL_FONT, bg=NAVY, fg=OFFWHITE).pack(anchor="w", pady=(0, 2), padx=40)
            pity5 = tk.Label(frame, text="", font=LABEL_FONT, bg=NAVY, fg=BTN_FG)
            pity5.pack(anchor="w", padx=40)
            setattr(self, f"{banner}_pity5_label", pity5)

            btn_frame = tk.Frame(frame, bg=NAVY)
            btn_frame.pack(fill="x", pady=(40, 0), padx=40)

            if banner == "Limited":
                self.limited_status_label = tk.Label(btn_frame, text="", font=LABEL_FONT, bg=NAVY, fg=OFFWHITE)
                self.limited_status_label.pack(anchor="w", pady=(0, 24))
                self._make_wish_buttons(btn_frame, self.add_limited_wish, self.add_limited_10pull, self.remove_limited_wish, self.limited_5star_early)
            elif banner == "Weapon":
                self.weapon_fate_label = tk.Label(btn_frame, text="", font=LABEL_FONT, bg=NAVY, fg=OFFWHITE)
                self.weapon_fate_label.pack(anchor="w", pady=(0, 24))
                self._make_wish_buttons(btn_frame, self.add_weapon_wish, self.add_weapon_10pull, self.remove_weapon_wish, self.weapon_5star_early)
            else:  # Standard
                self._make_wish_buttons(btn_frame, self.add_standard_wish, self.add_standard_10pull, self.remove_standard_wish, self.standard_5star_early)

    def _make_wish_buttons(self, parent, single_cmd, ten_cmd, remove_cmd, early_cmd):
        btn1 = tk.Button(
            parent, text="Single Pull", font=BTN_FONT, bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG,
            relief="flat", borderwidth=0, height=2, width=14, command=single_cmd
        )
        btn1.pack(side="left", padx=12, pady=10)
        btn2 = tk.Button(
            parent, text="10 Pull", font=BTN_FONT, bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG,
            relief="flat", borderwidth=0, height=2, width=14, command=ten_cmd
        )
        btn2.pack(side="left", padx=12, pady=10)
        btn3 = tk.Button(
            parent, text="Remove 1 Pull", font=BTN_FONT, bg=BTN_BG, fg=OFFWHITE,
            activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG,
            relief="flat", borderwidth=0, height=2, width=16, command=remove_cmd
        )
        btn3.pack(side="left", padx=12, pady=10)
        btn4 = tk.Button(
            parent, text="5★ Early", font=BTN_FONT, bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG,
            relief="flat", borderwidth=0, height=2, width=14, command=early_cmd
        )
        btn4.pack(side="left", padx=12, pady=10)

    def _show_banner(self):
        for f in self.banner_frames.values():
            f.pack_forget()
        frame = self.banner_frames[self.banner.get()]
        frame.pack(fill="both", expand=True)
        self.update_ui()

    def _apply_genshin_style(self):
        self.configure(bg=NAVY)
        self.content.configure(bg=NAVY)
        self.title_label.configure(bg=NAVY, fg=BTN_FG)
        for frame in self.banner_frames.values():
            frame.configure(bg=NAVY)
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=NAVY)

    def show_notification(self, message, duration=3000):
        if self.notification_label:
            self.notification_label.destroy()
        self.notification_label = tk.Label(
            self, text=message, font=LABEL_FONT, bg=BTN_BG, fg=BTN_FG
        )
        self.notification_label.place(relx=0.5, rely=0.97, anchor="s")
        self.after(duration, self.hide_notification)

    def hide_notification(self):
        if self.notification_label:
            self.notification_label.destroy()
            self.notification_label = None

    # ---- 50/50 Modal ----
    def ask_5050_ui(self, callback):
        if getattr(self, "_5050_dialog_open", False):
            return
        self._5050_dialog_open = True
        overlay = tk.Toplevel(self)
        overlay.transient(self)
        overlay.grab_set()
        overlay.geometry("340x180+{}+{}".format(self.winfo_rootx()+180, self.winfo_rooty()+140))
        overlay.configure(bg=NAVY)
        overlay.title("50/50 Result")
        tk.Label(overlay, text="Did you win the 50/50?", font=LABEL_FONT, bg=NAVY, fg=BTN_FG).pack(pady=24)
        btn_frame = tk.Frame(overlay, bg=NAVY)
        btn_frame.pack(pady=10)
        def win():
            overlay.destroy()
            self._5050_dialog_open = False
            callback(True)
        def lose():
            overlay.destroy()
            self._5050_dialog_open = False
            self.show_notification("You lost the 50/50. Next 5★ is guaranteed!", duration=4000)
            callback(False)
        tk.Button(btn_frame, text="Yes", font=BTN_FONT, bg=BTN_BG, fg=BTN_FG,
                  activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG, width=8, command=win).pack(side="left", padx=16)
        tk.Button(btn_frame, text="No", font=BTN_FONT, bg=BTN_BG, fg=OFFWHITE,
                  activebackground=BTN_BG_ACTIVE, activeforeground=BTN_FG, width=8, command=lose).pack(side="left", padx=16)

    # ---- UI Update Logic ----
    def update_ui(self):
        d = self.data["Limited"]
        self.Limited_pity5_label.config(text=f"{d['5star_pity']} / 90 (Pulls to next: {90 - d['5star_pity']})")
        self.limited_status_label.config(
            text=f"Guaranteed: {'Yes' if d['guaranteed'] else 'No'} | Won 50/50: {'Yes' if d['won_5050'] else 'No'}"
        )
        d = self.data["Weapon"]
        self.Weapon_pity5_label.config(text=f"{d['5star_pity']} / 80 (Pulls to next: {80 - d['5star_pity']})")
        self.weapon_fate_label.config(text=f"Fate Points: {d['fate_points']} / 2")
        d = self.data["Standard"]
        self.Standard_pity5_label.config(text=f"{d['5star_pity']} / 90 (Pulls to next: {90 - d['5star_pity']})")

    # ---- Wish Logic ----
    def add_limited_wish(self):
        d = self.data["Limited"]
        d["5star_pity"] += 1
        if d["5star_pity"] >= 90:
            def after_5050(result):
                d["won_5050"] = result
                d["guaranteed"] = not result
                d["5star_pity"] = 0
                save_data(self.username, self.data)
                self.update_ui()
                if result and not d["guaranteed"]:
                    self.show_notification("You won the 50/50!", duration=4000)
            if d["guaranteed"]:
                after_5050(True)
            else:
                self.ask_5050_ui(after_5050)
            return
        save_data(self.username, self.data)
        self.update_ui()

    def add_limited_10pull(self):
        for _ in range(10):
            self.add_limited_wish()

    def remove_limited_wish(self):
        d = self.data["Limited"]
        if d["5star_pity"] > 0:
            d["5star_pity"] -= 1
        save_data(self.username, self.data)
        self.update_ui()

    def limited_5star_early(self):
        d = self.data["Limited"]
        def after_5050(result):
            d["won_5050"] = result
            d["guaranteed"] = not result
            d["5star_pity"] = 0
            save_data(self.username, self.data)
            self.update_ui()
            if result and not d["guaranteed"]:
                self.show_notification("You won the 50/50!", duration=4000)
        if d["guaranteed"]:
            after_5050(True)
        else:
            self.ask_5050_ui(after_5050)

    def add_weapon_wish(self):
        d = self.data["Weapon"]
        d["5star_pity"] += 1
        if d["5star_pity"] >= 80:
            d["5star_pity"] = 0
            d["fate_points"] = min(d["fate_points"] + 1, 2)
        save_data(self.username, self.data)
        self.update_ui()

    def add_weapon_10pull(self):
        for _ in range(10):
            self.add_weapon_wish()

    def remove_weapon_wish(self):
        d = self.data["Weapon"]
        if d["5star_pity"] > 0:
            d["5star_pity"] -= 1
        save_data(self.username, self.data)
        self.update_ui()

    def weapon_5star_early(self):
        d = self.data["Weapon"]
        d["5star_pity"] = 0
        d["fate_points"] = min(d["fate_points"] + 1, 2)
        save_data(self.username, self.data)
        self.update_ui()

    def add_standard_wish(self):
        d = self.data["Standard"]
        d["5star_pity"] += 1
        if d["5star_pity"] >= 90:
            d["5star_pity"] = 0
        save_data(self.username, self.data)
        self.update_ui()

    def add_standard_10pull(self):
        for _ in range(10):
            self.add_standard_wish()

    def remove_standard_wish(self):
        d = self.data["Standard"]
        if d["5star_pity"] > 0:
            d["5star_pity"] -= 1
        save_data(self.username, self.data)
        self.update_ui()

    def standard_5star_early(self):
        d = self.data["Standard"]
        d["5star_pity"] = 0
        save_data(self.username, self.data)
        self.update_ui()

if __name__ == "__main__":
    app = WishCalculator()
    app.mainloop()
