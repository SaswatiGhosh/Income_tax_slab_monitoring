import pdfkit
import pdfplumber
import requests

path_wkthmltopdf = r"C:\Program Files\wkhtmltox\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

res = requests.get(
    "https://www.incometax.gov.in/iec/foportal/help/individual/return-applicable-1"
).text
print(res)

url = "https://www.incometax.gov.in/iec/foportal/help/individual/return-applicable-1"
output_pdf = "income_tax_page.pdf"
# pdfkit.from_url(url, output_pdf, configuration=config, options=options)
pdfkit.from_string(res, "output.pdf", configuration=config)


with pdfplumber.open(output_pdf) as pdf:
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    print(text)

    tables = first_page.extract_tables()
    l = []
    for table in tables:
        for row in table:
            print(row)
