import tkinter as tk
from tkinter import messagebox


# ─────────────────────────────────────────
#  GREEDY ALGORITHM (core logic)
# ─────────────────────────────────────────
def greedy_coin_change(amount, denominations):
    """
    Greedy approach: always pick the largest coin that fits.
    Returns a dict {coin: count} and the total coins used.
    """
    denominations = sorted(denominations, reverse=True)
    result = {}
    remaining = amount

    for coin in denominations:
        if remaining <= 0:
            break
        count = remaining // coin
        if count > 0:
            result[coin] = count
            remaining -= coin * count

    if remaining != 0:
        return None, -1  # can't make exact change

    total_coins = sum(result.values())
    return result, total_coins


# ─────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────
class CoinChangeApp:
    BG        = "#0f0f13"
    PANEL     = "#1a1a24"
    ACCENT    = "#f0c040"
    ACCENT2   = "#e05c5c"
    TEXT      = "#e8e8f0"
    MUTED     = "#6a6a8a"
    COIN_COLORS = ["#f0c040", "#a0c8f0", "#80e8a0", "#f09060", "#d080f0", "#60d0e0"]

    PRESETS = {
        "Indian ₹":  [1, 2, 5, 10, 20, 50, 100, 200, 500],
        "US Cents":  [1, 5, 10, 25, 50, 100],
        "Euro Cent": [1, 2, 5, 10, 20, 50, 100, 200],
        "Custom":    [],
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Coin Change — Greedy Algorithm")
        self.root.geometry("700x620")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        self._build_ui()

    # ── UI construction ──────────────────
    def _build_ui(self):
        # Title bar
        title_frame = tk.Frame(self.root, bg=self.ACCENT, height=4)
        title_frame.pack(fill="x")

        header = tk.Frame(self.root, bg=self.BG, pady=18)
        header.pack(fill="x", padx=30)

        tk.Label(header, text="COIN CHANGE", font=("Courier New", 22, "bold"),
                 bg=self.BG, fg=self.ACCENT).pack(side="left")
        tk.Label(header, text=" · GREEDY", font=("Courier New", 22),
                 bg=self.BG, fg=self.MUTED).pack(side="left")

        # ── Input panel ──
        panel = tk.Frame(self.root, bg=self.PANEL, bd=0, padx=24, pady=20)
        panel.pack(fill="x", padx=30, pady=(0, 12))

        # Amount
        row1 = tk.Frame(panel, bg=self.PANEL)
        row1.pack(fill="x", pady=(0, 14))
        tk.Label(row1, text="Amount  :", font=("Courier New", 12),
                 bg=self.PANEL, fg=self.MUTED, width=14, anchor="w").pack(side="left")
        self.amount_var = tk.StringVar(value="247")
        amount_entry = tk.Entry(row1, textvariable=self.amount_var,
                                font=("Courier New", 14, "bold"), width=12,
                                bg="#0f0f13", fg=self.ACCENT,
                                insertbackground=self.ACCENT,
                                relief="flat", bd=6)
        amount_entry.pack(side="left")

        # Preset selector
        row2 = tk.Frame(panel, bg=self.PANEL)
        row2.pack(fill="x", pady=(0, 10))
        tk.Label(row2, text="Preset  :", font=("Courier New", 12),
                 bg=self.PANEL, fg=self.MUTED, width=14, anchor="w").pack(side="left")
        self.preset_var = tk.StringVar(value="Indian ₹")
        for label in self.PRESETS:
            rb = tk.Radiobutton(row2, text=label, variable=self.preset_var,
                                value=label, command=self._on_preset,
                                font=("Courier New", 11),
                                bg=self.PANEL, fg=self.TEXT,
                                selectcolor=self.BG,
                                activebackground=self.PANEL,
                                activeforeground=self.ACCENT)
            rb.pack(side="left", padx=6)

        # Coins entry
        row3 = tk.Frame(panel, bg=self.PANEL)
        row3.pack(fill="x")
        tk.Label(row3, text="Coins   :", font=("Courier New", 12),
                 bg=self.PANEL, fg=self.MUTED, width=14, anchor="w").pack(side="left")
        self.coins_var = tk.StringVar(value="1, 2, 5, 10, 20, 50, 100, 200, 500")
        coins_entry = tk.Entry(row3, textvariable=self.coins_var,
                               font=("Courier New", 12), width=38,
                               bg="#0f0f13", fg=self.TEXT,
                               insertbackground=self.TEXT,
                               relief="flat", bd=6)
        coins_entry.pack(side="left")

        # Solve button
        btn = tk.Button(self.root, text="▶  SOLVE",
                        font=("Courier New", 13, "bold"),
                        bg=self.ACCENT, fg=self.BG,
                        activebackground="#d4a830", activeforeground=self.BG,
                        relief="flat", bd=0, padx=20, pady=10,
                        cursor="hand2", command=self.solve)
        btn.pack(pady=(0, 18))

        # ── Output area ──
        self.out_frame = tk.Frame(self.root, bg=self.BG)
        self.out_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def _on_preset(self):
        name = self.preset_var.get()
        coins = self.PRESETS[name]
        if coins:
            self.coins_var.set(", ".join(map(str, coins)))

    # ── Solve ────────────────────────────
    def solve(self):
        # Clear previous output
        for w in self.out_frame.winfo_children():
            w.destroy()

        # Parse inputs
        try:
            amount = int(self.amount_var.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a positive integer.")
            return

        try:
            raw = self.coins_var.get().strip()
            denoms = sorted(set(int(x.strip()) for x in raw.split(",") if x.strip()), reverse=True)
            if not denoms or any(d <= 0 for d in denoms):
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Coins must be positive integers separated by commas.")
            return

        result, total = greedy_coin_change(amount, denoms)

        if result is None:
            tk.Label(self.out_frame,
                     text=f"✗  Cannot make exact change for {amount} with given coins.",
                     font=("Courier New", 12), bg=self.BG, fg=self.ACCENT2).pack(pady=20)
            return

        # Summary row
        summary = tk.Frame(self.out_frame, bg=self.PANEL, padx=16, pady=12)
        summary.pack(fill="x", pady=(0, 12))
        tk.Label(summary, text=f"Amount : {amount}",
                 font=("Courier New", 12), bg=self.PANEL, fg=self.MUTED).pack(side="left")
        tk.Label(summary, text=f"Total coins used : {total}",
                 font=("Courier New", 13, "bold"), bg=self.PANEL, fg=self.ACCENT).pack(side="right")

        # Coin breakdown
        for i, (coin, count) in enumerate(sorted(result.items(), reverse=True)):
            color = self.COIN_COLORS[i % len(self.COIN_COLORS)]
            row = tk.Frame(self.out_frame, bg=self.BG, pady=4)
            row.pack(fill="x")

            # Coin badge
            badge = tk.Label(row, text=f" {coin:>5} ",
                             font=("Courier New", 12, "bold"),
                             bg=color, fg=self.BG, padx=8, pady=4)
            badge.pack(side="left")

            # Bar
            bar_bg = tk.Frame(row, bg=self.PANEL, height=28, width=360)
            bar_bg.pack(side="left", padx=10)
            bar_bg.pack_propagate(False)

            max_count = max(result.values())
            bar_w = int((count / max_count) * 350) + 10
            bar = tk.Frame(bar_bg, bg=color, height=28, width=bar_w)
            bar.place(x=0, y=0)

            tk.Label(bar_bg, text=f"× {count}  =  {coin * count}",
                     font=("Courier New", 11, "bold"),
                     bg=self.PANEL, fg=self.TEXT).place(relx=0.5, rely=0.5, anchor="center")

        # Step-by-step trace
        sep = tk.Frame(self.out_frame, bg=self.MUTED, height=1)
        sep.pack(fill="x", pady=10)
        tk.Label(self.out_frame, text="Step-by-step trace:",
                 font=("Courier New", 10), bg=self.BG, fg=self.MUTED).pack(anchor="w")

        remaining = amount
        for coin in sorted(result.keys(), reverse=True):
            count = result[coin]
            tk.Label(self.out_frame,
                     text=f"  {remaining:>5}  ÷  {coin}  →  take {count}  (−{coin*count})  →  remaining = {remaining - coin*count}",
                     font=("Courier New", 10), bg=self.BG, fg=self.MUTED, anchor="w").pack(fill="x")
            remaining -= coin * count


# ─────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = CoinChangeApp(root)
    root.mainloop()