import fitz

pdf=fitz.open("ResearchMate_AI_Sample_Research_Paper.pdf")

paper_text=""

for page in pdf:
    paper_text+=page.get_text() + "\n"
pdf.close()

print(paper_text)