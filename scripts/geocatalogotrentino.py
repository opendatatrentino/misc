# -*- coding: utf-8 -*-
"""
Created on Sun May 19 23:44:09 2013

@author: maurizio napolitano
"""
import csv
from owslib.csw import CatalogueServiceWeb
csw = CatalogueServiceWeb('http://www.territorio.provincia.tn.it/geoportlet/srv/eng/csw')
csw.getrecords()
data = {}
records = csw.records
for r in records:
    data[r]=records[r]
matches = csw.results['matches']
returned = csw.results['returned']
startposition = 0
while (returned != 0):
    records = csw.records
    for r in records:
        data[r]=records[r]
    csw.getrecords(startposition=csw.results['nextrecord'])
    returned = csw.results['returned']

with open('datafromgeocatalogpat.csv', 'wb') as csvfile:
    csvoutput = csv.writer(csvfile, delimiter=';',quoting=csv.QUOTE_ALL)
    firstrow = True
    for d in data:
        fields = {}
        fields = data[d].__dict__
        if (firstrow):
            csvoutput.writerow(fields.keys())
            firstrow = False
        csvoutput.writerow(fields.values())
csvfile.close()
    