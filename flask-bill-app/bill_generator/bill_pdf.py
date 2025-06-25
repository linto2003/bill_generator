from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from num2words import num2words
from reportlab.lib.units import inch

class Product:
    def __init__(self, name, hsn, quantity, unit, price_per_unit):
        self.name = name
        self.hsn = hsn
        self.quantity = quantity
        self.unit = unit
        self.price_per_unit = price_per_unit
        self.total_price = quantity * price_per_unit

def add_logo_and_company_name(logo_path, company_info, styles):
    logo = Image(logo_path, width=1.2*inch, height=1.2*inch)
    
    company_text = Paragraph(
        f"<b>{company_info['name']}</b><br/>{company_info['address']}<br/>"
        f"GSTIN: {company_info['gstin']}<br/>Contact: {company_info['contact']}", 
        styles["Normal"]
    )
    
    logo_table = Table([[logo, company_text]], colWidths=[1.5*inch, 4.5*inch])
    logo_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10
    ]))
    
    return logo_table

def create_bill_pdf(filename, products, company_info, client_info, invoice_details, logo_path):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()
    
    logo_table = add_logo_and_company_name(logo_path, company_info, styles)
    elements.append(logo_table)
    elements.append(Spacer(1, 20))

    client_paragraph = Paragraph(
        f"<b>{client_info['name']}</b><br/>{client_info['address']}<br/>GSTIN: {client_info['gstin']}",
        styles["Normal"]
    )
    invoice_paragraph = Paragraph(
        f"<b>Invoice No:</b> {invoice_details['invoice_no']}<br/><b>Date:</b> {invoice_details['date']}", 
        styles["Normal"]
    )

    elements.extend([client_paragraph, Spacer(1, 10), invoice_paragraph, Spacer(1, 20)])

    data = [["Sr No.", "Particulars", "HSN", "Qty", "Unit", "Rate", "Amount"]]
    total_taxable = 0
    for i, product in enumerate(products, start=1):
        data.append([
            i,
            product.name,
            product.hsn,
            f"{product.quantity} {product.unit}",
            product.unit,
            f"{product.price_per_unit:.2f}",
            f"{product.total_price:.2f}"
        ])
        total_taxable += product.total_price

    cgst = sgst = total_taxable * 0.09
    total_amount = total_taxable + cgst + sgst
    amount_in_words = num2words(total_amount, lang='en').title() + " Only"

    data.extend([
        ["", "", "", "", "", "Total Taxable Amount", f"{total_taxable:.2f}"],
        ["", "", "", "", "", "CGST 9%", f"{cgst:.2f}"],
        ["", "", "", "", "", "SGST 9%", f"{sgst:.2f}"],
        ["", "", "", "", "", "Total Amount", f"{total_amount:.2f}"]
    ])
    
    table = Table(data, colWidths=[0.5*inch, 2*inch, 1*inch, 0.7*inch, 0.7*inch, 1.2*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Amount in words: {amount_in_words}", styles["Normal"]))
    elements.append(Spacer(1, 24))

    declaration = Paragraph(
        "We declare that this invoice shows the actual price of the goods described and that all particulars are true and correct.",
        styles["Normal"]
    )
    elements.append(declaration)
    elements.append(Spacer(1, 48))
    elements.append(Paragraph("For " + company_info["name"], styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Authorized Signatory", styles["Normal"]))

    doc.build(elements)