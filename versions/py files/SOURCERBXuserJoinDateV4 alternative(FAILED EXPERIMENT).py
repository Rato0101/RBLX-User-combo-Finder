import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import requests
import os
import random
import string
import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Minimal integrated V4 tool: generator + checker + sorter + UI

DEFAULT_CONFIG = {
    "threads": 8,
    "delay": 0.05,
    "usernames_file": "usernames.txt",
    "sort_weights": {
        "len_weight": 40.0,
        "unique_frac_weight": 8.0,
        "sequential_weight": 35.0,
        "transitions_weight": 25.0,
        "special_char_penalty": -20.0,
        "digit_penalty": -8.0
    }
}

class JoinDateV4(tk.Tk):
    def __init__(self, project_dir):
        super().__init__()
        self.title("Join Date V4 - Integrated Tool")
        self.project_dir = project_dir
        self.config_path = os.path.join(project_dir, "gui_config.json")
        self.cfg = self.load_config(self.config_path)
        self._cancel_event = threading.Event()
        self.last_scored = None
        self.not_found = []
        self.last_generated = None
        self.create_widgets()
        self.refresh_preview()

    def load_config(self, path):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        self.cfg["threads"] = int(self.threads_var.get())
        self.cfg["usernames_file"] = self.usernames_var.get()
        self.cfg["sort_weights"] = {
            "len_weight": float(self.len_w.get()),
            "unique_frac_weight": float(self.unique_w.get()),
            "sequential_weight": float(self.seq_w.get()),
            "transitions_weight": float(self.trans_w.get()),
            "special_char_penalty": float(self.spec_w.get()),
            "digit_penalty": float(self.dig_w.get())
        }
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.cfg, f, indent=2)
            messagebox.showinfo("Saved", "Configuration saved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)

        row = 0
        ttk.Label(frm, text="Threads:").grid(column=0, row=row, sticky="w")
        self.threads_var = tk.IntVar(value=self.cfg.get("threads", 8))
        ttk.Entry(frm, textvariable=self.threads_var, width=6).grid(column=1, row=row, sticky="w")

        ttk.Label(frm, text="Usernames file:").grid(column=2, row=row, sticky="w", padx=(10,0))
        self.usernames_var = tk.StringVar(value=self.cfg.get("usernames_file", "usernames.txt"))
        ttk.Entry(frm, textvariable=self.usernames_var, width=30).grid(column=3, row=row, sticky="w")
        ttk.Button(frm, text="Browse", command=self.browse_usernames).grid(column=4, row=row, sticky="w")

        # weights
        row += 1
        sw = self.cfg.get("sort_weights", DEFAULT_CONFIG["sort_weights"]) or DEFAULT_CONFIG["sort_weights"]
        self.len_w = tk.DoubleVar(value=sw.get("len_weight", 40.0))
        self.unique_w = tk.DoubleVar(value=sw.get("unique_frac_weight", 8.0))
        self.seq_w = tk.DoubleVar(value=sw.get("sequential_weight", 35.0))
        self.trans_w = tk.DoubleVar(value=sw.get("transitions_weight", 25.0))
        self.spec_w = tk.DoubleVar(value=sw.get("special_char_penalty", -20.0))
        self.dig_w = tk.DoubleVar(value=sw.get("digit_penalty", -8.0))

        ttk.Label(frm, text="Len w:").grid(column=0, row=row, sticky="w")
        ttk.Entry(frm, textvariable=self.len_w, width=8).grid(column=1, row=row, sticky="w")
        ttk.Label(frm, text="Unique w:").grid(column=2, row=row, sticky="w")
        ttk.Entry(frm, textvariable=self.unique_w, width=8).grid(column=3, row=row, sticky="w")

        row += 1
        ttk.Label(frm, text="Seq w:").grid(column=0, row=row, sticky="w")
        ttk.Entry(frm, textvariable=self.seq_w, width=8).grid(column=1, row=row, sticky="w")
        ttk.Label(frm, text="Trans w:").grid(column=2, row=row, sticky="w")
        ttk.Entry(frm, textvariable=self.trans_w, width=8).grid(column=3, row=row, sticky="w")

        row += 1
        ttk.Label(frm, text="Spec pen:").grid(column=0, row=row, sticky="w")
        ttk.Entry(frm, textvariable=self.spec_w, width=8).grid(column=1, row=row, sticky="w")
        ttk.Label(frm, text="Digit pen:").grid(column=2, row=row, sticky="w")
        ttk.Entry(frm, textvariable=self.dig_w, width=8).grid(column=3, row=row, sticky="w")

        # buttons
        row += 1
        btn_frame = ttk.Frame(frm)
        btn_frame.grid(column=0, row=row, columnspan=5, pady=(8,0), sticky="w")
        ttk.Button(btn_frame, text="Generate usernames", command=self.on_generate).grid(column=0, row=0, padx=4)
        ttk.Button(btn_frame, text="Sort usernames now", command=self.on_sort).grid(column=1, row=0, padx=4)
        ttk.Button(btn_frame, text="Save scores", command=self.on_save_scores).grid(column=2, row=0, padx=4)
        ttk.Button(btn_frame, text="Save NOT FOUND", command=self.on_save_not_found).grid(column=3, row=0, padx=4)
        ttk.Button(btn_frame, text="Refresh list", command=self.on_refresh_list).grid(column=4, row=0, padx=4)
        ttk.Button(btn_frame, text="Cancel", command=self.on_cancel).grid(column=5, row=0, padx=4)

        row += 1
        self.progress = ttk.Progressbar(frm, length=500)
        self.progress.grid(column=0, row=row, columnspan=4, sticky="w", pady=(6,0))

        row += 1
        ttk.Label(frm, text="Preview (top results):").grid(column=0, row=row, sticky="w")
        row += 1
        self.preview = tk.Text(frm, height=18, width=100, wrap="none")
        self.preview.grid(column=0, row=row, columnspan=6, sticky="nsew")
        self.grid_rowconfigure(row, weight=1)

        # generation options
        row += 1
        gen_frame = ttk.Frame(frm)
        gen_frame.grid(column=0, row=row, columnspan=6, sticky="w", pady=(6,0))
        ttk.Label(gen_frame, text="Generate count:").grid(column=0, row=0, sticky="w")
        self.gen_count = tk.IntVar(value=1000)
        ttk.Entry(gen_frame, textvariable=self.gen_count, width=8).grid(column=1, row=0, sticky="w")
        ttk.Label(gen_frame, text="Min len:").grid(column=2, row=0, sticky="w")
        self.gen_min = tk.IntVar(value=6)
        ttk.Entry(gen_frame, textvariable=self.gen_min, width=6).grid(column=3, row=0, sticky="w")
        ttk.Label(gen_frame, text="Max len (<=7):").grid(column=4, row=0, sticky="w")
        self.gen_max = tk.IntVar(value=6)
        ttk.Entry(gen_frame, textvariable=self.gen_max, width=6).grid(column=5, row=0, sticky="w")
        ttk.Button(gen_frame, text="Save generated", command=self.on_save_generated).grid(column=6, row=0, padx=6)

        # internal
        self._current_task = None

    # ------------------ utilities ------------------
    def browse_usernames(self):
        p = filedialog.askopenfilename(initialdir=self.project_dir, title="Select usernames file")
        if p:
            self.usernames_var.set(os.path.relpath(p, self.project_dir))
            self.refresh_preview()

    def generate_username(self, min_length=6, max_length=6):
        length = random.randint(min_length, max_length)
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))

    def on_generate(self):
        count = max(1, int(self.gen_count.get()))
        min_len = max(1, int(self.gen_min.get()))
        max_len = min(7, max(1, int(self.gen_max.get())))
        names = [self.generate_username(min_len, max_len) for _ in range(count)]
        self.last_generated = names
        # append to usernames file
        path = os.path.join(self.project_dir, self.usernames_var.get())
        try:
            with open(path, "a", encoding="utf-8") as f:
                for n in names:
                    f.write(n + "\n")
            messagebox.showinfo("Generated", f"Appended {len(names)} usernames to {os.path.basename(path)}")
            self.refresh_preview()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_save_generated(self):
        if not self.last_generated:
            messagebox.showwarning("No generated", "No generated usernames in memory. Use 'Generate usernames' first.")
            return
        default = os.path.join(self.project_dir, f"generated_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt")
        p = filedialog.asksaveasfilename(initialdir=self.project_dir, defaultextension=".txt", initialfile=os.path.basename(default), title="Save generated as")
        if not p:
            return
        try:
            with open(p, 'w', encoding='utf-8') as f:
                for n in self.last_generated:
                    f.write(n + "\n")
            messagebox.showinfo("Saved", f"Saved {len(self.last_generated)} generated usernames to {os.path.basename(p)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------ sorting / scoring ------------------
    def rarity_score(self, name, weights):
        if not name:
            return -9999.0
        n = len(name)
        unique_frac = len(set(name)) / n
        seq = self.longest_sequential_run(name)
        trans = self.transitions_score(name)
        special_chars = sum(1 for c in name if not c.isalnum())
        digits = sum(1 for c in name if c.isdigit())

        score = 0.0
        score += weights.get("len_weight",40.0) * (1.0 / n)
        score += weights.get("unique_frac_weight",8.0) * unique_frac
        score += weights.get("sequential_weight",35.0) * (seq / max(1, n))
        score += weights.get("transitions_weight",25.0) * trans
        score += weights.get("special_char_penalty", -20.0) * special_chars
        score += weights.get("digit_penalty", -8.0) * digits
        return score

    def longest_sequential_run(self, name):
        if not name:
            return 0
        s = name.lower()
        best = 1
        cur = 1
        for i in range(1, len(s)):
            a, b = s[i-1], s[i]
            if a.isalpha() and b.isalpha():
                diff = ord(b) - ord(a)
                if diff == 1 or diff == -1:
                    cur += 1
                else:
                    cur = 1
            elif a.isdigit() and b.isdigit():
                diff = ord(b) - ord(a)
                if diff == 1 or diff == -1:
                    cur += 1
                else:
                    cur = 1
            else:
                cur = 1
            if cur > best:
                best = cur
        return best

    def transitions_score(self, name):
        s = ''.join([c for c in name if c.isalpha()])
        if len(s) < 2:
            return 0.0
        vowels = set('aeiou')
        trans = 0
        for i in range(1, len(s)):
            a, b = s[i-1] in vowels, s[i] in vowels
            if a != b:
                trans += 1
        return trans / max(1, len(s)-1)

    def sort_usernames_file(self, path, weights, progress_callback=None, cancel_event=None):
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path + ".backup." + ts
        shutil = __import__('shutil')
        shutil.copy2(path, backup)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [ln.rstrip("\n\r") for ln in f]
        entries = [ln.strip() for ln in lines if ln.strip()]

        scored = []
        total = len(entries)
        max_workers = max(1, int(weights.get('threads_override', 8)))
        completed = 0
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(lambda e: (self.rarity_score(e, weights), e), e): e for e in entries}
            for fut in as_completed(futures):
                if cancel_event and cancel_event.is_set():
                    for f in futures:
                        try:
                            f.cancel()
                        except Exception:
                            pass
                    return backup, 0, []
                try:
                    res = fut.result()
                except Exception:
                    res = (-9999.0, futures.get(fut, None))
                scored.append(res)
                completed += 1
                if progress_callback:
                    try:
                        progress_callback(completed, total)
                    except Exception:
                        pass

        scored.sort(key=lambda x: x[0], reverse=True)
        sorted_entries = [e for s,e in scored]
        with open(path, "w", encoding="utf-8") as f:
            for e in sorted_entries:
                f.write(e + "\n")
        return backup, len(entries), scored

    # ------------------ actions ------------------
    def on_sort(self):
        path = os.path.join(self.project_dir, self.usernames_var.get())
        if not os.path.exists(path):
            messagebox.showerror("Missing", "Usernames file not found")
            return
        weights = {
            'len_weight': float(self.len_w.get()),
            'unique_frac_weight': float(self.unique_w.get()),
            'sequential_weight': float(self.seq_w.get()),
            'transitions_weight': float(self.trans_w.get()),
            'special_char_penalty': float(self.spec_w.get()),
            'digit_penalty': float(self.dig_w.get())
        }
        weights['threads_override'] = max(1, int(self.threads_var.get()))
        self._cancel_event.clear()
        self.progress['value'] = 0

        def progress_cb(completed, total):
            def _u():
                try:
                    self.progress['maximum'] = total
                    self.progress['value'] = completed
                except Exception:
                    pass
            self.after(0, _u)

        def task():
            try:
                backup, count, scored = self.sort_usernames_file(path, weights, progress_callback=progress_cb, cancel_event=self._cancel_event)
            except FileNotFoundError:
                self.after(0, lambda: messagebox.showerror("Missing file", "Usernames file not found"))
                return
            if not scored:
                self.after(0, lambda: messagebox.showinfo("Canceled", "Sorting canceled or no results"))
                return
            self.last_scored = scored
            self.after(0, lambda: self.progress.configure(value=len(scored), maximum=len(scored)))
            self.after(0, lambda: messagebox.showinfo("Sorted", f"Sorted {len(scored)} usernames. Backup created: {os.path.basename(backup)}"))
            self.after(0, lambda: self.refresh_preview())

        t = threading.Thread(target=task, daemon=True)
        self._current_task = t
        t.start()

    def on_refresh_list(self):
        self.last_scored = None
        self.refresh_preview()

    def on_cancel(self):
        self._cancel_event.set()
        try:
            self.progress['value'] = 0
        except Exception:
            pass

    def refresh_preview(self):
        self.preview.delete('1.0', tk.END)
        path = os.path.join(self.project_dir, self.usernames_var.get())
        if os.path.exists(path):
            if self.last_scored:
                scored = list(self.last_scored)
            else:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [ln.strip() for ln in f if ln.strip()]
                weights = {
                    'len_weight': float(self.len_w.get()),
                    'unique_frac_weight': float(self.unique_w.get()),
                    'sequential_weight': float(self.seq_w.get()),
                    'transitions_weight': float(self.trans_w.get()),
                    'special_char_penalty': float(self.spec_w.get()),
                    'digit_penalty': float(self.dig_w.get())
                }
                weights['threads_override'] = max(1, int(self.threads_var.get()))
                scored = []
                with ThreadPoolExecutor(max_workers=weights['threads_override']) as ex:
                    futures = {ex.submit(lambda e: (self.rarity_score(e, weights), e), e): e for e in lines}
                    for fut in as_completed(futures):
                        try:
                            scored.append(fut.result())
                        except Exception:
                            scored.append((-9999.0, futures.get(fut, None)))
                scored.sort(key=lambda x: x[0], reverse=True)
            for s,e in scored[:200]:
                self.preview.insert(tk.END, f"{s:8.3f}    {e}\n")
        else:
            self.preview.insert(tk.END, "Usernames file not found\n")

    # ------------------ checking via API (integrated main.py) ------------------
    def check_username_api(self, username):
        url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"
        try:
            r = requests.get(url, timeout=8)
            data = r.json()
            code = data.get('code')
            if code == 0:
                return 'FOUND', data
            elif code == 1:
                return 'TAKEN', data
            elif code == 2:
                return 'CENSORED', data
            else:
                return 'UNKNOWN', data
        except requests.exceptions.RequestException as e:
            return 'GLITCH', {'error': str(e)}

    def run_check_batch(self, names, delay=0.05):
        results = []
        for n in names:
            if self._cancel_event.is_set():
                break
            status, data = self.check_username_api(n)
            results.append((n, status, data))
            time.sleep(delay)
        return results

    def on_save_scores(self):
        if not self.last_scored:
            messagebox.showwarning("No scores", "Run sort first")
            return
        default = os.path.join(self.project_dir, f"username_scores_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt")
        p = filedialog.asksaveasfilename(initialdir=self.project_dir, defaultextension=".txt", initialfile=os.path.basename(default), title="Save scores as")
        if not p:
            return
        with open(p, 'w', encoding='utf-8') as f:
            for s,e in self.last_scored:
                f.write(f"{s:.6f}\t{e}\n")
        messagebox.showinfo("Saved", f"Scores saved to {os.path.basename(p)}")

    def on_save_not_found(self):
        # run a quick pass to check top not found from file and save them
        path = os.path.join(self.project_dir, self.usernames_var.get())
        if not os.path.exists(path):
            messagebox.showerror("Missing", "Usernames file not found")
            return
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        # check in parallel
        threads = max(1, int(self.threads_var.get()))
        not_found = []
        def task(n):
            status, data = self.check_username_api(n)
            if status in ('FOUND','TAKEN'):
                return None
            return (n, status, data)
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futures = {ex.submit(task, n): n for n in lines}
            for fut in as_completed(futures):
                try:
                    res = fut.result()
                    if res:
                        not_found.append(res)
                except Exception:
                    pass
        if not not_found:
            messagebox.showinfo("None", "No NOT FOUND items found")
            return
        default = os.path.join(self.project_dir, f"not_found_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt")
        p = filedialog.asksaveasfilename(initialdir=self.project_dir, defaultextension=".txt", initialfile=os.path.basename(default), title="Save not found as")
        if not p:
            return
        with open(p, 'w', encoding='utf-8') as f:
            for n,status,data in not_found:
                f.write(f"{n}\t{status}\t{data}\n")
        messagebox.showinfo("Saved", f"Saved {len(not_found)} records to {os.path.basename(p)}")


if __name__ == '__main__':
    project = os.path.dirname(os.path.abspath(__file__))
    app = JoinDateV4(project)
    app.mainloop()
