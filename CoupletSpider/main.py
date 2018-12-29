from scrapy import cmdline
import commands

if __name__ == '__main__':
    commands.getstatusoutput('rm couplet.csv')
    cmdline.execute("cr crawl couplet-xpath -o couplet.csv -t csv".split())