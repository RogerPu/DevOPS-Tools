#!/usr/bin/env python
#Auth RogerPuX Plateno Groups Inc.
import pycurl
try:
	from io import BytesIO
except ImportError:
	from StringIO import StringIO as BytesIO

buffer = BytesIO()
c = pycurl.Curl()
#c.setopt(c.URL,'plateno.com')
c.setopt(c.URL,'plateno.com')
c.setopt(c.FOLLOWLOCATION,True)
c.setopt(c.WRITEDATA,buffer)
c.perform()

# HTTP response code, e.g. 200.
print('status: %d' % c.getinfo(c.RESPONSE_CODE))
# Elapsed time for the transfer.
print('status: %d' % c.getinfo(c.TOTAL_TIME))


# getinfo must be called before close.
c.close()
