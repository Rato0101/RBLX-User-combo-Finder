import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import base64
import threading
import time
import requests
import tempfile
import os

# === Keep your current ICON_BASE64 here ===
ICON_BASE64 = (
    "AAABAAEAAAAAAAEAIAD2BwAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAEAAAABAAgGAAAAXHKoZgAAB71JREFUeNrt3UFu3EgSBdCqQa8FzH72OoKv0TcSfKO5ho/g/ewH8AWqFwLVbUtykSwyMzL/ezujDTerJER8JiOT19vL8+0CRPpX7wsA+lEAIJgCAMH+6H0BMJPr1++r/t7t5bn3pV4uFwkAokkA8BtrO/qj/26vRCABQDAJgChndfSjrqt1EpAAIJgEwNCqdvRRSAAQTAKgBJ28DwkAgkkAnCK9o9++Pf305+uXH70v6UMSAAS7Og+ANXT0p8f/kcv6JNBqHkACgGDWAEKldvSjOvksJAAIJgEMLrWTL3T0x0gAEEwCKEZH19FbkgAgmARwMh1dR69MAoBgEsBGqR1dJ5+TBADBYvcCpHbyhY7eV5U9ARIABJtmDUBH19HZTgKAYGUTQHpHv0fH5wgSAARrlgBSO/q9Tl31rDgySAAQ7OEEkNbZH7331vGpRAKAYLsTwCyd/+zV9KM7vtV/jiQBQLDNewGqd/4qHfKozl/l83CO3nsCJAAIVnYScLTO516fEUkAEKxZAjjr+XnvTulen5FJABDstATQ6m2qy39v1UHd6zMTCQCCbU4Ay/PIe/MAeztztVl5HZ+ZSQAQrMwcwKydX8fnCEviPnoiUAKAYN0SQLUO616fHpbfk14JWAKAYM0TQJXOr+ODBADRTk8AVTp+1euBniQACLY7AaydCHyUe304jwQAwcpMAi50fGhHAoBgzU8EOutkH6v7JDh6T4AEAMGarwFUe55/9HXBHr32BEgAEKxZAjjq7D73+nAcCQCCPZwAWk0EPnydOj68IwFAsHKTgEfT+eFzEgAEGy4BnD1RCEkkAAg2XAJY6PQkO2pPgAQAwZoXgOuXH+XeAgRV3L49NU23EgAEO6wA3F6eD39vGXAuCQCCKQAQTAGAYMPOAYxq7RMQcw60IAFAMAmgka2zD1v/vsTAHhIABOuWAI46I5BXe6crff81rT0l+NE9ARIABDs8AYxyRiCvPJXIJgFAMAWAVezinJMCAMHMAZxsa9f8///+e7lcLpd//+fP3pdOAAkAgkkARSyd/7M/3yMxsIcEAMG6JwATgcfYmhgWkkM2CQCCXW8vz7dT/wcrJwJnTQBrnwLs7eBHWZsEZv05Vbd6YnPjngAJAIIpABBMAYBg3Z8CzMrcPCOQACCYBNBZ79V/skkAEKxMAbDfHNorUwCA9k4vAN4aDHVJABBMAYAB3L49rdqHcf36fdOJ3AoABFMAIJgCAMFMAh5s6yyDE3noSQKAYOUKgInA2vx85lKuAADtNCsAJgKhHgkAgikAMKG1E4EKAAQzB3CwZV571pVy7wXo6+jfLwkAgkkAJ9EpGYEEAMHKFgATZ3C+sgUAOF/zAmAiEOqQACCYAgDBFAAIpgDAxO7tCVAAIJgCAANa+56AexQACFa+AJgIhPOULwDAebrtBlymAbe8xwx45TwA4GHOA4CBHL0eJgFAMAkAJnZv560EAMEkABjA1nv/tWduSAAQbJgEsFRAp+2S5KzOv5AAIFj3BGAiEN5rtf9FAoBg3RMA8Le9nX/vSdsSAASTAGBgj75jQwKAYBIAFHD28/7PSAAQbLgEYCKQmfTq/AsJAIKVSQAmAklS5aRrCQCClUkA8E+b740HWRNqPel3jwQAwSQAStnbIR+9p66aIM7q/AsJAIJJAHA5blX+syTR+3n/ZyQACHa9vTzfel/Ehxe2ch6g6r0b+1R5Pt5Lq86/kAAgmDWAxj7rcJLMq+V7SE8CrUgAEEwCaOReR7PL8Wdrv4dZkkLre/+FBADBJACGtnfN4NeOm7oLVQKAYBJAMdYC9tmaBJaOvySBo+7BtyaJXvf+CwkAgpWdBHy7wMkmAmfd515N1dn7aiQACKYANHb79qSrF3T9+j3ySYACAMEUgOKuX35MM+3W0t6klZYEFAAIpgB0srVDSQL7SAK/pwBAMAWACJLAxxQACFZ+EvDtQiebCHz3+UwINlXtDT29SAAQTAEowlOBtqwJvFIAIJgCQLT0vRkKAARTAIqxFtDH5u99krUABQCCKQBFSQJjGD0JKAAQbJhJwLcLnnwi8N3nNSHYRcqkoAQAwRSA4qwF9JEyKagAQDAFYBCSQB+zJwEFAIIpALDCrElAAYBgCsBgrAX0NVsSUAAg2HCTgG8XHjYR+On3YFKwq9HfQiwBQDAFAB4w+jkCCgAEUwAG56lADaMmAQUAgikAk5AExtQ7CSgAEEwBgAONNimoAECwYScB3z6AicAPmRCsofrZghIABItJAFvN0hElgRqqJgEJAIL90fsCqur9jFwnnsvy89z6e7Uk3LOSgAQAwawB8CEJ5FxV1gQkAAg2fAG4vTyXO2VlBvYKnGvvxODRhi8AwH7DrwG8+0DWBA5VoUsl6HW2oAQAwaZLAEeZNUksnWPr55MEztXrqYAEAMEkgKKOTiCfdQpJoJbWSUACgGD2AhRltiFT6z0DEgAEkwDCbX0qsHQmawGPqTJlKQFAMAmAy+WSmwSqdOJeJAAIJgFQQnonfpQ5AGAzk4B8aNa9ELOxFwDYzRoAH9q7a5A2nAcAPEwCgIaq7fGQACCYBMBvzboWUK0T9yIBQDAJgFV+7ZhHJQKduC8JAIJJAOyic89BAoBgCgAEUwAgmAIAwRQACPYXuKfpOWvuwkMAAAAASUVORK5CYII="
)

