# 📊 Streamlit CSV Visualizer & App Encryptor

Welcome to the **streamlined data visualization and application protection suite**. This project serves two distinct purposes:
1.  **Data Visualization**: An interactive tool to upload and visualize CSV data sets.
2.  **Application Encryption**: A utility to encrypt Streamlit applications into a single, self-contained, protected script.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 📈 Component 1: CSV Data Visualizer (`app.py`)

This is the core application for data analysis. It allows users to upload CSV files and instantly generate insights.

### Features
*   **Automatic Data Detection**: Identifies numeric and categorical columns.
*   **Interactive Charts**: 
    *   **Scatter Plots**: Visualize relationships between two numeric variables.
    *   **Histograms**: Analyse the distribution of a single numeric variable.
    *   **Bar Charts**: Compare categorical data against numeric values/counts.

### How to Run
```bash
streamlit run app.py
```
*   Once running, open the URL (usually `http://localhost:8501`).
*   Upload any `.csv` file to start visualizing.

---

## 🔒 Component 2: Streamlit App Encryptor (`encryptor.py`)

This tool has been upgraded to a **web-based interface**. It allows you to protect your source code by encrypting it and wrapping it in a loader script.

### How it Works
The encryptor uses `cryptography.fernet` (symmetric encryption) to:
1.  Read your original source code (e.g., `app.py`).
2.  Generate a unique encryption key.
3.  Encrypt the code content.
4.  Embed the **encrypted blob** and the **key** into a new Python script.
5.  The new script can be run exactly like the original but hides the logic from casual inspection.

### How to Use
1.  **Start the Encryptor Service**:
    ```bash
    streamlit run encryptor.py
    ```
2.  **Upload Your App**:
    *   In the web interface, upload your target Python file (e.g., `app.py`).
3.  **Encrypt**:
    *   Click the **"Encrypt & Generate Protected App"** button.
4.  **Download**:
    *   A download button will appear for the generated file (e.g., `e_app.py`).

---

## 🛡️ Component 3: Running Protected Apps

The output from the Encryptor (e.g., `e_app.py` or default `protected_app.py`) is a standalone Streamlit application.

### How to Run
```bash
streamlit run e_app.py
```

### Technical Note
*   The protected app contains an `exec()` loop that decrypts the code in memory and executes it.
*   **Security Disclaimer**: The key is embedded in the script to allow it to run standalone. This provides **obfuscation** and prevents casual modifications, but it does **not** provide military-grade security against determined reverse engineering.

---

## 📂 File Structure

| File | Description |
| :--- | :--- |
| `app.py` | The original CSV visualization source code. |
| `encryptor.py` | The Streamlit-based tool for encrypting other Python files. |
| `protected_app.py` | A sample protected version of `app.py`. |
| `requirements.txt` | List of libraries needed to run the project. |
