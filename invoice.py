from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import datetime

app = Flask(__name__)

TAX = 18


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    customer = request.form["customer"]

    products = request.form.getlist("product")
    quantities = request.form.getlist("quantity")
    prices = request.form.getlist("price")

    subtotal = 0

    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    filename = f"invoices/{customer}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    c.setFont("Helvetica-Bold", 24)
    c.drawString(220, 800, "INVOICE")

    c.setFont("Helvetica", 12)
    c.drawString(40, 760, f"Customer : {customer}")
    c.drawString(40, 740, f"Date : {datetime.now().strftime('%d-%m-%Y')}")

    y = 690

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Product")
    c.drawString(250, y, "Qty")
    c.drawString(330, y, "Price")
    c.drawString(430, y, "Total")

    y -= 20

    c.line(40, y + 10, 520, y + 10)

    c.setFont("Helvetica", 12)

    for p, q, pr in zip(products, quantities, prices):

        if p.strip() == "":
            continue

        total = int(q) * float(pr)
        subtotal += total

        c.drawString(40, y, p)
        c.drawString(250, y, q)
        c.drawString(330, y, f"₹{pr}")
        c.drawString(430, y, f"₹{total:.2f}")

        y -= 25

    tax = subtotal * TAX / 100
    grand = subtotal + tax

    y -= 20

    c.drawString(300, y, f"Subtotal : ₹{subtotal:.2f}")
    y -= 20
    c.drawString(300, y, f"GST ({TAX}%) : ₹{tax:.2f}")
    y -= 20
    c.drawString(300, y, f"Grand Total : ₹{grand:.2f}")

    c.save()

    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)