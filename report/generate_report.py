"""Generate a PDF summary of RAG/RBAC deliverables."""
from datetime import date
from pathlib import Path

from fpdf import FPDF

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = PROJECT_ROOT / "report" / "deliverables_report.pdf"

DELIVERABLES = [
    ("Embedding generation module", "Completed", "processing/generate_embeddings.py"),
    ("Populated vector database with indexed documents", "Completed", "vectorstore/chroma"),
    ("Semantic search functionality and query interface", "Completed", "query/query_engine.py; demo preview/demo_*"),
    ("Search quality and performance benchmarking report", "Pending", "(add benchmark script/report)"),
    ("Role-based access control filtering module", "Completed", "rbac/rbac_filter.py"),
    ("Query processing and normalization utilities", "Completed", "query/query_engine.py"),
    ("Role permission configuration and hierarchy definition", "Completed", "rbac/rbac_filter.py"),
    ("Role-based access validation test suite and results", "Completed", "tests/verify_rbac.py; tests/verify_chromadb.py"),
]

SUMMARY_POINTS = [
    "Pipeline: clean -> chunk -> embed -> index (Chroma persistent store)",
    "Embeddings: sentence-transformers/all-MiniLM-L6-v2 (384 dims)",
    "Vectors: 135 chunks indexed with full metadata and role_* flags",
    "RBAC: enforced at query time using Chroma where filters (role_<dept>=True)",
    "Normalization: strip + lowercase + collapse whitespace before embedding",
    "Interfaces: terminal demo + Streamlit demo (demo preview/)",
]

DATA_COVERAGE = [
    "Engineering: 39 chunks",
    "Marketing: 49 chunks",
    "Finance: 36 chunks",
    "General: 11 chunks",
]

RBAC_NOTES = [
    "Hierarchy: admin > department roles (finance/engineering/hr/marketing) > employee",
    "Metadata: allowed_roles + boolean role_* flags stored per chunk",
    "Filtering: query-time where filters + validation tests block cross-department access",
]

TEST_NOTES = [
    "tests/verify_rbac.py confirms role-based filtering",
    "tests/verify_chromadb.py checks metadata presence and retrieval",
    "tests/verify_embeddings.py validates embedding dimensions and counts",
]

INTERFACE_NOTES = [
    "Terminal chatbot: demo preview/demo_chatbot.py",
    "Streamlit chatbot: demo preview/demo_web_chatbot.py",
    "Docs for demos: demo preview/DEMO_README.md",
]

PENDING_NOTES = [
    "Add a short search benchmarking run (latency/relevance) and capture results.",
]

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "RAG/RBAC Deliverables Report", ln=1, align="C")
        self.set_font("Helvetica", "", 10)
        self.cell(0, 8, f"Date: {date.today().isoformat()}", ln=1, align="C")
        self.ln(4)

    def add_section_title(self, title: str):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, title, ln=1)
        self.ln(2)

    def add_bullet(self, text: str):
        self.set_font("Helvetica", "", 10)
        safe = text.replace("/", "/ ")  # allow wrapping on slashes
        self.multi_cell(170, 6, f"- {safe}")

    def add_spacer(self, h: float = 4.0):
        self.ln(h)

    def add_table(self, rows):
        self.set_font("Helvetica", "B", 10)
        self.cell(75, 8, "Deliverable", border=1)
        self.cell(25, 8, "Status", border=1)
        self.cell(80, 8, "Location", border=1, ln=1)
        self.set_font("Helvetica", "", 10)
        for name, status, location in rows:
            self.cell(75, 8, name[:50] + ("..." if len(name) > 50 else ""), border=1)
            self.cell(25, 8, status, border=1)
            self.cell(80, 8, location, border=1, ln=1)


def build_report():
    pdf = PDF()
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_section_title("Summary")
    for point in SUMMARY_POINTS:
        pdf.add_bullet(point)
    pdf.add_spacer()

    pdf.add_section_title("Data Coverage")
    for point in DATA_COVERAGE:
        pdf.add_bullet(point)
    pdf.add_spacer()

    pdf.add_section_title("RBAC Implementation")
    for note in RBAC_NOTES:
        pdf.add_bullet(note)
    pdf.add_spacer()

    pdf.add_section_title("Interfaces")
    for note in INTERFACE_NOTES:
        pdf.add_bullet(note)
    pdf.add_spacer()

    pdf.add_section_title("Validation")
    for note in TEST_NOTES:
        pdf.add_bullet(note)
    pdf.add_spacer()

    pdf.add_section_title("Deliverables")
    pdf.add_table(DELIVERABLES)
    pdf.ln(4)

    pdf.add_section_title("Pending")
    for note in PENDING_NOTES:
        pdf.add_bullet(note)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(REPORT_PATH))
    return REPORT_PATH


if __name__ == "__main__":
    path = build_report()
    print(f"Report written to {path}")
