import os, sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import Color, black

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

INDEX = "158204/2026"
CAPTION_L = ("ROSA DELGADO, individually and on behalf of all others similarly situated,<br/><br/>"
             "&nbsp;&nbsp;&nbsp;&nbsp;Plaintiff,<br/><br/>- against -<br/><br/>"
             "RIVERSIDE TOWER MANAGEMENT LLC,<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;Defendant.")

base = ParagraphStyle("b", fontName="Times-Roman", fontSize=12, leading=18, alignment=TA_JUSTIFY)
center = ParagraphStyle("c", parent=base, alignment=TA_CENTER)
title = ParagraphStyle("t", parent=center, fontName="Times-Bold", fontSize=13, spaceBefore=6, spaceAfter=6)
small = ParagraphStyle("s", parent=base, fontSize=10, leading=13)


def decorate(doc_no, label):
    def draw(c, d):
        c.saveState()
        # top banner
        c.setFillColor(Color(0.85, 0.1, 0.1))
        c.rect(0, letter[1] - 30, letter[0], 30, fill=1, stroke=0)
        c.setFillColor(Color(1, 1, 1))
        c.setFont("Helvetica-Bold", 8.2)
        c.drawCentredString(letter[0] / 2, letter[1] - 19,
                            f"SIMULATED FILING FOR A CLASS PROJECT (Docket Clock demo)  |  Index No. {INDEX}  |  Doc No. {doc_no}  |  NOT FILED IN ANY COURT")
        # diagonal watermark
        c.setFillColor(Color(0.85, 0.1, 0.1, alpha=0.10))
        c.setFont("Helvetica-Bold", 54)
        c.translate(letter[0] / 2, letter[1] / 2)
        c.rotate(40)
        c.drawCentredString(0, 20, "SIMULATED")
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(0, -20, "Fictional case - not a court document")
        c.restoreState()
        c.setFont("Helvetica", 8.5)
        c.setFillColor(black)
        c.drawCentredString(letter[0] / 2, 28, f"{label}  -  page {d.page}  -  fictional parties, counsel and justice")
    return draw


def caption_block(doc_title):
    return [
        Paragraph("SUPREME COURT OF THE STATE OF NEW YORK<br/>COUNTY OF NEW YORK", center),
        Spacer(1, 10),
        Paragraph(CAPTION_L, base),
        Spacer(1, 6),
        Paragraph(f"Index No. {INDEX}", base),
        Spacer(1, 10),
        Paragraph(doc_title, title),
        Spacer(1, 6),
    ]


def build(fname, doc_no, label, doc_title, body):
    path = os.path.join(OUT, fname)
    doc = SimpleDocTemplate(path, pagesize=letter, topMargin=60, bottomMargin=54, leftMargin=72, rightMargin=72,
                            title=f"SIMULATED - {label} - Index No. {INDEX}", author="Docket Clock class demo (fictional)")
    story = caption_block(doc_title) + [Paragraph(p, base) if not p.startswith("<s>") else Paragraph(p[3:], small) for p in body]
    story = [x if not isinstance(x, str) else x for x in story]
    spaced = []
    for x in story:
        spaced.append(x); spaced.append(Spacer(1, 8))
    deco = decorate(doc_no, label)
    doc.build(spaced, onFirstPage=deco, onLaterPages=deco)
    return path


build("Doc01_Summons_and_Complaint_SIMULATED.pdf", 1, "Summons and Verified Class Action Complaint",
      "SUMMONS AND VERIFIED CLASS ACTION COMPLAINT", [
    "<b>TO THE ABOVE-NAMED DEFENDANT:</b> You are hereby summoned to answer the complaint in this action and to serve a copy of your answer on Plaintiff's attorneys within twenty (20) days after service of this summons, exclusive of the day of service, or within thirty (30) days after service is complete if this summons is not personally delivered to you within the State of New York. If you fail to answer, judgment will be taken against you by default for the relief demanded in the complaint.",
    "Plaintiff designates New York County as the place of trial. The basis of venue is the location of the property at issue, 2150 Riverside Drive, New York, New York.",
    "<b>NATURE OF THE ACTION</b>",
    "1. Plaintiff Rosa Delgado brings this action under CPLR Article 9 on behalf of herself and a class of approximately 340 current and former tenants of 2150 Riverside Drive who were charged rents above the lawful regulated amount and who were repeatedly left without adequate heat and hot water during the 2024-2025 and 2025-2026 heating seasons.",
    "2. Defendant Riverside Tower Management LLC is the managing agent of the building and collected the rents at issue.",
    "<b>CLASS ALLEGATIONS (CPLR 901)</b>",
    "3. The class is so numerous that joinder of all members is impracticable. Common questions of law and fact predominate, including whether Defendant's rent registrations were unlawful and whether Defendant failed to maintain heat as required. Plaintiff's claims are typical of the class, and Plaintiff will fairly and adequately protect the interests of the class. A class action is superior to other available methods for adjudicating this controversy.",
    "<b>CAUSES OF ACTION</b>",
    "4. First Cause of Action: rent overcharge. Second Cause of Action: breach of the warranty of habitability (Real Property Law section 235-b). Third Cause of Action: declaratory relief.",
    "<b>WHEREFORE</b>, Plaintiff demands judgment certifying the class, awarding damages in an amount to be determined at trial, and granting costs, attorneys' fees and such other relief as the Court deems just.",
    "Dated: New York, New York, August 17, 2026",
    "HARTWELL &amp; OSEI LLP (fictional), Attorneys for Plaintiff and the Proposed Class",
    "<s>This is a simulated document created for a classroom demonstration. The parties, counsel, court assignment and allegations are fictional.",
])

