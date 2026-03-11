# 📄 Context-Aware Multi-Document Summarization with Knowledge Graph Enhancement

This project implements a server using **FastAPI** to support uploading text documents, generating summaries in multiple languages using **Gemini LLM**, and visualizing **Knowledge Graphs** extracted from the summaries.

---

# 🚀 Features

- Upload `.txt` files (max 100KB)
- Generate summaries in selected languages via **Gemini API**
- Download or view summaries
- Create a **Knowledge Graph** from English summaries
- Store metadata for each upload (file ID, summary files, graph image)
- API endpoints for easy integration with frontend

---

# 🧐 Tech Stack

**Backend**
- FastAPI
- Python

**LLM Integration**
- Google Gemini API

**NLP**
- SpaCy (`en_core_web_lg`)

**Graph Visualization**
- NetworkX
- Matplotlib

**Frontend**
- React (Planned)

---

# 📁 Folder Structure

```
project/
│
├── backend/
│   ├── main.py               # FastAPI app
│   ├── genai_service.py      # Gemini LLM interaction
│   ├── uploaded_files/       # Uploaded raw .txt files
│   ├── summaries/            # Multilingual summaries
│   ├── graphs/               # PNGs of generated knowledge graphs
│   └── data/                 # Metadata JSON files
│
└── frontend/ (Coming soon)
    ├── public/               # Static assets
    ├── src/
    │   ├── components/       # React components
    │   ├── pages/            # Application pages
    │   ├── App.js            # Main React app
    │   └── index.js          # Entry point
    │
    ├── package.json          # Frontend dependencies
    └── tailwind.config.js    # TailwindCSS configuration
```

---

# 📱 API Endpoints

### Check Server Status
```
GET /status
```

### Upload File and Generate Summaries
```
POST /upload/
```

**FormData**

```
file: UploadFile (.txt)
languages: str (comma-separated e.g., "en,hi,fr")
```

### View a Summary
```
GET /view/{file_name}
```

### Download a Summary
```
GET /download/{file_name}
```

### Download Knowledge Graph
```
GET /graph/{file_name}
```

---

# 🛠️ Setup Instructions

## 1️⃣ Clone Repo

```bash
git clone https://github.com/yourusername/context-aware-summary.git
cd backend
```

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

## 3️⃣ Add Gemini API Key

Create `.env` file:

```
GEMINI_API_KEY=your-api-key-here
```

## 4️⃣ Run the Server

```bash
uvicorn main:app --reload
```

---

# 💻 Frontend Setup (Planned)

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm start
```

---

# ⚠️ Notes

- File size must be under **5MB**
- Only `.txt` files are supported
- Knowledge graph is based on **English summary (if available)**
- Summaries and metadata are stored persistently for each file ID

---

# 📌 Future Work

- Document clustering and semantic similarity integration
- Full **multi-document summarization support**
- Real-time updates and progress bars
- Complete frontend implementation

---

# 🧑‍💻 Author

**Avinash kumar**  
Student at **Lovely Professional University**

Project for research:  
**"Context-Aware Multi-Document Summarization with Knowledge Graph Enhancement"**

---

# 📃 License

MIT License
