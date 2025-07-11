import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime

class AAA_TradersApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide until splash is done
        self.PURCHASE_FILE = "purchase_data.csv"
        self.SALE_FILE = "sale_data.csv"
        self.MODEL_HISTORY_FILE = "model_history.csv"
        self.ELECTRONICS_ITEMS = [
            "Laptop", "Washing Machine", "Juicer", "LED", "Iron",
            "Air Fryer", "Blender", "Cooler", "Water Dispenser", "Steamer", "AC"
        ]
        self.CITIES = ["Lahore", "Multan", "Faisalabad", "Karachi", "Islamabad"]
        self.model_history = self.load_model_history()
        self.create_csv_files()
        self.setup_main_window()
        self.create_widgets()
        self.show_splash()

    def create_csv_files(self):
        # Create or reset purchase CSV
        purchase_columns = ["Date", "Item", "Company", "Model", "Dealer", "City", "Price Per Unit", "Units Purchased"]
        try:
            if not os.path.exists(self.PURCHASE_FILE) or os.path.getsize(self.PURCHASE_FILE) == 0:
                df = pd.DataFrame(columns=purchase_columns)
                df.to_csv(self.PURCHASE_FILE, index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create purchase_data.csv: {str(e)}")
            return

        # Create or reset sale CSV
        sale_columns = ["Date", "Sale Dealer", "Item Sold", "Company", "Model", "Units Sold", "Sale Price Per Unit", "Total Bill", "Profit"]
        try:
            if not os.path.exists(self.SALE_FILE) or os.path.getsize(self.SALE_FILE) == 0:
                df = pd.DataFrame(columns=sale_columns)
                df.to_csv(self.SALE_FILE, index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create sale_data.csv: {str(e)}")
            return

        # Create or reset model history CSV
        model_columns = ["Item", "Company", "Model"]
        try:
            if not os.path.exists(self.MODEL_HISTORY_FILE) or os.path.getsize(self.MODEL_HISTORY_FILE) == 0:
                df = pd.DataFrame(columns=model_columns)
                df.to_csv(self.MODEL_HISTORY_FILE, index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create model_history.csv: {str(e)}")
            return

    def load_model_history(self):
        try:
            if os.path.exists(self.MODEL_HISTORY_FILE) and os.path.getsize(self.MODEL_HISTORY_FILE) > 0:
                df = pd.read_csv(self.MODEL_HISTORY_FILE)
                return df.groupby('Item')['Model'].apply(list).to_dict()
            return {}
        except Exception as e:
            messagebox.showwarning("Warning", f"Error loading model history: {str(e)}. Starting with empty history.")
            return {}

    def save_model_history(self, item, company, model):
        if item and company and model:
            try:
                df = pd.read_csv(self.MODEL_HISTORY_FILE)
                new_row = {"Item": item, "Company": company, "Model": model}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(self.MODEL_HISTORY_FILE, index=False)
                if item not in self.model_history:
                    self.model_history[item] = []
                if model not in self.model_history[item]:
                    self.model_history[item].append(model)
                    self.entry_model['values'] = self.model_history.get(self.combo_item.get(), [])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save model history: {str(e)}")

    def setup_main_window(self):
        self.root.title("AAA Traders")
        self.root.geometry("900x700")
        self.center_window(self.root, 900, 700)
        self.root.resizable(True, True)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook.Tab", 
                       background="#E8F5E9", 
                       foreground="black", 
                       padding=[20, 10], 
                       font=("Arial", 14))
        style.map("TNotebook.Tab", 
                  background=[("selected", "#C8E6C9")])
        style.configure("TButton", 
                       background="#4CAF50", 
                       foreground="white", 
                       padding=10, 
                       relief="flat", 
                       font=("Arial", 12))
        style.configure("TEntry", 
                       fieldbackground="#F0F0F0", 
                       foreground="black", 
                       padding=10)
        style.configure("TLabel", 
                       foreground="black", 
                       font=("Arial", 14))
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill='both')

    def show_splash(self):
        splash = tk.Toplevel(self.root)
        splash.overrideredirect(True)
        splash.title("AAA Traders - Loading...")
        splash.geometry("400x200")
        self.center_window(splash, 400, 200)
        label = tk.Label(splash, text="Welcome to AAA Traders", font=("Arial", 18), bg="#2E7D32", fg="white")
        label.pack(expand=True, fill=tk.BOTH)
        splash.after(5000, lambda: [splash.destroy(), self.root.deiconify()])

    def center_window(self, window, width=800, height=600):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.create_purchase_tab()
        self.create_sale_tab()
        self.create_view_tab()

    def create_purchase_tab(self):
        purchase_tab = ttk.Frame(self.notebook)
        self.notebook.add(purchase_tab, text="Enter Purchase")
        for i in range(7):
            purchase_tab.grid_rowconfigure(i, weight=1)
        purchase_tab.grid_columnconfigure(0, weight=1)
        purchase_tab.grid_columnconfigure(1, weight=1)
        
        tk.Label(purchase_tab, text="Item", background="#F0F0F0").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.combo_item = ttk.Combobox(purchase_tab, values=self.ELECTRONICS_ITEMS + ["Add New..."], width=38)
        self.combo_item.grid(row=0, column=1, padx=10, pady=5)
        self.combo_item.bind('<<ComboboxSelected>>', self.update_model_dropdown)
        
        tk.Label(purchase_tab, text="Company", background="#F0F0F0").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entry_company = ttk.Entry(purchase_tab, width=40)
        self.entry_company.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(purchase_tab, text="Model Number", background="#F0F0F0").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.entry_model = ttk.Combobox(purchase_tab, width=38)
        self.entry_model.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(purchase_tab, text="Dealer", background="#F0F0F0").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.entry_dealer = ttk.Entry(purchase_tab, width=40)
        self.entry_dealer.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(purchase_tab, text="City", background="#F0F0F0").grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.combo_city = ttk.Combobox(purchase_tab, values=self.CITIES, width=38)
        self.combo_city.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(purchase_tab, text="Price Per Unit", background="#F0F0F0").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.entry_price = ttk.Entry(purchase_tab, width=40)
        self.entry_price.grid(row=5, column=1, padx=10, pady=5)
        
        tk.Label(purchase_tab, text="Units Purchased", background="#F0F0F0").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.entry_units = ttk.Entry(purchase_tab, width=40)
        self.entry_units.grid(row=6, column=1, padx=10, pady=5)
        
        ttk.Button(purchase_tab, text="Save Purchase", command=self.save_purchase_data).grid(
            row=7, column=0, columnspan=2, pady=10
        )

    def create_sale_tab(self):
        sale_tab = ttk.Frame(self.notebook)
        self.notebook.add(sale_tab, text="Enter Sale")
        for i in range(6):
            sale_tab.grid_rowconfigure(i, weight=1)
        sale_tab.grid_columnconfigure(0, weight=1)
        sale_tab.grid_columnconfigure(1, weight=1)
        
        tk.Label(sale_tab, text="Sale Dealer", background="#F0F0F0").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.entry_sale_dealer = ttk.Entry(sale_tab, width=40)
        self.entry_sale_dealer.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(sale_tab, text="Item Sold", background="#F0F0F0").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.combo_item_sold = ttk.Combobox(sale_tab, values=self.ELECTRONICS_ITEMS + ["Add New..."], width=38)
        self.combo_item_sold.grid(row=1, column=1, padx=10, pady=5)
        self.combo_item_sold.bind('<<ComboboxSelected>>', self.update_sale_model_dropdown)
        
        tk.Label(sale_tab, text="Company", background="#F0F0F0").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.entry_company_sold = ttk.Entry(sale_tab, width=40)
        self.entry_company_sold.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(sale_tab, text="Model Number", background="#F0F0F0").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.entry_model_sold = ttk.Combobox(sale_tab, width=38)
        self.entry_model_sold.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(sale_tab, text="Units Sold", background="#F0F0F0").grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.entry_quantity = ttk.Entry(sale_tab, width=40)
        self.entry_quantity.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(sale_tab, text="Sale Price Per Unit", background="#F0F0F0").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.entry_sale_price = ttk.Entry(sale_tab, width=40)
        self.entry_sale_price.grid(row=5, column=1, padx=10, pady=5)
        
        ttk.Button(sale_tab, text="Save Sale", command=self.save_sale_data).grid(
            row=6, column=0, columnspan=2, pady=10
        )

    def create_view_tab(self):
        view_tab = ttk.Frame(self.notebook)
        self.notebook.add(view_tab, text="View Records")
        ttk.Button(view_tab, text="View All Data", command=self.view_data).pack(pady=10)
        ttk.Button(view_tab, text="View Monthly Sales", command=self.view_monthly_sales).pack(pady=10)
        ttk.Button(view_tab, text="Delete Selected Record", command=self.delete_selected_record).pack(pady=10)
        ttk.Button(view_tab, text="Delete All Data", command=self.delete_all_data).pack(pady=10)

    def update_model_dropdown(self, event=None):
        item = self.combo_item.get()
        self.entry_model['values'] = self.model_history.get(item, [])

    def update_sale_model_dropdown(self, event=None):
        item = self.combo_item_sold.get()
        self.entry_model_sold['values'] = self.model_history.get(item, [])

    def save_purchase_data(self):
        item = self.combo_item.get().strip()
        company = self.entry_company.get().strip()
        model = self.entry_model.get().strip()
        dealer = self.entry_dealer.get().strip()
        city = self.combo_city.get().strip()
        price = self.entry_price.get().strip()
        units = self.entry_units.get().strip()
        date = datetime.now().strftime("%Y-%m-%d")
        
        if not (item and company and model and dealer and city and price and units):
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        try:
            price = float(price)
            units = int(units)
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a number and Units must be an integer.")
            return
            
        self.save_model_history(item, company, model)
        try:
            df = pd.read_csv(self.PURCHASE_FILE)
            new_row = {
                "Date": date,
                "Item": item,
                "Company": company,
                "Model": model,
                "Dealer": dealer,
                "City": city,
                "Price Per Unit": price,
                "Units Purchased": units
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(self.PURCHASE_FILE, index=False)
            messagebox.showinfo("Success", "Purchase data saved successfully!")
            self.clear_purchase_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save purchase data: {str(e)}")

    def save_sale_data(self):
        sale_dealer = self.entry_sale_dealer.get().strip()
        item_sold = self.combo_item_sold.get().strip().lower()
        company_sold = self.entry_company_sold.get().strip().lower()
        model_sold = self.entry_model_sold.get().strip().lower()
        quantity_sold = self.entry_quantity.get().strip()
        sale_price = self.entry_sale_price.get().strip()
        date = datetime.now().strftime("%Y-%m-%d")
        
        if not (sale_dealer and item_sold and company_sold and model_sold and quantity_sold and sale_price):
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        try:
            quantity_sold = int(quantity_sold)
            sale_price = float(sale_price)
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity and Sale Price must be numbers.")
            return
            
        try:
            purchase_df = pd.read_csv(self.PURCHASE_FILE)
            purchase_df["Item"] = purchase_df["Item"].astype(str).str.strip().str.lower()
            purchase_df["Company"] = purchase_df["Company"].astype(str).str.strip().str.lower()
            purchase_df["Model"] = purchase_df["Model"].astype(str).str.strip().str.lower()
            purchase_row = purchase_df[
                (purchase_df["Item"] == item_sold) &
                (purchase_df["Company"] == company_sold) &
                (purchase_df["Model"] == model_sold)
            ]
            if purchase_row.empty:
                messagebox.showerror("Error",
                                   f"No purchase record found for '{item_sold} - {company_sold} - {model_sold}'. "
                                   "Please verify that a matching purchase exists.")
                return
            cost_price = purchase_row["Price Per Unit"].values[0]
            total_bill = sale_price * quantity_sold
            profit = (sale_price - cost_price) * quantity_sold
            sale_df = pd.read_csv(self.SALE_FILE)
            new_row = {
                "Date": date,
                "Sale Dealer": sale_dealer,
                "Item Sold": item_sold.capitalize(),
                "Company": company_sold.capitalize(),
                "Model": model_sold.capitalize(),
                "Units Sold": quantity_sold,
                "Sale Price Per Unit": sale_price,
                "Total Bill": total_bill,
                "Profit": profit
            }
            sale_df = pd.concat([sale_df, pd.DataFrame([new_row])], ignore_index=True)
            sale_df.to_csv(self.SALE_FILE, index=False)
            messagebox.showinfo("Success", "Sale data saved successfully!")
            self.clear_sale_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sale data: {str(e)}")

    def clear_purchase_fields(self):
        self.combo_item.set('')
        self.entry_company.delete(0, tk.END)
        self.entry_model.set('')
        self.entry_dealer.delete(0, tk.END)
        self.combo_city.set('')
        self.entry_price.delete(0, tk.END)
        self.entry_units.delete(0, tk.END)

    def clear_sale_fields(self):
        self.entry_sale_dealer.delete(0, tk.END)
        self.combo_item_sold.set('')
        self.entry_company_sold.delete(0, tk.END)
        self.entry_model_sold.set('')
        self.entry_quantity.delete(0, tk.END)
        self.entry_sale_price.delete(0, tk.END)

    def view_data(self):
        win = tk.Toplevel(self.root)
        win.title("View Data")
        notebook = ttk.Notebook(win)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        try:
            purchase_frame = ttk.Frame(notebook)
            notebook.add(purchase_frame, text="Purchase Data")
            purchase_df = pd.read_csv(self.PURCHASE_FILE)
            self.display_table(purchase_frame, purchase_df, "purchase")
            
            sale_frame = ttk.Frame(notebook)
            notebook.add(sale_frame, text="Sale & Profit Data")
            sale_df = pd.read_csv(self.SALE_FILE)
            self.display_table(sale_frame, sale_df, "sale")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def view_monthly_sales(self):
        win = tk.Toplevel(self.root)
        win.title("Monthly Sales")
        notebook = ttk.Notebook(win)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        try:
            sale_df = pd.read_csv(self.SALE_FILE)
            sale_df['Date'] = pd.to_datetime(sale_df['Date'])
            sale_df['YearMonth'] = sale_df['Date'].dt.to_period('M')
            monthly_summary = sale_df.groupby('YearMonth').agg({
                'Units Sold': 'sum',
                'Total Bill': 'sum',
                'Profit': 'sum'
            }).reset_index()
            
            monthly_frame = ttk.Frame(notebook)
            notebook.add(monthly_frame, text="Monthly Summary")
            self.display_table(monthly_frame, monthly_summary, "monthly")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load monthly sales: {str(e)}")

    def delete_selected_record(self):
        win = tk.Toplevel(self.root)
        win.title("Delete Record")
        notebook = ttk.Notebook(win)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        try:
            purchase_frame = ttk.Frame(notebook)
            notebook.add(purchase_frame, text="Delete Purchase")
            purchase_df = pd.read_csv(self.PURCHASE_FILE)
            self.display_table(purchase_frame, purchase_df, "purchase", deletable=True)
            
            sale_frame = ttk.Frame(notebook)
            notebook.add(sale_frame, text="Delete Sale")
            sale_df = pd.read_csv(self.SALE_FILE)
            self.display_table(sale_frame, sale_df, "sale", deletable=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data for deletion: {str(e)}")

    def delete_all_data(self):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all purchase and sale data?"):
            try:
                pd.DataFrame(columns=["Date", "Item", "Company", "Model", "Dealer", "City", "Price Per Unit", "Units Purchased"]).to_csv(self.PURCHASE_FILE, index=False)
                pd.DataFrame(columns=["Date", "Sale Dealer", "Item Sold", "Company", "Model", "Units Sold", "Sale Price Per Unit", "Total Bill", "Profit"]).to_csv(self.SALE_FILE, index=False)
                messagebox.showinfo("Success", "All data deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete all data: {str(e)}")

    def display_table(self, frame, df, table_type, deletable=False):
        tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for i, row in df.iterrows():
            tree.insert("", tk.END, values=tuple(row), iid=str(i))
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill='both', expand=True)
        
        if deletable:
            def delete_record():
                selected_items = tree.selection()
                if not selected_items:
                    messagebox.showwarning("Selection Error", "Please select at least one record to delete!")
                    return
                try:
                    indices = [int(item) for item in selected_items]
                    df_new = df.drop(indices).reset_index(drop=True)
                    df_new.to_csv(self.PURCHASE_FILE if table_type == "purchase" else self.SALE_FILE, index=False)
                    tree.delete(*tree.get_children())
                    for i, row in df_new.iterrows():
                        tree.insert("", tk.END, values=tuple(row), iid=str(i))
                    messagebox.showinfo("Success", f"{len(indices)} record(s) deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete record(s): {str(e)}")
                
            ttk.Button(frame, text="Delete Selected", command=delete_record).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AAA_TradersApp(root)
    root.mainloop()