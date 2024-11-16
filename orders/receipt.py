import os
import qrcode  # type: ignore
from fpdf import FPDF  # type: ignore
from datetime import datetime
from django.conf import settings
from django.core.files import File

qr_filename = ''


class PDF(FPDF):
    def __init__(self, order, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order

    def set_order_number(self, order_number):
        self.order_number = order_number

    def set_get_order_number(self, get_order_number):
        self.get_order_number = get_order_number

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def header(self):
        # Calculate the image's dimensions to maintain aspect ratio
        image_width = self.w  # Full page width
        image_height = 0  # Dynamically calculate based on aspect ratio

        # Load the image and get its original width and height
        img_path = self.order.get_order_image
        try:
            from PIL import Image
            with Image.open(img_path) as img:
                img_width, img_height = img.size
                aspect_ratio = img_height / img_width
                image_height = image_width * aspect_ratio
        except Exception as e:
            print(f"Error loading image: {e}")
            return

        # Add the image to the PDF (positioned at x=0, y=0 with calculated height)
        self.image(img_path, x=0, y=0, w=image_width, h=image_height)

        # Adjust the y-position to account for the image height
        self.set_y(image_height)

        # Add text below the image
        self.set_font('helvetica', "", 12)
        self.multi_cell(0, 10, f"{self.first_name} {self.last_name}", ln=True)
        self.set_font('helvetica', "B", 14)
        self.multi_cell(0, 10, str(f"No. {self.get_order_number}"), ln=True)
        self.ln(4)
        self.set_font('helvetica', "B", 18)
        self.multi_cell(50, 7, str(self.order.description), ln=True)
        self.ln(4)

    def footer(self):
        self.set_y(-45)
        self.set_font("helvetica", "", 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def generate_receipt(order):
    global qr_filename
    # Create a URL for the QR code
    qr_data = f"{settings.SITE_DOMAIN}orders/order/{order.order_number}/"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Specify the directory for saving the QR code image
    qr_directory = os.path.join(settings.BASE_DIR, 'qrcodes')

    # Create the directory if it doesn't exist
    os.makedirs(qr_directory, exist_ok=True)

    # Save the QR code image
    qr_filename = os.path.join(
        qr_directory, f'qr_{order.get_order_number}.png')
    img.save(qr_filename)

    # Now, read the saved QR code image and save it to the Order model
    with open(qr_filename, 'rb') as qr_code_file:
        order.qr.save(
            f'qr_{order.get_order_number}.png', File(qr_code_file))

    # Creating PDF instance, setting properties, and generating the PDF
    pdf = PDF(order, "P", "mm", "A4")
    pdf.set_first_name(order.first_name)
    pdf.set_last_name(order.last_name)
    pdf.set_order_number(order.order_number)
    pdf.set_get_order_number(order.get_order_number)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf_output = pdf.output()
    return pdf_output
