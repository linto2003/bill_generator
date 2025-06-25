from flask import Blueprint

bill_generator = Blueprint('bill_generator', __name__)

from .bill_pdf import create_bill_pdf, Product, add_logo_and_company_name