#coding: utf-8  
__author__= 'rogerp'  

import logging  
from suds.client import Client  
from suds.sax.element import Element 

      
if __name__ == '__main__':  
    #logging.basicConfig(level=logging.INFO)  
    #logging.getLogger('suds.client').setLevel(logging.DEBUG)  
    client = Client('http:xxxx.asmx?wsdl',location='http://xxxxxx.asmx',cache=None)  
    #client = Client('http://xxxx:9200/xx?wsdl',cache=None)  
    #client = Client('http://xxxx:9100/xx?wsdl')  


    ns = ('ns1', 'http://tempuri.org/') 
    sAuthenticate = Element('sAuthenticate').setText('xxxxxxxxxxxxxxxxxxxxx')
    header = Element('AuthenHeader',ns=ns).append(sAuthenticate) 

    client.set_options(soapheaders=header)  
    
    result = client.service.GetMemberProperty2(nPropertyType=40, sPropertyValues=13570962349)  
   
    print result  

