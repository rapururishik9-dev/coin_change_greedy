# 💰 Coin Change — Greedy Algorithm (Python + Tkinter)

A simple desktop GUI app that solves the **Coin Change problem** using the **Greedy Algorithm**.

---

## 🧠 What is the Greedy Approach?

The greedy strategy always picks the **largest denomination coin** that fits into the remaining amount, repeating until the full amount is covered.

> ⚠️ Greedy works perfectly for standard currency systems (Indian ₹, US cents, Euro).  
> It may **not** always give the optimal answer for arbitrary coin sets.

---

## 🖥️ Features

- Clean dark-themed GUI built with **Tkinter** (no extra libraries needed)
- Choose from presets: **Indian ₹, US Cents, Euro Cent**, or enter **Custom** coins
- Visual **bar chart** breakdown of coins used
- **Step-by-step trace** of the greedy algorithm
- Works with any positive integer amount

---

## 📁 Project Structure

```
coin_change_greedy/
│
├── coin_change.py     # Main file — algorithm + GUI
└── README.md
```

---

## ▶️ How to Run

**Requirements:** Python 3.x (Tkinter is built-in, no pip install needed)

```bash
git clone https://github.com/YOUR_USERNAME/coin_change_greedy.git
cd coin_change_greedy
python coin_change.py
```

---

## 📸 How it Works

1. Enter the **amount** you want to make change for
2. Select a **coin preset** or type your own coin denominations
3. Click **▶ SOLVE**
4. See the minimum coins used + step-by-step greedy trace

---

## 🧩 Algorithm (core logic)

```python
def greedy_coin_change(amount, denominations):
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

    return result
```

**Time Complexity:** O(n) — where n = number of coin denominations  
**Space Complexity:** O(n)

---

## 👨‍💻 Author

Made as a Python Greedy Algorithm project.
