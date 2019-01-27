import boto3
import pprint
import getopt
import sys
import datetime
    
def main(argv):
    dnsname = ''
    ipaddress = ''
    rightnow = datetime.datetime.today().strftime('%Ya%ma%da%Ha%Ma%S')
    try:
      opts, args = getopt.getopt(argv,"d:i:",["dnsName=","ipAddr="])
    except getopt.GetoptError:
      print('updatedns.py -d <dnsname> -i <ip Address>')
      sys.exit(2)
    
    for opt,arg in opts:
        if opt in ("-d","--dnsname"):
            dnsname = '{}b{}'.format(rightnow,arg)
        elif opt in ("-i","--ipAddr"):
            ipaddress = arg

    #pp = pprint.PrettyPrinter(indent=4)
    
    client = boto3.client('route53')
    response = client.list_resource_record_sets(
        HostedZoneId='Z16N5SV2NYDNYA',
    )
    #pp.pprint(response)
    response = client.change_resource_record_sets(
        HostedZoneId='Z16N5SV2NYDNYA',
        ChangeBatch={
            'Comment': 'Automated record',
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': dnsname,
                        'Type': 'A',
                        'TTL': 300,
                        'ResourceRecords': [
                            {
                                'Value': ipaddress,
                            },
                        ]
                    }
                },
            ]
        }
    )
    print(dnsname)
    

if __name__ == "__main__":
    main(sys.argv[1:])
