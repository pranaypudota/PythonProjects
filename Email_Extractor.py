from email_validator import validate_email, EmailNotValidError
import re
import os

class EmailExtractor:
    def __init__(self):
        self.text = ""
        self.emails = []

    def from_file(self, filepath):
        if not os.path.isfile(filepath):
            print(f"[ERROR] File '{filepath}' does not exist.")
            return False
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.text = f.read()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to read file: {e}")
            return False

    def from_string(self, input_string):
        self.text = input_string

    def extract_rfc_emails(self):
        # Find candidate emails using broad regex
        candidates = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', self.text)
        valid = []
        for email in candidates:
            try:
                validated = validate_email(email, check_deliverability=False)
                valid.append(validated.email)
            except EmailNotValidError:
                continue
        self.emails = list(set(valid))  # Deduplicate
        if not self.emails:
            print("[INFO] No valid RFC-compliant emails found.")
        return self.emails

    def print_emails(self, separator='\n'):
        if not self.emails:
            print("[INFO] No emails to display.")
            return
        if separator == '\n':
            for email in self.emails:
                print(email)
        else:
            print(separator.join(self.emails))

    def save_to_file(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for e in self.emails:
                    f.write(e + "\n")
            print(f"[SUCCESS] Emails saved to {filename}")
        except Exception as e:
            print(f"[ERROR] Couldn't save to file: {e}")

    def __str__(self):
        return "\n".join(self.emails) if self.emails else "No valid emails found."

# Example usage:
# extractor = EmailExtractor()
# extractor.from_file("sample.txt")
# extractor.extract_rfc_emails()
# extractor.print_emails()
# extractor.save_to_file("emails.txt")
