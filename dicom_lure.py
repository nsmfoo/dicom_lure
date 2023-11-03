
#!/usr/local/bin/python3

import pydicom
import tempfile
import argparse
import os.path
import random
from pydicom.dataset import Dataset, FileDataset

def prepare_pdf(pdf_file):

    suffix = '.dcm'
    temp_filename = tempfile.NamedTemporaryFile(suffix=suffix).name
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.104.1'
    file_meta.MediaStorageSOPInstanceUID = '2.16.840.1.114430.287196081618142314176776725491661159509.60.1'
    file_meta.ImplementationClassUID = '1.2.276.0.7230010.3.0.3.6.6'
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'

    temp_ds = FileDataset(temp_filename, {},
                 file_meta=file_meta, preamble=b"\0" * 128)

    temp_ds.is_little_endian = True
    temp_ds.is_implicit_VR = False
    temp_ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.104.1'

    if os.path.isfile(args.pdf_file):
        print("-[ Reading PDF file:", args.pdf_file)
        with open(pdf_file, 'rb') as f:
            temp_ds.EncapsulatedDocument = f.read()
    else:
        print("* Unable to find: ",args.pdf_file)
        exit()
    temp_ds.MIMETypeOfEncapsulatedDocument = 'application/pdf'
    temp_ds.Modality = 'DOC'
    temp_ds.ConversionType = 'WSD'
    temp_ds.SpecificCharacterSet = 'ISO_IR 100' 

    return temp_ds

# Le Banner 
print("""
o-o   o-O-o   o-o  o-o  o   o   o                             */()
|  \    |    /    o   o |\ /|   |                          .  ( 
|   O   |   O     |   | | O |   |    o  o o-o o-o       */  ( %% 
|  /    |    \    o   o |   |   |    |  | |   |-'     (%/  ,(/
o-o   o-O-o   o-o  o-o  o   o   O---oo--o o   o-o   */( * ()  
                                               ,&&#/.,**%(,/,              
                                            (&%(#(//,,****                    
                                        (%%##&@&%#/..,**/.                      
                                  (&&@@@%##/((((*.,***,                         
                            .%&%#(((#%%&&%#(/*..****                            
                       .%%%&@@@@@%##((#(//(*.,*//.                              
                   .&@@&%%###%&@&&#%(**(/,.,**/  &(%&/                          
                /%%%&@@@@&%#(#(((#///*,..,*/* .  %  *%                          
             .%#%%####%&&&%((#/*/(*,/.,**/.      %/%/  %/                       
           ######(##(/*#/(#/*//**/,.,*//    .,#(,        /                      
         /%#/**(((####.#*//(**/,..,**((#(/#%.*          #                       
        &#/*(@&%,#//*/%..*,/* .,,***                                            
       &*##((/*%(.(#(/,.,..,,****     @nsmfoo - Mikael Keri                                               
      (&*,*//#/*//,*,,*******.                                                  
   &/,%%%//*********///*,                                                       
   *#&/   ..,,.  
""")

parser = argparse.ArgumentParser()
parser.add_argument('-T','--template', dest="template_file", required=True, help='This is the file that our lure will use as a template (dcm)')
parser.add_argument('-E','--embed', dest="pdf_file", required=True, help='PDF file to embedd in the new dcm file (pdf)')
parser.add_argument('-O','--output', dest="output_file", required=True, help='The name of the finished lure file (dcm)')
parser.add_argument('-N','--name', dest="title_name", required=False, help='Add a title (name) for the embedded document (Dicom image metadata)')
args = parser.parse_args()


# Read the template dicom image file
if os.path.isfile(args.template_file):
    print("-[ Reading template file:",args.template_file)
    org_ds = pydicom.dcmread(args.template_file)
else:
    print("* Unable to find:",args.template_file)
    exit()

# Prepare the PDF
new_ds = prepare_pdf(args.pdf_file)

new_ds.file_meta.ImplementationVersionName = org_ds.file_meta.ImplementationVersionName
# I thought it was "smart" to be in the same range, but not the exact S/N 
sn_rand = random.randint(100,400)

# A long list of values to use from the orginal image to make it blend in. These values can be omitted or extended as you see fit.
data_elements  = ['InstanceNumber',
                 'Manufacturer',
                 'StudyDate',
                 'ContentDate',
                 'AcquisitionTime',
                 'StudyTime',
                 'SeriesTime',
                 'ContentTime',
                 'AccessionNumber',
                 'PatientBirthDate',
                 'PatientSex',
                 'PatientID',
                 'PatientName',
                 'StudyID',
                 'StudyDescription',
                 'ImageComments',
                 'ProtocolName',
                 'StudyInstanceUID',
                 'SeriesInstanceUID',
                 'SeriesDescription',
                 'SeriesNumber']

for x in data_elements:
    try:
        if x == 'SeriesNumber':
            new_value = org_ds.data_element(x).value + sn_rand
            new_ds.SeriesNumber = new_value
        else:
            new_ds.add(org_ds.data_element(x))
    except:
        continue

new_ds.file_meta.SourceApplicationEntityTitle = org_ds.file_meta.SourceApplicationEntityTitle
  
if args.title_name:
    print("-[ Applying a custom title name:",args.title_name)
    new_ds.DocumentTitle = args.title_name
else:
    # Change the default title to something more serious
    new_ds.DocumentTitle =  'The Hoff medical history'

# Save the new file
new_ds.save_as(args.output_file)
print("-[ Lure file created:",args.output_file)