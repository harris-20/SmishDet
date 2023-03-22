import pandas as pd 
import numpy as np
import ipaddress
import socket as s
import requests
from urllib.parse import urlparse

import rf_model


class feature_extractor:

    def __init__(self,url:str):
        self.input_url = url

    def long_url(self,l):
        """ length of the URL"""
        l= str(l)
        if len(l) < 54:
            return 0
        elif len(l) >= 54 and len(l) <= 75:
            return 2
        return 1

    def have_at_symbol(self,l):
        """ whether the URL contains @ symbol or not"""
        if "@" in str(l):
            return 1
        return 0

    def redirection(self,l):
        """If the url has symbol(//) after protocol """
        if "//" in str(l):
            return 1
        return 0

    def prefix_suffix_seperation(self,l):
        """seprate prefix and suffix"""
        if '-' in str(l):
            return 1
        return 0

    def sub_domains(self,l):
        """check the subdomains"""
        l= str(l)
        if l.count('.') < 3:
            return 0
        elif l.count('.') == 3:
            return 2
        return 1
    
    def havingIP(self,url):
      try:
        s.gethostbyname(url)
        return 0
      except:
        return 1

    def havingServerinfo(self,url):
      try:
          requests.get(url)
          return 0
      except:
          return 1

    def havingDNSrec(self,url):
      try:
          dns.resolver.resolve(url,'NS')
          return 0
      except:
          return 1   

    def httpDomain(self,url):
        domain = urlparse(url)
        if 'https' in domain:
           return 0
        else:
           return 1


    def extract(self):
        print("in script 2")
        input_data = [{"URL":self.input_url}]
        print('input taken')
        temp_df = pd.DataFrame(input_data)
        print("dataframe created")
      
        seperation_of_protocol = temp_df['URL'].str.split("://",expand = True)
        print("step 1 done")
      
        seperation_domain_name = seperation_of_protocol[1].str.split("/",1,expand = True)
        print("step 2 done")
       
        seperation_domain_name.columns=["domain_name","address"]
        print("step 3 done")
      
        splitted_data = pd.concat([seperation_of_protocol[0],seperation_domain_name],axis=1)
        print("step 4 done")

        splitted_data.columns = ['protocol','domain_name','address']
        print("step 5 done")

        splitted_data.columns = ['protocol','domain_name',"address"]
        print("step 6 done")

        splitted_data.columns = ['protocol','domain_name',"address"]
        print("step 7 done")

        splitted_data.columns = ['protocol','domain_name',"address"]
        print("step 8 done")

        #splitted_data['is_phished'] = pd.Series(temp_df['Target'], index=splitted_data.index)
        #print("step 6 done")

        """extraction """
      
        splitted_data['long_url'] = temp_df['URL'].apply(self.long_url)
        print("feature extra 1")
        splitted_data['having_@_symbol'] = temp_df['URL'].apply(self.have_at_symbol)
        print("feature extra 2")
        splitted_data['redirection_//_symbol'] = seperation_of_protocol[1].apply(self.redirection)
        print("feature extra 3")
        splitted_data['prefix_suffix_seperation'] = seperation_domain_name['domain_name'].apply(self.prefix_suffix_seperation)
        print("feature extra 4")
        splitted_data['sub_domains'] = splitted_data['domain_name'].apply(self.sub_domains)
        print("feature extra 5")
        splitted_data['ip_address'] = splitted_data['domain_name'].apply(self.havingIP)
        print("feature extra 6")
        splitted_data['server_info'] = temp_df['URL'].apply(self.havingServerinfo)
        print("feature extra 7")
        splitted_data['httpsDomain'] = temp_df['URL'].apply(self.httpDomain)
        print("feature extra 8")
        
        splitted_data.to_csv(r'dataset3.csv',header= True)

        

        return rf_model.predictor(splitted_data)
