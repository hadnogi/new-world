from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import time
import subprocess
import mechanize
def login(p):
   bro= mechanize.Browser()
   bro.set_handle_robots(False)
   while 1:
      b=bro.open("https://ko.wikipedia.org/w/index.php?title=%ED%8A%B9%EC%88%98:%EB%A1%9C%EA%B7%B8%EC%9D%B8&returnto=%EC%9C%84%ED%82%A4%EB%B0%B1%EA%B3%BC:%EB%8C%80%EB%AC%B8")
      bro.form=list(bro.forms())[0]
      bro["wpName"]="a"
      bro["wpPassword"]="a"
      bro.submit()
      if re.search("captcha",str(b.get_data())):
         print "captcha"
         p.terminate()
         p.kill()
         break;
      else:
         print "safe"
   

def vpn():
        url="http://www.vpngate.net/en/"
        site=urllib2.urlopen(url)
        soup=BeautifulSoup(site.read(),"html.parser")
        sie=soup.find_all("td",{"vg_table_row_0","vg_table_row_1"})
        si=re.findall("do_openvpn.aspx?.*?\"",str(sie))
        i=1
        for do in si:
                do=re.sub("amp;","",do)
                do=re.sub("\"","",do)
                site=str(urllib2.urlopen(url+"/"+do).read())
                down=re.findall("/common/openvpn_download.aspx.*?.ovpn",site)
                for dodo in down:
                        dodo=re.sub("amp;","",dodo)
                        if(re.search("net_tcp",dodo)):
                                urllib.urlretrieve("http://www.vpngate.net"+dodo,"vpn")
                                print(dodo)
                                p=subprocess.Popen("sudo openvpn --connect-retry-max 1 --remap-usr1 SIGTERM --config vpn",shell=True,stdout=subprocess.PIPE)
                                for line in iter(p.stdout.readline,b''):
                                        if(re.search("Completed",str(line))):
                  print "ip change"
                                                p.stdout.close()
                                                login(p)
                                                p.wait()
                                                break
vpn()   
