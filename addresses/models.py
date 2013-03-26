import csv

from django.db import models



THIS_DIR = os.path.join(os.path.dirname(__file__))

def city_from_csv(zipcode):
    'grab the city information from the zipcode.csv'
    city, state, latitude, longitude = '', '', '', ''
    csv_file = join(THIS_DIR, 'zipcode.csv')
    with csv.reader(open(csv_file, 'rb')) as reader:
        for row in reader:
            if row and row[0].count(self.zipcode):
                longitude = row[4]
                latitude = row[3]
                city = row[1]
                state = row[2]
    return city, state, latitude, longitude 

class City(models.Model):
    'City in which a person lives. This is USA-centric'
    city = models.CharField('City', max_length=40)
    state = models.CharField('State', max_length=2,
                             choices=STATE_CHOICES, default='MA')
    zipcode = models.CharField('ZIP Code', max_length=5, blank=True,
                               unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   editable=False, default=0,
                                   blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    editable=False, default=0,
                                    blank=True)

    class Meta:
        db_table = 'city'
        ordering = ('zipcode', )
        verbose_name_plural = 'Cities'


    def __unicode__(self):
        return '%s, %s %s' % (self.city, self.state, self.zipcode)

    def __update__(self, zipcode):
        # need to update with regard to zipcode.
        pass
        

    def save(self, **kwargs):
        if self.longitude == 0 and self.latitude == 0:
            c, s, lat, lon = city_from_csv(self.zipcode)
            self.longitude, self.latitude = lon, lat
            self.city, self.state = city, state
        super(City, self).save(**kwargs)