build("Doc04_Affidavit_of_Service_SIMULATED.pdf", 4, "Affidavit of Service", "AFFIDAVIT OF SERVICE", [
    "STATE OF NEW YORK, COUNTY OF NEW YORK, ss.:",
    "Daniel Reyes (fictional), being duly sworn, deposes and says: I am over 18 years of age, am not a party to this action, and reside in the State of New York.",
    "On <b>August 24, 2026 at 2:15 p.m.</b>, at 410 Park Avenue South, New York, New York, I served the Summons and Verified Class Action Complaint upon Defendant RIVERSIDE TOWER MANAGEMENT LLC by <b>personal delivery</b> to Joanne Whitfield (fictional), managing agent of the Defendant, authorized to accept service on its behalf pursuant to CPLR 311-a.",
    "Description of person served: female, approximately 50 years of age, brown hair.",
    "Sworn to before me on August 27, 2026. [Notary signature block intentionally omitted from simulation]",
    "Filed: August 28, 2026.",
    "<s>This is a simulated document created for a classroom demonstration. All names are fictional.",
])

build("Doc09_Notice_of_Motion_to_Dismiss_SIMULATED.pdf", 9, "Notice of Motion to Dismiss (Mot. Seq. 001)",
      "NOTICE OF MOTION TO DISMISS<br/>(Motion Sequence No. 001)", [
    "PLEASE TAKE NOTICE that, upon the annexed affirmation of Calvin Pell (fictional), dated September 14, 2026, the exhibits thereto, and the accompanying memorandum of law, Defendant Riverside Tower Management LLC will move this Court at the Motion Submission Part, Room 130, 60 Centre Street, New York, New York, on <b>October 2, 2026</b> at 9:30 a.m., or as soon thereafter as counsel may be heard, for an order:",
    "(a) dismissing the complaint pursuant to CPLR 3211(a)(1), on the ground that documentary evidence, namely the building's rent registration records, establishes a defense;",
    "(b) dismissing the complaint pursuant to CPLR 3211(a)(7) for failure to state a cause of action; and",
    "(c) granting such other and further relief as the Court deems just and proper.",
    "PLEASE TAKE FURTHER NOTICE that, pursuant to CPLR 2214(b), answering papers, if any, are required to be served at least seven days before the return date.",
    "Dated: New York, New York, September 14, 2026",
    "BRANNOCK PELL LLP (fictional), Attorneys for Defendant",
    "<s>This is a simulated document created for a classroom demonstration. All names are fictional.",
])

build("Doc21_Decision_Order_Notice_of_Entry_SIMULATED.pdf", 21, "Decision and Order with Notice of Entry",
      "NOTICE OF ENTRY", [
    "PLEASE TAKE NOTICE that the within is a true copy of the Decision and Order of the Hon. Marisol T. Abernathy (fictional) on Motion Sequence No. 001, duly entered in the office of the Clerk of New York County on October 8, 2026, and served on all parties through the e-filing system on <b>October 9, 2026</b>.",
    "Dated: New York, New York, October 9, 2026. HARTWELL &amp; OSEI LLP (fictional), Attorneys for Plaintiff",
    "<b>DECISION AND ORDER ON MOTION</b>",
    "Defendant moves to dismiss the complaint under CPLR 3211(a)(1) and (a)(7). Plaintiff opposes. For the reasons below, the motion is <b>GRANTED IN PART and DENIED IN PART</b>.",
    "The rent registration records submitted by Defendant conclusively establish that the challenged rents for periods before January 1, 2020 fall outside the applicable lookback period. To that extent, the First Cause of Action is dismissed.",
    "Accepting the allegations of the complaint as true and according Plaintiff every favorable inference, the Second and Third Causes of Action adequately allege a failure to provide heat and hot water and a justiciable controversy. The motion is denied as to those claims and as to the remainder of the First Cause of Action.",
    "Accordingly, it is ORDERED that the motion is granted to the extent stated above and otherwise denied; and it is further ORDERED that Defendant shall serve an answer to the remaining claims within the time provided by CPLR 3211(f); and it is further ORDERED that counsel shall appear for a preliminary conference on November 18, 2026.",
    "This constitutes the decision and order of the Court. ENTER: Hon. Marisol T. Abernathy, J.S.C. (fictional)",
    "<s>This is a simulated document created for a classroom demonstration. It was not issued by any court.",
])
print("ok")
