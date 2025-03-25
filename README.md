# 🚀 DocuQuery: AI-Powered PDF Knowledge Assistant Using Google PALM
---

## 🌟 Overview
**DocuQuery** is an AI-powered PDF and CSV knowledge assistant that allows users to interact with documents using natural language queries. It uses **Google PALM** for text processing, embeddings, and question-answering. This project enables users to:

- Extract and analyze price lists from multiple suppliers.
- Summarize and interact with research papers.
- Match resumes with job descriptions for efficient hiring.
- Generate insights from CSV files and visualize data with automated plots.
---

## ✨ Features
- **PDF Analysis**: Extracts and analyzes text from PDF documents.
- **CSV Chat & Visualization**: Processes CSV files, answers queries, and generates plots.
- **Conversational AI**: Uses Google PALM for accurate and context-aware responses.
- **History Tracking**: Maintains a record of previous queries and responses.
- **Interactive UI**: Built with **Streamlit** for a seamless user experience.
---

## ⚙️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python, Google PALM API
- **Libraries Used**:
  - `PyPDF2` for text extraction from PDFs
  - `pandas` for data handling
  - `matplotlib` for data visualization
  - `google.generativeai` for AI-powered responses
  - `FAISS` for efficient embedding retrieval
---

## 🔧 Installation

### 🔹 Prerequisites
Ensure you have Python installed (version 3.8+ recommended).
---

### 🛠️ Clone the Repository
```bash
git clone https://github.com/your-repo/docuquery.git
cd docuquery
```
---

### 🏗️ Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```
---

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```
---

### 🔑 Setup Google PALM API Key
1. Obtain your Google PALM API key from [Google AI](https://ai.google.dev/).
2. Create a `.env` file in the project directory and add:
   ```bash
   API_KEY=your_google_palm_api_key
   ```
---

## ▶️ Running the Application
```bash
streamlit run app.py
```
---

## 💡 How to Use

### 📄 Upload and Analyze PDFs
1. Click **Upload PDF** and select one or multiple files.
2. Select a file from the dropdown to view extracted text.
3. Enter a query to ask questions about the document.
4. Download responses if needed.
---

### 📊 Upload and Query CSV Files
1. Upload one or more CSV files.
2. Select a file and view its data.
3. Ask a question about the data.
4. Generate a visualization based on your query.
---

### 📝 View Chat History
Scroll to the bottom of the page to see previous queries and responses.
---

## 👥 Collaborators
- Sahil Karne
- Kartikey Sapkal
- Siddhesh Kotwal
- Sachin Jadhav
---