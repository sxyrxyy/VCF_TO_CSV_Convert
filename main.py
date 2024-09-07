import quopri
import csv

def decode_quoted_printable(encoded_text):
    try:
        decoded_bytes = quopri.decodestring(encoded_text)
        decoded_text = decoded_bytes.decode('utf-8', errors='ignore')
        return decoded_text
    except Exception as e:
        print(f"Error decoding text: {e}")
        return ""

def extract_contact_info(vcf_file):
    contacts = []

    with open(vcf_file, 'r', encoding='utf-8') as file:
        contact = {}
        for line in file:
            if line.startswith('FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:'):
                encoded_text = line.split('ENCODING=QUOTED-PRINTABLE:')[1].strip()
                
                while encoded_text.endswith('='):
                    encoded_text = encoded_text[:-1] + next(file).strip()

                contact['Name'] = decode_quoted_printable(encoded_text)

            elif line.startswith('TEL'):
                phone_number = line.split(':')[1].strip()
                contact['Phone'] = phone_number
            
            elif line.startswith('END:VCARD'):
                if 'Name' in contact or 'Phone' in contact:
                    contacts.append(contact)
                contact = {}

    return contacts

def export_to_csv(contacts, output_file):
    headers = ['Name', 'Phone']

    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact)

    print(f"Contacts exported to {output_file}")


vcf_file = 'input.vcf'  # Replace with your VCF file path
contacts = extract_contact_info(vcf_file)

csv_file = 'output.csv'  # Replace with your desired output CSV file path
export_to_csv(contacts, csv_file)
