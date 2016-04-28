import pycurl
import send_messsage
import time

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

def response_code_and_time_check(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    #c.setopt(c.URL,'plateno.com')
    c.setopt(c.URL,url)
    c.setopt(c.FOLLOWLOCATION,True)
    c.setopt(c.WRITEDATA,buffer)
    c.perform()
    res_code = c.getinfo(c.RESPONSE_CODE)
    res_time = c.getinfo(c.TOTAL_TIME)
    c.close()
    return  (res_code,res_time)


# HTTP response code, e.g. 200.
#print('status: %d' % c.getinfo(c.RESPONSE_CODE))
# Elapsed time for the transfer.
#print('Time Cost: %d' % c.getinfo(c.TOTAL_TIME))

def alarm(url='http://localhost'):

    var = 1
    while var == 1:
        count = 1
        while count <= 2 :
            res_code,res_time=response_code_and_time_check(url)
            if res_code != 200 :
                print('Not 200 %d count' % (count))
                print('Error code %d' % (res_code))
                time.sleep(3)
                count = count + 1
            else:
                print('Web status: OK')
                count = 0
                return
alarm()

    # if  res_code != 200:
    #     count = count + 1
    #     return
    # time.sleep(30)
    # res_code,res_time=response_code_and_time_check(url)
    # if res_code != 200:
    #     count = count + 1
        # if count > 2 :
        #     for i in [18520138780]:
        #         print('be in send messages phase')
        #         send_messsage.send_messages(i,"mysql",'10.100.112.162')




# getinfo must be called before close.

