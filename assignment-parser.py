# Parses (Old Style) Sakai assignments XML records from the database
# Just fill in the Context
# SELECT * FROM ASSIGNMENT_SUBMISSION LEFT JOIN SAKAI_USER_ID_MAP ON SUBMITTER_ID = USER_ID WHERE CONTEXT IN (SELECT ASSIGNMENT_ID FROM ASSIGNMENT_ASSIGNMENT WHERE CONTEXT = '<SOME CONTEXT>')

# TODO: Does not handle multiple submitters

import argparse, csv
# Requires pandas
import pandas as pd
# Requires bs4
from bs4 import BeautifulSoup

from collections import OrderedDict

# Expects a filename
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

att = []

# Open the file and go through each row
with open(args.filename, newline='') as csvfile:
    df = pd.read_csv(csvfile)
    for index, row in df.iterrows():
        xml = BeautifulSoup(row['XML'], features='lxml')
        submitter = row['EID']
        #print (xml.submission.attrs.keys())
        context = xml.submission['context']
        assignment= xml.submission['assignment']
        n_attach = int(xml.submission.get('numberofsubmittedattachments'))
        s_text = xml.submission.get('submittedtext-html')
        if n_attach > 0:
            for n in range(0, n_attach):
                att.append([assignment, n, s_text, xml.submission.get('submittedattachment'+str(n)), submitter])

att_df = pd.DataFrame.from_records(att, columns=['assignment','submission num','submission text', 'attachment link','submitter'])
att_df.to_csv("attachments-result.csv", index=False)

