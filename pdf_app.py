# inspiration:
# https://realpython.com/python-modules-packages/
# realpython.com/pdf-python
# https://www.guru99.com/python-check-if-file-exists.html
# https://dzone.com/articles/creating-and-manipulating-pdfs-with-pdfrw

from os import path as FilePath
import pdfrw
import snoop

# GLOBAL VARIABLES
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_USER_FIELD_KEY = '/TU'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
pdf_keys = []

def add_slash(original_path):
    """adds '/' to end of paths that don't contain it. assumes using a linux or similar system that uses backslashes"""
    print(f"Adding '/' to '{original_path}' path")
    # print(f"'/' addition done")
    end_path = original_path + '/'
    # print(f"Original path: {original_path}")
    # print(f"New path: {end_path}")
    return end_path

def add_pdf_extension(filename):
    """adds '.pdf' to end of filenames that don't contain it. assumes file is of type PDF"""
    print("Adding '.pdf' extension")
    # print("'.pdf' added")
    end_file = filename + '.pdf'
    return end_file

def validate_template_directory_path(raw_path):
    """Assumes a linux server is used so file paths use '/' """
    print("Checking if template directory path ends with '/'")
    end_path = ''
    result = False
    if raw_path[-1] == '/':
        result = True
        print("Path already includes '/'")
        # end_path = raw_path
    else:
        print("Path does not contain '/'")
        print("Adding '/' to path")
        # end_path = raw_path + '/'
    # print("Template directory check done. Returning 'True' or 'False'")
    return result

def validate_pdf_extension(filename):
    """confirm file ends with .pdf extension"""
    print("Checking if file has '.pdf' extension")
    end_filename = ''
    result = False
    ext = filename[-4:]
    # print(ext)
    if ext == '.pdf':
        result = True
        print('File has .pdf extension')
        # end_filename = filename
    else:
        print("File does not have .pdf extension")
        # print(f"Adding .pdf to {filename}")
        # end_filename = filename + '.pdf'
    # print("File extension check done. Returning 'True' or 'False'")
    return result

def store_full_path(original_path):
    """confirms the full path has a '/' at the end"""
    print("Confirming path ends with '/'")
    end_path = ''
    if validate_template_directory_path(original_path):
        print("Path ends in '/'")
        end_path = original_path
    else:
        print("Path missing '/'. Adding it now...")
        end_path = add_slash(original_path)
    # print("Path check done")
    return end_path

class PdfManager:
    def __init__(self, template_directory):
        print('Creating new PdfManager object')
        self.template_directory = store_full_path(template_directory)
        # must have .pdf already added to the name
        self.under150_fullpath = ''
        self.over150_fullpath = ''
        self.under150_filename = ''
        self.over150_filename = ''
        self.under150_keyfile = self.template_directory + 'under150keys.txt'
        self.over150_keyfile = self.template_directory + 'over150keys.txt'
        self.under150_pdf_form_keys = []
        self.over150_pdf_form_keys = []
        self.under150_number_of_keys = 0
        self.over150_number_of_keys = 0
        self.under150_data = {}
        self.over150_data = {}

    def validate_path(self, filename):
        """Check file name - must end with .pdf"""
        # check file has proper ending
        # check file exists
        full_file_path = self.template_directory + filename
        result = FilePath.exists(full_file_path)
        # print(result)
        return result

    def store_under_150k_path(self, filename):
        """saves the full path of the pdf used for <= $150k loan forgiveness"""
        print("Starting under $150k PPP loan forgiveness PDF storage")
        if validate_pdf_extension(filename):
            # print("file has '.pdf' extension")
            self.under150_fullpath = self.template_directory + filename
            # print(f"Under $150k path: {self.under150_fullpath}")
        else:
            # print("'.pdf' extension missing")
            end_filename = add_pdf_extension(filename)
            self.under150_fullpath = self.template_directory + end_filename
            # print(f"Under $150k path: {self.under150_fullpath}")
        # print("Storage done")

    def store_over_150k_path(self, filename):
        """saves the full path of the pdf used for > $150k loan forgiveness"""
        print("Starting over $150k PPP loan forgiveness PDF storage")
        if validate_pdf_extension(filename):
            # print("file has '.pdf' extension")
            self.over150_fullpath = self.template_directory + filename
            # print(f"Under or equal to $150k path: {self.over150_fullpath}")
        else:
            # print("'.pdf' extension missing")
            end_filename = add_pdf_extension(filename)
            self.over150_fullpath = self.template_directory + end_filename
            # print(f"Over $150k path: {self.over150_fullpath}")
        # print("Storage done")

    def get_pdf_keys(self, filepath, selection):
        print("Begin storing form field names")
        # print("creating pdfrw object")
        temp = pdfrw.PdfFileReader(filepath)
        # print(f"This pdf has {len(temp.pages)} pages")
        if selection == 1:
            for page in temp.pages:
                annotations = page[ANNOT_KEY]
                if annotations is None:
                    continue
                for annotation in annotations:
                    if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                        if annotation[ANNOT_FIELD_KEY]:
                            key = annotation[ANNOT_FIELD_KEY][1:-1]
                            self.under150_pdf_form_keys.append(key)
                            # print(key)
        elif selection == 2:
            for page in temp.pages:
                annotations = page[ANNOT_KEY]
                if annotations is None:
                    continue
                for annotation in annotations:
                    if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                        if annotation[ANNOT_FIELD_KEY]:
                            key = annotation[ANNOT_FIELD_KEY][1:-1]
                            self.over150_pdf_form_keys.append(key)
                            # print(key)
        else:
            print("Wrong input. Try '1' or '2'")
        # print("End storing form field names")

    def get_pdf_info(self, filepath):
        """output general information on pdf"""
        pdf = pdfrw.PdfFileReader(filepath)
        print(pdf.keys())
        # print(pdf.info())
        # print(pdf.root.keys())
        print(f'pdf has {len(pdf.pages)} pages')

    def keys_to_file(self, selection):
        """
        Writes form field names (keys) to an ordinary '.txt' file
        Args:
            output_file ([type]): [description]
            selection ([type]): [description]
        """
        def save_file(self, alist, output_file):
            try:
                with open(output_file, 'w+') as file:
                    for item in alist:
                        file.write(f"{item}\n")
                    print(f"{output_file} successfully created.")
                    file.close()
            except: 
                print("Error saving to file")

        if selection == 1:
            the_list = self.under150_pdf_form_keys
            save_file(self, the_list, self.under150_keyfile)
        elif selection == 2:
            the_list = self.over150_pdf_form_keys
            save_file(self, the_list, self.over150_keyfile)
        else:
            print("Incorrect pdf form selection")

    def keys_to_variable(self, selection):
        result = []
        temp_list = []
        temp_file = ''
        the_file = ''
        temp_item = ''

        # 1 = less than or under $150,000; 2 = over $150,000
        if selection == 1:
            the_file = self.under150_keyfile
        elif selection == 2:
            the_file = self.over150_keyfile
        else:
            print("Incorrect selection made")

        try:
            temp_file = open(the_file, 'r')
            temp_list = temp_file.readlines()
            # print(temp_list)
            for item in temp_list:
                temp_item = item.rstrip("\n")
                result.append(temp_item)
            # print(result)
            return result
        except:
            print("Error extracting keys from file.")

    def write_to_pdf(self, input_file, output_file, data):
        template_pdf = pdfrw.PdfReader(input_file)
        for page in template_pdf.pages:
            annotations = page[ANNOT_KEY]
            if annotations is None:
                continue
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        if key in data.keys():
                            if type(data[key]) == bool:
                                if data[key] == True:
                                    annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))
                                else:
                                    annotation.update(pdfrw.PdfDict(V=''.format(data[key])))
                                    annotation.update(pdfrw.PdfDict(AP=''))
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write(output_file, template_pdf)


