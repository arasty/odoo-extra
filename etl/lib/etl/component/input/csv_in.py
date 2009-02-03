<<<<<<< TREE
# -*- encoding: utf-8 -*-
##############################################################################
#
#    ETL system- Extract Transfer Load system
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import etl
import csv

class csv_in(etl.component):
    """
        This is an ETL Component that use to read data from csv file.
       
		Type: Data Component
		Computing Performance: Streamline
		Input Flows: 0
		* .* : nothing
		Output Flows: 0-x
		* .* : return the main flow with data from csv file
    """
    def __init__(self, filename, *args, **argv):
        super(csv_in, self).__init__(*args, **argv)
        self.filename = filename

    def process(self):
        fp = csv.DictReader(file(self.filename))
        for row in fp:
            yield row, 'main'
=======
# -*- encoding: utf-8 -*-
##############################################################################
#
#    ETL system- Extract Transfer Load system
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""
This is an ETL Component that use to read data from csv file.
"""

from etl import etl
from etl.connector import file_connector
import csv
import datetime

class csv_in(etl.component):
    """
        This is an ETL Component that use to read data from csv file.
       
        Type: Data Component
        Computing Performance: Streamline
        Input Flows: 0
        * .* : nothing
        Output Flows: 0-x
        * .* : return the main flow with data from csv file
    """    

    def __init__(self,name,fileconnector,transformer=None,row_limit=0, csv_params={}):
        super(csv_in, self).__init__('(etl.component.input.csv_in) '+name,transformer=transformer)      
          
        self.fileconnector = fileconnector 
        self.csv_params=csv_params       
        self.row_limit=row_limit 
        self.row_count=0                                
        self.fp=None
        self.reader=None
<<<<<<< TREE
    
    def process(self):
<<<<<<< TREE
        fp = csv.DictReader(file(self.filename))
        for row in fp:
            yield row, 'main'
>>>>>>> MERGE-SOURCE
=======
=======

<<<<<<< TREE
    def action_start(self,key,singal_data={},data={}):
>>>>>>> MERGE-SOURCE
        try:
            super(csv_in, self).action_start(key,singal_data,data)                
            self.fp=self.fileconnector.open('r')                
            self.reader=csv.DictReader(self.fp,**self.csv_params)                            
        except Exception,e:                                                                    
            self.signal('error',{'error_msg': 'Error from start signal :'+str(e),'error_date':datetime.datetime.today()})

    def action_end(self,key,singal_data={},data={}):
        try:
            super(csv_in, self).action_end(key,singal_data,data)
            if self.fp:     
                 self.fp.close() 
            if self.fileconnector:    
                 self.fileconnector.close() 
        except Exception,e:                                                                    
            self.signal('error',{'error_msg': 'Error from end signal :'+str(e),'error_date':datetime.datetime.today()})

    def process(self):
        try:
            if not self.fileconnector:
                yield {'error_msg':'Error : Connector should be specified.','error_date':datetime.datetime.today()},'error'
            if not self.reader:
                yield {'error_msg':'Error : Reader should be specified.','error_date':datetime.datetime.today()},'error'
=======
    def action_start(self,key,singal_data={},data={}):        
        super(csv_in, self).action_start(key,singal_data,data)                
        self.fp=self.fileconnector.open('r')                
        self.reader=csv.DictReader(self.fp,**self.csv_params)                                    

    def action_end(self,key,singal_data={},data={}):        
        super(csv_in, self).action_end(key,singal_data,data)
        if self.fp:     
             self.fp.close() 
        if self.fileconnector:    
             self.fileconnector.close()         

    def process(self):        
        try:
>>>>>>> MERGE-SOURCE
            for data in self.reader:
                try:
                    chan='main'
                    for d in data.values():
                        d=unicode(d)                
                    self.row_count+=1
                    if self.row_limit and self.row_count > self.row_limit:
                         raise StopIteration                                        
                    if self.transformer:
                        data,chan=self.transformer.transform(data,chan)
                    yield data,chan                                     
                               
                except UnicodeEncodeError,e:    
                    error_d={'error_msg':'Error  :'+str(e),'error_date':datetime.datetime.today()}                                                                                                
                    yield error_d,'error'                    

            # TODO : call statistical iterator
        except TypeError,e:
            error_d={'error_msg':'Error  :'+str(e),'error_date':datetime.datetime.today()}                                                                                             
            yield error_d,'error'
        except IOError,e:
            error_d={'error_msg':'Error  :'+str(e),'error_date':datetime.datetime.today()}                                                                                             
            yield error_d,'error'
            
               
        

>>>>>>> MERGE-SOURCE
