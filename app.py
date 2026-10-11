import html

import streamlit as st
import fitz
from analyzer import ReasearchParagraphAnalysis, analyze_paper


st.set_page_config(
    page_title="ResearchMate AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #FAFAF9;
        color: #1C1917;
    }

    .block-container {
        max-width: 1040px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #1C1917;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 1.8rem;
        margin-bottom: 0.15rem;
    }

    h2 {
        font-size: 1.35rem;
        margin-top: 1.5rem;
    }

    h3 {
        font-size: 1.05rem;
        margin-top: 1.25rem;
    }

    p, li {
        color: #292524;
        line-height: 1.65;
    }

    [data-testid="stCaptionContainer"] {
        color: #78716C;
    }

    [data-testid="stFileUploader"] [data-testid="stWidgetLabel"] {
        color: #1C1917;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF;
        border: 1px dashed #D6D3D1 !important;
        border-radius: 5px;
        color: #1C1917;
    }

    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] small {
        color: #57534E;
    }

    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {
        min-height: 2.5rem;
        background: #F5F5F4;
        border: 1px solid #D6D3D1;
        border-radius: 5px;
        color: #1C1917;
    }

    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]:hover {
        background: #E7E5E4;
        border-color: #A8A29E;
        color: #1C1917;
    }

    [data-testid="stFileChip"] {
        background: #F5F5F4;
        border: 1px solid #E7E5E4;
        border-radius: 5px;
        color: #1C1917;
    }

    [data-testid="stFileChipName"] {
        color: #1C1917;
    }

    [data-testid="stFileChipDeleteBtn"] {
        color: #57534E;
    }

    [data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-borderlessIcon"] {
        color: #57534E;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E7E5E4;
        border-radius: 6px;
        padding: 0.75rem 1rem;
    }

    .stButton > button {
        min-height: 2.75rem;
        border-radius: 5px;
        font-weight: 500;
    }

    .stButton > button[kind="primary"] {
        background: #4F46E5;
        border-color: #4F46E5;
        color: #FFFFFF;
    }

    .stButton > button[kind="primary"] p {
        color: #FFFFFF;
    }

    .stButton > button[kind="primary"]:hover {
        background: #4338CA;
        border-color: #4338CA;
    }

    .stButton > button[kind="primary"]:disabled {
        background: #E7E5E4;
        border-color: #D6D3D1;
        color: #57534E;
    }

    .stButton > button[kind="primary"]:disabled p {
        color: #57534E;
    }

    .stButton > button:focus-visible,
    [data-testid="stTextInput"] input:focus-visible,
    [data-testid="stTabs"] [role="tab"]:focus-visible,
    [data-testid="stFileUploaderDropzone"] button:focus-visible {
        outline: 3px solid #A5B4FC;
        outline-offset: 2px;
    }

    [data-testid="stTextInput"] [data-testid="stTextInputRootElement"] {
        background: #FFFFFF;
        border: 1px solid #D6D3D1;
        border-radius: 5px;
    }

    [data-testid="stTextInput"] [data-testid="stTextInputRootElement"]:focus-within {
        border-color: #4F46E5;
        box-shadow: 0 0 0 1px #4F46E5;
    }

    [data-testid="stTextInput"] [data-testid="stTextInputRootElement"]:has(input:disabled) {
        background: #F5F5F4;
    }

    [data-testid="stTextInput"] [data-testid="stTextInputField"] {
        background: transparent;
        color: #1C1917;
    }

    [data-testid="stTextInput"] [data-testid="stTextInputField"]::placeholder {
        color: #78716C;
        opacity: 1;
    }

    [data-testid="stTextInput"] [data-testid="stTextInputField"]:disabled {
        color: #57534E;
    }

    [data-testid="stTabs"] [role="tab"] {
        min-height: 2.75rem;
        padding: 0.55rem 0.9rem;
        color: #57534E;
        font-size: 1rem;
        font-weight: 500;
    }

    [data-testid="stTabs"] [role="tab"] p {
        color: inherit;
        font-size: inherit;
        font-weight: inherit;
    }

    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: #4338CA;
        font-weight: 600;
    }

    [data-testid="stTabs"] [role="tab"][aria-selected="true"] > .react-aria-SelectionIndicator {
        background-color: #4F46E5 !important;
        transition: none !important;
    }

    hr {
        border-color: #E7E5E4;
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 1rem 1.5rem;
        }

        [data-testid="stTabs"] [role="tab"] {
            padding-right: 0.65rem;
            padding-left: 0.65rem;
            font-size: 0.95rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("ResearchMate AI")
st.caption("Understand research papers more efficiently.")

st.subheader("Research paper")
st.write("Upload a PDF to extract its text, generate a structured summary, or ask a question.")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    help="Upload a text-based research paper in PDF format.",
)

