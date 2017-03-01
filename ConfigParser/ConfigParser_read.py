
#read

import configparser
config = configparser.ConfigParser()
try:
    #temp2 = config.read('example.ini')
    #temp = config.read('test.cutlist')
    config.read('Inspector_Barnaby_14.02.03_20-15_zdfneo_100_TVOON_DE.mpg.HQ.avi.cutlist')
except :
    print('test')


for section in config.sections():
    for key in config[section]:
        print(config[section][key])

#for key in config['bitbucket.org']: print(config['bitbucket.org'][key])

