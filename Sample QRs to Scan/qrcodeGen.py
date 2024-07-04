import os

import qrcode


def create_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10, 
        border=1, 
    )
    qr.add_data(data)
    qr.make()
    img = qr.make_image(back_color='white')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)


if __name__ == "__main__":

    sample_data = [
    "PRD12345:Organic Green Tea:Beverages:January 15, 2023:January 15, 2024:BATCH67890:1000:Factory 1:ISO 9001:ORD2023001",
    "PRD23456:Almond Milk:Dairy:February 10, 2023:August 10, 2024:BATCH56789:500:Factory 1:USDA Organic:ORD2023002",
    "PRD34567:Dark Chocolate:Confectionery:March 05, 2023:September 05, 2024:BATCH45678:2000:Factory 1:Fair Trade:ORD2023003",
    "PRD45678:Olive Oil:Groceries:April 20, 2023:April 20, 2025:BATCH34567:750:Factory 1:USDA Organic:ORD2023004",
    "PRD56789:Protein Bar:Snacks:May 15, 2023:May 15, 2024:BATCH23456:1200:Factory 2:ISO 22000:ORD2023005",
    "PRD67890:Canned Tuna:Seafood:June 01, 2023:June 01, 2025:BATCH12345:1500:Factory 2:MSC Certified:ORD2023006",
    "PRD78901:Whole Wheat Bread:Bakery:June 10, 2023:July 10, 2024:BATCH34567:800:Factory 2:ISO 22000:ORD2023007",
    "PRD89012:Orange Juice:Beverages:June 14, 2024:December 15, 2024:BATCH45678:1000:Factory 3:HACCP5:ORD2023008",
]

    directory = "./Sample QRs to Scan"

    for index, data in enumerate(sample_data, start=1):
        filename = os.path.join(directory, f"{index}.png")
        create_qr_code(data, filename)
