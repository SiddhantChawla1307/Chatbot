import tkinter as tk
from tkinter import scrolledtext
from ai_client import get_bot_response  # ✅ backend logic

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Chatbot")
root.geometry("400x500")
root.resizable(False, False)

# ---------------- CHAT AREA ----------------
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 11),
    state=tk.DISABLED
)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# ---------------- INPUT FRAME ----------------
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10, fill=tk.X)

user_input = tk.Entry(input_frame, font=("Arial", 12))
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

# ---------------- SEND LOGIC ----------------
def send_message(event=None):
    message = user_input.get().strip()
    if not message:
        return

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {message}\n")

    # ✅ INTEGRATION POINT (your responsibility)
    bot_reply = get_bot_response(message)
    chat_area.insert(tk.END, f"Bot: {bot_reply}\n\n")

    chat_area.config(state=tk.DISABLED)
    chat_area.see(tk.END)

    user_input.delete(0, tk.END)
    user_input.focus_set()

# ---------------- BUTTON + BINDINGS ----------------
send_button = tk.Button(
    input_frame,
    text="Send",
    width=10,
    command=send_message
)
send_button.pack(side=tk.RIGHT)

user_input.bind("<Return>", send_message)

# ---------------- CLEAN EXIT ----------------
user_input.focus_set()
root.protocol("WM_DELETE_WINDOW", root.quit)

root.mainloop()
