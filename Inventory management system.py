import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# ---------- Backend Class ----------
class InventoryDB:
    def __init__(self, db_name="inventory.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS products (
                        product_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price REAL NOT NULL
                   )"""
        self.conn.execute(query)
        self.conn.commit()

    def add_product(self, product_id, name, quantity, price):
        try:
            self.conn.execute("INSERT INTO products VALUES (?, ?, ?, ?)", 
                              (product_id, name, quantity, price))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def view_products(self):
        cursor = self.conn.execute("SELECT * FROM products")
        return cursor.fetchall()

    def search_product(self, product_id):
        cursor = self.conn.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
        return cursor.fetchone()

    def update_product(self, product_id, name, quantity, price):
        cursor = self.conn.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
        if cursor.fetchone() is None:
            return False
        self.conn.execute("UPDATE products SET name=?, quantity=?, price=? WHERE product_id=?",
                          (name, quantity, price, product_id))
        self.conn.commit()
        return True

    def delete_product(self, product_id):
        cursor = self.conn.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
        if cursor.fetchone() is None:
            return False
        self.conn.execute("DELETE FROM products WHERE product_id=?", (product_id,))
        self.conn.commit()
        return True


# ---------- GUI Class ----------
class InventoryGUI:
    def __init__(self, root):
        self.db = InventoryDB()
        self.root = root
        self.root.title("🛒 Inventory Management System")
        self.root.geometry("750x500")
        self.root.configure(bg="lightyellow")

        # ----- Input Frame -----
        frame = tk.Frame(root, bg="lightyellow")
        frame.pack(pady=10)

        tk.Label(frame, text="Product ID:", bg="lightyellow").grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = tk.Entry(frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Name:", bg="lightyellow").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Quantity:", bg="lightyellow").grid(row=2, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(frame)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Price:", bg="lightyellow").grid(row=3, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(frame)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5)

        # ----- Buttons -----
        btn_frame = tk.Frame(root, bg="lightyellow")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Product", command=self.add_product, bg="green", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="View All", command=self.view_products, bg="blue", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Search", command=self.search_product, bg="orange", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_product, bg="purple", fg="white").grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_product, bg="red", fg="white").grid(row=0, column=4, padx=5)

        # ----- Table -----
        self.tree = ttk.Treeview(root, columns=("id", "name", "quantity", "price"), show="headings", height=10)
        self.tree.heading("id", text="Product ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("price", text="Price")
        self.tree.pack(fill="both", expand=True, pady=10)

    # ----- Functions -----
    def add_product(self):
        pid = self.id_entry.get()
        name = self.name_entry.get()
        qty = self.quantity_entry.get()
        price = self.price_entry.get()

        if pid and name and qty and price:
            if self.db.add_product(pid, name, int(qty), float(price)):
                messagebox.showinfo("Success", "Product Added Successfully!")
                self.view_products()
            else:
                messagebox.showerror("Error", "Product with this ID already exists!")
        else:
            messagebox.showwarning("Warning", "Please fill all fields!")

    def view_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for product in self.db.view_products():
            self.tree.insert("", "end", values=product)

    def search_product(self):
        pid = self.id_entry.get()
        product = self.db.search_product(pid)
        if product:
            messagebox.showinfo("Found", f"ID: {product[0]}\nName: {product[1]}\nQty: {product[2]}\nPrice: {product[3]}")
        else:
            messagebox.showerror("Not Found", "No product with this ID")

    def update_product(self):
        pid = self.id_entry.get()
        name = self.name_entry.get()
        qty = self.quantity_entry.get()
        price = self.price_entry.get()

        if pid and name and qty and price:
            if self.db.update_product(pid, name, int(qty), float(price)):
                messagebox.showinfo("Updated", "Product Updated Successfully!")
                self.view_products()
            else:
                messagebox.showerror("Error", "Product not found!")
        else:
            messagebox.showwarning("Warning", "Fill all fields!")

    def delete_product(self):
        pid = self.id_entry.get()
        if pid:
            if self.db.delete_product(pid):
                messagebox.showinfo("Deleted", "Product Deleted Successfully!")
                self.view_products()
            else:
                messagebox.showerror("Error", "Product not found!")
        else:
            messagebox.showwarning("Warning", "Enter Product ID to delete!")


# ---------- Run GUI ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop()
