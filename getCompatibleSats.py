import os
import sys
import git
import requests
import json
#from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def main():
    gr_sat_dir = '/home/andrew/Documents/gr-satellites/'
    gr_sat_list = []
   
    #Pull from gr-satellites remote repo
    print("Updating list of compatible satellites from remote gr-satellites repository")
    #git.cmd.Git(gr_sat_dir).pull()

    
    sat_data = {}

    for root, directory, files in os.walk(gr_sat_dir + 'apps/'):
        for f in files:
            if '.grc' in f:
                sat_name = os.path.splitext(f)[0]
                gr_sat_list.append(sat_name)
                #print(sat_name)

                #xml_tree = ET.parse(gr_sat_dir + 'apps/beesat.grc')
                xml_tree = ET.parse(os.path.join(root, f))
                norad_id_flag = False

                # Save list of norad ids from gr-satellites
                for elem in xml_tree.iter():
                    if norad_id_flag and elem.text.isdigit() and elem.text != '0':
                        norad_id = int(elem.text)
                        sat_data[norad_id] = {}
                        sat_data[norad_id]['sat_name'] = sat_name
                        norad_id_flag = False
                    if elem.tag == 'key' and elem.text == 'noradID':
                        norad_id_flag = True

                #print(norad_ids)


    #TODO: add local caching so we don't have to call get every time we execute script
    #Get satellite info from SatNOGS DB
    satnogs_url = 'http://db.satnogs.org/'
    
#    satnogs_sats_json = requests.get(satnogs_url + 'api/satellites/?format=json')
#    if satnogs_sats_json.status_code != 200:
#        print('Failed to retrieve satellite data from SatNOGS DB')
#        sys.exit()
#   
#    satnogs_transmitters_json = requests.get(satnogs_url + 'api/transmitters/?format=json')
#    if satnogs_transmitters_json.status_code != 200:
#        print('Failed to retrieve transmitter data from SatNOGS DB')
#        sys.exit()

    with open('/home/andrew/Documents/classes/capstone/sandbox/satnogs_transmitters.json') as f:
        data = json.load(f)
    #print(satnogs_transmitters_json.content)
    for transmitter in data:
        norad_id = transmitter['norad_cat_id']
        trans_name = transmitter['description']
        if norad_id in sat_data:
            sat_data[norad_id][trans_name] = {}
            sat_data[norad_id][trans_name]['downlink_low'] = transmitter['downlink_low']
        
        
    json_sat_data = json.dumps(sat_data, indent=4, sort_keys=True)
    print(json_sat_data)
    

if __name__ == "__main__":
    main()

