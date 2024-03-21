import re
from fpdf import FPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.document_loaders import WebBaseLoader


def url_to_doc(urls, company_name):
    docs = []
    for _, url in urls.items():
        try:
            loader = WebBaseLoader(url, continue_on_failure=True)
            loader.requests_per_second = 1
            document = loader.aload()

            text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ".", ","],
            chunk_size=1000,
            chunk_overlap=25,
            )
            docs.extend(text_splitter.split_documents(document))
        except UnicodeDecodeError:
            pass # Ignore the error and continue with the next URL

    wikidocs = WikipediaLoader(query=company_name, load_max_docs=1).load()
    docs.extend(wikidocs)

    return docs
    

def format_docs(docs): 
    return "\n\n".join(doc.page_content for doc in docs)


def remove_markdown_symbols(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"\'", "", text)
    text = re.sub(r"'", "", text)
    text = re.sub(r"€", "(Euros)", text)
    text = text.strip()

    return text

# def text_to_pdf(input_file, output_file):
#     # Read the content of the text file
#     with open(input_file, 'r', encoding='utf-8') as f:
#         text = f.read()
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size = 12)
#     pdf.multi_cell(0, 10, txt = text)
#     pdf.output(output_file)

#     return pdf

class PDF(FPDF):
    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 5, title)
        self.ln(1)

    def chapter_body(self, body):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 5, body)
        self.ln()

def text_to_pdf(reports, res, company_name):
    pdf = PDF()
    pdf.add_page()

    for query, content in zip(reports, res):
            pdf.chapter_title(query)
            pdf.chapter_body(content)

    pdf_file = company_name+"_Product_Research.pdf"
    pdf.output(pdf_file)