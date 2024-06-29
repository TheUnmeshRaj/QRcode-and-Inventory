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
        
    sample_data = ["12344:Fan:Electronics:June 1, 2024:June 1, 2026:B123:1000:Factory 1:ISO9001:Order6789"
,"12344:Fan:Electronics:June 1, 2024:June 1, 2026:B123:1000:Factory 1:ISO9001:Order6789"
,"12347:TV:Electronics:April 20, 2024:April 20, 2026:B126:1500:Factory 4:FCC:Order6792"
,"12348:Mobile:Electronics:June 5, 2024:June 5, 2026:B127:2000:Factory 5:RoHS:Order6793"
,"22347:Sprite:Food & Beverage:February 20, 2024:February 20, 2025:B226:900:Factory 9:SQF:Order7797"
,"32344:T-shirt:Clothing:January 1, 2024:January 1, 2026:B323:1000:Factory 11:OEKO-TEX:Order8799"
,"32345:Jeans:Clothing:February 15, 2024:February 15, 2026:B324:800:Factory 12:GOTS:Order8800"
,"42344:Table:Home & Garden:August 1, 2024:August 1, 2028:B423:100:Factory 16:FSC:Order9804"
,"42345:Chair:Home & Garden:July 15, 2024:July 15, 2028:B424:150:Factory 17:PEFC:Order9805"
,"42346:Sofa:Home & Garden:June 10, 2024:June 10, 2028:B425:200:Factory 18:ISO14001:Order9806"
,"42347:Lamp:Home & Garden:May 20, 2024:May 20, 2028:B426:250:Factory 19:Energy Star:Order9807"
,"42348:Rug:Home & Garden:April 5, 2024:April 5, 2028:B427:300:Factory 20:OEKO-TEX:Order9808"
,"52344:Tire:Automotive:November 1, 2024:November 1, 2026:B523:500:Factory 21:DOT:Order10809"
,"52345:Engine Oil:Automotive:October 15, 2024:October 15, 2026:B524:400:Factory 22:API:Order10810"
,"52346:Brake Pads:Automotive:September 10, 2024:September 10, 2026:B525:700:Factory 23:JIS:Order10811"
,"52347:Battery:Automotive:August 20, 2024:August 20, 2026:B526:900:Factory 24:CE:Order10812"
,"52348:Headlights:Automotive:July 5, 2024:July 5, 2026:B527:1000:Factory 25:ECE:Order10813"
]
    
    directory = "./Sample QRs to Scan"

    for index, data in enumerate(sample_data, start=1):
        filename = os.path.join(directory, f"{index}.png")
        create_qr_code(data, filename)
