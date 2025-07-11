# AAA Traders Application README

## Overview
The **AAA Traders** application is a simple desktop-based inventory management system built using Python. It allows users to:

- Record purchase details (e.g., item, company, model, dealer, price, units, and city).
- Record sale details (e.g., dealer, item sold, company, model, quantity, and sale price).
- Automatically calculate profit and total bill.
- View all recorded purchase and sale data in a tabular format.

This application uses `tkinter` for the GUI and `pandas` to manage data stored in CSV files.

---

## Features

### 1. **Purchase Entry**
Allows the user to input and save purchase information into a CSV file (`purchase_data.csv`). Fields include:
- Item (with predefined electronics list)
- Company
- Model Number
- Dealer
- Price Per Unit
- Units Purchased
- City

### 2. **Sale Entry**
Allows the user to input and save sale information into another CSV file (`sale_data.csv`). Fields include:
- Sale Dealer
- Item Sold
- Company
- Model Number
- Units Sold
- Sale Price Per Unit
- Total Bill (calculated automatically)
- Profit (calculated automatically by comparing with purchase price)

### 3. **View Records**
Displays both purchase and sale data in separate tabs within a new window using a table viewer.

---

## Technologies Used

- **Python **
- **Tkinter**: For building the graphical user interface.
- **Pandas**: For handling data and writing/reading from CSV files.
- **CSV Files**: For persistent storage of purchase and sale records.


## How to Run

### Prerequisites
Make sure you have Python 3 installed on your system.

### Steps
1. Clone or download this repository.
2. Open a terminal/command prompt and navigate to the project directory.
3. Install required packages:
   ```bash
   pip install pandas
   ```
4. Run the application:
   ```bash
   python main.py
   ```

---

## Screenshots (Conceptual)

| Section         | Description |
|----------------|-------------|
| Splash Screen  | Shows "Welcome to AAA Traders" for 5 seconds before launching the app. |
| Purchase Tab   | Input fields for recording purchases. |
| Sale Tab       | Input fields for recording sales with automatic profit calculation. |
| View Tab       | Displays all saved purchase and sale records in tables. |



## Contact
For any questions or contributions, feel free to reach out or open an issue on the repo.
