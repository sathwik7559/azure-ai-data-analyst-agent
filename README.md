

AI Data Analyst Agent (Streamlit + Python)

An AI-powered data analyst application that allows users to ask natural language business questions over tabular data and automatically generates:
	•	📊 Data analysis
	•	📈 Visualizations (bar, line, pie – auto-selected)
	•	📝 Clear, human-readable insights

Built with Python, Streamlit, and Pandas, this project demonstrates how AI-driven analysis can make data exploration accessible to non-technical users.

⸻

🚀 Features
	•	Upload or load structured CSV data
	•	Ask questions like:
	•	“What is the total revenue?”
	•	“Revenue share by category”
	•	“Compare Electronics vs Books revenue”
	•	Automatically:
	•	Computes metrics
	•	Selects the correct chart type
	•	Displays tabular output
	•	Generates a natural language explanation
	•	Interactive Streamlit UI
	•	Modular & extensible architecture

⸻



⸻

🧩 How It Works
	1.	User asks a business question in plain English
	2.	The analysis engine interprets intent (metric, dimension, comparison)
	3.	Pandas code is generated dynamically
	4.	Code is executed safely in a sandbox
	5.	Results are:
	•	Displayed as tables or charts
	•	Explained in simple business language

⸻

📊 Supported Analysis Types

Question Type	Output
Total metrics	KPI / scalar
Grouped analysis	Bar chart / table
Trend analysis	Line chart
Share / distribution	Pie chart
Comparisons	Bar chart + insights

Charts are auto-selected based on the question.

⸻

🖥 Local Setup

1️⃣ Clone the Repository

git clone https://github.com/<your-username>/azure-ai-data-analyst-agent.git
cd azure-ai-data-analyst-agent

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run the App

streamlit run app.py

App will be available at:

http://localhost:8501


⸻

☁️ Deployment (Azure App Service)

Startup command used in Azure:

streamlit run app.py --server.port=8000 --server.address=0.0.0.0


⸻

🔐 Security & Best Practices
	•	No secrets committed to GitHub
	•	.env excluded via .gitignore
	•	Code execution sandboxed
	•	Modular design for scalability

⸻

🧪 Sample Questions to Try
	•	What is the total revenue?
	•	Revenue by category
	•	Revenue share by category
	•	Compare Books vs Electronics revenue
	•	Which category performs best?

⸻

🎯 Why This Project Is Strong

✔ Demonstrates Data Analytics + AI
✔ Shows real-world business reasoning
✔ Uses clean, production-ready architecture
✔ Ideal for Data Analyst / Data Engineer / AI Engineer roles

⸻

📌 Next Enhancements (Planned)
	•	Azure OpenAI integration
	•	Multi-file upload support
	•	SQL-backed datasets
	•	Time-series forecasting
	•	User authentication

⸻

👤 Author

Sathwik Reddy
MS Information Systems
Data Analytics • AI • Cloud

⸻

⭐️ If you like this project

Give it a ⭐️ and feel free to fork or contribute!
