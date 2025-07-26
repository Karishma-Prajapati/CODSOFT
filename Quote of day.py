import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

FAVORITES_FILE = "favorites.json"

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quote of the Day")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.quote_text = tk.StringVar()

        self.quote_label = tk.Label(root, textvariable=self.quote_text, wraplength=450, font=("Helvetica", 12), justify="center")
        self.quote_label.pack(pady=20)

        self.author_label = tk.Label(root, text="", font=("Helvetica", 10, "italic"))
        self.author_label.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.refresh_btn = tk.Button(btn_frame, text="🔄 Refresh", command=self.get_quote)
        self.refresh_btn.grid(row=0, column=0, padx=5)

        self.copy_btn = tk.Button(btn_frame, text="📋 Copy", command=self.copy_quote)
        self.copy_btn.grid(row=0, column=1, padx=5)

        self.favorite_btn = tk.Button(btn_frame, text="❤ Save Favorite", command=self.save_favorite)
        self.favorite_btn.grid(row=0, column=2, padx=5)

        self.view_btn = tk.Button(root, text="📖 View Favorites", command=self.view_favorites)
        self.view_btn.pack(pady=10)

        self.get_quote()

    def get_quote(self):
        try:
            response = requests.get("https://zenquotes.io/api/random")
            if response.status_code == 200:
                data = response.json()[0]
                self.current_quote = f"{data['q']}"
                self.current_author = f"- {data['a']}"
                self.quote_text.set(self.current_quote)
                self.author_label.config(text=self.current_author)
            else:
                self.quote_text.set("Failed to fetch quote. Try again.")
                self.author_label.config(text="")
        except Exception as e:
            self.quote_text.set("Error fetching quote.")
            self.author_label.config(text="")

    def copy_quote(self):
        full_quote = f"{self.current_quote} {self.current_author}"
        self.root.clipboard_clear()
        self.root.clipboard_append(full_quote)
        messagebox.showinfo("Copied", "Quote copied to clipboard!")

    def save_favorite(self):
        favorite = {
            "quote": self.current_quote,
            "author": self.current_author
        }

        favorites = []
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r") as f:
                favorites = json.load(f)

        favorites.append(favorite)
        with open(FAVORITES_FILE, "w") as f:
            json.dump(favorites, f, indent=2)

        messagebox.showinfo("Saved", "Quote added to favorites!")

    def view_favorites(self):
        if not os.path.exists(FAVORITES_FILE):
            messagebox.showinfo("No Favorites", "You haven't saved any quotes yet.")
            return

        with open(FAVORITES_FILE, "r") as f:
            favorites = json.load(f)

        fav_window = tk.Toplevel(self.root)
        fav_window.title("Favorite Quotes")
        fav_window.geometry("500x300")

        text_area = tk.Text(fav_window, wrap="word", font=("Helvetica", 10))
        text_area.pack(expand=True, fill="both", padx=10, pady=10)

        for item in favorites:
            text_area.insert(tk.END, f"{item['quote']} {item['author']}\n\n")

        text_area.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()