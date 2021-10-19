import simplekml
import glob
import webbrowser
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS


#extrat exif from images
def get_exif(image):
    return image._getexif()


#extract GPS info from exif
def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


#dms to dd converter
def get_decimal_from_dms(dms, ref):
    degrees = float(dms[0])
    minutes = float(dms[1] / 60.0)
    seconds = float(dms[2] / 3600.0)

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


#return GPs position in latitude and logitude format
def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    return (lat,lon)


def main():

    kml = simplekml.Kml()
    for filename in glob.iglob("E:" + '**/*.jpg', recursive=True):
        img = Image.open(filename)

        #verify() raises an exception if there is a problem with the image and does nothing otherwise
        try:
            img.verify()
            print('Valid image')
        except Exception:
            print('Invalid image')

        #exception for the images without exif
        try:
            exif = get_exif(img)
            geotags = get_geotagging(exif)
            coordinates = get_coordinates(geotags)

            #add point on the kml file
            kml.newpoint(coords = [(coordinates[1], coordinates[0])])
        except Exception:
            pass

    #save kml file
    kml.save('CoordsFromImages.kml')
    #open Google Maps
    webbrowser.open('https://www.google.com/maps/d/u/0/?hl=en')


if __name__ == '__main__':
    main()

