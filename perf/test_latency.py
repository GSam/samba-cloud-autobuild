#!/usr/bin/env python

import optparse
import sys
import os
import unittest
import samba
import samba.getopt as options
import random

from samba.tests.subunitrun import SubunitOptions, TestProgram

from samba.tests import delete_force
from samba.dcerpc import security, misc
from samba.samdb import SamDB
from samba.auth import system_session
from samba.ndr import ndr_unpack
from ldb import Message, MessageElement, Dn, LdbError
from ldb import FLAG_MOD_ADD, FLAG_MOD_REPLACE, FLAG_MOD_DELETE
from ldb import SCOPE_BASE, SCOPE_SUBTREE, SCOPE_ONELEVEL

class MatchRulesTests(samba.tests.TestCase):
    def setUp(self):
        super(MatchRulesTests, self).setUp()
        self.lp = lp
        self.ldb = SamDB(host, credentials=creds, session_info=system_session(lp), lp=lp)
        self.base_dn = self.ldb.domain_dn()
        self.ou = "OU=pid%s,%s" % (os.getpid(), self.base_dn)
        self.ou_users = "OU=users,%s" % self.ou
        self.ou_groups = "OU=groups,%s" % self.ou
        self.ou_computers = "OU=computers,%s" % self.ou

        self.n_groups = 1

        try:
            for i in range(self.n_groups):
                delete_force(self.ldb, "cn=g%d,%s" % (i + 1, self.ou_groups))
                delete_force(self.ldb, "cn=u%d,%s" % (i + 1, self.ou_users))

            delete_force(self.ldb, "cn=c1,%s" % self.ou_computers)
            delete_force(self.ldb, "cn=c2,%s" % self.ou_computers)
            delete_force(self.ldb, "cn=c3,%s" % self.ou_computers)
            delete_force(self.ldb, self.ou_users)
            delete_force(self.ldb, self.ou_groups)
            delete_force(self.ldb, self.ou_computers)
            delete_force(self.ldb, "OU=o4,OU=o3,OU=o2,OU=o1,%s" % self.ou)
            delete_force(self.ldb, "OU=o3,OU=o2,OU=o1,%s" % self.ou)
            delete_force(self.ldb, "OU=o2,OU=o1,%s" % self.ou)
            delete_force(self.ldb, "OU=o1,%s" % self.ou)
            delete_force(self.ldb, "CN=e2,%s" % self.ou)
            delete_force(self.ldb, "CN=e1,%s" % self.ou)
            delete_force(self.ldb, self.ou)
        except Exception, e:
            print e


        try:
            # Add a organizational unit to create objects
            self.ldb.add({
                "dn": self.ou,
                "objectclass": "organizationalUnit"})


            # Create OU for users and groups
            self.ldb.add({
                "dn": self.ou_users,
                "objectclass": "organizationalUnit"})
            self.ldb.add({
                "dn": self.ou_groups,
                "objectclass": "organizationalUnit"})
            self.ldb.add({
                "dn": self.ou_computers,
                "objectclass": "organizationalUnit"})

            # Add groups
            for i in range(self.n_groups):
                self.ldb.add({
                    "dn": "cn=g%d,%s" % (i + 1, self.ou_groups),
                    "objectclass": "group" })
        except Exception, e:
            print e


    def tearDown(self):
        super(MatchRulesTests, self).tearDown()
        try:
            for i in range(self.n_groups):
                delete_force(self.ldb, "cn=g%d,%s" % (i + 1, self.ou_groups))
                delete_force(self.ldb, "cn=u%d,%s" % (i + 1, self.ou_users))

            delete_force(self.ldb, "cn=c1,%s" % self.ou_computers)
            delete_force(self.ldb, "cn=c2,%s" % self.ou_computers)
            delete_force(self.ldb, "cn=c3,%s" % self.ou_computers)
            delete_force(self.ldb, self.ou_users)
            delete_force(self.ldb, self.ou_groups)
            delete_force(self.ldb, self.ou_computers)
            delete_force(self.ldb, "OU=o4,OU=o3,OU=o2,OU=o1,%s" % self.ou)
            delete_force(self.ldb, "OU=o3,OU=o2,OU=o1,%s" % self.ou)
            delete_force(self.ldb, "OU=o2,OU=o1,%s" % self.ou)
            delete_force(self.ldb, "OU=o1,%s" % self.ou)
            delete_force(self.ldb, "CN=e2,%s" % self.ou)
            delete_force(self.ldb, "CN=e1,%s" % self.ou)
            delete_force(self.ldb, self.ou)
        except Exception, e:
            print e

    def test_u1_member_of_g4(self):
        i = 0
        import time
        print "KEYS: total add modify delete"

        while True:
            group = i % self.n_groups + 1

            start = time.time()
            self.ldb.add({
                "dn": "cn=u%d,%s" % (group, self.ou_users), "objectclass": "user"})
            end_add = time.time()

            start_mod = time.time()

            m = Message()
            m.dn = Dn(self.ldb, "CN=g%d,%s" % (group, self.ou_groups))
            m["member"] = MessageElement("cn=u%d,%s" % (group, self.ou_users),
                                         FLAG_MOD_ADD, "member")
            self.ldb.modify(m)
            end_mod = time.time()

            delete_force(self.ldb, "cn=u%d,%s" % (i, self.ou_users))
            end = time.time()
            print end - start, end_add - start, end_mod - start_mod, end - end_mod
            i += 1            
            #time.sleep(random.random())

parser = optparse.OptionParser("match_rules.py [options] <host>")
sambaopts = options.SambaOptions(parser)
parser.add_option_group(sambaopts)
parser.add_option_group(options.VersionOptions(parser))

# use command line creds if available
credopts = options.CredentialsOptions(parser)
parser.add_option_group(credopts)
opts, args = parser.parse_args()
subunitopts = SubunitOptions(parser)
parser.add_option_group(subunitopts)

if len(args) < 1:
    parser.print_usage()
    sys.exit(1)

host = args[0]

lp = sambaopts.get_loadparm()
creds = credopts.get_credentials(lp)

if not "://" in host:
    if os.path.isfile(host):
        host = "tdb://%s" % host
    else:
        host = "ldap://%s" % host

TestProgram(module=__name__, opts=subunitopts)
