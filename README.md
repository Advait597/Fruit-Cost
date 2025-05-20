🛒 Fruit Billing System

A Python-based GUI application for billing fruits, tracking sales, and visualizing data using bar graphs and pie charts. Built with Tkinter, SQLite, and Matplotlib.

⸻

🚀 Features
	•	Add fruits by quantity (in kg or per piece)
	•	Automatically calculate total, discount, and final amount
	•	Save bills to a local SQLite database
	•	View sales data as:
	•	📊 Bar graph: quantity sold per fruit
	•	🥧 Pie chart: revenue/profit distribution per fruit 
	•	Responsive and scalable UI
	•	Clear, editable itemized bill
	•	Prices vary per fruit with /kg or /pc display

⸻

🧾 Sample Fruits & Prices

Fruit	Price	Unit
Apple	₹90.10	/kg
Mango	₹68.00	/kg
Banana	₹45.50	/kg
Avocado	₹140.00	/pc
Dragonfruit	₹629.98	/pc
Cherry	₹1761.00	/kg

…and more!

⸻

📂 Project Structure

src/
│
├── main.py          # Main application code
├── fruit_billing.db # SQLite DB (created automatically)
└── README.md        # Project README


⸻

🛠️ Requirements
	•	Python 3.7+
	•	Tkinter (usually bundled with Python)
	•	Matplotlib

Install dependencies:

pip install matplotlib


⸻

▶️ Running the App

python main.py


⸻

💾 Database
	•	bills table:
	•	id, total, discount, final_total
	•	bill_items table:
	•	bill_id, fruit, qty, rate, total_cost

⸻

📈 Visualizations
	•	Bar Graph: Fruits vs Total Quantity Sold
	•	Pie Chart: Fruits vs Revenue Contribution & Profit Contribution

⸻

📋 To-Do (optional)
	•	Export bills as PDF or Excel
	•	Add user authentication
	•	Date filters for sales

⸻

🧑‍💻 Author

Built with ❤️ by [Advait597]
Open to suggestions and improvements!
