#!/bin/bash

# This shell script is a wrapper for a set of Python programs that perform
# the following:
# The updatedns.py program calculates a DNS name based on the argument passed to this 
# wrapper script and prepends the current date/time to it. It then creates
# a record set in AWS Route53 hosted zone that contains the calculated DNS
# name and specified IP address.
# Next, the wrapper checks to see if the DNS record has been created by calling
# nslookup and looping until it returns a non-zero code, indicating that the record
# has been published to DNS.
# The wrapper script then calls certbot to request a Let's Encrypt certificate
# From a base nginx install, there is a /var/www/html/template and a
# /etc/nginx/sites-available/template file. These files contain variables
# that are replaced by the setupnewhost.py script and are used to create
# new nginx html content pages and virtual host configuration scripts.
#
# The new nginx virtual hosts are updated with the calculated DNS hostname
# and path to the Let's Encrypt certs. The script also updates the default
# server with the last requested SSL cert. This will allow hosts that don't
# support SNI (network scanners) to find the most current certificate.

# This script is designed to be executed in a cronjob
calcdns=$(/usr/bin/python3 /root/istrustnetup/updatedns.py -d $1 -i $2)
nslookup $calcdns

while [ $? -eq 1 ]
do
        sleep 5
        nslookup $calcdns
done
/usr/bin/certbot --test-cert certonly -d $calcdns -n --standalone
/usr/bin/python3 /root/istrustnetup/setupnewhost.py -d $calcdns
service nginx restart
