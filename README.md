*Management Information Systems Project:** Research and application of the Odoo ERP system to digitalize the fresh tuna production process for a seafood processing enterprise (Simulated based on Ba Hai Joint Stock Company).

---

## 📖 Project Overview
The seafood processing industry faces strict requirements regarding processing time, storage temperature, and quality control standards (HACCP, GMP, SSOP). Manual management using Excel often leads to fragmented data, cold storage discrepancies, and poor product traceability. 

This project provides a comprehensive digital transformation solution (TO-BE) using the open-source **Odoo 16** ERP platform. The system seamlessly integrates the entire supply chain, starting from purchasing raw materials from fishermen, managing cold storage, tracking the production process (preparation, filleting, freezing, packaging), to handling sales and financial accounting.

## 🚀 Core Modules Implemented
The system utilizes Odoo's core modules to create a closed-loop management workflow:

*   🛒 **Purchase:** Manages the procurement of raw fresh tuna, recording quality, quantity, and temperature right at the time of receipt.
*   📦 **Inventory:** Real-time cold storage management. Tracks goods by Lot/Serial numbers, strictly controls expiration dates, and automates low-stock alerts.
*   🏭 **Manufacturing:** Sets up Bills of Materials (BOM). Manages Manufacturing Orders (MO) through various stages (Preparation -> Filleting -> Additives -> Freezing -> Packaging), with automated raw material deduction and finished goods entry.
*   👥 **HR (Human Resources):** Manages worker profiles, work shifts, and tracks production productivity to accurately calculate labor costs.
*   🤝 **Sales:** Handles export and domestic orders, linking directly to inventory to automatically suggest supplementary production plans when stock is low.
*   🧾 **Accounting:** Automatically generates invoices from the sales/purchase processes, tracks payables/receivables, and exports financial reports.

## ⭐ Highlight Feature: Custom GPS Attendance Add-on
In addition to the standard modules, our team developed a custom **GPS-integrated Attendance Add-on**. 
*   **Functionality:** Records Check-in/Check-out times along with geographical coordinates (Longitude/Latitude) and displays the locations directly on a built-in map.
*   **Purpose:** Ensures transparency in attendance, prevents timesheet fraud, and is highly suitable for enterprises with multiple workshops, cold storages, or employees working at the port/field.

## 🛠 Tech Stack & Environment
*   **OS:** Ubuntu Server 22.04
*   **ERP Platform:** Odoo 16 Community Edition
*   **Programming Language:** Python 3.10 (for custom module development)
*   **Database:** PostgreSQL

## 📊 Business Analysis Documentation
The project includes comprehensive system analysis documentation:
*   Current State (AS-IS) and Proposed Solution (TO-BE) analysis.
*   **Use Case Diagrams:** Describe the interaction flows of 6 user groups (Purchasing, Warehouse, Production, HR, Sales, Accounting).
