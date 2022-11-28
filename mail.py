from trycourier import Courier

client = Courier(auth_token="pk_prod_GMNSHH1R0N4X4WG2C1JVTZBHPC49")
def send_appointment_mail(name, appointment_id, appointment_type, email, message):
    resp = client.send_message(
        message={
            "to": { 
                "email":email
                },
            "template": "1J2VJ56V0T4RARJJSGSWJA90P853",
            "data": {
                "name": name,
                "appointment_number": appointment_id,
                "appointment_type": appointment_type,
                "message": message
                },
            }
        )
    
def send_approval_mail(email,name, appointment_id, appointment_type, appointment_date, appointment_time, appointment_remarks):
    resp = client.send_message(
        message={
            "to": {
                "email": email,
                },
            "template": "PXCAZ2PWD3MBMBMCX3P38V25K8X2",
            "data": {
                "name": name,
                "appointment_number": appointment_id,
                "appointment_type": appointment_type,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
                "appointment_remarks": appointment_remarks
                },
            }
        )
    
def send_completed_mail(email, name, appointment_id, link):
    resp = client.send_message(
        message={
            "to": {
                "email": email,
                },
            "template": "0X55E3DJFQMT0NG294CK5ZYR490X",
            "data": {
                "name": name,
                "appointment_number": appointment_id,
                "link": link
                },
            }
        )
def send_declined_mail(email,name,appointment_id, remarks):
    resp = client.send_message(
        message={
            "to": {
                "email": email,
                },
            "template": "E8V9HA654QMP7SHJW6NVQYS54WPF",
            "data": {
                "name": name,
                "appointment_number": appointment_id,
                "remarks": remarks,
                },
            }
        )

def send_contact_mail(name, email, message):
    resp = client.send_message(
        message={
            "to": {
                "email": email,
                },
            "template": "RPVABVC3ZH447QK5405RMZ7XASE9",
            "data": {
                "name": name,
                "message": message,
                },
            }
        )
    resp = client.send_message(
        message={
            "to": {
                "email": "ehcctesting@gmail.com",
                },
            "template": "RPVABVC3ZH447QK5405RMZ7XASE9",
            "data": {
                "name": name,
                "message": message,
                },
            }
        )


def send_document_upload_mail(name, email, appointment_id, link):
    resp = client.send_message(
        message={
            "to": {
                "email": email,
                },
            "template": "CK3QSXVW1MM2T0M9NSA11SPW8EE5",
            "data": {
                "name": name,
                "appointment_number": appointment_id,
                "link": link
                },
            }
        )