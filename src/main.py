import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import uuid
import matplotlib.pyplot as plt

# Fruit prices per kg or per piece
fruit_prices = {
    'apple': 90.1,
    'mango': 68,
    'orange': 73.92,
    'banana': 45.5,
    'grape': 112,
    'watermelon': 21,
    'pineapple': 52,
    'papaya': 39,
    'pomegranate': 145,
    'guava': 64,
    'avocado': 140,      # per piece
    'dragonfruit': 105.60,  # per piece
    'cherry': 1761      # per kg
}

# Units for each fruit
fruit_units = {
    'apple': 'kg',
    'mango': 'kg',
    'orange': 'kg',
    'banana': 'kg',
    'grape': 'kg',
    'watermelon': 'kg',
    'pineapple': 'kg',
    'papaya': 'kg',
    'pomegranate': 'kg',
    'guava': 'kg',
    'avocado': 'pc',
    'dragonfruit': 'pc',
    'cherry': 'kg'
}

# Discount rates for each fruit (e.g., 0.05 means 5% discount)
fruit_discounts = {
    'apple': 0.00,
    'mango': 0.00,
    'orange': 0.00,
    'banana': 0.00,
    'grape': 0.05,
    'watermelon': 0.00,
    'pineapple': 0.00,
    'papaya': 0.00,
    'pomegranate': 0.05,
    'guava': 0.05,
    'avocado': 0.10,
    'dragonfruit': 0.10,
    'cherry': 0.15
}

# Cost price per kg or per piece for each fruit
fruit_cost_prices = {
    'apple': 70,
    'mango': 50,
    'orange': 60,
    'banana': 30,
    'grape': 90,
    'watermelon': 15,
    'pineapple': 40,
    'papaya': 25,
    'pomegranate': 120,
    'guava': 50,
    'avocado': 100,
    'dragonfruit': 80,
    'cherry': 1500
}

class FruitBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruit Cost Calculator")
        self.root.geometry("700x550")
        self.root.minsize(600, 400)  # scalable window with min size

        self.fruits = []
        self.total_cost = 0

        # Setup SQLite connection and tables
        self.conn = sqlite3.connect('fruit_billing.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Fruit selection
        tk.Label(root, text="Fruit Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.fruit_var = tk.StringVar()
        self.fruit_dropdown = ttk.Combobox(root, textvariable=self.fruit_var, state="readonly")
        self.fruit_dropdown['values'] = list(fruit_prices.keys())
        self.fruit_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Quantity entry
        tk.Label(root, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.qty_entry = tk.Entry(root)
        self.qty_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.add_button = tk.Button(button_frame, text="Add to Bill", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear Bill", command=self.clear_bill)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text="Save Bill", command=self.save_bill)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.bargraph_button = tk.Button(button_frame, text="Show Bar Graph", command=self.show_bar_graph)
        self.bargraph_button.pack(side=tk.LEFT, padx=5)

        self.piechart_button = tk.Button(button_frame, text="Show Pie Chart", command=self.show_pie_chart)
        self.piechart_button.pack(side=tk.LEFT, padx=5)

        self.profit_piechart_button = tk.Button(button_frame, text="Show Profit Pie Chart", command=self.show_profit_pie_chart)
        self.profit_piechart_button.pack(side=tk.LEFT, padx=5)

        # Treeview setup
        self.tree = ttk.Treeview(root, columns=('Fruit', 'Qty', 'Rate', 'Discount', 'Total'), show='headings')
        self.tree.heading('Fruit', text='Fruit')
        self.tree.heading('Qty', text='Quantity')
        self.tree.heading('Rate', text='Rate')
        self.tree.heading('Discount', text='Discount')
        self.tree.heading('Total', text='Cost')

        # Align columns: Fruit=left, Qty=center, Rate=right, Discount=right, Total=right
        self.tree.column('Fruit', anchor='w', width=120)
        self.tree.column('Qty', anchor='center', width=80)
        self.tree.column('Rate', anchor='e', width=100)
        self.tree.column('Discount', anchor='e', width=100)
        self.tree.column('Total', anchor='e', width=100)

        self.tree.grid(row=3, column=0, columnspan=2, pady=10, sticky='nsew')

        # Summary labels
        label_font = ("Arial", 12)
        tk.Label(root, text="Total:").grid(row=4, column=0, sticky='w', padx=10)
        self.total_amt_value = tk.Label(root, text="₹0.00", font=label_font, anchor='e', width=12)
        self.total_amt_value.grid(row=4, column=1, sticky='e', padx=(0, 10))

        tk.Label(root, text="Discount:").grid(row=5, column=0, sticky='w', padx=10)
        self.discount_value = tk.Label(root, text="₹0.00", font=label_font, anchor='e', width=12)
        self.discount_value.grid(row=5, column=1, sticky='e', padx=(0, 10))

        tk.Label(root, text="Final Total:").grid(row=6, column=0, sticky='w', padx=10, pady=(0, 10))
        self.final_total_value = tk.Label(root, text="₹0.00", font=label_font, anchor='e', width=12)
        self.final_total_value.grid(row=6, column=1, sticky='e', padx=(0, 10), pady=(0, 10))

        # Removed profit label and value from bill summary
        # tk.Label(root, text="Profit:").grid(row=7, column=0, sticky='w', padx=10, pady=(0, 10))
        # self.profit_value = tk.Label(root, text="₹0.00", font=label_font, anchor='e', width=12)
        # self.profit_value.grid(row=7, column=1, sticky='e', padx=(0, 10), pady=(0, 10))

        # Make grid cells expandable for scaling window
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.fruit_discounts = fruit_discounts

    def create_tables(self):
        # Create bills and bill_items tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id TEXT PRIMARY KEY,
                total REAL,
                discount REAL,
                final_total REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bill_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_id TEXT,
                fruit TEXT,
                qty REAL,
                rate REAL,
                total_cost REAL,
                FOREIGN KEY (bill_id) REFERENCES bills(id)
            )
        ''')
        self.conn.commit()

    def add_item(self):
        fruit = self.fruit_var.get().strip().lower()
        if fruit == '':
            messagebox.showerror("Input Error", "Please select a fruit.")
            return
        try:
            qty = float(self.qty_entry.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive quantity.")
            return

        if fruit not in fruit_prices:
            messagebox.showerror("Input Error", f"Price for '{fruit}' not found.")
            return

        rate = fruit_prices[fruit]
        cost = rate * qty
        discount_rate = self.fruit_discounts.get(fruit, 0)
        discount_amt = cost * discount_rate
        cost_after_discount = cost - discount_amt
        cost_price = fruit_cost_prices.get(fruit, 0) * qty
        self.fruits.append((fruit, qty, rate, cost, discount_rate, cost_price))
        self.total_cost += cost

        unit = fruit_units.get(fruit, 'kg')
        qty_text = f"{qty} {unit}"
        rate_text = f"₹{rate:.2f} /{unit}"
        discount_text = f"{discount_rate * 100:.0f}%"  # Show percentage

        # Show discount percentage and cost after discount in the table
        self.tree.insert('', 'end', values=(
            fruit.capitalize(), qty_text, rate_text, discount_text, f"₹{cost_after_discount:.2f}"
        ))
        self.update_total()

        self.qty_entry.delete(0, tk.END)
        self.fruit_var.set("")

    def update_total(self):
        # Calculate total discount based on each fruit's discount rate
        total_discount = sum(cost * discount for _, _, _, cost, discount, _ in self.fruits)
        final_total = self.total_cost - total_discount
        # total_cost_price = sum(cost_price for *_, cost_price in self.fruits)
        # profit = final_total - total_cost_price

        self.total_amt_value.config(text=f"₹{self.total_cost:.2f}")
        self.discount_value.config(text=f"₹{total_discount:.2f}")
        self.final_total_value.config(text=f"₹{final_total:.2f}")
        # self.profit_value.config(text=f"₹{profit:.2f}")

    def clear_bill(self):
        self.fruits.clear()
        self.total_cost = 0
        self.tree.delete(*self.tree.get_children())
        self.update_total()
        self.fruit_var.set("")
        self.qty_entry.delete(0, tk.END)

    def save_bill(self):
        if not self.fruits:
            messagebox.showwarning("Save Error", "No items to save.")
            return

        bill_id = str(uuid.uuid4())
        total_discount = sum(cost * discount for _, _, _, cost, discount, _ in self.fruits)
        final_total = self.total_cost - total_discount

        try:
            self.cursor.execute("INSERT INTO bills (id, total, discount, final_total) VALUES (?, ?, ?, ?)",
                                (bill_id, self.total_cost, total_discount, final_total))
            for fruit, qty, rate, cost, discount, _ in self.fruits:
                self.cursor.execute(
                    "INSERT INTO bill_items (bill_id, fruit, qty, rate, total_cost) VALUES (?, ?, ?, ?, ?)",
                    (bill_id, fruit, qty, rate, cost)
                )
            self.conn.commit()
            messagebox.showinfo("Success", "Bill saved successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error saving bill: {e}")

    def show_bar_graph(self):
        # Sum quantities sold per fruit across all bills
        self.cursor.execute("SELECT fruit, SUM(qty) FROM bill_items GROUP BY fruit")
        data = self.cursor.fetchall()
        if not data:
            messagebox.showinfo("No Data", "No sales data to display.")
            return
        fruits = [row[0].capitalize() for row in data]
        quantities = [row[1] for row in data]

        plt.figure(figsize=(10, 6))
        plt.bar(fruits, quantities, color='skyblue')
        plt.xlabel("Fruits")
        plt.ylabel("Total Quantity Sold")
        plt.title("Fruits Sold - Bar Graph")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_pie_chart(self):
        # Sum revenue per fruit across all bills
        self.cursor.execute("SELECT fruit, SUM(total_cost) FROM bill_items GROUP BY fruit")
        data = self.cursor.fetchall()
        if not data:
            messagebox.showinfo("No Data", "No sales data to display.")
            return
        fruits = [row[0].capitalize() for row in data]
        revenues = [row[1] for row in data]

        plt.figure(figsize=(8, 8))
        plt.pie(revenues, labels=fruits, autopct='%1.1f%%', startangle=140)
        plt.title("Revenue Distribution by Fruit - Pie Chart")
        plt.tight_layout()
        plt.show()

    def show_profit_pie_chart(self):
        # Calculate profit per fruit across all bills
        self.cursor.execute("SELECT fruit, SUM(qty), SUM(total_cost) FROM bill_items GROUP BY fruit")
        data = self.cursor.fetchall()
        if not data:
            messagebox.showinfo("No Data", "No sales data to display.")
            return

        fruits = []
        profits = []
        for row in data:
            fruit = row[0]
            total_qty = row[1]
            total_revenue = row[2]
            cost_price = fruit_cost_prices.get(fruit, 0)
            total_cost = cost_price * total_qty
            profit = total_revenue - total_cost
            if profit > 0:
                fruits.append(fruit.capitalize())
                profits.append(profit)

        if not profits:
            messagebox.showinfo("No Profit", "No profitable fruits to display.")
            return

        plt.figure(figsize=(8, 8))
        plt.pie(profits, labels=fruits, autopct='%1.1f%%', startangle=140)
        plt.title("Profit Distribution by Fruit - Pie Chart")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = FruitBillingApp(root)
    root.mainloop()