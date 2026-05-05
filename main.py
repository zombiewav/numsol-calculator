import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp
import csv
import re
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from methods.bisection import bisection_method
from methods.newton import newton_raphson_method
from methods.secant import secant_method
from methods.gauss import gauss_seidel_method
from methods.regula_falsi import regula_falsi_method
from methods.incremental import incremental_search_method
from methods.fixed_point import fixed_point_iteration
from methods.jacobi import jacobi_method

class NumSolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NumSol Calculator")
        self.root.geometry("1200x850")
        self.root.configure(bg="#EAF4FF")
        
        try:
            self.root.iconbitmap(resource_path('icon.ico'))
        except Exception:
            pass
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="white", foreground="black", rowheight=35, fieldbackground="white", font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        self.sidebar_frame = tk.Frame(self.root, width=350, bg="#D6E9FF")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        self.inner_sidebar = tk.Frame(self.sidebar_frame, bg="#D6E9FF", padx=25, pady=20)
        self.inner_sidebar.pack(fill="both", expand=True)

        self.main_frame = tk.Frame(self.root, bg="#EAF4FF")
        self.main_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.create_sidebar_widgets()
        self.create_main_area_widgets()

    def create_sidebar_widgets(self):
        tk.Label(self.inner_sidebar, text="INPUTS", font=("Segoe UI", 13, "bold"), bg="#D6E9FF", fg="#0A3D91").pack(anchor="w", pady=(0, 10))

        self.func_label = tk.Label(self.inner_sidebar, text="Function f(x) or Matrix:", font=("Segoe UI", 11), bg="#D6E9FF")
        self.func_label.pack(anchor="w")
        self.input_frame = tk.Frame(self.inner_sidebar, bg="#D6E9FF")
        self.input_frame.pack(fill="x", pady=5)

        self.func_entry = tk.Entry(self.input_frame, font=("Segoe UI", 11), relief="flat")
        self.func_entry.insert(0, "x^3 - x - 1")
        self.func_entry.pack(fill="x")

        self.system_text = tk.Text(self.input_frame, font=("Segoe UI", 11), relief="flat", height=4, wrap="word")
        self.system_text.insert("1.0", "10x-y+2z=6\n-x+11y-z=25\n2x-y+10z=-11")

        tk.Label(self.inner_sidebar, text="Method Selection:", font=("Segoe UI", 13, "bold"), bg="#D6E9FF", fg="#0A3D91").pack(anchor="w", pady=(15, 5))
        self.method_var = tk.StringVar()
        self.method_dropdown = ttk.Combobox(self.inner_sidebar, textvariable=self.method_var, font=("Segoe UI", 11), state="readonly")
        self.method_dropdown['values'] = ("Incremental Search", "Bisection", "Regula-Falsi", "Fixed-Point", "Newton Raphson", "Secant", "Gauss-Seidel", "Jacobi")
        self.method_dropdown.current(1)
        self.method_dropdown.pack(fill="x", pady=5)
        self.method_dropdown.bind("<<ComboboxSelected>>", self.update_labels)

        tk.Label(self.inner_sidebar, text="Parameters:", font=("Segoe UI", 11, "bold"), bg="#D6E9FF").pack(anchor="w", pady=(10, 0))
        
        self.p1_label = tk.Label(self.inner_sidebar, text="Param 1 (xL):", font=("Segoe UI", 10), bg="#D6E9FF")
        self.p1_label.pack(anchor="w")
        self.p1_entry = tk.Entry(self.inner_sidebar, font=("Segoe UI", 11), relief="flat")
        self.p1_entry.pack(fill="x", pady=(0, 8))

        self.p2_label = tk.Label(self.inner_sidebar, text="Param 2 (xR):", font=("Segoe UI", 10), bg="#D6E9FF")
        self.p2_label.pack(anchor="w")
        self.p2_entry = tk.Entry(self.inner_sidebar, font=("Segoe UI", 11), relief="flat")
        self.p2_entry.pack(fill="x", pady=(0, 8))

        self.tol_label = tk.Label(self.inner_sidebar, text="Tolerance:", font=("Segoe UI", 10), bg="#D6E9FF")
        self.tol_label.pack(anchor="w")
        self.tol_entry = tk.Entry(self.inner_sidebar, font=("Segoe UI", 11), relief="flat")
        self.tol_entry.insert(0, "0.0001")
        self.tol_entry.pack(fill="x", pady=(0, 8))

        tk.Label(self.inner_sidebar, text="Max Iterations:", font=("Segoe UI", 10), bg="#D6E9FF").pack(anchor="w")
        self.iter_entry = tk.Entry(self.inner_sidebar, font=("Segoe UI", 11), relief="flat")
        self.iter_entry.insert(0, "50")
        self.iter_entry.pack(fill="x", pady=(0, 8))

        self.solve_btn = tk.Button(self.inner_sidebar, text="Solve", command=self.solve, font=("Segoe UI", 11, "bold"), bg="#4A90E2", fg="white", relief="flat", pady=8, cursor="hand2")
        self.solve_btn.pack(fill="x", pady=(15, 5))

        self.export_btn = tk.Button(self.inner_sidebar, text="Export to Excel (CSV)", command=self.export_to_csv, font=("Segoe UI", 11, "bold"), bg="#28A745", fg="white", relief="flat", pady=8, cursor="hand2")
        self.export_btn.pack(fill="x", pady=5)

        tk.Label(self.inner_sidebar, text="SYNTAX GUIDE", font=("Segoe UI", 10, "bold"), bg="#D6E9FF", fg="#0A3D91").pack(anchor="w", pady=(20, 5))
        self.syntax_body = tk.Label(
            self.inner_sidebar,
            text=self.get_syntax_text(self.method_var.get()),
            font=("Segoe UI", 9),
            bg="#D6E9FF",
            fg="#444444",
            justify="left"
        )
        self.syntax_body.pack(anchor="w")

        tk.Label(self.inner_sidebar, text="FINAL ANSWER", font=("Segoe UI", 13, "bold"), bg="#D6E9FF", fg="#0A3D91").pack(anchor="w", pady=(20, 5))
        self.result_label = tk.Label(self.inner_sidebar, text="Result: ", font=("Segoe UI", 14, "bold"), fg="#0A3D91", bg="#D6E9FF", wraplength=300, justify="left")
        self.result_label.pack(anchor="w")

    def get_syntax_text(self, method):
        if method in ["Gauss-Seidel", "Jacobi"]:
            return (
                "Type one equation per line or use matrix format.\n"
                "Initial guesses: 0,0,0\n"
                "Matrix: 10,-1,2,6; -1,11,-1,25; 2,-1,10,-11\n"
                "Or list: [[10,-1,2,6],[-1,11,-1,25],[2,-1,10,-11]]\n"
                "Or equations:\n10x-y+2z=6\n-x+11y-z=25\n2x-y+10z=-11"
            )
        return (
            "Exponents: x^2 or x**2\nMultiplication: 5*x or 5x\n"
            "Roots: sqrt(x)\nTrigonometry: sin(x), cos(x), tan(x)\n"
            "Constants: pi, e\nLogarithms: log(x), log(x, 10)"
        )

    def set_input_mode(self, use_system_input):
        if use_system_input:
            if self.func_entry.winfo_manager():
                self.func_entry.pack_forget()
            if not self.system_text.winfo_manager():
                self.system_text.pack(fill="x")
        else:
            if self.system_text.winfo_manager():
                self.system_text.pack_forget()
            if not self.func_entry.winfo_manager():
                self.func_entry.pack(fill="x")

    def update_labels(self, event=None):
        method = self.method_var.get()
        if method == "Incremental Search":
            self.set_input_mode(False)
            self.func_label.config(text="Function f(x):")
            self.p1_label.config(text="Param 1 (xL):")
            self.p2_label.config(text="Increment:")
            self.tol_label.config(text="Tolerance:")
        elif method in ["Bisection", "Regula-Falsi"]:
            self.set_input_mode(False)
            self.func_label.config(text="Function f(x):")
            self.p1_label.config(text="Param 1 (xL):")
            self.p2_label.config(text="Param 2 (xR):")
            self.tol_label.config(text="Tolerance:")
        elif method in ["Newton Raphson", "Fixed-Point"]:
            self.set_input_mode(False)
            self.func_label.config(text="Function g(x):" if method == "Fixed-Point" else "Function f(x):")
            self.p1_label.config(text="Initial Guess (x0):")
            self.p2_label.config(text="Unused:")
            self.tol_label.config(text="Tolerance:")
        elif method == "Secant":
            self.set_input_mode(False)
            self.func_label.config(text="Function f(x):")
            self.p1_label.config(text="Param 1 (Xa):")
            self.p2_label.config(text="Param 2 (Xb):")
            self.tol_label.config(text="Tolerance:")
        elif method in ["Gauss-Seidel", "Jacobi"]:
            self.set_input_mode(True)
            self.func_label.config(text="Equations or Matrix:")
            self.p1_label.config(text="Initial Guesses (x0,y0,z0):")
            self.p2_label.config(text="Unused:")
            self.tol_label.config(text="Tolerance:")
            current_guess_text = self.p1_entry.get().strip()
            if "," not in current_guess_text:
                self.p1_entry.delete(0, tk.END)
                self.p1_entry.insert(0, "0,0,0")
        self.syntax_body.config(text=self.get_syntax_text(method))

    def create_main_area_widgets(self):
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        
        self.graph_frame = tk.Frame(self.main_frame, bg="white", highlightthickness=1, highlightbackground="#D6E9FF")
        self.graph_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        self.fig, self.ax = plt.subplots(figsize=(5, 4), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.table_frame = tk.Frame(self.main_frame, bg="white", highlightthickness=1, highlightbackground="#D6E9FF")
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.table = ttk.Treeview(self.table_frame, show='headings')
        self.table.tag_configure("final_row", background="#FFF3BF", foreground="#0A3D91")
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def export_to_csv(self):
        items = self.table.get_children()
        if not items:
            messagebox.showwarning("Export Error", "No data to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.table["columns"])
                for item_id in items:
                    writer.writerow(self.table.item(item_id)["values"])
            messagebox.showinfo("Export Success", "File saved.")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def display_results(self, steps, result):
        for item in self.table.get_children():
            self.table.delete(item)
        if not steps: return
        cols = list(steps[0].keys())
        self.table["columns"] = cols
        for col in cols:
            self.table.heading(col, text=col)
            width = 280 if col.startswith("Equation ") else 120
            self.table.column(col, anchor="center", width=width)
        last_index = len(steps) - 1
        for idx, s in enumerate(steps):
            row_tags = ("final_row",) if idx == last_index else ()
            self.table.insert("", "end", values=list(s.values()), tags=row_tags)
        
        if isinstance(result, (float, int)):
            self.result_label.config(text=f"Result: {result:.6f}")
        else:
            self.result_label.config(text=f"Result: {result}")

    def plot_graph(self, f, p1, p2):
        self.ax.clear()
        self.ax.set_facecolor('white')
        try:
            x_min, x_max = min(p1, p2) - 2, max(p1, p2) + 2
            x_vals = np.linspace(x_min, x_max, 400)
            y_vals = f(x_vals)
            self.ax.plot(x_vals, y_vals, label="f(x)", color="#4A90E2", lw=2)
            self.ax.axhline(0, color='black', lw=1)
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.canvas.draw()
        except: pass

    def parse_function(self, func_str):
        try:
            func_str = func_str.replace('^', '**')
            func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)
            x = sp.symbols('x')
            expr = sp.sympify(func_str)
            return sp.lambdify(x, expr, modules=['numpy', 'sympy']), func_str
        except: return None, None

    def solve(self):
        method = self.method_var.get()
        if method in ["Gauss-Seidel", "Jacobi"]:
            func_raw = self.system_text.get("1.0", "end").strip()
        else:
            func_raw = self.func_entry.get().strip()
        
        if method == "Gauss-Seidel":
            try:
                tol = float(self.tol_entry.get())
                m_iter = int(self.iter_entry.get())
                initial_guesses = self.p1_entry.get().strip()
                steps, res = gauss_seidel_method(func_raw, tol, m_iter, initial_guesses)
                self.display_results(steps, res)
            except Exception as e: messagebox.showerror("Error", str(e))
            return
        if method == "Jacobi":
            try:
                tol = float(self.tol_entry.get())
                m_iter = int(self.iter_entry.get())
                initial_guesses = self.p1_entry.get().strip()
                steps, res = jacobi_method(func_raw, tol, m_iter, initial_guesses)
                self.display_results(steps, res)
            except Exception as e: messagebox.showerror("Error", str(e))
            return

        f, fixed_str = self.parse_function(func_raw)
        if not f:
            messagebox.showerror("Error", "Invalid Function")
            return

        try:
            p1 = float(self.p1_entry.get())
            p2_val = self.p2_entry.get()
            p2 = float(p2_val) if p2_val else 0.0
            tol = float(self.tol_entry.get())
            m_iter = int(self.iter_entry.get())
        except:
            messagebox.showerror("Error", "Check numeric parameters")
            return

        methods_map = {
            "Incremental Search": lambda: incremental_search_method(f, p1, p2, tol, m_iter),
            "Bisection": lambda: bisection_method(f, p1, p2, tol, m_iter),
            "Regula-Falsi": lambda: regula_falsi_method(f, p1, p2, tol, m_iter),
            "Fixed-Point": lambda: fixed_point_iteration(f, p1, tol, m_iter, fixed_str),
            "Newton Raphson": lambda: newton_raphson_method(f, p1, tol, m_iter, fixed_str),
            "Secant": lambda: secant_method(f, p1, p2, tol, m_iter)
        }

        if method in methods_map:
            steps, res = methods_map[method]()
            if isinstance(steps, list):
                self.display_results(steps, res)
                self.plot_graph(f, p1, p2)
            else: messagebox.showerror("Error", res)

if __name__ == "__main__":
    root = tk.Tk()
    app = NumSolApp(root)
    root.mainloop()
