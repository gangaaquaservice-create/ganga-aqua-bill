import streamlit as st
from fpdf import FPDF

st.set_page_config(
    page_title="Ganga Aqua Service - Cash Memo",
    layout="centered"
)

# 1. INITIALIZE SESSION STATE FIRST
if "items" not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = [
        {"qty": 3, "rate": 150, "description": "1 litr BISLERI Mineral water"},
        {"qty": 3, "rate": 210, "description": "500ml. BISLERI Mineral water"},
        {"qty": 3, "rate": 250, "description": "200ml BISLERI Mineral water"}
    ]

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
st.markdown("### Bill Items")

# Render bill item fields
for i, item in enumerate(st.session_state.items):
    col1, col2, col3, col4 = st.columns([1, 1, 3, 1])

    with col1:
        item["qty"] = st.number_input(
            "Qty",
            min_value=0,
            value=item["qty"],
            key=f"qty_{i}"
        )

    with col2:
        item["rate"] = st.number_input(
            "Rate",
            min_value=0,
            value=item["rate"],
            key=f"rate_{i}"
        )

    with col3:
        item["description"] = st.text_input(
            "Description",
            value=item["description"],
            key=f"description_{i}"
        )

    with col4:
        total = item["qty"] * item["rate"]
        st.write(f"₹{total}")

# Add new item button
if st.button("➕ Add Item"):
    st.session_state.items.append(
        {"qty": 1, "rate": 0, "description": ""}
    )
    st.rerun()

# Grand Total Calculation
grand_total = sum(
    item["qty"] * item["rate"]
    for item in st.session_state.items
)

# ============================================================
# AMOUNT IN WORDS
# ============================================================

def number_to_words(n):
    ones = [
        "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
        "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
        "Seventeen", "Eighteen", "Nineteen"
    ]

    tens = [
        "", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"
    ]

    def two_digits(num):
        if num < 20:
            return ones[num]
        return tens[num // 10] + (" " + ones[num % 10] if num % 10 else "")

    def three_digits(num):
        if num < 100:
            return two_digits(num)
        return ones[num // 100] + " Hundred" + (" " + two_digits(num % 100) if num % 100 else "")

    if n == 0:
        return "Zero"

    words = []

    crore = n // 10000000
    n = n % 10000000

    lakh = n // 100000
    n = n % 100000

    thousand = n // 1000
    n = n % 1000

    if crore:
        words.append(three_digits(crore) + " Crore")
    if lakh:
        words.append(three_digits(lakh) + " Lakh")
    if thousand:
        words.append(three_digits(thousand) + " Thousand")
    if n:
        words.append(three_digits(n))

    return " ".join(words)

amount_words = "Rupees " + number_to_words(int(grand_total)) + " Only"

# ============================================================
# FUNCTION TO GENERATE PDF
# ============================================================

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()

    # Business Header
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(190, 7, "GANGA AQUA SERVICE", ln=True, align="C")

    pdf.set_font("Helvetica", size=9)
    pdf.cell(190, 5, "'Aganda' nivas,near mangalwar bazar,", ln=True, align="C")
    pdf.cell(190, 5, "Old kupwad road,sangli 416416", ln=True, align="C")
    pdf.cell(190, 5, "Mob no.7387 255834", ln=True, align="C")

    pdf.set_font("Helvetica", style="BU", size=11)
    pdf.cell(190, 7, "CASH MEMO", ln=True, align="C")
    pdf.ln(3)

    # Meta Information
    pdf.set_font("Helvetica", size=10)
    pdf.cell(25, 6, f"Sr No {sr_no}", align="L")
    pdf.cell(120, 6, f"To,{customer}", align="L")
    pdf.cell(45, 6, f"Date: {date}", align="R", ln=True)
    pdf.ln(2)

    # Table Header
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.cell(25, 8, "QUANTITY", border=1, align="C")
    pdf.cell(25, 8, "RATE", border=1, align="C")
    pdf.cell(100, 8, "DESCRIPTION", border=1, align="C")
    pdf.cell(40, 8, "TOTAL", border=1, align="C")
    pdf.ln()

    # Dynamic Items
    pdf.set_font("Helvetica", size=10)
    items_data = [
        (
            f"{item['qty']:02d}",
            str(item["rate"]),
            item["description"],
            str(item["qty"] * item["rate"])
        )
        for item in st.session_state.items
    ]

    for q, r, desc, tot in items_data:
        pdf.cell(25, 10, q, border="LR", align="C")
        pdf.cell(25, 10, r, border="R", align="C")
        pdf.cell(100, 10, f" {desc}", border="R", align="L")
        pdf.cell(40, 10, tot, border="R", align="C")
        pdf.ln()

    # Spacer Rows
    spacer_count = max(1, 8 - len(items_data))
    for _ in range(spacer_count):
        pdf.cell(25, 10, "", border="LR")
        pdf.cell(25, 10, "", border="R")
        pdf.cell(100, 10, "", border="R")
        pdf.cell(40, 10, "", border="R")
        pdf.ln()

    pdf.cell(190, 0, "", border="T", ln=True)

    # Footer
    pdf.set_font("Helvetica", size=9)
    pdf.cell(150, 12, f"Amount in words: {amount_words}", border=1, align="L")

    pdf.set_font("Helvetica", style="B", size=10)
    pdf.cell(40, 12, f"G.TOTAL: {grand_total}/-", border=1, align="C", ln=True)

    # Signature
    pdf.ln(8)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(150, 8, "", border=0)
    pdf.cell(40, 8, "SIGN : __________________", border=0, align="C")

    return bytes(pdf.output())

# ============================================================
# STREAMLIT UI & DOWNLOAD BUTTON
# ============================================================

st.markdown("---")
st.markdown(f"### **Grand Total: ₹{grand_total}**")

st.download_button(
    label="Download PDF Bill",
    data=generate_pdf(),
    file_name=f"Bill_Sr_{sr_no}.pdf",
    mime="application/pdf"
)
