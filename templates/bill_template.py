import os
from datetime import datetime
from tkinter import messagebox as mb

import customtkinter as ctk
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from config import bills_path


class BillPreviewWindow:
    """A top-level window to display and save bill as PDF"""

    def __init__(self, parent, bill_data, user_data):
        self.parent = parent
        self.bill_data = bill_data
        self.user_data = user_data

        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Bill Preview - {bill_data.bill_no}")
        self.window.geometry("800x600")
        self.window.grab_set()

        self.create_ui()
        self.pdf_path = None

    def create_ui(self):
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        header_label = ctk.CTkLabel(
            main_frame,
            text="Bill Preview",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header_label.pack(pady=10)

        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(info_frame, text=f"Bill Number: {self.bill_data.bill_no}", font=ctk.CTkFont(size=14)).pack(
            anchor="w", padx=10, pady=2)
        ctk.CTkLabel(info_frame, text=f"Customer: {self.bill_data.customer_name}", font=ctk.CTkFont(size=14)).pack(
            anchor="w", padx=10, pady=2)
        ctk.CTkLabel(info_frame, text=f"Phone: {self.bill_data.customer_phone}", font=ctk.CTkFont(size=14)).pack(
            anchor="w", padx=10, pady=2)

        timestamp = self.bill_data.timestamp
        date_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if isinstance(timestamp, datetime) else str(timestamp)
        ctk.CTkLabel(info_frame, text=f"Date: {date_str}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=2)

        preview_label = ctk.CTkLabel(
            main_frame,
            text="PDF Preview will appear here\n\n(In a production app, this would display the actual PDF content)",
            font=ctk.CTkFont(size=16),
            height=300
        )
        preview_label.pack(fill="both", expand=True, padx=10, pady=10)

        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        save_btn = ctk.CTkButton(buttons_frame, text="Save as PDF", command=self.save_pdf, width=150, height=40,
                                 font=ctk.CTkFont(size=14))
        save_btn.pack(side="left", padx=10, pady=10)

        print_btn = ctk.CTkButton(buttons_frame, text="Print Bill", command=self.print_pdf, width=150, height=40,
                                  font=ctk.CTkFont(size=14))
        print_btn.pack(side="left", padx=10, pady=10)

        close_btn = ctk.CTkButton(buttons_frame, text="Close", command=self.window.destroy, width=150, height=40,
                                  font=ctk.CTkFont(size=14))
        close_btn.pack(side="right", padx=10, pady=10)

    def generate_pdf(self, output_path):
        doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CenteredTitle', parent=styles['Heading1'], alignment=1, fontSize=18, spaceAfter=6)
        normal_style = styles['Normal']
        address_style = ParagraphStyle('Address', parent=normal_style, fontSize=10, alignment=1)
        thank_you_style = ParagraphStyle('ThankYou', parent=normal_style, fontSize=12, alignment=1, spaceBefore=20)

        story = []
        story.append(Paragraph(self.user_data['shop_name'].upper(), title_style))
        story.append(Paragraph(self.user_data['shop_address'].capitalize(), address_style))
        story.append(Paragraph(f"Email: {self.user_data['email']}", address_style))
        story.append(Spacer(1, 0.25 * inch))

        header_data = [
            ["Bill No:", self.bill_data.bill_no, "Date:",
             datetime.now().strftime("%Y-%m-%d %H:%M:%S") if isinstance(self.bill_data.timestamp, datetime) else str(
                 self.bill_data.timestamp)],
            ["Customer:", self.bill_data.customer_name, "Phone:", self.bill_data.customer_phone]
        ]

        header_table = Table(header_data, colWidths=[1.2 * inch, 1.8 * inch, 1.2 * inch, 1.8 * inch])
        header_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (2, 0), (2, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.25 * inch))

        products_data = [["Sr.", "Product Name", "Price", "Qty", "Total"]]
        for i, item in enumerate(self.bill_data.items, 1):
            products_data.append([
                i,
                item.product_name,
                f"₹{item.price:.2f}",
                item.quantity,
                f"₹{item.total:.2f}"
            ])

        products_table = Table(products_data, colWidths=[0.5 * inch, 3.0 * inch, 1.0 * inch, 0.5 * inch, 1.0 * inch])
        products_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (2, 1), (4, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ]))
        story.append(products_table)
        story.append(Spacer(1, 0.25 * inch))

        summary_data = []
        if self.bill_data.medical_total > 0:
            summary_data.append(["Medical Items Total:", f"₹{self.bill_data.medical_total:.2f}"])
        if self.bill_data.grocery_total > 0:
            summary_data.append(["Grocery Items Total:", f"₹{self.bill_data.grocery_total:.2f}"])
        if self.bill_data.drinks_total > 0:
            summary_data.append(["Cold Drinks Total:", f"₹{self.bill_data.drinks_total:.2f}"])
        if self.bill_data.medical_tax > 0:
            summary_data.append(["Medical Tax (5%):", f"₹{self.bill_data.medical_tax:.2f}"])
        if self.bill_data.grocery_tax > 0:
            summary_data.append(["Grocery Tax (1%):", f"₹{self.bill_data.grocery_tax:.2f}"])
        if self.bill_data.drinks_tax > 0:
            summary_data.append(["Drinks Tax (10%):", f"₹{self.bill_data.drinks_tax:.2f}"])

        summary_data.append([" ", " "])
        summary_data.append(["Total Bill Amount:", f"₹{self.bill_data.total_amount:.2f}"])

        summary_table = Table(summary_data, colWidths=[4.0 * inch, 2.0 * inch])
        summary_table.setStyle(TableStyle([
            ('GRID', (0, -1), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(summary_table)
        story.append(Paragraph("Thank you for shopping with us!", thank_you_style))

        doc.build(story)
        return output_path

    def save_pdf(self):
        try:
            bills_dir = bills_path()
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = os.path.join(bills_dir, f"Bill_{self.bill_data.bill_no}_{timestamp}.pdf")
            self.pdf_path = self.generate_pdf(filename)
            mb.showinfo("Success", f"Bill saved as PDF at {filename}")
            try:
                if os.name == 'nt':
                    os.startfile(filename)
                else:
                    os.system(f'xdg-open "{filename}"')
            except:
                pass
        except Exception as e:
            mb.showerror("Error", f"Failed to save PDF: {str(e)}")

    def print_pdf(self):
        try:
            if not self.pdf_path:
                temp_pdf = f"temp_bill_{self.bill_data.bill_no}.pdf"
                self.pdf_path = self.generate_pdf(temp_pdf)
            if os.name == 'nt':
                os.system(f'start /min print "{self.pdf_path}"')
            else:
                os.system(f'lpr "{self.pdf_path}"')
            mb.showinfo("Success", "Bill sent to printer")
        except Exception as e:
            mb.showerror("Error", f"Failed to print bill: {str(e)}")