# === Colors and constants ===
BG_COLOR = "#1C1C1C"       # Dark background (keep grey-ish)
TEXT_COLOR = "#FFFFFF"     # White text default
# Use the single red color everywhere non-grey is desired
PROGRESS_BASE = "#F52D05"  # Exact red requested by user
ACCENT_COLOR = PROGRESS_BASE
XBOX_GREEN = PROGRESS_BASE
BTN_BG_COLOR = PROGRESS_BASE

MAX_COMBOS = 500_000

def load_combos(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        combos = f.readlines()
    combo_count = len(combos)
    if combo_count > MAX_COMBOS:
        print(f"Error: File has {combo_count} combos, which exceeds the 500K limit.")
        return []
    print(f"Loaded {combo_count} combos from {filename}.")
    return combos

def scan_combos(combos):
    total = len(combos)
    for idx, combo in enumerate(combos, 1):
        # Your scanning logic here
        combos_left = total - idx
        print(f"Scanning combo {idx}/{total}... {combos_left} combos left.")
        # Simulate scan
        # time.sleep(0.1)
    print("Scan complete.")

class MetroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-alpha', 0.0)  # Start fully transparent
        self.after(10, self._fade_in_window)

        self.title("Roblox Finder V3.5- by CloudKernelFox")
        self.geometry("1200x800")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self._scan_cancelled = threading.Event()
        self._scan_thread = None
        self._not_taken_results = []
        self._error_results = []

        # Set icon from Base64 embedded
        try:
            self._icon_tempfile = tempfile.NamedTemporaryFile(delete=False, suffix=".ico")
            self._icon_tempfile.write(base64.b64decode(ICON_BASE64))
            self._icon_tempfile.flush()
            self.iconbitmap(self._icon_tempfile.name)
        except Exception as e:
            print("Icon load error:", e)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Style for ttk widgets
        self.style = ttk.Style(self)
        self._set_theme()

        self._build_ui()
        self._animate_header_fadein()
        self.pulse_progress_bar()

        self.combo_file = None
        self.combo_lines = []

    def _set_theme(self):
        # Use clam theme for ttk
        self.style.theme_use("clam")

        # Base Metro button (use red accent)
        self.style.configure("Metro.TButton",
                             background=BTN_BG_COLOR,
                             foreground=TEXT_COLOR,
                             font=("Comic Sans MS", 11, "bold"),
                             borderwidth=0,
                             focusthickness=2,
                             focuscolor=PROGRESS_BASE,
                             padding=(12, 8))
        self.style.map("Metro.TButton",
                       background=[("active", "#d32603"), ("disabled", "#222")],
                       foreground=[("active", BG_COLOR), ("disabled", "#888")])

        # Red variant (primary accent)
        self.style.configure("Red.Metro.TButton", background=PROGRESS_BASE, foreground="#FFFFFF", font=("Comic Sans MS", 11, "bold"), padding=(12, 8))
        self.style.map("Red.Metro.TButton", background=[("active", "#d32603"), ("disabled", "#666")])

        # Keep named variants but use red for non-grey ones
        self.style.configure("Green.Metro.TButton", background=PROGRESS_BASE, foreground="#FFFFFF", font=("Comic Sans MS", 11, "bold"), padding=(12, 8))
        self.style.map("Green.Metro.TButton", background=[("active", "#d32603"), ("disabled", "#666")])

        self.style.configure("Grey.Metro.TButton", background="#333333", foreground="#DDDDDD", font=("Comic Sans MS", 11, "bold"), padding=(12, 8))
        self.style.map("Grey.Metro.TButton", background=[("active", "#444444"), ("disabled", "#222")])

        # Label style
        self.style.configure("Metro.TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Comic Sans MS", 12))

        # Progressbar (red)
        self.style.configure("Red.Horizontal.TProgressbar", troughcolor=BG_COLOR, background=PROGRESS_BASE, bordercolor=BG_COLOR, lightcolor=PROGRESS_BASE, darkcolor=PROGRESS_BASE)

        # Scrollbar layout and colors
        self.style.layout("Black.Vertical.TScrollbar", [('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.uparrow', {'side': 'top', 'sticky': ''}), ('Vertical.Scrollbar.downarrow', {'side': 'bottom', 'sticky': ''}), ('Vertical.Scrollbar.thumb', {'unit': '1', 'children': [('Vertical.Scrollbar.grip', {'sticky': ''})], 'sticky': 'nswe'})], 'sticky': 'ns'})])
        self.style.configure("Black.Vertical.TScrollbar", troughcolor="#111111", background="#222222", bordercolor="#000000", arrowcolor=PROGRESS_BASE, lightcolor="#333333", darkcolor="#000000", gripcount=0, relief="flat", borderwidth=2)
        self.style.map("Black.Vertical.TScrollbar", background=[("active", "#333333"), ("!active", "#222222")])

    def _build_ui(self):
        # --- Modern Layout ---
        # Header
        header_frame = tk.Frame(self, bg=BG_COLOR)
        header_frame.pack(fill="x", pady=(18, 0), padx=0)

        self.header_label = tk.Label(
            header_frame,
            text="Roblox User & Combo Finder V3\nBy CloudKernelFox",
            font=("Comic Sans MS", 17, "bold"),
            bg=BG_COLOR,
            fg=BG_COLOR,
            anchor="w",
            justify="left"
        )
        self.header_label.pack(side="left", padx=(30, 0), anchor="w", fill="x", expand=True)

        self.load_btn = ttk.Button(header_frame, text="Open Combo", style="Metro.TButton",
                                   command=self.load_file)
        self.load_btn.pack(side="right", padx=(0, 30), ipadx=6, ipady=2)

        # --- Main content frame with shadow effect ---
        main_frame = tk.Frame(self, bg="#181818", bd=0, highlightthickness=0)
        main_frame.pack(fill="both", expand=True, padx=30, pady=(10, 18))

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=540, mode="determinate",
                                        style="Metro.Horizontal.TProgressbar")
        self.progress.pack(pady=(10, 18))

        # Results area with shadow
        results_shadow = tk.Frame(main_frame, bg="#111", bd=0)
        results_shadow.pack(fill="both", expand=True, padx=6, pady=(0, 12))
        frame_results = tk.Frame(results_shadow, bg="#23272A", bd=0)
        frame_results.pack(fill="both", expand=True, padx=4, pady=4)

        # --- Clear button (tiny, top right of results) ---
        clear_btn = ttk.Button(frame_results, text="✕", style="Metro.TButton", width=2, command=self._clear_results)
        clear_btn.pack(side="top", anchor="ne", padx=2, pady=2)

        # --- Combos left label (right of clear button) ---
        self.combos_label = tk.Label(frame_results, text="Combos: 0", bg="#23272A", fg=ACCENT_COLOR, font=("Comic Sans MS", 10, "bold"))
        self.combos_label.pack(side="top", anchor="ne", padx=(0, 40), pady=2)

        self.results_box = tk.Text(frame_results, bg="#23272A", fg=TEXT_COLOR,
                                   font=("Comic Sans MS", 10, "normal"), relief="flat",
                                   wrap="none", height=14, bd=2, highlightthickness=1, highlightbackground="#333")
        self.results_box.pack(side="left", fill="both", expand=True, padx=(0, 0), pady=(0, 0))

        scrollbar = ttk.Scrollbar(frame_results, orient="vertical",
                                  command=self.results_box.yview, style="Black.Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y")
        self.results_box.configure(yscrollcommand=scrollbar.set)

        # --- Button row ---
        btn_frame = tk.Frame(main_frame, bg="#181818")
        btn_frame.pack(pady=(0, 10))

        self.start_btn = ttk.Button(btn_frame, text="Start Scan", style="Metro.TButton",
                                    command=self.start_scan)
        self.start_btn.grid(row=0, column=0, padx=10, ipadx=8, ipady=2)

        self.cancel_btn = ttk.Button(btn_frame, text="Cancel Scan and Save", style="Metro.TButton",
                                     command=self.cancel_scan, state="disabled")
        self.cancel_btn.grid(row=0, column=1, padx=10, ipadx=8, ipady=2)

        self.save_btn = ttk.Button(btn_frame, text="Save Results", style="Metro.TButton",
                                   command=self.save_results)
        self.save_btn.grid(row=0, column=2, padx=10, ipadx=8, ipady=2)
        # Save All relocated to generator row (as 'Save Sorted and Generated')

        # --- Generator & Sorting controls (integrated from V4) ---
        gen_frame = tk.Frame(main_frame, bg="#181818")
        gen_frame.pack(pady=(6, 8))

        tk.Label(gen_frame, text="Generate length:", bg="#181818", fg=TEXT_COLOR, font=("Comic Sans MS", 10)).grid(row=0, column=0, padx=6)
        self.gen_length = tk.IntVar(value=5)
        self.gen_length_entry = tk.Spinbox(gen_frame, from_=1, to=7, textvariable=self.gen_length, width=4, font=("Comic Sans MS", 10))
        self.gen_length_entry.grid(row=0, column=1, padx=6)

        tk.Label(gen_frame, text="Count:", bg="#181818", fg=TEXT_COLOR, font=("Comic Sans MS", 10)).grid(row=0, column=2, padx=6)
        self.gen_count = tk.IntVar(value=100)
        self.gen_count_entry = tk.Spinbox(gen_frame, from_=1, to=10000, textvariable=self.gen_count, width=6, font=("Comic Sans MS", 10))
        self.gen_count_entry.grid(row=0, column=3, padx=6)

        self.generate_btn = ttk.Button(gen_frame, text="Generate", style="Metro.TButton", command=self.on_generate)
        self.generate_btn.grid(row=0, column=4, padx=8)

        self.save_generated_btn = ttk.Button(gen_frame, text="Save Generated", style="Metro.TButton", command=self.on_save_generated, state="disabled")
        self.save_generated_btn.grid(row=0, column=5, padx=8)

        self.sort_generated_btn = ttk.Button(gen_frame, text="Sort Generated", style="Metro.TButton", command=self.on_sort_generated, state="disabled")
        self.sort_generated_btn.grid(row=0, column=6, padx=8)

        self.sort_file_btn = ttk.Button(gen_frame, text="Sort File", style="Metro.TButton", command=self.on_sort_file)
        self.sort_file_btn.grid(row=0, column=7, padx=8)

        # Save Sorted and Generated (renamed Save All) - placed here and same action as save_generated
        self.save_all_btn = ttk.Button(gen_frame, text="Save Sorted and Generated", style="Metro.TButton", command=self.on_save_generated, state="disabled")
        self.save_all_btn.grid(row=0, column=8, padx=8)

        # --- Manual Lookup Section ---
        manual_shadow = tk.Frame(main_frame, bg="#111", bd=0)
        manual_shadow.pack(fill="x", padx=6, pady=(0, 0))
        manual_frame = tk.Frame(manual_shadow, bg="#23272A", bd=0)
        manual_frame.pack(fill="x", padx=4, pady=4)

        tk.Label(manual_frame, text="Manual User Lookup:", bg="#23272A", fg=ACCENT_COLOR, font=("Comic Sans MS", 11, "bold")).pack(side="left", padx=(10, 2))
        tk.Label(manual_frame, text="Username:", bg="#23272A", fg=TEXT_COLOR, font=("Comic Sans MS", 10)).pack(side="left", padx=(10, 2))
        self.manual_username = tk.Entry(manual_frame, font=("Comic Sans MS", 10), width=22, relief="flat", bg="#181818", fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
        self.manual_username.pack(side="left", padx=2)
        self.manual_btn = ttk.Button(manual_frame, text="Lookup", style="Metro.TButton", command=self.manual_lookup)
        self.manual_btn.pack(side="left", padx=10, ipadx=4, ipady=2)

        # More space for manual result
        self.manual_result = tk.Text(manual_frame, height=3, width=80, font=("Comic Sans MS", 10), bg="#23272A", fg=TEXT_COLOR, relief="flat", bd=2, highlightthickness=1, highlightbackground="#333")
        self.manual_result.pack(side="left", padx=10, pady=4, fill="x", expand=True)
        self.manual_result.config(state="disabled")

        # Color tags
        # Color mapping per user request:
        # found -> green, censored -> yellow, notfound -> red, glitched -> blue
        self.results_box.tag_configure("found", foreground="#00FF00")
        self.results_box.tag_configure("censored", foreground="#FFD700")
        self.results_box.tag_configure("notfound", foreground=PROGRESS_BASE)
        self.results_box.tag_configure("glitched", foreground="#00B0FF")
        # keep fallback tags
        self.results_box.tag_configure("error", foreground="#FF0000")
        self.results_box.tag_configure("skipped", foreground="#AAAAAA")

    def manual_lookup(self):
        username = self.manual_username.get().strip()
        if not username:
            messagebox.showerror("Input Error", "Please enter a username.")
            return
        self.manual_btn.config(state="disabled")
        self.manual_result.config(state="normal")
        self.manual_result.delete("1.0", tk.END)
        self.manual_result.insert(tk.END, "Looking up...\n")
        self.manual_result.config(state="disabled")
        threading.Thread(target=self._manual_lookup_thread, args=(username,), daemon=True).start()

    def _manual_lookup_thread(self, username):
        session = requests.Session()
        try:
            resp = session.post(
                "https://users.roblox.com/v1/usernames/users",
                json={"usernames": [username], "excludeBannedUsers": False},
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("data") and data["data"][0]:
                    user_data = data["data"][0]
                    uid = user_data["id"]
                    uname = user_data["name"]
                    # Get join date
                    join_resp = session.get(
                        f"https://users.roblox.com/v1/users/{uid}",
                        timeout=5
                    )
                    if join_resp.status_code == 200:
                        join_data = join_resp.json()
                        joined = join_data.get("created", "")
                        if joined:
                            try:
                                from datetime import datetime
                                dt = datetime.fromisoformat(joined.replace("Z", "+00:00"))
                                join_str = dt.strftime("%d/%m/%Y")
                            except Exception:
                                join_str = joined
                        else:
                            join_str = "unknown"
                    else:
                        join_str = "unknown"
                    # Compose result (no password, no RAP)
                    result = f"[FOUND] {uname}  -ID.{uid}   -joined.{join_str}"
                else:
                    result = "[NOT FOUND] User not found."
            else:
                result = f"[ERROR] API error {resp.status_code}"
        except Exception as e:
            result = f"[ERROR] {e}"
        self.after(0, self._show_manual_result, result)

    def _show_manual_result(self, result):
        self.manual_result.config(state="normal")
        self.manual_result.delete("1.0", tk.END)
        self.manual_result.insert(tk.END, result)
        self.manual_result.config(state="disabled")
        self.manual_btn.config(state="normal")

    def _get_user_rap(self, user_id):
        """Fetch total RAP for a user. Returns int or None."""
        try:
            total_rap = 0
            cursor = ""
            session = requests.Session()
            while True:
                url = f"https://inventory.roproxy.com/v1/users/{user_id}/assets/collectibles?sortOrder=Asc&limit=100&cursor={cursor}"
                resp = session.get(url, timeout=7)
                if resp.status_code != 200:
                    break
                data = resp.json()
                for collectible in data.get("data", []):
                    rap = collectible.get("recentAveragePrice")
                    if rap:
                        total_rap += rap
                cursor = data.get("nextPageCursor")
                if not cursor:
                    break
            return total_rap if total_rap > 0 else None
        except Exception:
            return None

    def _animate_header_fadein(self):
        """Fade-in the header label by gradually changing fg color brightness from BG_COLOR to white."""
        steps = 20
        def fade(step=0):
            if step > steps:
                return
            # interpolate color between BG_COLOR and TEXT_COLOR
            bg_rgb = self._hex_to_rgb(BG_COLOR)
            fg_rgb = self._hex_to_rgb(TEXT_COLOR)
            new_rgb = tuple(
                int(bg + (fg - bg) * (step / steps))
                for bg, fg in zip(bg_rgb, fg_rgb)
            )
            color_hex = self._rgb_to_hex(new_rgb)
            self.header_label.config(fg=color_hex)
            self.after(40, lambda: fade(step + 1))
        fade()

    def pulse_progress_bar(self):
        """Super cool animated progress bar with glowing highlight."""
        self._pulse_pos = 0
        self._pulse_dir = 1
        self._pulse_max = 100  # Number of steps for the highlight to travel

        def pulse():
            # Calculate highlight position
            self._pulse_pos += self._pulse_dir
            if self._pulse_pos >= self._pulse_max or self._pulse_pos <= 0:
                self._pulse_dir *= -1

            # Create a gradient effect: base green, with a bright highlight moving across
            base_green = 136
            highlight_green = 255
            highlight_width = 20  # width of the highlight

            # Calculate color for the current step
            def get_color(pos):
                # If within highlight, interpolate to highlight green
                if abs(pos - self._pulse_pos) < highlight_width:
                    ratio = 1 - abs(pos - self._pulse_pos) / highlight_width
                    green = int(base_green + (highlight_green - base_green) * ratio)
                else:
                    green = base_green
                return f"#00{green:02x}00"

            # Simulate a gradient by updating the bar's color
            # (ttk.Progressbar only supports one color, so we fake it by changing the color rapidly)
            color = get_color(self._pulse_pos)
            self.style.configure("Metro.Horizontal.TProgressbar", background=color, lightcolor=color, darkcolor=color)
            self.after(15, pulse)

        pulse()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            self.combo_file = None
            self.combo_lines = []
            self.combos_label.config(text="Combos: 0")
            return

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read().splitlines()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
            self.combo_file = None
            self.combo_lines = []
            self.combos_label.config(text="Combos: 0")
            return

        combo_count = len(lines)
        if combo_count > MAX_COMBOS:
            messagebox.showerror("Too Many Combos", f"File has {combo_count} combos.\nLimit is {MAX_COMBOS:,}.")
            self.combo_file = None
            self.combo_lines = []
            self.combos_label.config(text="Combos: 0")
            return

        self.combo_file = file_path
        self.combo_lines = lines
        self.results_box.delete("1.0", tk.END)
        self.progress.config(value=0, maximum=combo_count)
        self.combos_label.config(text=f"Combos: {combo_count}")
        messagebox.showinfo("Loaded", f"Loaded combo file:\n{file_path}\n\nCombos: {combo_count}")
        self.title(f"Roblox Finder V3.5 - {combo_count} combos loaded")

    def start_scan(self):
        if not self.combo_file or not self.combo_lines:
            messagebox.showerror("Error", "Please load a combo file first!")
            return
        self.start_btn.config(state="disabled")
        self.save_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self._scan_cancelled.clear()
        self._found_results = []
        self._scan_thread = threading.Thread(target=self._lookup_public_users, daemon=True)
        self._scan_thread.start()

    def cancel_scan(self):
        self._scan_cancelled.set()
        self.cancel_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.save_btn.config(state="normal")
        self.save_all_btn.config(state="normal")
        messagebox.showinfo("Cancelled", "Scan cancelled. You can now save the partial results.")
        self._prompt_save_on_cancel()

    def _prompt_save_on_cancel(self):
        if messagebox.askyesno("Save Results", "Do you want to save the current results?"):
            self.save_results()

    def _lookup_public_users(self):
        """Fetch Roblox ID, join date, and canonical username for provided usernames."""
        self.results_box.delete("1.0", tk.END)
        self._found_results = []
        lines = self.combo_lines
        total = len(lines)
        self._thread_safe_progress(0, total)
        session = requests.Session()

        for idx, line in enumerate(lines, 1):
            if self._scan_cancelled.is_set():
                break
            time.sleep(0.05)
            user_part = line.split(":")[0].strip()
            combo = line.strip()

            if "@" in user_part:
                result = f"[EMAIL] {user_part} — skipped (email, no public lookup)\n"
                tag = "skipped"
            else:
                try:
                    # First use the validate endpoint (from main.py style) to check username status
                    validate_url = f"https://auth.roblox.com/v1/usernames/validate?Username={user_part}&Birthday=2000-01-01"
                    vresp = session.get(validate_url, timeout=6)
                    if vresp.status_code == 200:
                        vdata = vresp.json()
                        code = vdata.get('code')
                        # code meanings: 0 = valid (available), 1 = taken, 2 = censored
                        if code == 0:
                            # valid => NOT TAKEN (available)
                            result = f"[NOT TAKEN] {user_part}\n"
                            tag = "notfound"
                            self._not_taken_results.append((user_part, vdata))
                        elif code == 2:
                            result = f"[CENSORED] {user_part}\n"
                            tag = "censored"
                            self._error_results.append((user_part, vdata))
                        elif code == 1:
                            # Taken: fetch canonical info via users endpoint
                            users_resp = session.post(
                                "https://users.roblox.com/v1/usernames/users",
                                json={"usernames": [user_part], "excludeBannedUsers": False},
                                timeout=6
                            )
                            if users_resp.status_code == 200:
                                udata = users_resp.json()
                                if udata.get('data') and udata['data'][0]:
                                    user_data = udata['data'][0]
                                    uid = user_data.get('id')
                                    uname = user_data.get('name')
                                    # attempt to fetch join date
                                    join_resp = session.get(f"https://users.roblox.com/v1/users/{uid}", timeout=6)
                                    if join_resp.status_code == 200:
                                        join_data = join_resp.json()
                                        joined = join_data.get('created', '')
                                        if joined:
                                            try:
                                                from datetime import datetime
                                                dt = datetime.fromisoformat(joined.replace('Z', '+00:00'))
                                                join_str = dt.strftime('%d/%m/%Y')
                                            except Exception:
                                                join_str = joined
                                        else:
                                            join_str = 'unknown'
                                    else:
                                        join_str = 'unknown'
                                    result = f"[FOUND] {uname} (ID: {uid}) - joined: {join_str}\n"
                                    tag = 'found'
                                    save_line = f"[FOUND] {uname}  -ID.{uid}   -joined.{join_str}  {combo}"
                                    self._found_results.append(save_line)
                                else:
                                    result = f"[ERROR] {user_part} - user lookup failed\n"
                                    tag = 'error'
                                    self._error_results.append((user_part, udata))
                            else:
                                result = f"[ERROR] {user_part} - users API {users_resp.status_code}\n"
                                tag = 'error'
                                self._error_results.append((user_part, {'status': users_resp.status_code}))
                        else:
                            result = f"[UNKNOWN] {user_part}\n"
                            tag = 'error'
                            self._error_results.append((user_part, vdata))
                    else:
                        result = f"[ERROR] {user_part} — validate API {vresp.status_code}\n"
                        tag = 'error'
                        self._error_results.append((user_part, {'status': vresp.status_code}))
                except Exception as e:
                    result = f"[GLITCH] {user_part} — {e}\n"
                    tag = 'glitched'
                    self._error_results.append((user_part, {'error': str(e)}))

            combos_left = total - idx
            self._thread_safe_insert(result, tag)
            self._thread_safe_progress(idx, total)
            # Update combos left label
            self.after(0, lambda left=combos_left: self.combos_label.config(text=f"Combos: {left}"))
            # Show combos left in window title
            self.after(0, lambda left=combos_left: self.title(
                f"Roblox Finder V3.5 - {left} combos left" if left > 0 else "Roblox Finder V3.5 - Scan complete"
            ))

        self._thread_safe_btns_reset()
        if not self._scan_cancelled.is_set():
            self._thread_safe_messagebox("Done", "Scan completed.")
            self.after(0, lambda: self.title("Roblox Finder V3.5 - Scan complete"))
            self.after(0, lambda: self.combos_label.config(text="Combos: 0"))
            # enable Save All
            self.after(0, lambda: self.save_all_btn.config(state="normal"))

    def save_results(self):
        # Save the full contents of the results box (all statuses: FOUND, NOT TAKEN, CENSORED, GLITCH, skipped, etc.)
        try:
            content = self.results_box.get("1.0", tk.END).rstrip()
        except Exception:
            content = ""
        if not content:
            messagebox.showinfo("No Results", "No results to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content + "\n")
                messagebox.showinfo("Saved", f"Results saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results: {e}")

    def save_all(self):
        # Save found, not-taken and errors into one file with sections
        if not (hasattr(self, "_found_results") or self._not_taken_results or self._error_results):
            messagebox.showinfo("No Data", "No data to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("== FOUND ==\n")
                for line in getattr(self, '_found_results', []):
                    f.write(line + "\n")
                f.write("\n== NOT TAKEN ==\n")
                for n,data in self._not_taken_results:
                    f.write(f"{n}\t{data}\n")
                f.write("\n== ERRORS / CENSORED / GLITCHES ==\n")
                for n,data in self._error_results:
                    f.write(f"{n}\t{data}\n")
            messagebox.showinfo("Saved", f"All data saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    # Thread-safe UI helpers
    def _thread_safe_insert(self, text, tag):
        self.after(0, lambda: (self.results_box.insert(tk.END, text, tag), self.results_box.see(tk.END)))

    def _thread_safe_progress(self, value, maximum):
        # Reset progress bar if needed
        self.after(0, lambda: (
            self.progress.config(maximum=maximum),
            self.progress.config(value=value if value <= maximum else maximum)
        ))

    def _thread_safe_btns_reset(self):
        self.after(0, lambda: (
            self.start_btn.config(state="normal"),
            self.save_btn.config(state="normal"),
            self.cancel_btn.config(state="disabled")
        ))

    def _thread_safe_messagebox(self, title, message):
        self.after(0, lambda: messagebox.showinfo(title, message))

    def _on_close(self):
        self._scan_cancelled.set()
        try:
            self.destroy()
        finally:
            # Clean up temp icon file
            if hasattr(self, "_icon_tempfile"):
                try:
                    self._icon_tempfile.close()
                    os.unlink(self._icon_tempfile.name)
                except Exception:
                    pass

    # Utility color conversion helpers
    @staticmethod
    def _hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))

    @staticmethod
    def _rgb_to_hex(rgb_tuple):
        return "#%02x%02x%02x" % rgb_tuple

    def _fade_in_window(self):
        alpha = self.attributes('-alpha')
        if alpha < 1.0:
            alpha = min(alpha + 0.05, 1.0)
            self.attributes('-alpha', alpha)
            self.after(20, self._fade_in_window)

    def _clear_results(self):
        self.results_box.delete("1.0", tk.END)

    # ----------------- Generator & Sorting Logic (old single-threaded method) -----------------
    def on_generate(self):
        length = int(self.gen_length.get())
        count = int(self.gen_count.get())
        # Run generation in background to avoid blocking UI
        self.generate_btn.config(state="disabled")
        threading.Thread(target=self._generate_thread, args=(length, count), daemon=True).start()

    def _generate_thread(self, length, count):
        import random
        consonants = 'bcdfghjklmnpqrstvwxyz'
        vowels = 'aeiou'
        # Build pronounceable pseudo-words
        generated = []
        for _ in range(count):
            name_chars = []
            # Start with consonant mostly for more word-like feel
            use_consonant = random.random() < 0.7
            while len(name_chars) < length:
                if use_consonant:
                    name_chars.append(random.choice(consonants))
                    # sometimes add a vowel after a consonant
                    if random.random() < 0.6 and len(name_chars) < length:
                        name_chars.append(random.choice(vowels))
                else:
                    name_chars.append(random.choice(vowels))
                use_consonant = not use_consonant
            name = ''.join(name_chars)[:length]
            # small chance to capitalize
            if random.random() < 0.05:
                name = name.capitalize()
            generated.append(name)

        # store generated and statuses
        self._generated = generated
        self._generated_status = {n: None for n in generated}

        # Clear results and dump generated names
        def dump_gen():
            self.results_box.delete('1.0', tk.END)
            self.results_box.insert(tk.END, f"[GENERATED] {len(self._generated)} names\n")
            for n in self._generated:
                self.results_box.insert(tk.END, n + '\n')
            self.results_box.see(tk.END)
        self.after(0, dump_gen)

        # Verify generated names (rate-limited to avoid hammering API)
        session = requests.Session()
        for i, name in enumerate(self._generated, 1):
            try:
                validate_url = f"https://auth.roblox.com/v1/usernames/validate?Username={name}&Birthday=2000-01-01"
                vresp = session.get(validate_url, timeout=6)
                if vresp.status_code == 200:
                    vdata = vresp.json()
                    code = vdata.get('code')
                    if code == 0:
                        line = f"[NOT TAKEN] {name}\n"
                        self._generated_status[name] = ('NOT TAKEN', vdata)
                    elif code == 2:
                        line = f"[CENSORED] {name}\n"
                        self._generated_status[name] = ('CENSORED', vdata)
                    elif code == 1:
                        users_resp = session.post(
                            "https://users.roblox.com/v1/usernames/users",
                            json={"usernames": [name], "excludeBannedUsers": False},
                            timeout=6
                        )
                        if users_resp.status_code == 200:
                            udata = users_resp.json()
                            if udata.get('data') and udata['data'][0]:
                                user_data = udata['data'][0]
                                uid = user_data.get('id')
                                uname = user_data.get('name')
                                join_resp = session.get(f"https://users.roblox.com/v1/users/{uid}", timeout=6)
                                if join_resp.status_code == 200:
                                    join_data = join_resp.json()
                                    joined = join_data.get('created', '')
                                    if joined:
                                        try:
                                            from datetime import datetime
                                            dt = datetime.fromisoformat(joined.replace('Z', '+00:00'))
                                            join_str = dt.strftime('%d/%m/%Y')
                                        except Exception:
                                            join_str = joined
                                    else:
                                        join_str = 'unknown'
                                else:
                                    join_str = 'unknown'
                                line = f"[FOUND] {uname} (ID: {uid}) - joined: {join_str}\n"
                                self._generated_status[name] = ('FOUND', {'id': uid, 'name': uname, 'joined': join_str})
                            else:
                                line = f"[ERROR] {name} - user lookup failed\n"
                                self._generated_status[name] = ('ERROR', users_resp.text if users_resp is not None else None)
                        else:
                            line = f"[ERROR] {name} - users API {users_resp.status_code}\n"
                            self._generated_status[name] = ('ERROR', {'status': users_resp.status_code})
                    else:
                        line = f"[UNKNOWN] {name}\n"
                        self._generated_status[name] = ('UNKNOWN', vdata)
                else:
                    line = f"[ERROR] {name} - validate API {vresp.status_code}\n"
                    self._generated_status[name] = ('ERROR', {'status': vresp.status_code})
            except Exception as e:
                line = f"[GLITCH] {name} - {e}\n"
                self._generated_status[name] = ('GLITCH', {'error': str(e)})

            # append to results box
            self.after(0, lambda t=line: (self.results_box.insert(tk.END, t), self.results_box.see(tk.END)))

            # simple sleep to be gentle to the API
            time.sleep(0.12)

        # Sort generated names by rarity and print the top section
        scored = self.sort_usernames_list(self._generated)
        self._generated = [n for n, s in scored]

        def append_sorted():
            self.results_box.insert(tk.END, '\n')
            self.results_box.insert(tk.END, f"[SORTED GENERATED] {len(self._generated)} names\n")
            for n in self._generated[:200]:
                status = self._generated_status.get(n)
                if status and status[0] != 'FOUND':
                    self.results_box.insert(tk.END, f"{n}\t[{status[0]}]\n")
                else:
                    self.results_box.insert(tk.END, n + '\n')
            self.results_box.see(tk.END)
            # enable buttons
            self.save_generated_btn.config(state='normal')
            self.sort_generated_btn.config(state='normal')
            self.save_all_btn.config(state='normal')
            self.generate_btn.config(state='normal')

        self.after(0, append_sorted)

    def _thread_after_generate(self):
        self.results_box.insert(tk.END, f"[GENERATED] {len(getattr(self, '_generated', []))} names\n")
        self.results_box.see(tk.END)
        self.generate_btn.config(state="normal")
        self.save_generated_btn.config(state="normal")
        self.sort_generated_btn.config(state="normal")

    def on_save_generated(self):
        if not hasattr(self, '_generated') or not self._generated:
            messagebox.showinfo('No Generated', 'No generated list to save.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files','*.txt')])
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                for n in self._generated:
                    status = self._generated_status.get(n)
                    if status:
                        f.write(f"{n}\t{status[0]}\t{status[1]}\n")
                    else:
                        f.write(n + '\n')
            messagebox.showinfo('Saved', f'Generated names saved to:\n{path}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save generated: {e}')

    def on_sort_generated(self):
        if not hasattr(self, '_generated') or not self._generated:
            messagebox.showinfo('No Generated', 'No generated list to sort.')
            return
        self.sort_generated_btn.config(state='disabled')
        threading.Thread(target=self._sort_generated_thread, daemon=True).start()

    def _sort_generated_thread(self):
        names = list(self._generated)
        scored = self.sort_usernames_list(names)
        # Replace generated with sorted
        self._generated = [n for n,score in scored]
        self.after(0, lambda: (self.results_box.insert(tk.END, f"[SORTED GENERATED] {len(self._generated)} names\n"), self.results_box.see(tk.END), self.sort_generated_btn.config(state='normal')))

    def on_sort_file(self):
        # Sort the currently loaded combo file by username rarity using old method
        if not self.combo_file:
            messagebox.showinfo('No File', 'No usernames file loaded. Use Open Combo to load usernames.txt')
            return
        self.sort_file_btn.config(state='disabled')
        threading.Thread(target=self._sort_file_thread, daemon=True).start()

    def _sort_file_thread(self):
        # Read file lines
        try:
            with open(self.combo_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [l.strip() for l in f.read().splitlines() if l.strip()]
        except Exception as e:
            self.after(0, lambda: messagebox.showerror('Error', f'Failed to read file: {e}'))
            self.after(0, lambda: self.sort_file_btn.config(state='normal'))
            return

        # Extract usernames (before colon) and score using old single-threaded method
        names = [l.split(':')[0].strip() for l in lines]
        scored = self.sort_usernames_list(names)

        # Reconstruct lines sorted by name score descending
        score_map = {name: score for name, score in scored}
        sorted_lines = sorted(lines, key=lambda L: score_map.get(L.split(':')[0].strip(), 0), reverse=True)

        # Backup and write
        try:
            backup = self.combo_file + f".backup.{time.strftime('%Y%m%d-%H%M%S')}"
            with open(backup, 'w', encoding='utf-8') as bf:
                for l in lines:
                    bf.write(l + '\n')
            with open(self.combo_file, 'w', encoding='utf-8') as wf:
                for l in sorted_lines:
                    wf.write(l + '\n')
            self.after(0, lambda: (self.results_box.insert(tk.END, f"[SORTED FILE] Wrote sorted file and backup {os.path.basename(backup)}\n"), self.results_box.see(tk.END)))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror('Error', f'Failed to write sorted file: {e}'))
        finally:
            self.after(0, lambda: self.sort_file_btn.config(state='normal'))

    def sort_usernames_list(self, names):
        """Old single-threaded scoring (slower). Returns list of tuples (name, score)."""
        def rarity_score(name):
            # Simple heuristic from previous versions
            score = 0.0
            name = name.lower()
            score += len(name) * 1.0
            # unique chars
            score += len(set(name)) * 2.0
            # penalize repeats
            for ch in set(name):
                cnt = name.count(ch)
                if cnt > 1:
                    score -= (cnt - 1) * 0.5
            # digits penalty
            digits = sum(c.isdigit() for c in name)
            score -= digits * 1.0
            # sequential runs penalty
            maxseq = 1
            cur = 1
            for a,b in zip(name, name[1:]):
                if ord(b) == ord(a) + 1:
                    cur += 1
                    maxseq = max(maxseq, cur)
                else:
                    cur = 1
            score -= maxseq * 0.8
            return score

        scored = []
        for n in names:
            try:
                s = rarity_score(n)
            except Exception:
                s = 0.0
            scored.append((n, s))
        # sort descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def on_save_scores(self):
        # Save last-scored generated or file-scored results if present
        # We'll save generated if present, otherwise nothing
        if hasattr(self, '_generated') and self._generated:
            # if sorted, it's replaced
            path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files','*.txt')])
            if not path:
                return
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    for n in self._generated:
                        f.write(n + '\n')
                messagebox.showinfo('Saved', f'Scores saved to:\n{path}')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save scores: {e}')
        else:
            messagebox.showinfo('No Data', 'No scored/generated data to save.')
if __name__ == "__main__":
    app = MetroApp()
    app.mainloop()