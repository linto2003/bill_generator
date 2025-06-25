# Flask Bill Application

This project is a Flask web application that generates styled bill PDFs. It allows users to input company, client, and product information, and then generates a PDF bill with a logo and formatted details.

## Project Structure

```
flask-bill-app
├── app.py                  # Entry point of the Flask application
├── bill_generator
│   ├── __init__.py        # Initializes the bill_generator package
│   └── bill_pdf.py        # Contains logic for generating the styled bill PDF
├── static
│   └── logo.png           # Logo image used in the bill PDF
├── templates
│   └── index.html         # HTML template for the main page
├── requirements.txt        # Lists dependencies for the application
└── README.md               # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd flask-bill-app
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```
   python app.py
   ```

2. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000/`.

3. **Generate a bill**:
   - Fill in the company, client, and product information in the form.
   - Click the "Generate Bill" button to create the PDF.

## Dependencies

- Flask
- ReportLab
- num2words

