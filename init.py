#!/usr/bin/python
from optparse import OptionParser
import swarmtoolscore
import ConfigParser
import sys
import json
import base64

def usage(script_name):
    print "%s [init] \n"%(script_name)
    print "Use '%s [method] --help' for a method's usage and options."%(script_name)
    sys.exit()

def init(args):
    if len(args) != 3:
        print "Invalid number of args. See --help for correct usage."
        sys.exit()
    user_id = args[1]
    password = args[2]
    
    config = ConfigParser.ConfigParser()
    config.add_section("User Information")
    config.add_section("Keys")
    with open("swarm.cfg", "wb") as configfile:
        config.write(configfile)

    swarmtoolscore.set_user_info(user_id)
    swarmtoolscore.set_keys(user_id, password)
 
def main():
    if len(sys.argv) == 1:
        usage(sys.argv[0])
    if sys.argv[1] == "init":
        opt_usage = "usage: %s <user_id> <password>"%(sys.argv[1])
        opt_usage += "\n*user_id: Your BUGnet account User ID." \
                    +"\n*password: Your BUGnet account password."
        parser = OptionParser(usage = opt_usage)
        (options, args) = parser.parse_args()
        init(args)

main()