paper_text = ""
page_count = 0
extraction_error = None

if uploaded_file is not None:
    try:
        with fitz.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf",
        ) as pdf:
            page_count = len(pdf)
            pages_text = [
                page.get_text("text")
                for page in pdf
            ]
        paper_text = "\n".join(
            text for text in pages_text if isinstance(text, str)
        )
    except Exception as error:
        extraction_error = error
        paper_text = ""
        page_count = 0

    if extraction_error is not None:
        st.error(f"Could not process this PDF: {extraction_error}")
    elif not paper_text.strip():
        st.warning(
            f"{uploaded_file.name} was opened, but no readable text was found. "
            "The PDF may contain scanned pages that require OCR."
        )
    else:
        st.success(f"Text extracted from {uploaded_file.name}")

        metric_pages, metric_words, metric_characters = st.columns(3)
        metric_pages.metric("Pages", f"{page_count:,}")
        metric_words.metric("Words", f"{len(paper_text.split()):,}")
        metric_characters.metric("Characters", f"{len(paper_text):,}")

        with st.expander("Preview extracted text"):
            preview_text = html.escape(paper_text[:5000])
            st.markdown(
                f"""
                <div style="
                    max-height: 24rem;
                    overflow-y: auto;
                    padding: 1rem;
                    background: #FFFFFF;
                    color: #1C1917;
                    border: 1px solid #E7E5E4;
                    border-radius: 5px;
                    font-family: inherit;
                    font-size: 0.95rem;
                    line-height: 1.65;
                    white-space: pre-wrap;
                    overflow-wrap: anywhere;
                ">{preview_text}</div>
                """,
                unsafe_allow_html=True,
            )
            if len(paper_text) > 5000:
                st.caption("Preview limited to the first 5,000 characters.")

st.subheader("Analysis")
summary_tab, question_tab = st.tabs(
    ["Summarize paper", "Ask a question"]
)
document_ready = bool(paper_text.strip())

with summary_tab:
    st.write(
        "Create a structured overview of the paper's purpose, methods, "
        "findings, limitations, and future directions."
    )
    summary_clicked = st.button(
        "Generate summary",
        key="summary_button",
        type="primary",
        disabled=not document_ready,
    )

    if summary_clicked:
        try:
            with st.spinner("Analyzing the paper..."):
                result = analyze_paper(
                    paper_text=paper_text,
                    mode="summary",
                )

            if not isinstance(result, ReasearchParagraphAnalysis):
                st.error("The analyzer returned an unexpected summary format.")
            else:
                st.divider()
                st.subheader(result.title)

                st.markdown("#### Research domain")
                st.write(result.research_domain)

                st.markdown("#### Objective")
                st.write(result.objective)

                st.markdown("#### Methodology")
                st.write(result.methodology)

                st.markdown("#### Key findings")
                for finding in result.key_findings:
                    st.markdown(f"- {finding}")

                st.markdown("#### Limitations")
                for limitation in result.limitations:
                    st.markdown(f"- {limitation}")

                st.markdown("#### Future research directions")
                for direction in result.future_directions:
                    st.markdown(f"- {direction}")

                if result.research_author:
                    st.markdown("#### Authors")
                    st.write(result.research_author)
        except Exception as error:
            st.error(f"Could not generate the summary: {error}")

with question_tab:
    st.write("Ask a question about the uploaded paper.")
    question = st.text_input(
        "Question about the paper",
        placeholder="For example: What methodology did the researchers use?",
        key="research_question",
        disabled=not document_ready,
    )
    answer_clicked = st.button(
        "Generate answer",
        key="answer_button",
        type="primary",
        disabled=not document_ready,
    )

    if answer_clicked:
        if not question.strip():
            st.warning("Enter a question about the paper first.")
        else:
            try:
                with st.spinner("Finding an answer in the paper..."):
                    answer = analyze_paper(
                        paper_text=paper_text,
                        mode="qa",
                        question=question,
                    )

                st.markdown("#### Your question")
                st.write(question)
                st.markdown("#### Answer")
                st.write(answer)
                st.caption(
                    "AI-generated answers can be incomplete. Verify important "
                    "claims against the source paper."
                )
            except Exception as error:
                st.error(f"Could not generate an answer: {error}")
