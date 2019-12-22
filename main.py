# -*- encoding: utf-8 -*-


import datetime
import ssl_check

if __name__ == '__main__':
    filename = 'sites.txt'
    with open(filename) as fp:
        for cnt, line in enumerate(fp):
            line = line.replace('\n', '')
            print("Line {}: {}".format(cnt, line))
            hostinfo = ssl_check.check_it_out(line, 443)
            print('Expiration Date: {}'.format(hostinfo.cert.not_valid_after))
            recent_time = datetime.datetime.now()
            delta = hostinfo.cert.not_valid_after - recent_time
            print('{} days left'.format(delta.days))