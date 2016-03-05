#!/usr/bin/env python

import sys
import urllib2
import json
import logging

log = logging.getLogger(__name__)

HOST = "localhost"
PACKAGE = "com.cloudmon.demo"
CLASS_NAME = "ServiceManager"
JOLOKIA_PORT = 7000
JOLOKIA_TIMEOUT = 1.0


def read_attribute(attribute):
    url = "http://%(host)s:%(port)d/jolokia/?maxCollectionSize=1000000&maxObjects=1000000" % dict(host=HOST, port=JOLOKIA_PORT)
    data = json.dumps(dict(type='read',
                       mbean='%(package)s:type=%(class_name)s' % dict(package=PACKAGE, class_name=CLASS_NAME),
                       attribute=attribute))

    log.debug('read_attribute(): %s, %s', url, data)
    opener = urllib2.build_opener()
    result = json.loads(opener.open(url, data, timeout=JOLOKIA_TIMEOUT).read())
    if 'error' in result:
        raise Exception('jolokia reported error: %s/%s/%s - %s' % (PACKAGE, CLASS_NAME, attribute, result['error']))
    if 'value' not in result:
        raise Exception('jolokia reported unknown attribute: %s/%s/%s' % (PACKAGE, CLASS_NAME, attribute))
    return result['value']


def write_attribute(attribute, value):
    url = "http://%(host)s:%(port)d/jolokia/?maxCollectionSize=1000000&maxObjects=1000000" % dict(host=HOST, port=JOLOKIA_PORT)
    data = json.dumps(dict(type='write',
                           mbean='%(package)s:type=%(class_name)s' % dict(package=PACKAGE, class_name=CLASS_NAME),
                           attribute=attribute,
                           value=value))

    log.debug('write_attribute(): %s, %s', url, data)
    opener = urllib2.build_opener()
    result = json.loads(opener.open(url, data, timeout=JOLOKIA_TIMEOUT).read())
    if 'error' in result:
        raise Exception('jolokia reported error: %s/%s/%s - %s' % (PACKAGE, CLASS_NAME, attribute, result['error']))
    if 'status' not in result:
        raise Exception('missing status in response - not sure if the attribute got set')


def usage():
    print """
    read and set demo app management attribute

    demomgr read [attribute e.g. UserServiceVersion]
    demomgr write [attribute e.g. UserServiceVersion] [value]
    """


def main(argv):
    if len(argv) < 2:
        sys.exit(usage())

    action, attribute = argv[0], argv[1]
    if action.lower() == "read":
        print "%s: %s" % (attribute, read_attribute(attribute))
    elif action.lower() == "write":
        if len(argv) != 3:
            usage()
        else:
            write_attribute(attribute, argv[2])
            print "write succeeded. read back:"
            print "%s: %s" % (attribute, read_attribute(attribute))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(usage())
    main(sys.argv[1:])
