#!/usr/bin/env python
"""
I know, this code is ugly as hell. but it works and it's hosted at github/frickler. did you expect something else?
;-)
"""

import sys, os, json
from urllib2 import urlopen, HTTPError
from urllib import urlencode
from xml.etree import ElementTree

GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?region=us&key=' + os.environ['GOOGLE_APIKEY'] + '&'


def parse_feed(rss):
    tree = ElementTree.parse(rss)
    result = []
    for item in tree.iter('item'):
       post = list(item.find(child).text for child in ('title', 'link', 'pubDate'))
       result.append(post)
    return result


def fetch_posts(feed):
    url = feed + '&paged=' if '?' in feed else feed + '?paged='
    posts = []
    for page in range(1,11):  # I'd bet noone wrote more than 10 pages of blogposts
        try:
            rss = urlopen(url + str(page))
            parsed = parse_feed(rss)
            if parsed:
                posts.extend(parsed)
            else:
                break
        except HTTPError:
            break
    return list(reversed(posts))


def to_kml(posts, out_filename):
    """tries to geocode each post by its title. for each title the user is asked
        whether this title place (the post-title) is ok for geocoding. 
        "hello world" cannot be geocoded for example 
    """
    with open(out_filename, 'w') as outfile:
        outfile.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>""")
        all_locations = []
        for title, link, pubDate in posts:
            answer = raw_input("""Place/Post-Title: 

    """ + title + """

    use this place for geocoding? (press enter for yes or type in the correct place):""")
            place = title if len(answer.strip()) == 0 else answer
            url = GEOCODE_URL + urlencode(dict(address=place))
            api_result = json.loads(urlopen(url).read())
            if api_result['status'] == 'OK':
                location = api_result['results'][0]['geometry']['location']
                all_locations.append(str(location['lng']) + ',' + str(location['lat']))
                outfile.write("""
    <Placemark>
      <name><![CDATA[%s]]></name>
      <description>
        <![CDATA[
          <h1>%s</h1>
          <a href="%s">checkout the blogpost</a>
        ]]>
      </description>
      <Point>
        <coordinates>%s,%s</coordinates>
      </Point>
    </Placemark>                
""" % (title,title,link,location['lng'],location['lat']))
            else:
                sys.stderr.write('geocoding %s failed! skipping!' % place)
        outfile.write("""
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>4</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff00</color>
      </PolyStyle>
    </Style>
    <Placemark>
      <name>generated route</name>
      <description>please consider the environment before printing this plot</description>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>
        %s
        </coordinates>
      </LineString>
    </Placemark>
""" % '\n'.join(all_locations))
        outfile.write("""
  </Document>
</kml>""")


def init():
    try:
        posts = fetch_posts(sys.argv[1])
        to_kml(posts, sys.argv[2])
    except IndexError:
        print('USAGE: python traveller.py http://path_to_rss_feed name_of_output.kml')
        sys.exit(1)

if __name__ == '__main__':
    init()

