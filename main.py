import sys
import pdfplumber

# Grade to gradepoint (GP) mapping
GRADES_DICT = {
    "S": 10.0,
    "A+": 9.0,
    "A": 8.5,
    "B+": 8.0,
    "B": 7.5,
    "C+": 7.0,
    "C": 6.5,
    "D": 6.0,
    "P": 5.5,
    "F": 0.0,
    "FE": 0.0,
    "Absent": 0.0,
    "Withheld": 0.0
}

# Course to credit mapping
CREDIT_DICT = {

    # ECE
    "GYMAT301" : 3.0,
    "PCECT302" : 4.0,
    "PCECT303" : 4.0,
    "PBECT304" : 4.0,
    "GNEST305" : 4.0,
    "UCHUT346" : 2.0,
    "PCECL307" : 2.0,
    "PCECL308" : 2.0,

    # CSE
    "GAMAT301" : 3.0,
    "PCCST302" : 4.0,
    "PCCST303" : 4.0,
    "PBCST304" : 4.0,
    "GAEST305" : 4.0,
    "UCHUT347" : 2.0,
    "PCCSL307" : 2.0,
    "PCCSL308" : 2.0,

    # EB
    "GYMAT301" : 3.0,
    "PCEBT302" : 4.0,
    "PCEBT303" : 4.0,
    "PBEBT304" : 4.0,
    "GNEST305" : 4.0,
    "UCHUT347" : 2.0,
    "PCEBL307" : 2.0,
    "PCEBL308" : 2.0,

    # EEE
    "GYMAT301" : 3.0,
    "PCEET302" : 4.0,
    "PCEET303" : 4.0,
    "PBEET304" : 4.0,
    "GNEST305" : 4.0,
    "UCHUT346" : 2.0,
    "PCEEL307" : 2.0,
    "PCEEL308" : 2.0,

    # MEC
    "GYMAT301" : 3.0,
    "PCMET302" : 4.0,
    "PCMET303" : 4.0,
    "PBMET304" : 4.0,
    "GNEST305" : 4.0,
    "UCHUT346" : 2.0,
    "PCMEL307" : 2.0,
    "PCMEL308" : 2.0,

    # CU
    "GAMAT301" : 3.0,
    "PCCBT302" : 4.0,
    "PCCST303" : 4.0,
    "PBCST304" : 4.0,
    "GAEST305" : 4.0,
    "UCHUT347" : 2.0,
    "PCCSL307" : 2.0,
    "PCCBL308" : 2.0,

    # EV
    "GYMAT301" : 3.0,
    "PCECT302" : 4.0,
    "PCECT303" : 4.0,
    "PBECT304" : 4.0,
    "GNEST305" : 4.0,
    "UCHUT346" : 2.0,
    "PCECL307" : 2.0,
    "PCECL308" : 2.0,
}

# Extracting text into full text
# FUTURE UPDATE: this function can be combined with iterate_to_compute_sgpa
def extract_values(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:

        full_text = []

        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                text = text.replace(",","")
                text = text.split()
                full_text.extend(text)
            else:
                # No extractable text
                continue
        
        return full_text

# SGPA calculator
def obtain_sgpa(candidate):
    total_cred = 0
    weighted_numerator = 0

    for i in range(len(candidate)):
        if i == 0:
            continue
        course_name, grade = candidate[i].rstrip(")").split("(")

        # Optional try statement
        weight = CREDIT_DICT[course_name]
        grade_point = GRADES_DICT[grade]
        weighted_numerator += weight * grade_point
        total_cred += weight

    return [candidate[0], round(weighted_numerator / total_cred, 2)]

# Checking if course is valid
# Course validity is checked by checking the following 2 conditions
# 1. If '(' and ')' are present within the string
# 2. If course name is present in  CREDIT_DICT
def course_is_valid(code):
    if "(" in code and ")" in code:
        course_name, grade = code.rstrip(")").split("(")
        return True if course_name in CREDIT_DICT else False
    return False

# Core function which computes sgpa
def iterate_to_compute_sgpa(entire_data):
    length = len(entire_data)
    i = 0

    # Iterating through data
    while i < length:

        # Checking if MDL is present in the subtext, which is the registration code
        if "MDL" in entire_data[i]:
            cand = [entire_data[i]]
            i += 1

            # We append everything which shows up after that until MDL is not present and course is valid
            # FUTURE UPDATE: only course validity may be required, untested
            while "MDL" not in entire_data[i] and course_is_valid(entire_data[i]):
                cand.append(entire_data[i])
                i += 1
            
            # Obtaining sgpa using calculator and printing it
            # cand contains the candidates registration code and the grades for subjects
            sgpa = obtain_sgpa(cand)
            print(sgpa)
        else:
            i += 1

if __name__ == "__main__":

    # Error case
    if len(sys.argv) < 2:
        print("Usage: python prog.py <path_to_pdf>")
        sys.exit(1)

    # Obtaining path, extracting values and computing sgpa for each student present in the PDF in the requird format
    pdf_path = sys.argv[1]
    text = extract_values(pdf_path)
    iterate_to_compute_sgpa(text)
