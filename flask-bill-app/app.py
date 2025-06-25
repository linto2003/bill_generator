from flask import Flask, render_template, request, send_file
from bill_generator.bill_pdf import create_bill_pdf
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_info = {
            "name": request.form['company_name'],
            "address": request.form['company_address'],
            "gstin": request.form['company_gstin'],
            "contact": request.form['company_contact']
        }
        
        client_info = {
            "name": request.form['client_name'],
            "address": request.form['client_address'],
            "gstin": request.form['client_gstin']
        }
        
        invoice_details = {
            "invoice_no": request.form['invoice_no'],
            "date": request.form['invoice_date']
        }
        
        products = []
        for i in range(int(request.form['product_count'])):
            product_name = request.form[f'product_name_{i}']
            hsn = request.form[f'product_hsn_{i}']
            quantity = int(request.form[f'product_quantity_{i}'])
            unit = request.form[f'product_unit_{i}']
            price_per_unit = float(request.form[f'product_price_{i}'])
            products.append(Product(product_name, hsn, quantity, unit, price_per_unit))

        logo_path = os.path.join(app.static_folder, 'logo.png')
        pdf_filename = "Styled_Bill_with_Logo.pdf"
        create_bill_pdf(pdf_filename, products, company_info, client_info, invoice_details, logo_path)
        
        return send_file(pdf_filename, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)