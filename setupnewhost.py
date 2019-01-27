import sys
import getopt
import pprint
import shutil
import fileinput
import os
import datetime
import bs4

def main(argv):
    dnsname = ''
    ipaddress = ''
    try:
      opts, args = getopt.getopt(argv,"d:",["dnsName="])
    except getopt.GetoptError:
      print('updatedns.py -d <dnsname>')
      sys.exit(2)

    for opt,arg in opts:
        if opt in ("-d","--dnsname"):
            dnsname = arg

    defaultdoc = '/var/www/html/index.nginx-debian.html'
    templatefile = '/etc/nginx/sites-available/template'
    sitefile = '/etc/nginx/sites-available/{}'.format(dnsname)
    defaulttemplatefile = '/etc/nginx/sites-available/deftemplate'
    defaultfile = '/etc/nginx/sites-available/default'
    shutil.copyfile(defaulttemplatefile,defaultfile)
    shutil.copyfile(templatefile,sitefile)
    templatewwwfile = '/var/www/html/template.html'
    sitewwwfile = '{}.html'.format(dnsname)
    shutil.copyfile(templatewwwfile,'/var/www/html/{}'.format(sitewwwfile))
    with fileinput.input(files=(sitefile,'/var/www/html/{}'.format(sitewwwfile),defaultfile),inplace=True) as f:
        for line in f:
            if(line.count("REPLACEMENAME") > 0):
                newline = line.replace("REPLACEMENAME",dnsname)
                print(newline,end='')
            elif(line.count("REPLACEMEPAGE") > 0):
                newline = line.replace("REPLACEMEPAGE",sitewwwfile)
                print(newline,end='')
            else:
                print(line,end='')

    with open(defaultdoc) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt,features="html.parser")
    bodytag = soup.body
    bodytag.append("Virtualhost: {}".format(dnsname))
    brtag = bs4.Tag(name = "br")
    bodytag.append(brtag)
    with open(defaultdoc,"w") as outf:
        outf.write(str(soup))

    os.symlink(sitefile,'/etc/nginx/sites-enabled/{}'.format(dnsname))
if __name__ == "__main__":
    main(sys.argv[1:])
