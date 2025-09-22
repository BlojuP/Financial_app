# Financial Tracker v1.0

A personal finance management application developed in Python with Tkinter GUI. Track expenses, income, and budget planning on a monthly basis.

[Română](README.ro.md) | English

## Key Features

- 📊 Expense management with multiple categories
- 💰 Income and meal ticket tracking
- 🔄 Recurring expenses (fixed, limited duration, or indefinite)
- 💳 Support for credits with insurance and advance payments
- 🏠 Financial summary with interactive charts
- 🌐 Multilingual support (Romanian/English)
- 🗓️ Month navigation with automatic saving
- 💾 Automatic saving in JSON format

## Screenshots

![Main Interface](screenshot.png)

## System Requirements

- Python 3.8 or newer
- Operating System: Windows, macOS, Linux
- Minimum RAM: 512 MB
- Disk space: 50 MB

## Dependencies

The application uses only standard Python libraries:

- `tkinter` - GUI framework (included with Python)
- `json` - Data storage
- `datetime` - Date management
- `pathlib` - File management
- `typing` - Type hints

## Installation

### Step 1: Install Python

Download and install Python from [python.org](https://python.org):
- Windows: Download installer and follow instructions
- macOS: Use Homebrew: `brew install python`
- Linux: `sudo apt-get install python3 python3-tkinter`

### Step 2: Download Application

```bash
# Clone repository
git clone https://github.com/BlojuP/Financial_app.git
cd financial-tracker

# OR download ZIP
wget https://github.com/BlojuP/Financial_app/archive/main.zip
unzip main.zip
cd financial-tracker-main
```

### Step 3: Run Application

```bash
# Run directly
python financial_tracker v1.py

# OR on Linux/macOS
python3 financial_tracker v1.py
```

## Usage

### Starting the Application

The application opens with the main interface containing:

- **Left panel**: Expense list with categories, amounts, and status
- **Right panel**: Income, meal tickets, other income, and financial summary

### Expense Management

#### Adding an Expense

1. Click "Add Expense"
2. Fill in expense name
3. Choose type:
   - **Normal Expense**: For regular expenses
   - **Credit with Insurance/Advance**: For credits with additional costs

#### Available Categories

- **Bills**: Utilities, phone, internet
- **Transport**: Fuel, public transport, car maintenance
- **Food**: Groceries, restaurants
- **Health**: Medicine, medical consultations
- **Entertainment**: Movies, books, hobbies
- **Clothing**: Clothes, footwear
- **Education**: Courses, books, materials
- **Other**: Miscellaneous expenses

#### Credit Types

For credits with insurance/advance:
- **Mortgage**: Real estate loans
- **Personal**: Consumer loans
- **Overdraft**: Account overdraft
- **Credit Card**: Card payments

#### Recurring Expenses

- **Fixed Recurrence**: Specify exact number of months
- **Indefinite Recurrence**: Leave field empty for continuous recurrence
- **Credits**: Automatically added for remaining months

#### Expense Status

- **Paid**: Expense has been paid
- **Unpaid**: Expense not yet paid
- **Reserved**: Money reserved for this expense

### Income Management

#### Monthly Income

- Set fixed monthly income in dedicated field
- Click "Update" to save

#### Meal Tickets

- **Working Days**: Number of working days in month
- **Value/Day**: Value of one meal ticket
- Total calculated automatically

#### Other Income

- Add supplementary income (freelancing, bonuses, etc.)
- Specify source and amount

### Month Navigation

- Use arrows "◄ Previous Month" and "Next Month ►"
- Data saves automatically when navigating
- Click "Save Month" for manual save

### Financial Summary

Summary panel displays:

- **Total Household Income**: Sum of all income sources
- **Monthly Income**: Base salary
- **Additional Income**: Other income sources
- **Tickets Value**: Total meal tickets
- **Total Expenses**: Sum of all expenses
- **Paid/Unpaid/Reserved**: Expense breakdown
- **Remaining Income**: Difference between income and expenses

### Pie Chart

- Visualizes proportion of paid, unpaid, and reserved expenses
- Intuitive colors: Green (paid), Orange (unpaid), Blue (reserved)
- Interactive legend with exact values

## Advanced Features

### Quick Edit

- **Double-click** any list item to edit
- **F2** for quick edit
- Changes save automatically

### Duplicate Expenses

- Select an expense and click "Duplicate Expense"
- Useful for similar recurring expenses

### Search and Filter

- Expenses organized by categories
- Status displayed visually with colors

### Backup and Restore

Data saved in `~/financial_data.json`:

```bash
# Manual backup
cp ~/financial_data.json ~/financial_backup_$(date +%Y%m%d).json

# Restore
cp ~/financial_backup_20250101.json ~/financial_data.json
```

## Data Structure

Data organized by months in JSON format:

```json
{
  "monthly_data": {
    "2025_01": {
      "income": {"monthly_income": 2000.0},
      "expenses": [
        {
          "name": "Electricity",
          "type": "Normal",
          "category": "bills",
          "base_amount": 150.0,
          "total_amount": 150.0,
          "status": "Unpaid"
        }
      ],
      "meal_tickets": {
        "worked_days": 20,
        "value_per_day": 35.0
      },
      "other_income": []
    }
  }
}
```

## Troubleshooting

### Application won't start

```bash
# Check Python version
python --version

# Check if tkinter is installed
python -c "import tkinter; print('Tkinter OK')"

# On Linux, install tkinter separately
sudo apt-get install python3-tkinter
```

### Permission error when saving

- Application tries to save to home directory
- If issues occur, will save to current directory
- Check permissions for `~/financial_data.json`

### Corrupted data

```bash
# Delete data file for complete reset
rm ~/financial_data.json

# Application will create new file on next startup
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add new feature"`
4. Push to branch: `git push origin feature-name`
5. Create Pull Request

### Developer Guide

```python
# Main structure
class FinancialTrackerGUI:  # Main interface
class ExpenseDialog:        # Expense dialog
class OtherIncomeDialog:    # Other income dialog

# Important files
financial_tracker_gui.py   # Main application
README.md                 # This documentation
README.ro.md             # Romanian version
```

## License

© 2025 BlojuP - All rights reserved.

For support: blojup@pentrucasata.ro

## Roadmap

- [ ] Excel/CSV export
- [ ] Monthly/yearly reports
- [ ] Custom categories
- [ ] Cloud synchronization
- [ ] Mobile application
- [ ] Bank import
- [ ] Bill notifications
- [ ] Trend charts

---

**Current version**: 1.0  
**Last updated**: September 2025  
**Compatibility**: Python 3.8+