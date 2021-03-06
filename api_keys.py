#!/usr/bin/python
from optparse import OptionParser
from lib import swarmtoolscore
import sys
import httplib
import json
import base64

def usage(script_name):
    print "%s [create|list] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()
 
def create(hostname, user_id, password, key_type):
    conn = httplib.HTTPConnection(hostname)
    auth_hash = user_id + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    if (key_type != None):
        conn.request("POST", "/keys/" + key_type, None, {"Authorization":auth_header})
    else:
        conn.request("POST", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)
    swarmtoolscore.set_keys(hostname, user_id, password)

def list(hostname, user_id, password, key_type):
    conn = httplib.HTTPConnection(hostname)
    auth_hash = user_id + ":" + password
    auth_header = "Basic " + base64.b64encode(auth_hash)
    if (key_type != None):
        conn.request("GET", "/keys/" + key_type, None, {"Authorization":auth_header})
    else:
        conn.request("GET", "/keys", None, {"Authorization":auth_header})
    resp = conn.getresponse()
    txt = resp.read()
    conn.close()
    print json.dumps(json.loads(txt), sort_keys=True, indent=4)

def main():
    server_info = swarmtoolscore.get_server_info()
    keys = swarmtoolscore.get_keys()
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    elif sys.argv[1] == "create":
        opt_usage = "usage: \n  %s PASSWORD [options]"%(sys.argv[1])
        opt_usage += "\n\n  *PASSWORD: Your Bug Labs account password."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-t", "--type", dest="key_type", help="Specify the type of API key you wish to create. Valid types; 'configuration', 'participation' (both keys are created if no type specified).", metavar="KEY_TYPE")
        (options, args) =  parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        password = args[1]
        user_info = swarmtoolscore.get_user_info()
        create(server_info["hostname"], user_info["user_id"], password, options.key_type)
    elif sys.argv[1] == "list":
        opt_usage = "usage: \n  %s PASSWORD [options]"%(sys.argv[1])
        opt_usage += "\n\n  *PASSWORD: Your Bug Labs account password."
        parser = OptionParser(usage = opt_usage)
        parser.add_option("-t", "--type", dest="key_type", help="Specify the type of API key. Valid types; 'configuration', 'participation' (configuration is created by default).", metavar="KEY_TYPE")
        (options, args) = parser.parse_args()
        if len(args) != 2:
            print "Invalid number of args. See --help for correct usage."
            sys.exit()
        password = args[1]
        user_info = swarmtoolscore.get_user_info()
        list(server_info["hostname"], user_info["user_id"], password, options.key_type)
    else:
        usage(sys.argv[0])
main()
