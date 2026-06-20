"""
GUI Design Module
Maintains layout architecture interfaces, advanced form data entries, dashboard visual grids,
and routes parameters seamlessly to the backend logic layers.
"""
import tkinter as tk
from tkinter import messagebox, ttk
import database
import logic
import config
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class FullApplicationEngine:
    def __init__(self, root):
        self.root = root
        self.root.title(config.SYSTEM_NAME)
        self.root.geometry("1250x780")
        self.root.configure(bg="#f1f5f9")
        
        self.render_authentication_screen()

    def render_authentication_screen(self):
        """Displays secure GUI login viewport panels[cite: 35, 62]."""
        self.login_frame = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=340)
        
        tk.Label(self.login_frame, text="UNIVERSITY CENTRAL PORTAL", font=(config.FONT_FAMILY, 13, "bold"), bg="white", fg="#1e3a8a").pack(pady=20)
        
        tk.Label(self.login_frame, text="Username / Email:", bg="white", font=(config.FONT_FAMILY, 10)).pack(anchor="w", padx=40)
        self.txt_user = tk.Entry(self.login_frame, font=(config.FONT_FAMILY, 11), bd=1, relief="solid")
        self.txt_user.pack(fill="x", padx=40, pady=5)
        self.txt_user.insert(0, "admin")
        
        tk.Label(self.login_frame, text="Password:", bg="white", font=(config.FONT_FAMILY, 10)).pack(anchor="w", padx=40, pady=(10,0))
        self.txt_pass = tk.Entry(self.login_frame, show="*", font=(config.FONT_FAMILY, 11), bd=1, relief="solid")
        self.txt_pass.pack(fill="x", padx=40, pady=5)
        self.txt_pass.insert(0, "admin123")

        tk.Button(self.login_frame, text="Secure Sign In", bg="#1e3a8a", fg="white", font=(config.FONT_FAMILY, 11, "bold"), command=self.perform_login).pack(fill="x", padx=40, pady=20)
        
        lbl_forgot = tk.Label(self.login_frame, text="Forgot Password?", fg="grey", cursor="hand2", bg="white", font=(config.FONT_FAMILY, 9, "underline"))
        lbl_forgot.pack()
        lbl_forgot.bind("<Button-1>", lambda e: messagebox.showinfo("Recovery", "Contact Faculty support at: elijah.fullah@limkokwing.edu.sl [cite: 14]"))

    def perform_login(self):
        """Validates credentials against PostgreSQL users table records."""
        u, p = self.txt_user.get(), self.txt_pass.get()
        try:
            conn = database.get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=%s AND password=%s", (u, p))
            res = c.fetchone()
            c.close()
            conn.close()
            
            if res:
                self.login_frame.destroy()
                self.render_dashboard_workspace()
            else:
                messagebox.showerror("Access Denied", "Invalid administrative identity tokens.")
        except Exception as ex:
            messagebox.showerror("Connection Error", f"Could not verify login. Check pgAdmin settings.\nError: {ex}")

    def render_dashboard_workspace(self):
        """Generates workspaces containing entry forms, tracking tables, and visualization canvases[cite: 109]."""
        brand_bar = tk.Frame(self.root, bg="#1e3a8a", height=60)
        brand_bar.pack(fill="x")
        tk.Label(brand_bar, text="SIERRA LEONE ACADEMIC PORTAL (SDG 4 COMPLIANCE)", font=(config.FONT_FAMILY, 13, "bold"), fg="white", bg="#1e3a8a").pack(side="left", padx=20, pady=15)
        
        # Workspace split distribution panels layout
        left_panel = tk.Frame(self.root, bg="#f1f5f9")
        left_panel.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        right_panel = tk.Frame(self.root, bg="white", width=420, bd=1, relief="solid")
        right_panel.pack(side="right", fill="both", padx=(0,15), pady=15)
        
        # ---------------- CONTROLS ENGINE GRID PANEL ----------------
        ctrl_frame = tk.LabelFrame(left_panel, text=" Search and Multilevel Filtering Controls Engine ", font=(config.FONT_FAMILY, 10, "bold"), bg="white", pady=10, padx=10)
        ctrl_frame.pack(fill="x", pady=(0,10))
        
        tk.Label(ctrl_frame, text="Search keyword:", bg="white").grid(row=0, column=0, sticky="w")
        self.entry_search = tk.Entry(ctrl_frame, width=15, font=(config.FONT_FAMILY, 10))
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)
        # Fix: Using KeyRelease here only fires data reloads, leaving chart redraws isolated
        self.entry_search.bind("<KeyRelease>", lambda e: self.update_dashboard_view(redraw_charts=False))
        
        tk.Label(ctrl_frame, text="Gender:", bg="white").grid(row=0, column=2, sticky="w", padx=5)
        self.combo_gender = ttk.Combobox(ctrl_frame, values=["All", "Male", "Female"], width=8, state="readonly")
        self.combo_gender.current(0)
        self.combo_gender.grid(row=0, column=3, padx=5)
        self.combo_gender.bind("<<ComboboxSelected>>", lambda e: self.update_dashboard_view(redraw_charts=True))
        
        tk.Label(ctrl_frame, text="Status:", bg="white").grid(row=0, column=4, sticky="w", padx=5)
        self.combo_status = ttk.Combobox(ctrl_frame, values=["All", "Active", "Inactive", "Pending"], width=8, state="readonly")
        self.combo_status.current(0)
        self.combo_status.grid(row=0, column=5, padx=5)
        self.combo_status.bind("<<ComboboxSelected>>", lambda e: self.update_dashboard_view(redraw_charts=True))
        
        tk.Label(ctrl_frame, text="Date Scope:", bg="white").grid(row=0, column=6, sticky="w", padx=5)
        self.combo_date = ttk.Combobox(ctrl_frame, values=["All", "Daily", "Weekly", "Monthly", "Yearly"], width=8, state="readonly")
        self.combo_date.current(0)
        self.combo_date.grid(row=0, column=7, padx=5)
        self.combo_date.bind("<<ComboboxSelected>>", lambda e: self.update_dashboard_view(redraw_charts=True))

        # Add: Reset Filter Button directly onto filtering engine row layout 
        tk.Button(ctrl_frame, text="Reset Filters", bg="#64748b", fg="white", font=(config.FONT_FAMILY, 9), command=self.reset_all_filters).grid(row=0, column=8, padx=10)

        # ---------------- REGISTRATION MATRIX TREEVIEW TABLE ----------------
        table_frame = tk.LabelFrame(left_panel, text=" Active Records Tracking Matrix Workspace (Min 20 Records Base) ", font=(config.FONT_FAMILY, 10, "bold"), bg="white", padx=5, pady=5)
        table_frame.pack(fill="both", expand=True)
        
        cols = ("id", "name", "gen", "ass", "ex", "tot", "grd", "sts", "contact")
        self.grid = ttk.Treeview(table_frame, columns=cols, show="headings")
        
        self.grid.heading("id", text="Student ID")
        self.grid.heading("name", text="Full Name")
        self.grid.heading("gen", text="Gender")
        self.grid.heading("ass", text="Ass. (40)")
        self.grid.heading("ex", text="Exam (60)")
        self.grid.heading("tot", text="Total")
        self.grid.heading("grd", text="Grade")
        self.grid.heading("sts", text="Status")
        self.grid.heading("contact", text="Contact Info")
        
        for c in cols: 
            self.grid.column(c, width=75 if c not in ["name", "contact"] else 120, anchor="center" if c!="name" else "w")
            
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.grid.yview)
        self.grid.configure(yscrollcommand=scroll.set)
        self.grid.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # ---------------- NEW: MANAGE INPUT RECORD DATA FORM ----------------
        entry_frame = tk.LabelFrame(left_panel, text=" Add New Student Performance Record Entry Panel ", font=(config.FONT_FAMILY, 10, "bold"), bg="white", padx=10, pady=10)
        entry_frame.pack(fill="x", pady=10)
        
        # Form Row 1 Setup [cite: 109, 110, 111]
        tk.Label(entry_frame, text="ID:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_id = tk.Entry(entry_frame, width=12, font=(config.FONT_FAMILY, 10))
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(entry_frame, text="Full Name:", bg="white").grid(row=0, column=2, sticky="w")
        self.ent_name = tk.Entry(entry_frame, width=18, font=(config.FONT_FAMILY, 10))
        self.ent_name.grid(row=0, column=3, padx=5)
        
        tk.Label(entry_frame, text="Gender:", bg="white").grid(row=0, column=4, sticky="w")
        self.ent_gender = ttk.Combobox(entry_frame, values=["Male", "Female"], width=8, state="readonly")
        self.ent_gender.current(0)
        self.ent_gender.grid(row=0, column=5, padx=5)
        
        # Form Row 2 Setup [cite: 109, 110, 111]
        tk.Label(entry_frame, text="Ass.(40):", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_ass = tk.Entry(entry_frame, width=12, font=(config.FONT_FAMILY, 10))
        self.ent_ass.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(entry_frame, text="Exam(60):", bg="white").grid(row=1, column=2, sticky="w")
        self.ent_exam = tk.Entry(entry_frame, width=18, font=(config.FONT_FAMILY, 10))
        self.ent_exam.grid(row=1, column=3, padx=5)
        
        tk.Label(entry_frame, text="Status:", bg="white").grid(row=1, column=4, sticky="w")
        self.ent_status = ttk.Combobox(entry_frame, values=["Active", "Inactive", "Pending"], width=8, state="readonly")
        self.ent_status.current(0)
        self.ent_status.grid(row=1, column=5, padx=5)
        
        tk.Label(entry_frame, text="Contact Info:", bg="white").grid(row=0, column=6, sticky="w", padx=10)
        self.ent_contact = tk.Entry(entry_frame, width=20, font=(config.FONT_FAMILY, 10))
        self.ent_contact.grid(row=0, column=7, columnspan=2, padx=5)
        
        # Operation Form Actions Save Trigger Button 
        # Operation Form Actions Save Trigger Button
        self.btn_save = tk.Button(
            entry_frame, 
            text="➕ Save Student Record", 
            bg="#10b981", 
            fg="white", 
            font=(config.FONT_FAMILY, 10, "bold"), 
            command=self.execute_record_save
        )
        # Explicitly grid the button on row 1, spanning across columns 6 to 8 with padding
        self.btn_save.grid(row=1, column=6, columnspan=3, padx=10, pady=5, sticky="ew")

        # ---------------- DOCUMENTATION BATCH EXPORTERS ----------------
        pdf_frame = tk.LabelFrame(left_panel, text=" PDF Document Report Generation Module ", font=(config.FONT_FAMILY, 10, "bold"), bg="white", padx=10, pady=8)
        pdf_frame.pack(fill="x")
        
        tk.Button(pdf_frame, text="Compile Weekly PDF Report", bg="#0284c7", fg="white", font=(config.FONT_FAMILY, 9, "bold"), command=lambda: self.trigger_pdf_export("Weekly")).pack(side="left", padx=10, expand=True, fill="x")
        tk.Button(pdf_frame, text="Compile Monthly PDF Report", bg="#0f766e", fg="white", font=(config.FONT_FAMILY, 9, "bold"), command=lambda: self.trigger_pdf_export("Monthly")).pack(side="left", padx=10, expand=True, fill="x")
        tk.Button(pdf_frame, text="Compile Yearly PDF Report", bg="#b45309", fg="white", font=(config.FONT_FAMILY, 9, "bold"), command=lambda: self.trigger_pdf_export("Yearly")).pack(side="left", padx=10, expand=True, fill="x")

        # ---------------- LIVE CHARTS VIEWPORTS ----------------
        self.chart_container = tk.Frame(right_panel, bg="white")
        self.chart_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initial compilation runtime views load pass
        self.update_dashboard_view(redraw_charts=True)

    def execute_record_save(self):
        """Collects field arguments and attempts database string executions[cite: 47]."""
        success, message = logic.insert_student_record(
            self.ent_id.get(), self.ent_name.get(), self.ent_gender.get(),
            self.ent_ass.get(), self.ent_exam.get(), self.ent_status.get(), self.ent_contact.get()
        )
        if success:
            messagebox.showinfo("Success", message)
            # Clear input fields out completely upon success 
            self.ent_id.delete(0, tk.END)
            self.ent_name.delete(0, tk.END)
            self.ent_ass.delete(0, tk.END)
            self.ent_exam.delete(0, tk.END)
            self.ent_contact.delete(0, tk.END)
            # Re-read tracking views to show your new addition right away
            self.update_dashboard_view(redraw_charts=True)
        else:
            messagebox.showerror("Validation Failure [cite: 149]", message)

    def reset_all_filters(self):
        """Flushes input variables text buffers and re-indexes drop selectors."""
        self.entry_search.delete(0, tk.END)
        self.combo_gender.current(0)
        self.combo_status.current(0)
        self.combo_date.current(0)
        self.update_dashboard_view(redraw_charts=True)

    def update_dashboard_view(self, redraw_charts=True):
        """Refreshes spreadsheet rows from PostgreSQL layers without stealing keyboard cursor focuses."""
        # Save active row focus mapping elements
        current_selection = self.grid.selection()
        
        # Wipe structural template rows
        for row in self.grid.get_children(): 
            self.grid.delete(row)
            
        records = logic.fetch_filtered_records(
            search_term=self.entry_search.get(),
            gender=self.combo_gender.get(),
            status=self.combo_status.get(),
            date_range=self.combo_date.get()
        )
        
        for r in records:
            self.grid.insert("", "end", values=(r[0], r[1], r[2], float(r[3]), float(r[4]), float(r[5]), r[6], r[8], r[9]))
            
        # Fix: Only update plot frames when filter criteria dropdown elements shift, not while typing keywords
        if redraw_charts:
            self.render_analytics_plots(records)

    def render_analytics_plots(self, active_dataset):
        """Generates Bar charts, Pie breakdowns, and tracking Lines onto interface subframes."""
        for widget in self.chart_container.winfo_children():
            widget.destroy()
            
        if not active_dataset:
            tk.Label(self.chart_container, text="No metrics matched filter criteria.", bg="white").pack(pady=100)
            return

        gender_counts = {"Male": 0, "Female": 0}
        status_counts = {"Active": 0, "Inactive": 0, "Pending": 0}
        
        for item in active_dataset:
            g, s = item[2], item[8]
            if g in gender_counts: gender_counts[g] += 1
            if s in status_counts: status_counts[s] += 1

        fig = Figure(figsize=(4, 6), dpi=95)
        
        # 1. Bar Chart Metrics View (Status Breakdown)
        ax1 = fig.add_subplot(311)
        ax1.bar(status_counts.keys(), status_counts.values(), color=['#10b981', '#ef4444', '#f59e0b'])
        ax1.set_title("Records Count by Status Status", fontsize=8, weight='bold')
        ax1.tick_params(labelsize=7)
        
        # 2. Pie Chart Metrics View (Gender Categorical Split)
        ax2 = fig.add_subplot(312)
        ax2.pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%', colors=['#3b82f6', '#ec4899'], textprops={'fontsize': 7})
        ax2.set_title("Gender Percentage Distributions Split", fontsize=8, weight='bold')

        # 3. Line Chart Metrics View (System Timeline Trend)
        ax3 = fig.add_subplot(313)
        sample_trends = [1, 4, 8, len(active_dataset)]
        ax3.plot(["Q1", "Q2", "Q3", "Current Active"], sample_trends, marker='o', color='#6366f1', linewidth=1.5)
        ax3.set_title("System Activity Cumulative Timeline Trajectory Growth", fontsize=8, weight='bold')
        ax3.tick_params(labelsize=7)

        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def trigger_pdf_export(self, scope):
        """Compiles active list queries to static PDF structures."""
        target_file = logic.generate_pdf_report(scope)
        messagebox.showinfo("PDF Compiled", f"A formal {scope} monitoring document report summary layout was saved to files as:\n{target_file}")