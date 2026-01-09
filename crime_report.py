import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
import pytz
import json
import os
import pyperclip

class CrimeReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UK Crime Reporting System")
        self.root.geometry("1000x750")
        
        # UK Timezone
        self.uk_tz = pytz.timezone('Europe/London')
        
        # Crime lists
        self.TOP_CHARGES = [
            "PC 3.1.6 Banditry",
            "PC 2.10.6 Robbery",
            "PC 2.8.3 Taking a hostage",
            "PC 2.5.6 Brandishing of a weapon",
            "PC 3.4.2 Trespassing in a State Facility",
            "PC 3.11 Murder or Attempted murder of a public servant"
        ]
        
        self.ALL_CHARGES = [
            "PC 2.2.4 Cultivation of cannabis (small quantities)",
            "PC 2.2.5 Cultivation of cannabis (large quantities)",
            "PC 2.5.3 Open Carrying",
            "PC 2.5.8 Discharging a weapon in a public place",
            "PC 2.8.1 Abduction",
            "PC 2.8.2 Kidnapping",
            "PC 2.8.4 Human Trafficking",
            "PC 2.13.3 Vandalism",
            "PC 3.1.1 Participation in terrorism",
            "PC 3.1.4 Committing a terrorist act",
            "PC 3.1.5 Creation of a stable armed group",
            "PC 3.8.2 Impersonating a law enforcement officer",
            "PC 3.10 Battery of a public servant",
            "PC 3.20 Participation in a cyber attack of the state's resources"
        ]
        
        # Combine all crimes
        self.all_crimes = self.TOP_CHARGES + self.ALL_CHARGES
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="UK CRIME REPORTING SYSTEM", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Report Type Selection
        ttk.Label(main_frame, text="Select Report Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.report_type = tk.StringVar(value="Gang")
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(type_frame, text="Gang", variable=self.report_type, 
                       value="Gang", command=self.update_fields).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(type_frame, text="Family", variable=self.report_type, 
                       value="Family", command=self.update_fields).pack(side=tk.LEFT, padx=5)
        
        # Basic Information Frame
        info_frame = ttk.LabelFrame(main_frame, text="Basic Information", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10, padx=5)
        
        # Name input
        ttk.Label(info_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=0, column=1, pady=5, padx=(5, 0))
        
        # Crime Type
        ttk.Label(info_frame, text="Crime Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.crime_var = tk.StringVar()
        crime_entry = ttk.Entry(info_frame, textvariable=self.crime_var, width=40)
        crime_entry.grid(row=1, column=1, pady=5, padx=(5, 0))
        
        # Date and Time (UK)
        ttk.Label(info_frame, text="Date (DD.MM.YYYY):").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_frame = ttk.Frame(info_frame)
        date_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(date_frame, textvariable=self.date_var, width=15)
        self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(date_frame, text="Now", width=5, 
                  command=self.set_current_date).pack(side=tk.LEFT)
        
        ttk.Label(info_frame, text="Time (24h HH:MM):").grid(row=3, column=0, sticky=tk.W, pady=5)
        time_frame = ttk.Frame(info_frame)
        time_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        self.time_var = tk.StringVar()
        self.time_entry = ttk.Entry(time_frame, textvariable=self.time_var, width=15)
        self.time_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(time_frame, text="Now", width=5, 
                  command=self.set_current_time).pack(side=tk.LEFT)
        
        # Set current date/time initially
        self.set_current_datetime()
        
        # Crimes Committed Frame with larger window
        crimes_frame = ttk.LabelFrame(main_frame, text="Select Crimes (Double-click to open full list)", padding="10")
        crimes_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10, padx=5)
        
        # Frame for selected crimes display
        selected_frame = ttk.Frame(crimes_frame)
        selected_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(selected_frame, text="Selected Crimes:").pack(side=tk.LEFT, padx=(0, 10))
        
        # Text widget to show selected crimes
        self.selected_crimes_text = scrolledtext.ScrolledText(selected_frame, height=3, width=70)
        self.selected_crimes_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.selected_crimes_text.config(state='disabled')
        
        # Open crimes selection button
        ttk.Button(crimes_frame, text="📋 Open Crimes Selection", 
                  command=self.open_crimes_selection, width=20).pack()
        
        # Initialize selected crimes list
        self.selected_crimes_list = []
        
        # Special Fields Frame
        self.special_frame = ttk.LabelFrame(main_frame, text="Evidence Links", padding="10")
        self.special_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10, padx=5)
        
        # Initialize special fields
        self.create_gang_fields()
        
        # Buttons Frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        ttk.Button(buttons_frame, text="📋 Generate Report", 
                  command=self.generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="📋 Copy Part 1", 
                  command=self.copy_part1).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="📋 Copy Part 2", 
                  command=self.copy_part2).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="💾 Save to File", 
                  command=self.save_to_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="🔄 Clear All", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Output Frame
        output_frame = ttk.LabelFrame(main_frame, text="Generated Report", padding="10")
        output_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=5)
        
        # Configure weights for expansion
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Scrolled Text for output
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, font=('Courier', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def set_current_datetime(self):
        """Set current UK date and time"""
        uk_now = datetime.now(self.uk_tz)
        self.date_var.set(uk_now.strftime("%d.%m.%Y"))
        self.time_var.set(uk_now.strftime("%H:%M"))
    
    def set_current_date(self):
        """Set current UK date"""
        uk_now = datetime.now(self.uk_tz)
        self.date_var.set(uk_now.strftime("%d.%m.%Y"))
    
    def set_current_time(self):
        """Set current UK time"""
        uk_now = datetime.now(self.uk_tz)
        self.time_var.set(uk_now.strftime("%H:%M"))
    
    def update_fields(self):
        """Update fields based on report type"""
        # Clear previous special fields
        for widget in self.special_frame.winfo_children():
            widget.destroy()
        
        # Update title
        self.special_frame.config(text=f"{self.report_type.get()} - Evidence Links")
        
        # Create appropriate fields
        if self.report_type.get() == "Gang":
            self.create_gang_fields()
        else:
            self.create_family_fields()
    
    def create_gang_fields(self):
        """Create fields specific to Gang reports"""
        fields = [
            ("Proof of bodycam / refresh / upload:", "gang_bodycam_proof"),
            ("Bodycam Footage:", "gang_bodycam_footage"),
            ("Bodycam Footage of interrogation:", "gang_interrogation"),
            ("Culprit Identification Proof:", "gang_culprit_id"),
            ("License plates:", "gang_license_plates")
        ]
        
        self.create_special_fields(fields)
    
    def create_family_fields(self):
        """Create fields specific to Family reports"""
        fields = [
            ("Proof of bodycam / refresh / upload:", "family_bodycam_proof"),
            ("Bodycam Footage:", "family_bodycam_footage"),
            ("Culprit Identification Proof:", "family_culprit_id"),
            ("Bodycam Footage of interrogation:", "family_interrogation"),
            ("License plates:", "family_license_plates"),
            ("License plates searched in PDA:", "family_pda_search"),
            ("Owner of the car searched in PDA:", "family_car_owner")
        ]
        
        self.create_special_fields(fields)
    
    def create_special_fields(self, fields):
        """Create labeled entry fields"""
        self.special_vars = {}
        
        for i, (label, var_name) in enumerate(fields):
            # Label
            ttk.Label(self.special_frame, text=label, font=('Arial', 9, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=5)
            
            # Create variable and entry
            self.special_vars[var_name] = tk.StringVar()
            entry = ttk.Entry(self.special_frame, textvariable=self.special_vars[var_name], 
                             width=70)
            entry.grid(row=i, column=1, padx=(5, 0), pady=5, sticky=tk.W)
            
            # Add paste button
            btn_frame = ttk.Frame(self.special_frame)
            btn_frame.grid(row=i, column=2, padx=(5, 0), sticky=tk.W)
            ttk.Button(btn_frame, text="Paste", width=8,
                      command=lambda v=var_name: self.paste_link(v)).pack(side=tk.LEFT)
    
    def paste_link(self, field_name):
        """Paste link from clipboard"""
        try:
            clipboard_text = self.root.clipboard_get()
            if clipboard_text:
                self.special_vars[field_name].set(clipboard_text)
        except:
            try:
                import pyperclip
                clipboard_text = pyperclip.paste()
                if clipboard_text:
                    self.special_vars[field_name].set(clipboard_text)
            except:
                pass
    
    def open_crimes_selection(self):
        """Open a new window for selecting crimes"""
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Crimes")
        selection_window.geometry("600x500")
        
        # Make modal
        selection_window.transient(self.root)
        selection_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(selection_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Select Crimes (Ctrl+Click for multiple)", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # TOP CHARGES tab
        top_frame = ttk.Frame(notebook)
        notebook.add(top_frame, text="Top Charges")
        
        # Listbox for TOP CHARGES
        top_scrollbar = ttk.Scrollbar(top_frame)
        top_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.top_listbox = tk.Listbox(top_frame, selectmode=tk.MULTIPLE, 
                                     yscrollcommand=top_scrollbar.set, 
                                     height=15, font=('Arial', 10))
        self.top_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        top_scrollbar.config(command=self.top_listbox.yview)
        
        for crime in self.TOP_CHARGES:
            self.top_listbox.insert(tk.END, crime)
        
        # ALL CHARGES tab
        all_frame = ttk.Frame(notebook)
        notebook.add(all_frame, text="All Charges")
        
        # Listbox for ALL CHARGES
        all_scrollbar = ttk.Scrollbar(all_frame)
        all_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.all_listbox = tk.Listbox(all_frame, selectmode=tk.MULTIPLE, 
                                     yscrollcommand=all_scrollbar.set, 
                                     height=15, font=('Arial', 10))
        self.all_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        all_scrollbar.config(command=self.all_listbox.yview)
        
        for crime in self.ALL_CHARGES:
            self.all_listbox.insert(tk.END, crime)
        
        # Pre-select already selected crimes
        self.preselect_crimes()
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)
        
        ttk.Button(buttons_frame, text="Select All", 
                  command=self.select_all_crimes).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Clear All", 
                  command=self.clear_selection).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Done", 
                  command=lambda: self.save_selection(selection_window)).pack(side=tk.LEFT, padx=5)
    
    def preselect_crimes(self):
        """Preselect already selected crimes"""
        for i, crime in enumerate(self.TOP_CHARGES):
            if crime in self.selected_crimes_list:
                self.top_listbox.selection_set(i)
        
        for i, crime in enumerate(self.ALL_CHARGES):
            if crime in self.selected_crimes_list:
                self.all_listbox.selection_set(i)
    
    def select_all_crimes(self):
        """Select all crimes in both lists"""
        self.top_listbox.selection_set(0, tk.END)
        self.all_listbox.selection_set(0, tk.END)
    
    def clear_selection(self):
        """Clear all selections"""
        self.top_listbox.selection_clear(0, tk.END)
        self.all_listbox.selection_clear(0, tk.END)
    
    def save_selection(self, window):
        """Save selected crimes and close window"""
        # Get selected crimes from both lists
        selected_top = [self.top_listbox.get(i) for i in self.top_listbox.curselection()]
        selected_all = [self.all_listbox.get(i) for i in self.all_listbox.curselection()]
        
        # Combine and deduplicate
        self.selected_crimes_list = list(set(selected_top + selected_all))
        
        # Update display
        self.update_selected_crimes_display()
        
        window.destroy()
    
    def update_selected_crimes_display(self):
        """Update the selected crimes display"""
        self.selected_crimes_text.config(state='normal')
        self.selected_crimes_text.delete(1.0, tk.END)
        
        if self.selected_crimes_list:
            for crime in self.selected_crimes_list:
                self.selected_crimes_text.insert(tk.END, f"• {crime}\n")
        else:
            self.selected_crimes_text.insert(tk.END, "No crimes selected")
        
        self.selected_crimes_text.config(state='disabled')
    
    def generate_report(self):
        """Generate the formatted report"""
        # Basic validation
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing Information", "Please enter a Name")
            return
        
        crime_type = self.crime_var.get().strip()
        date = self.date_var.get().strip()
        time = self.time_var.get().strip()
        
        # Use current date/time if empty
        if not date or not time:
            self.set_current_datetime()
            date = self.date_var.get()
            time = self.time_var.get()
        
        # Create PART 1: Header with Name instead of Report Type
        part1 = f"{name} | {crime_type} | {date} | {time}\n\n"
        
        # Create PART 2: Body
        part2 = f"{self.report_type.get()} Name: {name}\n\n"
        part2 += "=" * 50 + "\n"
        
        # Get fields based on report type
        if self.report_type.get() == "Gang":
            fields = [
                ("Proof of bodycam / refresh / upload:", "gang_bodycam_proof"),
                ("Bodycam Footage:", "gang_bodycam_footage"),
                ("Bodycam Footage of interrogation:", "gang_interrogation"),
                ("Culprit Identification Proof:", "gang_culprit_id"),
                ("License plates:", "gang_license_plates")
            ]
        else:
            fields = [
                ("Proof of bodycam / refresh / upload:", "family_bodycam_proof"),
                ("Bodycam Footage:", "family_bodycam_footage"),
                ("Culprit Identification Proof:", "family_culprit_id"),
                ("Bodycam Footage of interrogation:", "family_interrogation"),
                ("License plates:", "family_license_plates"),
                ("License plates searched in PDA:", "family_pda_search"),
                ("Owner of the car searched in PDA:", "family_car_owner")
            ]
        
        # Add evidence fields - N/A on same line, links on next line
        for label, var_name in fields:
            value = self.special_vars[var_name].get().strip()
            if value:  # If there's a link
                part2 += f"{label}\n{value}\n"
            else:  # If empty, show N/A on same line
                part2 += f"{label} N/A\n"
            part2 += "=" * 50 + "\n"
        
        # Add Crimes Committed with dash format
        part2 += "Crimes Committed "
        part2 += "(Mandatory):\n" if self.report_type.get() == "Gang" else ":\n"
        
        if self.selected_crimes_list:
            for crime in self.selected_crimes_list:
                part2 += f"- {crime}\n"
        else:
            part2 += "N/A\n"
        
        part2 += "=" * 50 + "\n"
        
        # Combine full report
        full_report = part1 + part2
        
        # Display in output
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, full_report)
        
        # Store for clipboard/file
        self.current_report = full_report
        self.part1 = part1
        self.part2 = part2
        self.report_data = {
            "type": self.report_type.get(),
            "name": name,
            "crime": crime_type,
            "date": date,
            "time": time,
            "crimes": self.selected_crimes_list,
            "fields": {var: self.special_vars[var].get().strip() for var in self.special_vars}
        }
        
        # Update status
        self.status_var.set(f"Report generated!")
    
    def copy_part1(self):
        """Copy Part 1 to clipboard"""
        if not hasattr(self, 'part1'):
            messagebox.showwarning("No Report", "Please generate a report first")
            return
        
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.part1.strip())  # Remove extra newline
            self.status_var.set("Part 1 copied to clipboard")
        except:
            try:
                import pyperclip
                pyperclip.copy(self.part1.strip())
                self.status_var.set("Part 1 copied to clipboard")
            except:
                messagebox.showerror("Copy Failed", "Could not copy to clipboard")
    
    def copy_part2(self):
        """Copy Part 2 to clipboard"""
        if not hasattr(self, 'part2'):
            messagebox.showwarning("No Report", "Please generate a report first")
            return
        
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.part2.strip())
            self.status_var.set("Part 2 copied to clipboard")
        except:
            try:
                import pyperclip
                pyperclip.copy(self.part2.strip())
                self.status_var.set("Part 2 copied to clipboard")
            except:
                messagebox.showerror("Copy Failed", "Could not copy to clipboard")
    
    def save_to_file(self):
        """Save report to file - user chooses location"""
        if not hasattr(self, 'current_report'):
            messagebox.showwarning("No Report", "Please generate a report first")
            return
        
        # Ask user where to save
        default_name = f"{self.name_var.get().strip()}_{self.date_var.get().strip().replace('.', '-')}.txt"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_name
        )
        
        if filename:
            try:
                # Save TXT file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.current_report)
                
                # Also save JSON file
                json_file = filename.replace('.txt', '.json')
                with open(json_file, 'w') as f:
                    json.dump(self.report_data, f, indent=2)
                
                self.status_var.set(f"Saved: {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def clear_all(self):
        """Clear all fields"""
        # Clear basic fields
        self.name_var.set("")
        self.crime_var.set("")
        self.set_current_datetime()
        
        # Clear crimes selection
        self.selected_crimes_list = []
        self.update_selected_crimes_display()
        
        # Clear special fields
        if hasattr(self, 'special_vars'):
            for var in self.special_vars.values():
                var.set("")
        
        # Clear output
        self.output_text.delete(1.0, tk.END)
        
        # Reset to Gang
        self.report_type.set("Gang")
        self.update_fields()
        
        # Reset status
        self.status_var.set("Ready")

def main():
    root = tk.Tk()
    app = CrimeReportApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()