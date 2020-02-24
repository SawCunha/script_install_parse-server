#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import json
import sys
import time

host = sys.argv[1]
pushKey = sys.argv[2]

ARQUIVO_CONFIGURACAO = "config_install.json"
appName = ''
appKey = ''
masterKey = ''

jsonConfig = json.load(open(ARQUIVO_CONFIGURACAO,'r'))

def update_system(update_system):
    print '\n\n######### Install GIT #############\n\n'
    print os.system(update_system['install_git'])
    time.sleep(2)
    print '\n\n######### Install HTOP #############\n\n'
    print os.system(update_system['install_htop'])
    time.sleep(2)
    print '\n\n######### Install VIM #############\n\n'
    print os.system(update_system['install_vim'])
    time.sleep(2)
    print '\n\n######### Install LBS-CORE #############\n\n'
    print os.system(update_system['install_lbs-core'])
    time.sleep(2)
    print '\n\n######### Install NET-Tools #############\n\n'
    print os.system(update_system['install_net-tools'])
    time.sleep(2)
    print '\n\n######### Install EPEL #############\n\n'
    print os.system(update_system['install_system'])
    time.sleep(2)
    print '\n\n######### Update System #############\n\n'
    print os.system(update_system['update'])

def install_node(node):
    print '\n\n######### Install NODE #############\n\n'
    print os.system(node['repositorio'])
    print os.system(node['install'])
    print os.system(node['verificando_node'])
    print os.system(node['verificando_npm'])

def install_mongo(mongo):
    print '\n\n######### Install MONGO #############\n\n'
    file = open(mongo['dir_yum'],'w')
    print str(mongo['mongo_yum'])
    file.writelines(str(mongo['mongo_yum']))
    file.close()
    print os.system(mongo['install'])
    print os.system(mongo['start'])
    print os.system(mongo['enable'])

def install_parse_server(parse):
    print '\n\n######### Install PARSE-SERVER #############\n\n'
    global appName
    global appKey
    global masterKey

    os.chdir(parse['cd_dir'])

    print os.system(parse['mkidr'])

    os.chdir(parse['dir'])
    
    appName = parse['appName']
    appKey = parse['appId']
    masterKey = parse['masterKey']

    file = open(parse['config_name'],'w')
    temp = json.dumps(parse['config'])
    temp = temp.replace('$appId$',appKey)
    temp = temp.replace('$masterKey$',masterKey)
    temp = temp.replace('$appName$',appName)
    temp = temp.replace('$keyPush$',pushKey)
    file.write(temp)
    file.close()

    file = open(parse['package_name'],'w')
    temp = json.dumps(parse['package'])
    temp = temp.replace('$appName$',appName)
    file.write(temp)
    file.close()

    print os.system(parse['mkdir_cloud'])
    
    file = open(parse['cloud_name'],'w')
    file.write(parse['cloud'])
    file.close()

    print os.system(parse['mkdir_public'])
    print os.system(parse['install'])
    print os.system(parse['install_mongo'])

def install_parse_dashboard(parse):
    print '\n\n######### Install PARSER-DASHBOARD #############\n\n'
    global appName
    global appKey
    global masterKey
    print os.system(parse['install'])
    print os.system(parse['create_file_config']['mkdir'])
    os.chdir(parse['create_file_config']['dir'])
    file = open(parse['create_file_config']['name'],'w')
    temp = json.dumps(parse['create_file_config']['data'])
    temp = temp.replace('$appId$',appKey)
    temp = temp.replace('$masterKey$',masterKey)
    temp = temp.replace('$appName$',appName)
    temp = temp.replace('$ipServer$',host)
    file.write(temp)
    file.close()


def init_systemd(systemd):
    print '\n\n######### Criando Service #############\n\n'
    print os.system(systemd['mkdir'])
    init_parse(systemd['parse-server'],systemd['reload'])
    init_parse(systemd['parse-dashboar'],systemd['reload'])

def init_parse(parse,reload):
    file = open(parse['script_name'],'w')
    file.write(parse['script'])
    file.close()
    
    file = open(parse['systemd_name'],'w')
    file.write(parse['systemd'])
    file.close()

    os.system(parse['chmod'])

    print os.system(reload)
    print os.system(parse['start'])
    print os.system(parse['enable'])

def firewall(fire):
    print '\n\n######### Add ao Firewall #############\n\n'
    print os.system(fire['parse-server'])
    print os.system(fire['parse-dashboard'])
    print os.system(fire['reload'])

update_system(jsonConfig['update_system'])
install_node(jsonConfig['install_node'])
install_mongo(jsonConfig['install_mongo'])
install_parse_server(jsonConfig['install_parse-server'])
install_parse_dashboard(jsonConfig['install_parse-dashboard'])
init_systemd(jsonConfig['init_systemd'])
firewall(jsonConfig['firewall'])