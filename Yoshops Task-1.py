#!/usr/bin/env python
# coding: utf-8

# In[66]:


get_ipython().system(' pip install pdfplumber')
get_ipython().system(' pip install requests')
import requests
import pdfplumber
import pandas as pd


# In[67]:


def download_file(url):
    local_filename = url.split('/')[-1]
    
    with requests.get(url) as r:
        with open(local_filename, 'wb') as f:
            f.write(r.content)
            
    return local_filename


# In[68]:


ap_url='https://cr.indianrailways.gov.in/uploads/files/1392699979463-MOBILE%20No.2014.pdf'


# In[69]:


ap = download_file(ap_url)


# In[70]:


with pdfplumber.open(ap) as pdf:
    page = pdf.pages[15]
    text=page.extract_text()
    


# In[71]:


print(text)


# In[80]:


get_ipython().system(' pip install pyperclip')


import pyperclip, re

IndianNumber = re.compile(r'''(
(\d{1,10})
)''',re.VERBOSE)

phoneRegex = re.compile(r'''(
(\d{3}|\(\d{3}\))?              # Area Code(Optional)
(\s|-|\.)                       # Separator
(\d{3})                         # First Three Digits
(\s|-|\.)                       # Separator
(\d{4})                         # Last Four Digits
(\s*(ext|x|ext.)\s*(\d{2,5}))?  # Extension
)''', re.VERBOSE)



# Find Matches in Clipboard Text

phone_groups = phoneRegex.findall(text)

Indian_Contacts = IndianNumber.findall(text)

matched = []


for group in Indian_Contacts:
    if group[1] == '+91':
        phoneNum = group[1] + group[2]
    matched.append(phoneNum)



if len(matched) > 0:
    pyperclip.copy('\n'.join(matched))
    print('Copied to clipboard!\n')
    print('\n'.join(matched))
else:
    print('No Phone Numbers found')


# In[ ]:





# In[ ]:




