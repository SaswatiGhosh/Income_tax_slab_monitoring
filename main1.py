import pdfkit
import pdfplumber
import requests
import re

path_wkthmltopdf = r"C:\Program Files\wkhtmltox\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

res = requests.get(
    "https://www.incometax.gov.in/iec/foportal/help/individual/return-applicable-1"
).text

filename = "income_tax_page.html"

# 1. Remove tags that load or execute external resources
res = re.sub(r"<script[^>]*>.*?</script>", "", res, flags=re.IGNORECASE | re.DOTALL)
res = re.sub(r"<iframe[^>]*>.*?</iframe>", "", res, flags=re.IGNORECASE | re.DOTALL)
res = re.sub(r"<noscript[^>]*>.*?</noscript>", "", res, flags=re.IGNORECASE | re.DOTALL)
res = re.sub(r"<object[^>]*>.*?</object>", "", res, flags=re.IGNORECASE | re.DOTALL)
res = re.sub(r"<embed[^>]*>.*?</embed>", "", res, flags=re.IGNORECASE | re.DOTALL)
res = re.sub(r"<source[^>]*>.*?</source>", "", res, flags=re.IGNORECASE | re.DOTALL)
res = re.sub(r"<video[^>]*>.*?</video>", "", res, flags=re.IGNORECASE | re.DOTALL)
res = re.sub(r"<audio[^>]*>.*?</audio>", "", res, flags=re.IGNORECASE | re.DOTALL)

# 2. Remove self-closing resource tags
res = re.sub(r"<link[^>]*?>", "", res, flags=re.IGNORECASE)
res = re.sub(r"<meta[^>]*?>", "", res, flags=re.IGNORECASE)
res = re.sub(r"<img[^>]*?>", "", res, flags=re.IGNORECASE)

# 3. Remove problematic attributes (href, src, JS events, etc.)
res = re.sub(
    r'\s+(href|src|srcset|data-src|prefix)\s*=\s*["\'][^"\']*["\']',
    "",
    res,
    flags=re.IGNORECASE,
)
res = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', "", res, flags=re.IGNORECASE)

with open(filename, "w", encoding="utf-8") as f:
    f.write(res)
print(f"res file '{filename}' created successfully.")

# print(res)
options = {"load-error-handling": "ignore", "load-media-error-handling": "ignore"}
url = "https://www.incometax.gov.in/iec/foportal/help/individual/return-applicable-1"
output_pdf = "income_tax_page.pdf"
# pdfkit.from_url(url, output_pdf, configuration=config, options=options)
pdfkit.from_file(filename, output_pdf, configuration=config)


with pdfplumber.open(output_pdf) as pdf:
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    print(text)

    tables = first_page.extract_tables()
    l = []
    for table in tables:
        for row in table:
            print(row)
