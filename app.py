import os
import nest_asyncio
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from search import web_search
from docs import url_to_doc
from docs import format_docs
from docs import remove_markdown_symbols
from docs import text_to_pdf
from vector_store import doc_to_vectorstore

load_dotenv()
nest_asyncio.apply()  # for parallel scraping of text from the websites

#API_keys
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY") 

def main():
    st.title("Company Market Research Tool")
    company_name = st.text_input("Enter the company name:", placeholder="Google")
    if st.button("Generate Report"):
        with st.spinner("Generating your PDF..."):
            company_name = company_name.lower()
            urls = web_search(company_name)
            docs = url_to_doc(urls, company_name)
            db = doc_to_vectorstore(docs, company_name)
            retriever = db.as_retriever(search_type="mmr")
            print("Going to LLM")
            llm = ChatOpenAI(model="gpt-3.5-turbo")

            template = """
            You are tasked with generating a market analysis report in plain text format, avoiding symbols like * and #. Use the retrieved context from the vector store and the provided user query to answer the question comprehensively.
            
            User Query: {question}
            
            Context: {context}

            Report Structure:
            Avoid the use of Symbols such as **,#
            Avoid the use of headings and subheadings.
            For reporting any amount use American Dollars($) if the information is in Euro(€) convert it to Dollars($).
            The report should be structured in paragraphs, separated by newline characters.
            Use numbered lists where necessary to present information clearly.
            Ensure the report addresses the user query directly and provides clear insights using information from the context.
            Quantify your analysis with data from the context whenever possible.
            Aim for a minimum length of 1000 words, but provide accurate content with relevant and necessary information.
            Include a list of sources used at the end of the report, ensuring each source is referenced only once.

            Note: If insufficient context is available to answer the question comprehensively, state this clearly in the report.

            ---

            Output:

            Generate a plain text report following the above structure, avoiding the use of *, #, or markdown formatting entirely. Use numbered lists only where necessary to enhance clarity. Strive for a minimum length of 1000 words, but prioritize providing comprehensive and relevant information
            """

            prompt = PromptTemplate.from_template(template)
            rag_chain = (
                {"question": RunnablePassthrough(), "context": retriever | format_docs}
                | prompt
                | llm
                | StrOutputParser()
            )
            # Queries for the report
            reports = [
                "Introduction of " + company_name,
                "Define the primary industry "
                + company_name
                + " operates in, outlining its size, growth trajectory, and key players",
                company_name
                + "'s target market, including demographic information such as age, gender, income level",
                "Pinpoint the major trends and emerging technologies reshaping this industry, assessing how "
                + company_name
                + " adapts and leverages them strategically",
                company_name
                + "'s product offerings, pricing strategies, and marketing efforts against its key competitors",
                company_name
                + "'s financial performance over recent years, focusing on revenue, profitability, and investment returns.",
                "the primary cost drivers for "
                + company_name
                + ", exploring potential strategies for optimizing its cost structure and enhancing profitability",
                company_name
                + "'s sales strategy, including its sales processes, distribution channels, and sales force",
                "Conduct a SWOT analysis to identify the "
                + company_name
                + "'s strengths, weaknesses, opportunities, and threats",
            ]
            res = []
            chunk_size = 1
            for i in range(0, len(reports), chunk_size):
                chunk = reports[i:i+chunk_size]
                for questions in chunk:
                    res.append(remove_markdown_symbols(rag_chain.invoke(questions)))
            
            file_name=company_name+"_research.txt"
            file = open(file_name, 'w', encoding='utf-8')
            for query, item in zip(reports, res):
                file.write("%s\n" % query)
                file.write("%s\n" % item)
            file.close()

            print("Going to generate PDF")
            output_file=company_name+"_Product_Research.pdf"
            #pdf_data = text_to_pdf(file_name,output_file)
            text_to_pdf(reports, res, company_name)
            print("PDF Generated")

            pdf_file_path = './'+output_file
            with open(pdf_file_path, "rb") as f:
                pdf_file_data = f.read()


            st.subheader("Download PDF:")
            st.download_button(
                label="Download PDF",
                data=pdf_file_data,  # Use the read data directly
                file_name=output_file
            )

if __name__ == "__main__":
    main()