# @snoop
def main():
    pdf_template_path = './pdf/templates/active/PPP-PDFs'
    pdf_under150 = 'PPP-3508S-3.pdf'
    pdf_over150 = 'PPP-3508EZ-3.pdf'
    pdf_no_ext = 'PPP-350EZ'
    pdf_output1 = 'under150.pdf'
    pdf_output2 = 'over150.pdf'
    
    try:
        pdf = PdfManager(pdf_template_path)
        # validate_pdf_extension(pdf_under150)
        # print(pdf.template_directory)
        pdf.validate_path(pdf_under150)
        pdf.validate_path(pdf_over150)
        pdf.store_under_150k_path(pdf_under150)
        pdf.store_over_150k_path(pdf_over150)
        pdf.get_pdf_keys(pdf.under150_fullpath, 1)
        pdf.get_pdf_keys(pdf.over150_fullpath, 2)
        pdf.get_pdf_info(pdf.under150_fullpath)
        pdf.get_pdf_info(pdf.over150_fullpath)

        pdf.under150_number_of_keys = len(pdf.under150_pdf_form_keys)
        pdf.over150_number_of_keys = len(pdf.over150_pdf_form_keys)

        print("\n")
        print("####")
        print("<= $150,000 form field keys")
        print(pdf.under150_pdf_form_keys)
        print(f"Number of form field keys: {pdf.under150_number_of_keys}")
        print("####")
        print("\n")

        print("\n")
        print("####")
        print("> $150,000 form field keys")
        print(pdf.over150_pdf_form_keys)
        print(f"Number of form field keys: {pdf.over150_number_of_keys}")
        print("####")
        print("\n")

        # enter 1 for less than or under $150,000 or 2 for over
        pdf.keys_to_file(1)
        pdf.keys_to_file(2)

        # enter 1 for less than or under $150,000 or 2 for over
        # reads each line of previously saved key file
        pdf.keys_to_variable(1)
        pdf.keys_to_variable(2)

        # under 150 data list
        data1 = [str(item) for item in range(1, pdf.under150_number_of_keys + 1)]
        dict1 = dict(zip(pdf.under150_pdf_form_keys, data1))
        print(dict1)

        data2 = [item for item in range(1, pdf.over150_number_of_keys + 1)]
        dict2 = dict(zip(pdf.over150_pdf_form_keys, data1))
        print(dict2)
        pdf.write_to_pdf(pdf.under150_fullpath, 'output.pdf', dict1)

    except:
        print("Error")

# putting parentheses around namespace allows executing as module or script
if (__name__=='__main__'):
    main()
