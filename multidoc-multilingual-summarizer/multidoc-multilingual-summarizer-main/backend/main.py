from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import spacy
import networkx as nx
import matplotlib.pyplot as plt
import json

from genai_service import generate_summary_with_gemini

# Load SpaCy model for entity and SVO extraction
nlp = spacy.load("en_core_web_lg")

# Directories
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
UPLOAD_DIR = "uploaded_files"
SUMMARY_DIR = "summaries"
GRAPH_DIR = "graphs"
DATA_DIR = "data"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# FastAPI App
app = FastAPI()

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/status")
def server_status():
    return {"status": "ok", "message": "Server is running!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), languages: str = Form(...)):
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        return JSONResponse(status_code=400, content={"error": "File too large. Max 100KB allowed."})

    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    text = contents.decode("utf-8")
    languages_list = [lang.strip() for lang in languages.split(",")]
    print(languages_list)
    summaries = {}

    for lang in languages_list:
        summary_text = generate_summary_with_gemini(text, lang)
        # lang_safe = lang.replace("\"", "").replace("[", "").replace("]", "").replace(" ", "")
        lang_safe = lang.replace("\"", "").replace(" ", "")
        summary_filename = f"{file_id}_{lang_safe}.txt"
        summary_path = os.path.join(SUMMARY_DIR, summary_filename)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary_text)
        summaries[lang_safe] = summary_filename

    # Knowledge graph from first language summary
    first_lang_key = next(iter(summaries))
    with open(os.path.join(SUMMARY_DIR, summaries[first_lang_key]), encoding="utf-8") as f:
        summary_text = f.read()
    doc = nlp(summary_text)
    svos = extract_svo(doc)
    graph_path = create_graph(svos, file_id)

    # Save metadata
    metadata_path = os.path.join(DATA_DIR, f"{file_id}_meta.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump({"original_file": filename, "summaries": summaries, "graph": os.path.basename(graph_path)}, f)

    return {
        "status": "success",
        "file_id": file_id,
        "summary_files": summaries,
        "graph_image": os.path.basename(graph_path)
    }

@app.get("/view/{file_name}")
async def view_file(file_name: str):
    file_path = os.path.join(SUMMARY_DIR, file_name)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "File not found"})
    with open(file_path, "r", encoding="utf-8") as f:
        return {"content": f.read()}

@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = os.path.join(SUMMARY_DIR, file_name)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(path=file_path, filename=file_name, media_type="text/plain")

@app.get("/graph/{file_name}")
async def download_graph(file_name: str):
    file_path = os.path.join(GRAPH_DIR, file_name)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "Graph image not found"})
    return FileResponse(path=file_path, filename=file_name, media_type="image/png")

# ---------- Helper Functions ---------- #
def extract_svo(doc):
    svos = []
    for token in doc:
        if token.dep_ in {"nsubj", "nsubjpass"} and token.head.pos_ == "VERB":
            subject = token.text
            verb = token.head.text
            obj = [child.text for child in token.head.children if child.dep_ in {"dobj", "attr"}]
            if obj:
                svos.append((subject, verb, obj[0]))
    return svos

def create_graph(svos, file_id):
    graph = nx.DiGraph()
    for subj, verb, obj in svos:
        graph.add_edge(subj, obj, label=verb)
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): d['label'] for u, v, d in graph.edges(data=True)})
    path = os.path.join(GRAPH_DIR, f"{file_id}_graph.png")
    plt.savefig(path)
    plt.close()
    return path
