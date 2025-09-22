import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from calendar import monthrange, month_name
import locale
from pathlib import Path

class FinancialTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Tracker v1.0")
        self.root.geometry("1366x900")
        
        # Use user's home directory for data file
        home_dir = Path.home()
        self.data_file = home_dir / 'financial_data.json'
        self.data = self.load_data()
        
        # Language translations
        self.translations = {
            'ro': {
                'title': 'Financial Tracker - Interfață Excel',
                'expenses': 'Cheltuieli',
                'expense_name': 'Numele Cheltuielii',
                'amount': 'Sumă (RON)',
                'status': 'Status',
                'add_expense': 'Adaugă Cheltuială',
                'delete_expense': 'Șterge Cheltuială',
                'duplicate_expense': 'Duplică Cheltuială',
                'income': 'Venituri',
                'monthly_income': 'Venitul Lunar:',
                'update': 'Actualizează',
                'meal_tickets': 'Tichete de Masă',
                'worked_days': 'Zile Lucrate:',
                'value_per_day': 'Valoare/Zi:',
                'family_income': 'Venituri Familie',
                'member_name': 'Numele Cheltuielii',
                'family_role': 'Rolul în Famil',
                'add_family_member': 'Adaugă Membru Familie',
                'delete': 'Șterge',
                'other_income': 'Alte Venituri',
                'income_source': 'Sursa Venitului',
                'add_other_income': 'Adaugă Alt Venit',
                'financial_summary': 'Sumar Financiar',
                'total_expenses': 'Total Cheltuieli:',
                'paid': 'Plătit (Achitat):',
                'unpaid': 'Neplătit (Neachitat):',
                'reserved': 'Rezervat:',
                'monthly_income': 'Venit Lunar:',
                'family_other_income': 'Venit Adițional:',
                'tickets_value': 'Valoarea Tichetelor:',
                'remaining': 'Venit Rămas:',
                'total_household': 'Venitul Total al Casei:',
                'language': 'Limba',
                'currency': 'Monedă',
                'history': 'Istoric',
                'previous_month': '◄ Luna Anterioară',
                'next_month': 'Luna Următoare ►',
                'save_month': 'Salvează Luna',
                'note': '💡 Dublu-click pe orice celulă pentru editare, sau apasă F2',
                'months': ['Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie', 
                          'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie'],
                'achitat': 'Achitat',
                'neachitat': 'Neachitat',
                'reserved': 'Rezervat',
                'recurring': 'Recurent (luni)',
                'category': 'Categorie',
                'categories': {
                    'bills': 'Facturi',
                    'transport': 'Transport',
                    'food': 'Mâncare',
                    'health': 'Sănătate',
                    'entertainment': 'Divertisment',
                    'clothing': 'Îmbrăcăminte',
                    'education': 'Educație',
                    'other': 'Altele'
                },
                'credit_types': {  
                    'mortgage': 'Ipotecar',
                    'personal': 'Nevoi Personale',
                    'overdraft': 'Overdraft',
                    'credit_card': 'Card de Credit'
                },
                'total_bill': 'Valoare Totală Factură:',
                'paid_amount': 'Suma Achitată:',
                'remaining_bill': 'Rest de Plată:'
            },
            'en': {
                'title': 'Financial Tracker - Excel Interface',
                'expenses': 'Expenses',
                'expense_name': 'Expense Name',
                'amount': 'Amount (RON)',
                'status': 'Status',
                'add_expense': 'Add Expense',
                'delete_expense': 'Delete Expense',
                'duplicate_expense': 'Duplicate Expense',
                'income': 'Income',
                'monthly_income': 'Monthly Income:',
                'update': 'Update',
                'meal_tickets': 'Meal Tickets',
                'worked_days': 'Worked Days:',
                'value_per_day': 'Value/Day:',
                'family_income': 'Family Income',
                'member_name': 'Member Name',
                'family_role': 'Family Role',
                'add_family_member': 'Add Family Member',
                'delete': 'Delete',
                'other_income': 'Other Income',
                'income_source': 'Income Source',
                'add_other_income': 'Add Other Income',
                'financial_summary': 'Financial Summary',
                'total_expenses': 'Total Expenses:',
                'paid': 'Paid:',
                'unpaid': 'Unpaid:',
                'reserved': 'Reserved:',
                'monthly_income': 'Monthly Income:',
                'family_other_income': 'Additional Income:',
                'tickets_value': 'Tickets Value:',
                'remaining': 'Remaining Income:',
                'total_household': 'Total Household Income:',
                'language': 'Language',
                'currency': 'Currency',
                'history': 'History',
                'previous_month': '◄ Previous Month',
                'next_month': 'Next Month ►',
                'save_month': 'Save Month',
                'note': '💡 Double-click on any cell to edit, or press F2',
                'months': ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December'],
                'achitat': 'Paid',
                'neachitat': 'Unpaid',
                'reserved': 'Reserved',
                'recurring': 'Recurring (months)',
                'category': 'Category',
                'categories': {
                    'bills': 'Bills',
                    'transport': 'Transport',
                    'food': 'Food',
                    'health': 'Health',
                    'entertainment': 'Entertainment',
                    'clothing': 'Clothing',
                    'education': 'Education',
                    'other': 'Other'
                },
                'credit_types': { 
                    'mortgage': 'Mortgage',
                    'personal': 'Personal Loan',
                    'overdraft': 'Overdraft',
                    'credit_card': 'Credit Card'
                },
                'total_bill': 'Total Bill Amount:',
                'paid_amount': 'Paid Amount:',
                'remaining_bill': 'Remaining:'
            }
        }
        
        # Current settings
        self.current_date = datetime.now()
        self.language = tk.StringVar(value='ro')
        self.currency = tk.StringVar(value='LEI')
        
        # Initialize monthly data structure
        if 'monthly_data' not in self.data:
            self.data['monthly_data'] = {}
        
        # Load current month data or create new
        self.load_current_month()
        
        self.setup_ui()
        self.update_displays()
    
    def load_data(self) -> Dict:
        """Load data from JSON file or create default structure"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
        
        return {
            'monthly_data': {},
            'settings': {
                'language': 'ro',
                'currency': 'LEI'
            }
        }
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            # Save current month data
            self.save_current_month_data()
            
            # Ensure the parent directory exists
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write to file with UTF-8 encoding
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            return True
        except PermissionError:
            messagebox.showerror("Eroare de Permisiuni", 
                               f"Nu am permisiunea să salvez fișierul în:\n{self.data_file}\n\n"
                               f"Încerc să salvez în directorul curent...")
            try:
                fallback_file = Path('financial_data.json')
                with open(fallback_file, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False)
                self.data_file = fallback_file
                messagebox.showinfo("Succes", f"Date salvate în: {fallback_file.absolute()}")
                return True
            except Exception as e2:
                messagebox.showerror("Eroare", f"Nu pot salva datele: {e2}")
                return False
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la salvarea datelor: {e}")
            return False
    
    def get_month_key(self):
        """Get the key for current month"""
        return f"{self.current_date.year}_{self.current_date.month:02d}"
    
    def load_current_month(self):
        """Load data for current month"""
        month_key = self.get_month_key()
        print(f"Loading month: {month_key}")
        
        if month_key in self.data.get('monthly_data', {}):
            month_data = self.data['monthly_data'][month_key]
            self.current_month_data = month_data
            print(f"Loaded existing month data with {len(month_data.get('expenses', []))} expenses")
            
            # Check if we need to add indefinite recurring expenses
            # (in case they were added to previous month after this month was created)
            self.check_and_add_indefinite_recurring()
        else:
            print(f"Month {month_key} doesn't exist, creating new")
            # Create new month data
            self.current_month_data = {
                'income': {'monthly_income': 2000.0},
                'expenses': [],
                'family_income': [],
                'other_income': [],
                'meal_tickets': {'worked_days': 20, 'value_per_day': 35.0}
            }
            
            # Check for indefinite recurring expenses from previous month
            self.copy_indefinite_recurring_expenses()
            
            print(f"After copying recurring: {len(self.current_month_data['expenses'])} expenses")
    
    
    def show_about(self):
        """Show about dialog"""
        if self.language.get() == 'ro':
            about_text = """Financial Tracker v1

            © 2025 BlojuP
            Toate drepturile rezervate.

            Aplicație pentru gestiunea finanțelor personale
            dezvoltată în Python cu Tkinter.

            Email: blojup@pentrucasata.ro"""
            messagebox.showinfo("Despre", about_text)
        else:
            about_text = """Financial Tracker v1

            © 2025 BlojuP
            All rights reserved.

            Personal finance management application
            developed in Python with Tkinter.

            Email: blojup@pentrucasata.ro"""
            messagebox.showinfo("About", about_text)

 
    def check_and_add_indefinite_recurring(self):
        """Check if we need to add indefinite recurring expenses to existing month"""
        # Get previous month
        if self.current_date.month == 1:
            prev_month = 12
            prev_year = self.current_date.year - 1
        else:
            prev_month = self.current_date.month - 1
            prev_year = self.current_date.year
        
        prev_month_key = f"{prev_year}_{prev_month:02d}"
        
        print(f"Checking existing month for missing recurring from {prev_month_key}")
        
        if prev_month_key in self.data.get('monthly_data', {}):
            prev_month_data = self.data['monthly_data'][prev_month_key]
            
            # Get names of expenses already in current month
            current_expense_names = {exp['name'] for exp in self.current_month_data.get('expenses', [])}
            
            # Check for indefinite recurring that aren't already here
            added_count = 0
            for expense in prev_month_data.get('expenses', []):
                if (expense.get('recurring_indefinite') or expense.get('is_indefinite_recurring')) and \
                   expense['name'] not in current_expense_names:
                    # Create a copy and add it
                    expense_copy = expense.copy()
                    self.current_month_data['expenses'].append(expense_copy)
                    added_count += 1
                    print(f"Added missing recurring expense: {expense['name']}")
            
            if added_count > 0:
                print(f"Added {added_count} recurring expenses to existing month")
                # Save the updated month data
                self.save_current_month_data()
                self.save_data()
    
    def copy_indefinite_recurring_expenses(self):
        """Copy indefinite recurring expenses from previous month"""
        if self.current_date.month == 1:
            prev_month = 12
            prev_year = self.current_date.year - 1
        else:
            prev_month = self.current_date.month - 1
            prev_year = self.current_date.year
        
        prev_month_key = f"{prev_year}_{prev_month:02d}"
        
        if prev_month_key in self.data.get('monthly_data', {}):
            prev_month_data = self.data['monthly_data'][prev_month_key]
            
            for expense in prev_month_data.get('expenses', []):
                if expense.get('recurring_indefinite') or expense.get('is_indefinite_recurring'):
                    expense_copy = expense.copy()
                    self.current_month_data['expenses'].append(expense_copy)
    
    def remove_recurring_from_future_months(self, expense_name):
        """Remove recurring expense from all future months"""
        current = self.current_date
        
        print(f"Removing recurring expense '{expense_name}' from future months")
        removed_count = 0
        
        # Check next 24 months (2 years ahead)
        for i in range(1, 25):
            if current.month + i > 12:
                next_month = (current.month + i - 1) % 12 + 1
                next_year = current.year + ((current.month + i - 1) // 12)
            else:
                next_month = current.month + i
                next_year = current.year
            
            month_key = f"{next_year}_{next_month:02d}"
            
            if month_key in self.data.get('monthly_data', {}):
                month_data = self.data['monthly_data'][month_key]
                
                # Find and remove expenses with matching name that have recurring flag
                expenses_to_remove = []
                for idx, exp in enumerate(month_data.get('expenses', [])):
                    if exp['name'] == expense_name and \
                       (exp.get('recurring_indefinite') or exp.get('is_indefinite_recurring') or 
                        exp.get('recurring_months') or exp.get('auto_add')):
                        expenses_to_remove.append(idx)
                
                # Remove in reverse order to maintain indices
                for idx in reversed(expenses_to_remove):
                    month_data['expenses'].pop(idx)
                    removed_count += 1
                    print(f"Removed from {month_key}")
        
        if removed_count > 0:
            print(f"Total removed: {removed_count} instances")
            self.save_data()
    
    def save_current_month_data(self):
        """Save current month data to main data structure"""
        month_key = self.get_month_key()
        self.data['monthly_data'][month_key] = self.current_month_data.copy()
        self.data['monthly_data'][month_key]['saved_at'] = datetime.now().isoformat()
    
    def t(self, key):
        """Get translation for current language"""
        return self.translations[self.language.get()][key]
    
    def setup_ui(self):
        """Setup the main UI"""
        # Top bar with language, currency and date navigation
        top_bar = ttk.Frame(self.root, padding="5")
        top_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), columnspan=2)
        
        # Language selector
        self.lang_frame = ttk.LabelFrame(top_bar, text=self.t('language'), padding="5")
        self.lang_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(self.lang_frame, text="Română", value="ro", 
                       variable=self.language, command=self.change_language).pack(side=tk.LEFT)
        ttk.Radiobutton(self.lang_frame, text="English", value="en",
                       variable=self.language, command=self.change_language).pack(side=tk.LEFT)
        
        # Currency selector
        self.curr_frame = ttk.LabelFrame(top_bar, text=self.t('currency'), padding="5")
        self.curr_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Combobox(self.curr_frame, textvariable=self.currency, 
                    values=["LEI", "EUR", "USD", "RON"], width=10, state="readonly").pack()
        
        # Date navigation
        self.hist_frame = ttk.LabelFrame(top_bar, text=self.t('history'), padding="5")
        self.hist_frame.pack(side=tk.LEFT, padx=5)
        
        self.prev_btn = ttk.Button(self.hist_frame, text=self.t('previous_month'), command=self.previous_month)
        self.prev_btn.pack(side=tk.LEFT, padx=2)
        
        month_name = self.t('months')[self.current_date.month - 1]
        self.date_label = ttk.Label(self.hist_frame, text=f"{month_name} {self.current_date.year}", 
                                   font=('Arial', 10, 'bold'))
        self.date_label.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = ttk.Button(self.hist_frame, text=self.t('next_month'), command=self.next_month)
        self.next_btn.pack(side=tk.LEFT, padx=2)
        
        self.save_month_btn = ttk.Button(self.hist_frame, text=self.t('save_month'), command=self.save_month)
        self.save_month_btn.pack(side=tk.LEFT, padx=10)
        
        # About button (?) in top right
        about_btn = ttk.Button(top_bar, text="?", width=3, command=self.show_about)
        about_btn.pack(side=tk.RIGHT, padx=5)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left panel - Expenses
        self.left_panel = ttk.LabelFrame(main_frame, text=self.t('expenses'), padding="10")
        self.left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Expenses table
        columns = (self.t('category'), self.t('expense_name'), self.t('amount'), self.t('status'), self.t('recurring'))
        self.expense_tree = ttk.Treeview(self.left_panel, columns=columns, show='headings', height=15)
        
        self.expense_tree.heading(self.t('category'), text=self.t('category'))
        self.expense_tree.heading(self.t('expense_name'), text=self.t('expense_name'))
        self.expense_tree.heading(self.t('amount'), text=self.t('amount'))
        self.expense_tree.heading(self.t('status'), text=self.t('status'))
        self.expense_tree.heading(self.t('recurring'), text=self.t('recurring'))

        self.expense_tree.column(self.t('category'), width=80)
        self.expense_tree.column(self.t('expense_name'), width=120)
        self.expense_tree.column(self.t('amount'), width=80)
        self.expense_tree.column(self.t('status'), width=80)
        self.expense_tree.column(self.t('recurring'), width=80)
        
        # Bind double-click to edit
        self.expense_tree.bind('<Double-1>', self.edit_expense)
        
        scrollbar = ttk.Scrollbar(self.left_panel, orient=tk.VERTICAL, command=self.expense_tree.yview)
        self.expense_tree.configure(yscroll=scrollbar.set)
        
        self.expense_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Expense buttons
        btn_frame = ttk.Frame(self.left_panel)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        self.add_exp_btn = ttk.Button(btn_frame, text=self.t('add_expense'), command=self.add_expense)
        self.add_exp_btn.pack(side=tk.LEFT, padx=2)
        self.del_exp_btn = ttk.Button(btn_frame, text=self.t('delete_expense'), command=self.remove_expense)
        self.del_exp_btn.pack(side=tk.LEFT, padx=2)
        self.dup_exp_btn = ttk.Button(btn_frame, text=self.t('duplicate_expense'), command=self.duplicate_expense)
        self.dup_exp_btn.pack(side=tk.LEFT, padx=2)
 
        # Note
        self.note_label = ttk.Label(self.left_panel, text=self.t('note'), 
                              font=('Arial', 8), foreground='gray')
        self.note_label.grid(row=2, column=0, columnspan=2, pady=(5, 0))
        
        # Right panel with scrollbar
        right_scroll_frame = ttk.Frame(main_frame)
        right_scroll_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create canvas and scrollbar for right panel
        canvas = tk.Canvas(right_scroll_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Use scrollable_frame instead of right_panel for all right-side content
        right_panel = scrollable_frame
        
        # Income section
        self.income_frame = ttk.LabelFrame(right_panel, text=self.t('income'), padding="10")
        self.income_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.income_label = ttk.Label(self.income_frame, text=self.t('monthly_income'))
        self.income_label.grid(row=0, column=0, sticky=tk.W)
        self.income_var = tk.StringVar(value=str(self.current_month_data['income']['monthly_income']))
        ttk.Entry(self.income_frame, textvariable=self.income_var, width=15).grid(row=0, column=1, padx=5)
        self.update_income_btn = ttk.Button(self.income_frame, text=self.t('update'), command=self.update_income)
        self.update_income_btn.grid(row=0, column=2)
        
        # Meal tickets section
        self.tickets_frame = ttk.LabelFrame(right_panel, text=self.t('meal_tickets'), padding="10")
        self.tickets_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.days_label = ttk.Label(self.tickets_frame, text=self.t('worked_days'))
        self.days_label.grid(row=0, column=0, sticky=tk.W)
        self.days_var = tk.StringVar(value=str(self.current_month_data['meal_tickets']['worked_days']))
        ttk.Entry(self.tickets_frame, textvariable=self.days_var, width=15).grid(row=0, column=1, padx=5)
        
        self.value_label = ttk.Label(self.tickets_frame, text=self.t('value_per_day'))
        self.value_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.ticket_value_var = tk.StringVar(value=str(self.current_month_data['meal_tickets']['value_per_day']))
        ttk.Entry(self.tickets_frame, textvariable=self.ticket_value_var, width=15).grid(row=1, column=1, padx=5, pady=(5, 0))
        
        self.update_tickets_btn = ttk.Button(self.tickets_frame, text=self.t('update'), command=self.update_tickets)
        self.update_tickets_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        
        # Other Income section
        self.other_frame = ttk.LabelFrame(right_panel, text=self.t('other_income'), padding="10")
        self.other_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.other_tree = ttk.Treeview(self.other_frame, 
                                      columns=(self.t('income_source'), self.t('amount')), 
                                      show='headings', height=3)
        self.other_tree.heading(self.t('income_source'), text=self.t('income_source'))
        self.other_tree.heading(self.t('amount'), text=self.t('amount'))
        self.other_tree.bind('<Double-1>', self.edit_other_income)
        self.other_tree.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        other_btn_frame = ttk.Frame(self.other_frame)
        other_btn_frame.grid(row=1, column=0, pady=(5, 0))
        self.add_other_btn = ttk.Button(other_btn_frame, text=self.t('add_other_income'), command=self.add_other_income)
        self.add_other_btn.pack(side=tk.LEFT, padx=2)
        self.del_other_btn = ttk.Button(other_btn_frame, text=self.t('delete'), command=self.remove_other_income)
        self.del_other_btn.pack(side=tk.LEFT, padx=2)
        
        # Financial Summary section with chart
        summary_container = ttk.Frame(right_panel)
        summary_container.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        # Left side - Summary table
        self.summary_frame = ttk.LabelFrame(summary_container, text=self.t('financial_summary'), padding="10")
        self.summary_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # Configure frame background
        summary_inner = ttk.Frame(self.summary_frame, relief='solid', borderwidth=1, padding="10")
        summary_inner.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.summary_labels = {}
        
        # New order: Income section first, then expenses, then remaining at the end
        summary_items = [
            ('total_household', 'total_household', 'darkblue'),  # VENITUL TOTAL AL CASEI
            ('monthly_income', 'monthly_income', 'black'),        # Venit Lunar
            ('family_other_income', 'family_other_income', 'darkgreen'),  # Venit Adițional
            ('tickets_value', 'tickets_value', 'green'),          # Valoarea Tichetelor
            ('separator1', None, None),                           # Separator line
            ('total_expenses', 'total_expenses', 'black'),        # Total Cheltuieli
            ('paid', 'paid', 'green'),                            # Plătit
            ('reserved', 'reserved', 'blue'),                     # Rezervat
            ('unpaid', 'unpaid', 'orange'),                       # Neplătit
            ('separator2', None, None),                           # Separator line
            ('remaining', 'remaining', 'darkgreen'),              # VENIT RĂMAS (at the end)
        ]
        
        row_idx = 0
        for idx, item_data in enumerate(summary_items):
            key = item_data[0]
            
            if key.startswith('separator'):
                separator = ttk.Separator(summary_inner, orient='horizontal')
                separator.grid(row=row_idx, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
                row_idx += 1
            else:
                trans_key = item_data[1]
                color = item_data[2]
                
                is_important = key in ['total_household', 'remaining']
                font_size = 11 if is_important else 10
                
                label = ttk.Label(summary_inner, text=self.t(trans_key), 
                                font=('Arial', font_size, 'bold'))
                label.grid(row=row_idx, column=0, sticky=tk.W, pady=3, padx=5)
                
                value_label = ttk.Label(summary_inner, text="0.00 RON", 
                                       foreground=color,
                                       font=('Arial', font_size, 'bold'))
                value_label.grid(row=row_idx, column=1, sticky=tk.E, pady=3, padx=5)
                
                self.summary_labels[key] = {
                    'label': label,
                    'value': value_label,
                    'color': color
                }
                row_idx += 1
        
        # Right side - Pie Chart
        chart_container = ttk.Frame(summary_container)
        chart_container.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N))
        
        # Chart title
        ttk.Label(chart_container, text="Grafic", font=('Arial', 10, 'bold')).pack()
        
        # Create canvas for pie chart with transparent background
        self.chart_canvas = tk.Canvas(chart_container, width=200, height=200, 
                                     bg=self.root.cget('bg'), highlightthickness=0)
        self.chart_canvas.pack()
        
        # Legend frame below chart
        self.legend_frame = ttk.Frame(chart_container)
        self.legend_frame.pack(pady=(5, 0))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(0, weight=1)
                
        # Copyright/Signature label
        copyright_frame = ttk.Frame(self.root)
        copyright_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        copyright_label = ttk.Label(copyright_frame, 
                                   text="© 2025 BlojuP - Financial Tracker v1",
                                   font=('Arial', 8),
                                   foreground='gray')
        copyright_label.pack(pady=5)
    
    def change_language(self):
        """Change interface language"""
        # Update all text elements
        self.root.title(self.t('title'))
        self.lang_frame.config(text=self.t('language'))
        self.curr_frame.config(text=self.t('currency'))
        self.hist_frame.config(text=self.t('history'))
        self.prev_btn.config(text=self.t('previous_month'))
        self.next_btn.config(text=self.t('next_month'))
        self.save_month_btn.config(text=self.t('save_month'))
        
        # Update month display
        month_name = self.t('months')[self.current_date.month - 1]
        self.date_label.config(text=f"{month_name} {self.current_date.year}")
        
        # Update left panel
        self.left_panel.config(text=self.t('expenses'))
        self.add_exp_btn.config(text=self.t('add_expense'))
        self.del_exp_btn.config(text=self.t('delete_expense'))
        self.dup_exp_btn.config(text=self.t('duplicate_expense'))
        self.note_label.config(text=self.t('note'))
        
        # Update right panel
        self.income_frame.config(text=self.t('income'))
        self.income_label.config(text=self.t('monthly_income'))
        self.update_income_btn.config(text=self.t('update'))
        
        self.tickets_frame.config(text=self.t('meal_tickets'))
        self.days_label.config(text=self.t('worked_days'))
        self.value_label.config(text=self.t('value_per_day'))
        self.update_tickets_btn.config(text=self.t('update'))
        
        self.other_frame.config(text=self.t('other_income'))
        self.add_other_btn.config(text=self.t('add_other_income'))
        self.del_other_btn.config(text=self.t('delete'))
        
        self.summary_frame.config(text=self.t('financial_summary'))
        
        # Update summary labels
        summary_keys = ['total_household', 'monthly_income', 'family_other_income', 'tickets_value',
                       'remaining', 'total_expenses', 'paid', 'reserved', 'unpaid']
        summary_label_keys = ['total_household', 'monthly_income', 'family_other_income', 'tickets_value',
                              'remaining', 'total_expenses', 'paid', 'reserved', 'unpaid']
        
        for key in summary_label_keys:
            if key in self.summary_labels:
                self.summary_labels[key]['label'].config(text=self.t(key))
        
        # Refresh displays
        self.update_displays()
    
    def previous_month(self):
        """Navigate to previous month"""
        # Save current month before switching
        self.save_current_month_data()
        
        # Move to previous month
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        
        # Update date label
        month_name = self.t('months')[self.current_date.month - 1]
        self.date_label.config(text=f"{month_name} {self.current_date.year}")
        
        # Load data for this month
        self.load_current_month()
        self.update_displays()
    
    def next_month(self):
        """Navigate to next month"""
        # Save current month before switching
        self.save_current_month_data()
        print(f"Saved current month before moving to next")
        
        # Move to next month
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        
        print(f"Moving to {self.current_date.year}-{self.current_date.month:02d}")
        
        # Update date label
        month_name = self.t('months')[self.current_date.month - 1]
        self.date_label.config(text=f"{month_name} {self.current_date.year}")
        
        # Load data for this month
        self.load_current_month()
        self.update_displays()
    
    def save_month(self):
        """Save current month data"""
        self.save_current_month_data()
        if self.save_data():
            month_name = self.t('months')[self.current_date.month - 1]
            messagebox.showinfo("Succes" if self.language.get() == 'ro' else "Success", 
                              f"Luna {month_name} {self.current_date.year} a fost salvată!" if self.language.get() == 'ro' 
                              else f"Month {month_name} {self.current_date.year} was saved!")
    
    def edit_expense(self, event):
        """Edit expense on double-click"""
        selection = self.expense_tree.selection()
        if not selection:
            return
        
        idx = self.expense_tree.index(selection[0])
        expense = self.current_month_data['expenses'][idx]
        
        # Open edit dialog with current expense data
        dialog = ExpenseDialog(self.root, 
                              "Editează Cheltuială" if self.language.get() == 'ro' else "Edit Expense", 
                              self.language.get(), 
                              edit_mode=True, 
                              expense_data=expense)
        
        if dialog.result:
            # Normalize status (always store in Romanian internally)
            status = dialog.result['status']
            if status in ['Achitat', 'Paid']:
                dialog.result['status'] = 'Achitat'
            elif status in ['Rezervat', 'Reserved']:
                dialog.result['status'] = 'Rezervat'
            else:
                dialog.result['status'] = 'Neachitat'
            
            # Check if recurring flag was removed
            old_recurring = expense.get('recurring_indefinite') or expense.get('is_indefinite_recurring')
            new_recurring = dialog.result.get('recurring_indefinite') or dialog.result.get('is_indefinite_recurring')
            
            if old_recurring and not new_recurring:
                # Recurring was turned off - remove from future months
                print(f"Recurring turned off for '{expense['name']}', removing from future months")
                self.remove_recurring_from_future_months(expense['name'])
            
            # Update the expense
            self.current_month_data['expenses'][idx] = dialog.result
            
            # If it has auto_add flag and is new, add to future months
            if dialog.result.get('auto_add') and not expense.get('auto_add'):
                self.auto_add_to_future_months(dialog.result)
            
            self.save_data()
            self.update_displays()
    

    
    def edit_other_income(self, event):
        """Edit other income on double-click"""
        selection = self.other_tree.selection()
        if not selection:
            return
        
        item = self.other_tree.selection()[0]
        column = self.other_tree.identify_column(event.x)
        
        idx = self.other_tree.index(item)
        income = self.current_month_data['other_income'][idx]
        
        col_idx = int(column.replace('#', '')) - 1
        
        if col_idx == 0:  # Source
            new_value = simpledialog.askstring("Edit", "Sursă:", initialvalue=income['source'])
            if new_value:
                income['source'] = new_value
        elif col_idx == 1:  # Amount
            new_value = simpledialog.askfloat("Edit", "Sumă:", initialvalue=income['amount'])
            if new_value is not None:
                income['amount'] = new_value
        
        self.update_displays()
        self.save_data()
    
    def update_displays(self):
        """Update all displays"""
        # Clear expense tree
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        
        # Populate expense tree
        for expense in self.current_month_data['expenses']:
            # Translate status to current language
            status = expense['status']
            if status in ['Achitat', 'Paid']:
                status_text = self.t('achitat')
            elif status in ['Rezervat', 'Reserved']:
                status_text = self.t('reserved')
            else:
                status_text = self.t('neachitat')
            
            # Determine recurring status (just numbers)
            recurring_text = '-'  # Default: no recurrence
            if expense.get('recurring_indefinite') or expense.get('is_indefinite_recurring'):
                recurring_text = '∞'  # Infinity symbol
            elif expense.get('recurring_months'):
                recurring_text = str(expense['recurring_months'])  # Just the number
            elif expense['type'] == 'Credit' and expense.get('remaining_months'):
                remaining = expense.get('remaining_months', 1)
                recurring_text = str(remaining)  # Just the number
            
            name_display = expense['name']
            if expense['type'] == 'Credit' and expense.get('credit_type'):
                credit_type_text = self.translations[self.language.get()]['credit_types'].get(
                    expense['credit_type'], '')
                name_display = f"{expense['name']} ({credit_type_text})"
            
            # Get category display text
            category = expense.get('category', 'other')
            category_text = self.t('categories').get(category, 'Altele')

            self.expense_tree.insert('', 'end', values=(
                category_text,
                expense['name'],
                f"{expense['total_amount']:.2f}",
                status_text,
                recurring_text
            ))
        
       
        # Update other income tree
        for item in self.other_tree.get_children():
            self.other_tree.delete(item)
        for income in self.current_month_data['other_income']:
            self.other_tree.insert('', 'end', values=(
                income['source'],
                f"{income['amount']:.2f}"
            ))
        
        # Update income fields
        self.income_var.set(str(self.current_month_data['income']['monthly_income']))
        self.days_var.set(str(self.current_month_data['meal_tickets']['worked_days']))
        self.ticket_value_var.set(str(self.current_month_data['meal_tickets']['value_per_day']))
        
        # Update summary
        self.update_summary()
    
    def update_summary(self):
        """Update financial summary"""
        totals = self.calculate_totals()
        currency = self.currency.get()
        
        # Update values in new order
        self.summary_labels['total_household']['value'].config(
            text=f"{totals['total_household_income']:.2f} {currency}",
            foreground='darkblue',
            font=('Arial', 11, 'bold')
        )
        
        self.summary_labels['monthly_income']['value'].config(
            text=f"{totals['monthly_income']:.2f} {currency}",
            foreground='black',
            font=('Arial', 10, 'bold')
        )
        
        self.summary_labels['family_other_income']['value'].config(
            text=f"{totals['additional_income']:.2f} {currency}",
            foreground='darkgreen',
            font=('Arial', 10, 'bold')
        )
        
        self.summary_labels['tickets_value']['value'].config(
            text=f"{totals['meal_tickets_total']:.2f} {currency}",
            foreground='green',
            font=('Arial', 10, 'bold')
        )
        
        # Expenses section
        self.summary_labels['total_expenses']['value'].config(
            text=f"{totals['total_expenses']:.2f} {currency}",
            foreground='black',
            font=('Arial', 10, 'bold')
        )
        
        self.summary_labels['paid']['value'].config(
            text=f"{totals['paid_amount']:.2f} {currency}",
            foreground='green',
            font=('Arial', 10, 'bold')
        )
        
        self.summary_labels['reserved']['value'].config(
            text=f"{totals['reserved_amount']:.2f} {currency}",
            foreground='blue',
            font=('Arial', 10, 'bold')
        )
        
        self.summary_labels['unpaid']['value'].config(
            text=f"{totals['unpaid_amount']:.2f} {currency}",
            foreground='orange',
            font=('Arial', 10, 'bold')
        )
        
        # REMAINING at the end - dynamic color
        remaining = totals['remaining_after_expenses']
        remaining_color = 'red' if remaining < 0 else 'darkgreen'
        self.summary_labels['remaining']['value'].config(
            text=f"{remaining:.2f} {currency}",
            foreground=remaining_color,
            font=('Arial', 11, 'bold')
        )
        
        # Update pie chart
        self.draw_pie_chart(totals)
    
    def draw_pie_chart(self, totals):
        """Draw an attractive pie chart showing expense breakdown by status"""
        self.chart_canvas.delete('all')
        
        # Clear previous legend
        for widget in self.legend_frame.winfo_children():
            widget.destroy()
        
        # Get values
        paid = totals['paid_amount']
        reserved = totals['reserved_amount']
        unpaid = totals['unpaid_amount']
        total_expenses = totals['total_expenses']
        
        if total_expenses <= 0:
            # Draw "No Data" message
            self.chart_canvas.create_text(100, 100, text="Fără cheltuieli", 
                                         font=('Arial', 12), fill='gray')
            return
        
        # Colors matching the summary
        colors = {
            'paid': '#51CF66',      # Green
            'reserved': '#339AF0',   # Blue
            'unpaid': '#FF922B'      # Orange
        }
        
        # Get background color for transparency effect
        bg_color = self.root.cget('bg')
        
        # Calculate percentages
        slices = []
        if paid > 0:
            slices.append(('Plătit', paid / total_expenses * 360, colors['paid'], paid))
        if reserved > 0:
            slices.append(('Rezervat', reserved / total_expenses * 360, colors['reserved'], reserved))
        if unpaid > 0:
            slices.append(('Neachitat', unpaid / total_expenses * 360, colors['unpaid'], unpaid))
        
        # Draw pie chart with shadow effect
        center_x, center_y = 100, 100
        radius = 65
        
        # Shadow
        self.chart_canvas.create_oval(
            center_x - radius + 3, center_y - radius + 3,
            center_x + radius + 3, center_y + radius + 3,
            fill='#CCCCCC', outline=''
        )
        
        # Draw slices
        start_angle = 90
        for label, extent, color, amount in slices:
            self.chart_canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=-extent,
                fill=color, outline='white', width=3
            )
            start_angle -= extent
        
        # Center circle for donut effect
        inner_radius = 35
        self.chart_canvas.create_oval(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            fill=bg_color, outline=''
        )
        
        # Center text - total expenses
        self.chart_canvas.create_text(center_x, center_y - 10, 
                                      text="Total", 
                                      font=('Arial', 9), fill='gray')
        self.chart_canvas.create_text(center_x, center_y + 8, 
                                      text=f"{total_expenses:.0f}", 
                                      font=('Arial', 12, 'bold'), fill='black')
        
        # Create legend outside the canvas in the legend_frame
        for label, extent, color, amount in slices:
            legend_item = ttk.Frame(self.legend_frame)
            legend_item.pack(anchor='w', pady=2)
            
            # Color box
            color_canvas = tk.Canvas(legend_item, width=15, height=15, 
                                    bg=bg_color, highlightthickness=0)
            color_canvas.pack(side='left', padx=(0, 5))
            color_canvas.create_rectangle(0, 0, 15, 15, fill=color, outline='black')
            
            # Label text
            ttk.Label(legend_item, text=f"{label} ({amount:.0f})", 
                     font=('Arial', 9)).pack(side='left')
    
    def calculate_totals(self) -> Dict:
        """Calculate all financial totals"""
        total_expenses = sum(item['total_amount'] for item in self.current_month_data['expenses'])
        
        # Handle both Romanian and English status values
        paid_amount = sum(item['total_amount'] for item in self.current_month_data['expenses'] 
                         if item['status'] in ['Achitat', 'Paid'])
        unpaid_amount = sum(item['total_amount'] for item in self.current_month_data['expenses'] 
                           if item['status'] in ['Neachitat', 'Unpaid'])
        reserved_amount = sum(item['total_amount'] for item in self.current_month_data['expenses'] 
                             if item['status'] in ['Rezervat', 'Reserved'])
        
        # Calculate meal tickets and income
        meal_tickets_total = (self.current_month_data['meal_tickets']['worked_days'] * 
                            self.current_month_data['meal_tickets']['value_per_day'])
        monthly_income = self.current_month_data['income']['monthly_income']
        
        # Calculate other income
        other_income_total = sum(item['amount'] for item in self.current_month_data.get('other_income', []))
        additional_income = other_income_total
        
        # Total household income = Monthly + Additional + Meal tickets
        total_household_income = monthly_income + additional_income + meal_tickets_total
        
        # Remaining = Monthly Income - Total Expenses
        remaining_after_expenses = monthly_income - total_expenses
        
        return {
            'total_expenses': total_expenses,
            'paid_amount': paid_amount,
            'unpaid_amount': unpaid_amount,
            'reserved_amount': reserved_amount,
            'meal_tickets_total': meal_tickets_total,
            'monthly_income': monthly_income,
            'additional_income': additional_income,
            'remaining_after_expenses': remaining_after_expenses,
            'total_household_income': total_household_income
        }
    
    def add_expense(self):
        """Add new expense"""
        dialog = ExpenseDialog(self.root, self.t('add_expense') if self.language.get() == 'ro' else "Add Expense", self.language.get())
        if dialog.result:
            print(f"Received result from dialog: {dialog.result}")
            
            # Normalize status to internal format (always use Romanian internally)
            status = dialog.result['status']
            if status in ['Achitat', 'Paid']:
                dialog.result['status'] = 'Achitat'
            elif status in ['Rezervat', 'Reserved']:
                dialog.result['status'] = 'Rezervat'
            else:
                dialog.result['status'] = 'Neachitat'
            
            # Add to current month
            self.current_month_data['expenses'].append(dialog.result)
            print(f"Added to current month. Auto-add flag: {dialog.result.get('auto_add')}")
            
            # Auto-add to future months if applicable
            if dialog.result.get('auto_add'):
                print("Calling auto_add_to_future_months...")
                self.auto_add_to_future_months(dialog.result)
            else:
                print("No auto_add flag, skipping future months")
            
            # Save and update
            saved = self.save_data()
            print(f"Data saved: {saved}")
            self.update_displays()
    
    def auto_add_to_future_months(self, expense):
        """Automatically add expense to future months"""
        print(f"Auto-adding expense: {expense['name']}, Type: {expense.get('type')}, Recurring: {expense.get('recurring_months')}, Indefinite: {expense.get('recurring_indefinite')}")
        
        if expense['type'] == 'Credit':
            # For credit with remaining months
            remaining = expense.get('remaining_months', 1)
            print(f"Credit: Adding to {remaining - 1} months")
            self.add_to_next_months(expense, remaining - 1)  # -1 because current month already has it
        
        elif expense.get('recurring_indefinite'):
            # For indefinite recurring (will be added month by month when navigating)
            # Mark it as indefinite in the data
            expense['is_indefinite_recurring'] = True
            print(f"Marked as indefinite recurring")
        
        elif expense.get('recurring_months'):
            # For fixed number of recurring months
            months = expense['recurring_months']
            print(f"Fixed recurring: Adding to {months - 1} months")
            self.add_to_next_months(expense, months - 1)  # -1 because current month already has it
    
    def add_to_next_months(self, expense, num_months):
        """Add expense to the next N months"""
        current = self.current_date
        
        for i in range(1, num_months + 1):
            # Calculate next month
            if current.month + i > 12:
                next_month = (current.month + i - 1) % 12 + 1
                next_year = current.year + ((current.month + i - 1) // 12)
            else:
                next_month = current.month + i
                next_year = current.year
            
            # Get month key
            month_key = f"{next_year}_{next_month:02d}"
            
            # Create month data if doesn't exist
            if month_key not in self.data['monthly_data']:
                self.data['monthly_data'][month_key] = {
                    'income': self.current_month_data['income'].copy(),
                    'expenses': [],
                    'family_income': [],
                    'other_income': [],
                    'meal_tickets': self.current_month_data['meal_tickets'].copy()
                }
            
            # Create a copy of the expense for next month
            expense_copy = expense.copy()
            
            # For credit type, decrease remaining months
            if expense['type'] == 'Credit' and 'remaining_months' in expense_copy:
                expense_copy['remaining_months'] = expense['remaining_months'] - i
                if expense_copy['remaining_months'] <= 0:
                    continue  # Don't add if no months remaining
            
            # Add to next month (avoid duplicates)
            # Check if expense with same name doesn't already exist
            exists = False
            for existing_exp in self.data['monthly_data'][month_key]['expenses']:
                if existing_exp['name'] == expense_copy['name']:
                    exists = True
                    break
            
            if not exists:
                self.data['monthly_data'][month_key]['expenses'].append(expense_copy)
    
    def remove_expense(self):
        """Remove selected expense"""
        selection = self.expense_tree.selection()
        if not selection:
            messagebox.showwarning("Atenție" if self.language.get() == 'ro' else "Warning", 
                                 "Selectați o cheltuială de șters!" if self.language.get() == 'ro' else "Select an expense to delete!")
            return
        
        idx = self.expense_tree.index(selection[0])
        if messagebox.askyesno("Confirmare" if self.language.get() == 'ro' else "Confirmation", 
                              f"Ștergeți '{self.current_month_data['expenses'][idx]['name']}'?" if self.language.get() == 'ro' 
                              else f"Delete '{self.current_month_data['expenses'][idx]['name']}'?"):
            self.current_month_data['expenses'].pop(idx)
            self.save_data()
            self.update_displays()
    
    def duplicate_expense(self):
        """Duplicate selected expense"""
        selection = self.expense_tree.selection()
        if not selection:
            messagebox.showwarning("Atenție" if self.language.get() == 'ro' else "Warning", 
                                 "Selectați o cheltuială de duplicat!" if self.language.get() == 'ro' else "Select an expense to duplicate!")
            return
        
        idx = self.expense_tree.index(selection[0])
        expense_copy = self.current_month_data['expenses'][idx].copy()
        expense_copy['name'] = expense_copy['name'] + (" (copie)" if self.language.get() == 'ro' else " (copy)")
        self.current_month_data['expenses'].append(expense_copy)
        self.save_data()
        self.update_displays()
    
    def update_income(self):
        """Update monthly income"""
        try:
            self.current_month_data['income']['monthly_income'] = float(self.income_var.get())
            self.save_data()
            self.update_summary()
            messagebox.showinfo("Succes" if self.language.get() == 'ro' else "Success", 
                              "Venit actualizat!" if self.language.get() == 'ro' else "Income updated!")
        except ValueError:
            messagebox.showerror("Eroare" if self.language.get() == 'ro' else "Error", 
                               "Suma invalidă!" if self.language.get() == 'ro' else "Invalid amount!")
    
    def update_tickets(self):
        """Update meal tickets"""
        try:
            self.current_month_data['meal_tickets']['worked_days'] = int(self.days_var.get())
            self.current_month_data['meal_tickets']['value_per_day'] = float(self.ticket_value_var.get())
            self.save_data()
            self.update_summary()
            messagebox.showinfo("Succes" if self.language.get() == 'ro' else "Success", 
                              "Tichete actualizate!" if self.language.get() == 'ro' else "Tickets updated!")
        except ValueError:
            messagebox.showerror("Eroare" if self.language.get() == 'ro' else "Error", 
                               "Valori invalide!" if self.language.get() == 'ro' else "Invalid values!")
    

    def add_other_income(self):
        """Add other income"""
        dialog = OtherIncomeDialog(self.root, self.language.get())
        if dialog.result:
            self.current_month_data['other_income'].append(dialog.result)
            self.save_data()
            self.update_displays()
    
    def remove_other_income(self):
        """Remove other income"""
        selection = self.other_tree.selection()
        if not selection:
            return
        idx = self.other_tree.index(selection[0])
        self.current_month_data['other_income'].pop(idx)
        self.save_data()
        self.update_displays()

class ExpenseDialog:
    def __init__(self, parent, title, language='ro', edit_mode=False, expense_data=None):
        self.result = None
        self.language = language
        self.edit_mode = edit_mode
        
        # Local translations dictionary
        self.translations = {
            'ro': {
                'categories': {
                    'bills': 'Facturi',
                    'transport': 'Transport',
                    'food': 'Mâncare',
                    'health': 'Sănătate',
                    'entertainment': 'Divertisment',
                    'clothing': 'Îmbrăcăminte',
                    'education': 'Educație',
                    'other': 'Altele'
                },
                'credit_types': {
                    'mortgage': 'Ipotecar',
                    'personal': 'Nevoi Personale',
                    'overdraft': 'Overdraft',
                    'credit_card': 'Card de Credit'
                }
            },
            'en': {
                'categories': {
                    'bills': 'Bills',
                    'transport': 'Transport',
                    'food': 'Food',
                    'health': 'Health',
                    'entertainment': 'Entertainment',
                    'clothing': 'Clothing',
                    'education': 'Education',
                    'other': 'Other'
                },
                'credit_types': {
                    'mortgage': 'Mortgage',
                    'personal': 'Personal Loan',
                    'overdraft': 'Overdraft',
                    'credit_card': 'Credit Card'
                }
            }
        }
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        #self.dialog.geometry("450x450")

        
        labels = {
            'ro': {
                'name': 'Numele Cheltuielii:',
                'type': 'Tipul Cheltuielii:',
                'normal': 'Cheltuială Normală',
                'credit': 'Credit cu Asigurare/Avans',
                'base': 'Suma de Bază:',
                'insurance': 'Asigurare:',
                'advance': 'Plată în Avans:',
                'total': 'Suma Totală:',
                'status': 'Status:',
                'paid': 'Achitat',
                'unpaid': 'Neachitat',
                'reserved': 'Rezervat',
                'remaining_months': 'Luni Rămase:',
                'recurring': 'Recurență (luni):',
                'utilities': 'Utilități și Cheltuieli',
                'is_recurring': 'Este recurent?',
                'category': 'Categorie:',
                'total_bill': 'Valoare Totală Factură:',
                'paid_amount': 'Suma Achitată:',
                'remaining_bill': 'Rest de Plată:',
                'credit_type': 'Tipul Creditului:'
            },
            'en': {
                'name': 'Expense Name:',
                'type': 'Expense Type:',
                'normal': 'Normal Expense',
                'credit': 'Credit with Insurance/Advance',
                'base': 'Base Amount:',
                'insurance': 'Insurance:',
                'advance': 'Advance Payment:',
                'total': 'Total Amount:',
                'status': 'Status:',
                'paid': 'Paid',
                'unpaid': 'Unpaid',
                'reserved': 'Reserved',
                'remaining_months': 'Remaining Months:',
                'recurring': 'Recurrence (months):',
                'utilities': 'Utilities and Expenses',
                'is_recurring': 'Is Recurring?',
                'category': 'Category:',
                'total_bill': 'Total Bill Amount:',
                'paid_amount': 'Paid Amount:',
                'remaining_bill': 'Remaining:',
                'credit_type': 'Credit Type:'
            }
        }
        
        l = labels[language]
        
        # Pre-fill data if editing
        if edit_mode and expense_data:
            name_val = expense_data.get('name', '')
            type_val = expense_data.get('type', 'Normal')
            base_val = str(expense_data.get('base_amount', ''))
            insurance_val = str(expense_data.get('insurance', '0'))
            advance_val = str(expense_data.get('advance_payment', '0'))
            total_val = str(expense_data.get('total_amount', ''))
            
            # Status translation
            status = expense_data.get('status', 'Neachitat')
            if status in ['Achitat', 'Paid']:
                status_val = l['paid']
            elif status in ['Rezervat', 'Reserved']:
                status_val = l['reserved']
            else:
                status_val = l['unpaid']
            
            months_val = str(expense_data.get('remaining_months', '1'))
            is_recurring = expense_data.get('recurring_months') or expense_data.get('recurring_indefinite', False)
            recurring_val = str(expense_data.get('recurring_months', '')) if expense_data.get('recurring_months') else ''
        else:
            name_val = ''
            type_val = 'Normal'
            base_val = ''
            insurance_val = '0'
            advance_val = '0'
            total_val = ''
            status_val = l['unpaid']
            months_val = '1'
            is_recurring = False
            recurring_val = ''
        
        # Name
        ttk.Label(self.dialog, text=l['name']).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.name_var = tk.StringVar(value=name_val)
        ttk.Entry(self.dialog, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        # Type
        ttk.Label(self.dialog, text=l['type']).grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.type_var = tk.StringVar(value=type_val)
        ttk.Radiobutton(self.dialog, text=l['normal'], variable=self.type_var, 
                       value="Normal", command=self.toggle_type).grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(self.dialog, text=l['credit'], variable=self.type_var, 
                       value="Credit", command=self.toggle_type).grid(row=2, column=1, sticky=tk.W)
        
        #Credit type
        self.credit_type_label = ttk.Label(self.dialog, text=l['credit_type'])
        credit_type_list = list(self.translations[language]['credit_types'].keys())
        credit_type_values = [self.translations[language]['credit_types'][ct] for ct in credit_type_list]

        # Determină valoarea default
        if edit_mode and expense_data and expense_data.get('credit_type'):
            default_credit_type = self.translations[language]['credit_types'].get(expense_data['credit_type'], credit_type_values[0])
        else:
            default_credit_type = credit_type_values[0]

        self.credit_type_var = tk.StringVar(value=default_credit_type)
        self.credit_type_combo = ttk.Combobox(self.dialog, textvariable=self.credit_type_var, 
                                              values=credit_type_values, width=27, state="readonly")
        
        # Category selector
        ttk.Label(self.dialog, text=l['category']).grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        translations = {
            'ro': {
                'category': 'Categorie:',
                'categories': {
                    'bills': 'Facturi',
                    'transport': 'Transport',
                    'food': 'Mâncare',
                    'health': 'Sănătate',
                    'entertainment': 'Divertisment',
                    'clothing': 'Îmbrăcăminte',
                    'education': 'Educație',
                    'other': 'Altele'
                }
            },
            'en': {
                'category': 'Category:',
                'categories': {
                    'bills': 'Bills',
                    'transport': 'Transport',
                    'food': 'Food',
                    'health': 'Health',
                    'entertainment': 'Entertainment',
                    'clothing': 'Clothing',
                    'education': 'Education',
                    'other': 'Other'
                }
            }
        }

        category_list = list(translations[language]['categories'].keys())
        category_values = [translations[language]['categories'][cat] for cat in category_list]

        if edit_mode and expense_data:
            default_category = expense_data.get('category', 'other')
            default_category_text = self.translations[language]['categories'].get(default_category, 'Altele')
        else:
            default_category_text = self.translations[language]['categories']['other']

        self.category_var = tk.StringVar(value=default_category_text)
        self.category_combo = ttk.Combobox(self.dialog, textvariable=self.category_var, 
                                           values=category_values, width=27, state="readonly")
        self.category_combo.grid(row=3, column=1, padx=10, pady=5)
        self.category_combo.bind('<<ComboboxSelected>>', lambda e: self.toggle_bill_fields())
        
        # Base Amount (for both types, this is the monthly amount or base credit amount)
        ttk.Label(self.dialog, text=l['base']).grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.base_amount_var = tk.StringVar(value=base_val)
        self.base_entry = ttk.Entry(self.dialog, textvariable=self.base_amount_var, width=30)
        self.base_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Credit-specific fields
        self.insurance_label = ttk.Label(self.dialog, text=l['insurance'])
        self.insurance_var = tk.StringVar(value=insurance_val)
        self.insurance_entry = ttk.Entry(self.dialog, textvariable=self.insurance_var, width=30)
        self.insurance_entry.bind('<KeyRelease>', lambda e: self.calculate_total())
        
        self.advance_label = ttk.Label(self.dialog, text=l['advance'])
        self.advance_var = tk.StringVar(value=advance_val)
        self.advance_entry = ttk.Entry(self.dialog, textvariable=self.advance_var, width=30)
        self.advance_entry.bind('<KeyRelease>', lambda e: self.calculate_total())
        
        self.months_label = ttk.Label(self.dialog, text=l['remaining_months'])
        self.months_var = tk.StringVar(value=months_val)
        self.months_entry = ttk.Entry(self.dialog, textvariable=self.months_var, width=30)
        
        # Total Amount label (only for Credit type)
        self.total_label = ttk.Label(self.dialog, text=l['total'])
        self.total_amount_var = tk.StringVar(value=total_val)
        self.total_entry = ttk.Entry(self.dialog, textvariable=self.total_amount_var, width=30, state='readonly')
        
        # Normal expense - recurring fields
        self.recurring_check_var = tk.BooleanVar(value=is_recurring)
        self.recurring_check = ttk.Checkbutton(self.dialog, text=l['is_recurring'], 
                                               variable=self.recurring_check_var,
                                               command=self.toggle_recurring)
        
        self.recurring_label = ttk.Label(self.dialog, text=l['recurring'])
        self.recurring_var = tk.StringVar(value=recurring_val)
        self.recurring_entry = ttk.Entry(self.dialog, textvariable=self.recurring_var, width=30)
        
        # Status
        self.status_label = ttk.Label(self.dialog, text=l['status'])
        self.status_var = tk.StringVar(value=status_val)
        status_options = [l['paid'], l['unpaid'], l['reserved']] if language == 'ro' else ['Paid', 'Unpaid', 'Reserved']
        self.status_combo = ttk.Combobox(self.dialog, textvariable=self.status_var, 
                                         values=status_options, width=27)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Anulează" if language == 'ro' else "Cancel", 
                  command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Bind base amount change for total calculation
        self.base_entry.bind('<KeyRelease>', lambda e: self.calculate_total())
        
        # Bill payment fields (for Bills category)
        self.total_bill_label = ttk.Label(self.dialog, text=l['total_bill'])
        self.total_bill_var = tk.StringVar(value='')
        self.total_bill_entry = ttk.Entry(self.dialog, textvariable=self.total_bill_var, width=30)

        self.paid_label = ttk.Label(self.dialog, text=l['paid_amount'])
        self.paid_var = tk.StringVar(value='0')
        self.paid_entry = ttk.Entry(self.dialog, textvariable=self.paid_var, width=30)

        self.remaining_label = ttk.Label(self.dialog, text=l['remaining_bill'])
        self.remaining_var = tk.StringVar(value='0.00')
        self.remaining_entry = ttk.Entry(self.dialog, textvariable=self.remaining_var, width=30, state='readonly')

        # Bind pentru calcul automat
        self.total_bill_entry.bind('<KeyRelease>', lambda e: self.calculate_remaining())
        self.paid_entry.bind('<KeyRelease>', lambda e: self.calculate_remaining())
        
        # Set initial type display
        self.toggle_type()
        self.toggle_bill_fields()  # ADAUGĂ ACEST RÂnd
        
        # Auto-resize dialog to fit content
        self.dialog.update_idletasks()
        width = max(450, self.dialog.winfo_reqwidth() + 20)
        height = self.dialog.winfo_reqheight() + 20
        self.dialog.geometry(f'{width}x{height}')
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)
    
    def toggle_type(self):
        """Toggle between normal and credit expense fields"""
        if self.type_var.get() == "Credit":
            # ASCUNDE categoria pentru Credit
            ttk.Label(self.dialog, text='').grid(row=3, column=0)  # Clear row 3
            self.category_combo.grid_remove()
            
            # Show credit type selector la row 3
            self.credit_type_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
            self.credit_type_combo.grid(row=3, column=1, padx=10, pady=5)
            
            # Show credit fields
            self.insurance_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
            self.insurance_entry.grid(row=5, column=1, padx=10, pady=5)
            self.advance_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
            self.advance_entry.grid(row=6, column=1, padx=10, pady=5)
            self.months_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
            self.months_entry.grid(row=7, column=1, padx=10, pady=5)
            
            # Show total amount (calculated)
            self.total_label.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)
            self.total_entry.grid(row=8, column=1, padx=10, pady=5)
            
            # Status
            self.status_label.grid(row=9, column=0, padx=10, pady=5, sticky=tk.W)
            self.status_combo.grid(row=9, column=1, padx=10, pady=5)
            
            # Hide category selector (pentru Normal type)
            # Presupunând că ai un self.category_label și self.category_combo
            
            # Hide recurring fields
            self.recurring_check.grid_remove()
            self.recurring_label.grid_remove()
            self.recurring_entry.grid_remove()
            
            self.calculate_total()
        else:
            # Hide credit type selector
            self.credit_type_label.grid_remove()
            self.credit_type_combo.grid_remove()
            
            # ARATĂ categoria pentru Normal
            l = {'ro': {'category': 'Categorie:'}, 'en': {'category': 'Category:'}}[self.language]
            ttk.Label(self.dialog, text=l['category']).grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
            self.category_combo.grid(row=3, column=1, padx=10, pady=5)
            
            # Hide total amount for normal expenses
            self.total_label.grid_remove()
            self.total_entry.grid_remove()
            
            # Show recurring checkbox (MOVED to row 5)
            self.recurring_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
            
            # Status for normal expense (MOVED to row 7)
            self.status_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
            self.status_combo.grid(row=7, column=1, padx=10, pady=5)
            
            # Show/hide recurring fields based on checkbox
            self.toggle_recurring()
            
        # ADAUGĂ ACESTE LINII LA FINAL:
        self.dialog.update_idletasks()
        width = max(450, self.dialog.winfo_reqwidth() + 20)
        height = self.dialog.winfo_reqheight() + 20
        self.dialog.geometry(f'{width}x{height}')
    
    def toggle_recurring(self):
            """Toggle recurring entry state"""
            if self.recurring_check_var.get():
                self.recurring_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
                self.recurring_entry.grid(row=6, column=1, padx=10, pady=5)
                # Move Status down when recurring is shown
                self.status_label.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)
                self.status_combo.grid(row=8, column=1, padx=10, pady=5)
            else:
                self.recurring_label.grid_remove()
                self.recurring_entry.grid_remove()
                # Move Status back up when recurring is hidden
                self.status_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
                self.status_combo.grid(row=7, column=1, padx=10, pady=5)

    def toggle_bill_fields(self):
        """Show/hide bill payment fields based on category"""
        if self.type_var.get() == "Normal":
            selected_category = self.category_var.get()
            
            category_key = None
            for key, val in self.translations[self.language]['categories'].items():
                if val == selected_category:
                    category_key = key
                    break
            
            if category_key == 'bills':
                # Hide base amount for bills
                self.base_entry.grid_remove()
                
                # Show bill fields
                self.total_bill_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
                self.total_bill_entry.grid(row=4, column=1, padx=10, pady=5)
                self.paid_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
                self.paid_entry.grid(row=5, column=1, padx=10, pady=5)
                self.remaining_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
                self.remaining_entry.grid(row=6, column=1, padx=10, pady=5)
                
                # Add recurring checkbox for bills
                self.recurring_check.grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
                
                # Status
                self.status_label.grid(row=9, column=0, padx=10, pady=5, sticky=tk.W)
                self.status_combo.grid(row=9, column=1, padx=10, pady=5)
            else:
                # ADAUGĂ ACEASTĂ LINIE ÎNAINTE DE grid_remove():
                l = {'ro': {'base': 'Suma de Bază:'}, 'en': {'base': 'Base Amount:'}}[self.language]
                ttk.Label(self.dialog, text=l['base']).grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
                self.base_entry.grid(row=4, column=1, padx=10, pady=5)  # Re-show entry
                
                
                # Show base amount for other categories
                self.total_bill_label.grid_remove()
                self.total_bill_entry.grid_remove()
                self.paid_label.grid_remove()
                self.paid_entry.grid_remove()
                self.remaining_label.grid_remove()
                self.remaining_entry.grid_remove()
                
        # ADAUGĂ ACESTE LINII LA FINAL:
        self.dialog.update_idletasks()
        width = max(450, self.dialog.winfo_reqwidth() + 20)
        height = self.dialog.winfo_reqheight() + 20
        self.dialog.geometry(f'{width}x{height}')


    def calculate_remaining(self):
        """Calculate remaining amount for bills"""
        try:
            total = float(self.total_bill_var.get() or 0)
            paid = float(self.paid_var.get() or 0)
            remaining = total - paid
            self.remaining_var.set(f"{remaining:.2f}")
            
            # Update base amount with total
            self.base_amount_var.set(str(total))
        except ValueError:
            pass 

 
    def calculate_total(self):
        """Calculate total for credit type"""
        if self.type_var.get() == "Credit":
            try:
                base = float(self.base_amount_var.get() or 0)
                insurance = float(self.insurance_var.get() or 0)
                advance = float(self.advance_var.get() or 0)
                total = base + insurance + advance
                self.total_amount_var.set(f"{total:.2f}")
            except ValueError:
                pass
    
    def ok(self):
        try:
            if self.type_var.get() == "Credit":
                base_amount = float(self.base_amount_var.get() or 0)  # ADAUGĂ ACEASTĂ LINIE
                insurance = float(self.insurance_var.get() or 0)
                advance = float(self.advance_var.get() or 0)
                total_amount = base_amount + insurance + advance
                remaining_months = int(self.months_var.get() or 1)
                selected_credit_type = self.credit_type_var.get()
                credit_type_key = None
                for key, val in self.translations[self.language]['credit_types'].items():
                    if val == selected_credit_type:
                        credit_type_key = key
                        break
                
                self.result = {
                    'name': self.name_var.get(),
                    'type': 'Credit',
                    'credit_type': credit_type_key,  # ADAUGĂ
                    'base_amount': base_amount,
                    'insurance': insurance,
                    'advance_payment': advance,
                    'total_amount': total_amount,
                    'status': self.status_var.get(),
                    'reserved': False,
                    'remaining_months': remaining_months
                }
                
                # Add auto_add flag if creating new (not editing)
                if not self.edit_mode:
                    self.result['auto_add'] = True
                    print(f"Setting auto_add=True for credit with {remaining_months} months")
            else:
                # Check if it's a bill
                selected_category = self.category_var.get()
                category_key = None
                for key, val in self.translations[self.language]['categories'].items():
                    if val == selected_category:
                        category_key = key
                        break
                
                if category_key == 'bills':
                    # For bills, use total_bill as base_amount
                    base_amount = float(self.total_bill_var.get() or 0)
                else:
                    base_amount = float(self.base_amount_var.get())
                
                result = {
                    'name': self.name_var.get(),
                    'type': 'Normal',
                    'base_amount': base_amount,
                    'total_amount': base_amount,
                    'status': self.status_var.get(),
                    'reserved': False,
                    'category': category_key
                }
                
                # Check for recurring (works for all categories including bills)
                if self.recurring_check_var.get():
                    recurring_months = self.recurring_var.get().strip()
                    if recurring_months:
                        result['recurring_months'] = int(recurring_months)
                        if not self.edit_mode:
                            result['auto_add'] = True
                    else:
                        result['recurring_indefinite'] = True
                        if not self.edit_mode:
                            result['auto_add'] = True
                
                # For bills, save payment tracking
                if category_key == 'bills' and self.total_bill_var.get():
                    result['bill_total'] = float(self.total_bill_var.get())
                    result['bill_paid'] = float(self.paid_var.get() or 0)
                    result['bill_remaining'] = result['bill_total'] - result['bill_paid']
                
                self.result = result
            
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Eroare" if self.language == 'ro' else "Error", 
                               "Valoare invalidă!" if self.language == 'ro' else "Invalid value!")

class FamilyIncomeDialog:
    def __init__(self, parent, language='ro'):
        self.result = None
        self.language = language
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Adaugă Membru Familie" if language == 'ro' else "Add Family Member")
        #self.dialog.geometry("350x200")
 
        
        labels = {
            'ro': {'name': 'Numele:', 'role': 'Rolul:', 'amount': 'Suma:'},
            'en': {'name': 'Name:', 'role': 'Role:', 'amount': 'Amount:'}
        }
        
        l = labels[language]
        
        ttk.Label(self.dialog, text=l['name']).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.name_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.name_var, width=25).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(self.dialog, text=l['role']).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.role_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.role_var, width=25).grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(self.dialog, text=l['amount']).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.amount_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.amount_var, width=25).grid(row=2, column=1, padx=10, pady=10)
        
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Anulează" if language == 'ro' else "Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Auto-resize
        self.dialog.update_idletasks()
        width = max(350, self.dialog.winfo_reqwidth() + 20)
        height = self.dialog.winfo_reqheight() + 20
        self.dialog.geometry(f'{width}x{height}')
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)
    
    def ok(self):
        try:
            self.result = {
                'name': self.name_var.get(),
                'role': self.role_var.get(),
                'amount': float(self.amount_var.get())
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Eroare" if self.language == 'ro' else "Error", 
                               "Suma invalidă!" if self.language == 'ro' else "Invalid amount!")

class OtherIncomeDialog:
    def __init__(self, parent, language='ro'):
        self.result = None
        self.language = language
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Adaugă Alt Venit" if language == 'ro' else "Add Other Income")
        #self.dialog.geometry("350x150")

        
        labels = {
            'ro': {'source': 'Sursa:', 'amount': 'Suma:'},
            'en': {'source': 'Source:', 'amount': 'Amount:'}
        }
        
        l = labels[language]
        
        ttk.Label(self.dialog, text=l['source']).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.source_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.source_var, width=25).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(self.dialog, text=l['amount']).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.amount_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.amount_var, width=25).grid(row=1, column=1, padx=10, pady=10)
        
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Anulează" if language == 'ro' else "Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Auto-resize
        self.dialog.update_idletasks()
        width = max(350, self.dialog.winfo_reqwidth() + 20)
        height = self.dialog.winfo_reqheight() + 20
        self.dialog.geometry(f'{width}x{height}')
        self.dialog.resizable(False, False)
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)
    
    def ok(self):
        try:
            self.result = {
                'source': self.source_var.get(),
                'amount': float(self.amount_var.get())
            }
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Eroare" if self.language == 'ro' else "Error", 
                               "Suma invalidă!" if self.language == 'ro' else "Invalid amount!")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FinancialTrackerGUI(root)
        
        # Show where data is being saved
        print(f"Financial Tracker started")
        print(f"Data file location: {app.data_file.absolute()}")
        
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()