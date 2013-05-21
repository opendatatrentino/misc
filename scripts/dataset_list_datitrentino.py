# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:47:10 2013

@author: maurizio napolitano
"""

import ckanclient
import urllib
import datetime, dateutil.parser
import csv
def convertday(s):
    s = dateutil.parser.parse(s)
    return s
def shorten(longURL):
    result = None
    f = urllib.urlopen("http://tinyurl.com/api-create.php?url=%s" % longURL)
    try:
        result = f.read()
    finally:
        f.close()
    return result

now = datetime.datetime.now()    
ckan = ckanclient.CkanClient(base_location='http://dati.trentino.it/api')
package_list = ckan.package_register_get()
with open('ckan_packages.csv', 'wb') as csvfile:
    csvoutput = csv.writer(csvfile, delimiter=';',quoting=csv.QUOTE_ALL)
    csvoutput.writerow(["name","author","maintainer","url","metadata_created","metadata_modified","dayaftercreation"])
    for package in package_list:
        ckan.package_entity_get(package)
        package_entity = ckan.last_message
        message = "Pubblicato oggi il dataset %s %s #opendatatrentino" % (package_entity['title'],shorten(package_entity['ckan_url']))
        maintainer = package_entity['maintainer']
        ckanurl = package_entity['ckan_url']
        #name = package_entity('name')
        author = package_entity['author']
        author = author.encode('utf8')
        maintainer = maintainer.encode('utf8')
        creation = convertday(package_entity['metadata_created'])
        modified = convertday(package_entity['metadata_modified'])
        age = now - creation
        modified = modified.strftime("%c")
        creation = creation.strftime("%c")
        name = package_entity['name']
        name = name.replace("-"," ").encode('utf8')
        csvoutput.writerow([name,author,maintainer,ckanurl,creation,modified,age.days])
csvfile.close()

