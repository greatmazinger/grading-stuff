import os
import re
import pprint
from shutil import copy2

pp = pprint.PrettyPrinter(indent = 4)

def verify_users(summary = {}):
    global pp
    problist = summary.keys()
    users = {}
    for prob in problist:
        users[prob] = set( summary[prob].keys() )
    problist = sorted(problist)
    missing = dict( [ (prob, set([])) for prob in problist ] )
    for pindex in xrange(len(problist) - 1):
        prob1 = problist[pindex]
        prob2 = problist[pindex + 1]
        if not ((users[prob1] ^ users[prob2]) == 0):
            if (users[prob1] <= users[prob2]):
                missing[prob1] = users[prob2] - users[prob1]
            else:
                missing[prob2] = users[prob1] - users[prob2]
    return missing

hw = "hw3"
myre = re.compile("hw3p(.)")
dir_re = re.compile("(.*)\.([0-9]+)$")
summary = {}
for item in os.listdir("."):
    m = myre.match(item)
    if m:
        problem = m.group(1)
        print item, problem
        print "=======[ %s ]===================================================================" % item
        filedict = {}
        os.chdir(item)
        for directory in os.listdir("."):
            mdir = dir_re.match(directory)
            if mdir and os.path.isdir(directory):
                print directory + ":",
                # print directory, mdir.group(1), mdir.group(2)
                username = mdir.group(1)
                subnum = int(mdir.group(2))
                if mdir.group(1) == "rveroy":
                    print "SKIP:", directory
                    continue
                pdf = "p" + problem + ".pdf"
                target = os.path.join(directory, pdf)
                if not os.path.isfile(target):
                    print "XXX: Can't find %s" % str(target)
                    continue
                print "OK"
                if (username in filedict) and (filedict[username]["subnum"] < subnum):
                    print "LATER SUB."
                    filedict[username] = { "target" : target, "subnum" : subnum, "dir" : item }
                elif username not in filedict:
                    filedict[username] = { "target" : target, "subnum" : subnum, "dir" : item }
                else:
                    print "Ignoring earlier sub:", directory
        os.chdir("..")
        assert(int(problem) not in filedict)
        summary[int(problem)] = filedict
pp.pprint(summary)
print "#######[ MISSING ]##############################################################"
missing = verify_users(summary)
pp.pprint(missing)
for prob, mset in missing.iteritems():
    if len(mset) > 0:
        print "WARNING missing from problem %d:" % prob
        pprint(list(mset))
print "#######[ MERGING ]##############################################################"
print "Current directory: %s" % os.getcwd()
print "Making directory MERGED..."
if not os.path.isdir("MERGED"):
    os.mkdir("MERGED")
else:
    print "WARNING!!!!! MERGED exists!!!!!!"
    raw_input("Please enter to continue:")
for prob, userdict in summary.iteritems():
    for user, valdict in userdict.iteritems():
        target = os.path.join(valdict["dir"], valdict["target"])
        subnum = valdict["subnum"]
        print "Moving [ %d -- %s ] for user %s..." % (subnum, target, user)
        userpath = os.path.join("MERGED", "%s.%d" % (user, 1))
        if not os.path.isdir(userpath):
            os.mkdir(userpath)
        copy2(target, userpath)
print "########[ DONE ]################################################################"
