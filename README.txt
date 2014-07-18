generate a google maps compatible .kml file out of your travel-blog.
it's almost manually but at least the feed parsing and geocoding is automated... ;-)

USAGE:  
GOOGLE_APIKEY='' python traveler.py http://krigu.ch/feed/ krigu.kml
GOOGLE_APIKEY='' python traveler.py http://stef.beikaesers.ch/?feed=rss2 stef.kml

Example:
https://maps.google.ch/maps?q=https:%2F%2Fraw.githubusercontent.com%2Ffrickler%2Ftraveler%2Fmaster%2Fkrigu.kml&hl=en&sll=46.813187,8.22421&sspn=3.150545,6.086426&t=m&z=3
