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
        
    sample_data = ["12344:Fan:Electronics:June 1, 2024:June 1, 2024:B123:1000:Factory 1:ISO9001:Order6789"]
    
    directory = "./Sample QRs to Scan"

    for index, data in enumerate(sample_data, start=1):
        filename = os.path.join(directory, f"lol.png")
        create_qr_code(data, filename)
