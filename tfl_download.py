import xml.etree.cElementTree as et
import requests
import os

def get_data(root):
    return {
        x.tag.replace('{http://s3.amazonaws.com/doc/2006-03-01/}', ''):
        x.attrib.get('name', x.text) for x in root.getchildren()
    }


def download(url, file_name, session):
    with open(file_name, "wb") as file:
        response = session.get(url)
        file.write(response.content)

url = "https://s3-eu-west-1.amazonaws.com/jamcams.tfl.gov.uk/"
s = requests.Session()
r = s.get(url)
root = et.fromstring(r.content)
data = {x.find('{http://s3.amazonaws.com/doc/2006-03-01/}Key').text: get_data(x) for x in root.iter(tag='{http://s3.amazonaws.com/doc/2006-03-01/}Contents')}

for value in data:
    print(value, data[value])
    split_value = value.split('.')
    dirname = split_value[1]
    filename = '.'.join(split_value[:-1]) + data[value]['LastModified'].replace('-', '').replace(':', '').split('.')[0] + '.' + split_value[-1]
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    if not os.path.exists(dirname+'/'+filename):
        download(url+value, dirname+'/'+filename, s)
