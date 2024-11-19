#smartBanking_system

This project is an advanced banking system implemented in Python, featuring a graphical user interface (GUI), data persistence using SQLite, encryption for secure account storage, and basic AI capabilities for predictive analytics. The system allows users to perform key banking operations such as deposits, withdrawals, balance inquiries, and balance predictions.

Key Features

	•	Graphical User Interface (GUI): Built with Tkinter, the GUI provides an intuitive interface for managing accounts, performing transactions, and viewing account balances or predictions.
	•	Data Persistence: Account and transaction data are stored securely in an SQLite database, ensuring reliability and scalability.
	•	Encryption: Account IDs are encrypted using the AES-based cryptography library to protect sensitive information.
	•	Predictive Analytics: Implements a basic AI feature to predict future account balances using transaction history and a moving average algorithm.
	•	Error Handling and Logging: Comprehensive error handling with logs for all actions, including errors, transactions, and predictions.
	•	Secure Key Management: A unique encryption key is generated and stored securely for account data protection.

Functionalities

	•	Add Account: Create new accounts with an initial balance.
	•	Deposit Money: Securely deposit funds into an existing account.
	•	Withdraw Money: Withdraw funds from an account, with checks for sufficient balance.
	•	Check Balance: View the current balance of any account.
	•	Predict Balance: Predict future balances based on recent transaction trends.

How It Works

	1.	Setup: On the first run, the system initializes an encryption key and database schema.
	2.	Account Management: Users can manage accounts directly through the GUI, making transactions and inquiries seamless.
	3.	Data Integrity: Changes are committed to the database immediately, ensuring data consistency and reliability.
	4.	Security: All account IDs are encrypted before storage, ensuring confidentiality.

Requirements

To run this project, ensure the following Python packages are installed:
	•	cryptography
	•	sqlite3 (Standard Library)
	•	tkinter (Standard Library)

Use the included requirements.txt file to install dependencies.
