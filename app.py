import streamlit as st
from fpdf import FPDF

st.set_page_config(
    page_title="Ganga Aqua Service - Cash Memo",
    layout="centered"
)

st.title("Ganga Aqua Service")
st.subheader("Cash Memo Generator")

# Inputs Header
sr_no = st.text_input("Sr No", "19")
date = st.text_input("Date", "03/09/26")
customer = st.text_input(
    "Customer Name",
    "Karmaveer Bhaurao Patil Nagari Patsanstha,Sangli"
)

st.markdown("---")

# Item Inputs
col1, col2 = st.columns(2)

with col1:
    qty1 = st.number_input("1L Bisleri Qty", min_value=0, value=3)
    qty2 = st.number_input("500ml Bisleri Qty", min_value=0, value=3)
    qty3 = st.number_input("200ml Bisleri Qty", min_value=0, value=3)

with col2:
    rate1 = st.number_input("1L Rate (₹)", min_value=0, value=150)
    rate2 = st.number_input("500ml Rate (₹)", min_value=0, value=210)
    rate3 = st.number_input("200ml Rate (₹)", min_value=0, value=250)

# Calculations
t1 = qty1 * rate1
t2 = qty2 * rate2
t3 = qty3 * rate3

grand_total = t1 + t2 + t3


# Function to generate PDF layout
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", size=10)

    # Border
    pdf.rect(10, 10, 190, 260)

    # Business Header
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(
        190, 7,
        "GANGA AQUA SERVICE",
        ln=True,
        align="C"
    )

    pdf.set_font("Helvetica", size=9)

    pdf.cell(
        190, 5,
        "'Aganda' nivas,near mangalwar bazar,",
        ln=True,
        align="C"
    )

    pdf.cell(
        190, 5,
        "Old kupwad road,sangli 416416",
        ln=True,
        align="C"
    )

    pdf.cell(
        190, 5,
        "Mob no.7387 255834",
        ln=True,
        align="C"
    )

    pdf.set_font("Helvetica", style="BU", size=11)

    pdf.cell(
        190, 7,
        "CASH MEMO",
        ln=True,
        align="C"
    )

    pdf.ln(3)

    # Meta Information
    pdf.set_font("Helvetica", size=10)

    pdf.cell(
        25, 6,
        f"Sr No {sr_no}",
        align="L"
    )

    pdf.cell(
        120, 6,
        f"To,{customer}",
        align="L"
    )

    pdf.cell(
        45, 6,
        f"Date: {date}",
        align="R",
        ln=True
    )

    pdf.ln(2)

    # Table Header
    pdf.set_font("Helvetica", style="B", size=10)

    pdf.cell(
        25, 8,
        "QUANTITY",
        border=1,
        align="C"
    )

    pdf.cell(
        25, 8,
        "RATE",
        border=1,
        align="C"
    )

    pdf.cell(
        100, 8,
        "DESCRIPTION",
        border=1,
        align="C"
    )

    pdf.cell(
        40, 8,
        "TOTAL",
        border=1,
        align="C"
    )

    pdf.ln()

    # Items Data
    pdf.set_font("Helvetica", size=10)

    items = [
        (
            f"{qty1:02d}",
            str(rate1),
            "1 litr BISLERI Mineral water",
            str(t1)
        ),
        (
            f"{qty2:02d}",
            str(rate2),
            "500ml. BISLERI Mineral water",
            str(t2)
        ),
        (
            f"{qty3:02d}",
            str(rate3),
            "200ml BISLERI Mineral water",
            str(t3)
        )
    ]

    for q, r, desc, tot in items:
        pdf.cell(
            25, 10,
            q,
            border="LR",
            align="C"
        )

        pdf.cell(
            25, 10,
            r,
            border="R",
            align="C"
        )

        pdf.cell(
            100, 10,
            f" {desc}",
            border="R",
            align="L"
        )

        pdf.cell(
            40, 10,
            tot,
            border="R",
            align="C"
        )

        pdf.ln()

    # Spacer rows for vertical length
    for _ in range(8):
        pdf.cell(
            25, 10,
            "",
            border="LR"
        )

        pdf.cell(
            25, 10,
            "",
            border="R"
        )

        pdf.cell(
            100, 10,
            "",
            border="R"
        )

        pdf.cell(
            40, 10,
            "",
            border="R"
        )

        pdf.ln()

    pdf.cell(
        190, 0,
        "",
        border="T",
        ln=True
    )

    # Footer Section
    pdf.cell(
        115, 12,
        "Amount in words: Total calculated amount",
        border=1,
        align="L"
    )

    pdf.cell(
        35, 12,
        "G.TOTAL:\nSIGN :",
        border=1,
        align="L"
    )

    pdf.set_font(
        "Helvetica",
        style="B",
        size=11
    )

    pdf.cell(
        40, 12,
        f"{grand_total}/-",
        border=1,
        align="C"
    )

    return bytes(pdf.output())


# PDF Button
st.markdown("---")

st.markdown(
    f"### **Grand Total: ₹{grand_total}**"
)

st.download_button(
    label="Download PDF Bill",
    data=generate_pdf(),
    file_name=f"Bill_Sr_{sr_no}.pdf",
    mime="application/pdf"
)
