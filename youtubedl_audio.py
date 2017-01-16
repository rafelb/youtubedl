##################################################################
# Script to extract audio from youtube video
# written in python 3.5.2
#
# Should not be used to retrieve copywrite protected audio
#
# in order to run script:
# use pip to install youtube-dl
# create folder in windows "D:/Downloads/MP3/"


import youtube_dl, shutil, os, subprocess, re
import urllib.request as ur
##################################################################
# fixed string variables
strLeft     = '<title>'                             # needed to extract final filename from youtube title
strRight    = ' - YouTube</title>'                  # needed to extract final filename from youtube title
path        = os.getcwd()+'/MP3/'                   # output dir
convpath    = os.getcwd()+'/ffmpeg/bin/'            # for converting temporary file to mp3
##################################################################
def getResponseCode(url):                           # Check if url exists
    conn = ur.urlopen(url)
    return conn.getcode()
##################################################################

path = path.replace('\\','/')

try:
    os.stat(path)
except:
    os.mkdir(path) 

Document = input('Geef url van pagina: ')

try:
    getResponseCode(Document)
except:
    print('Url bestaat niet')
    input('Druk op een toets...')
    raise SystemExit()

lcTmpfile = path + Document.rsplit('=',1)[1]        # Get all characters after last occurence of '=' to determine temporary filename -
                                                    # needed for conversion to mp3

                                                    # Get a file-like object in binary mode for the Web site's page and read from the
                                                    # object, storing the page's contents in 'filehandler'.
filehandler = ur.urlopen(Document)
                                                    # The bytes type was introduced in Python 3

for line in [x.decode('utf8').strip() for x in filehandler.readlines()]: # Decode bytes while adding to the list and devide it into separate lines.
    try:
        lcTmpFilename = (line.split(strLeft)[1]).split(strRight)[0] # filename 
    except IndexError:
        pass
    
options = options = { 
    'format': 'bestaudio/best', # choice of quality
    'extractaudio' : True,      # only keep the audio
    'audioformat' : "mp3",      # convert to mp3 
    'outtmpl': '%(id)s',        # name the file the ID of the video
    'noplaylist' : True,        # only download single song, not playlist
}
    
os.chdir (path)

with youtube_dl.YoutubeDL(options) as ydl:          # import raw audio
    ydl.download([Document])                        # save temporary file as the YouTube ID

# the final filename is a bit messy
# below this is (mostly) fixed
lcFile = lcTmpFilename.replace(' ', '_') # To convert to mp3, filename cannot contain spaces

# a regular filename cannot contain certain characters, so they must be replaced
lcFile = lcFile.replace('\\','_')
lcFile = lcFile.replace('/','_')
lcFile = lcFile.replace(':','_')
lcFile = lcFile.replace('<','_')
lcFile = lcFile.replace('>','_')
lcFile = lcFile.replace('?','_')
lcFile = lcFile.replace('"','_')
lcFile = lcFile.replace('|','_')
lcFile = lcFile.replace('&nbsp;','_')
lcFile = lcFile.replace('&quot;','_')
lcFile2 = lcFile.replace('&iexcl;','¡')
lcFile2 = lcFile.replace('&amp;', '&')

re.sub(r'&[0-9a-zA-Z];',        # 0..9, a..z and A..Z
       '',                    # replaced with nothing
       lcFile2)

print('lcFile: '+lcFile2)
convpath = convpath.replace('\\', '/')
print('convpath: '+ convpath)
# the file should be of type mp3 and located in D:\Downloads\MP3\
lcFile = path + lcFile + '.mp3'
# somehow the retrieved file is not exactly mp3, so we have to convert temporary file 
# to mp3 and alter filename allready a bit using a third party program
subprocess.call(convpath + 'ffmpeg -i ' + lcTmpfile + ' -vn -ar 44100 -ac 2 -f mp3 ' + lcFile)

# rename file to final name
lcFinalFilename = lcFile.replace('_', ' ')
# because of all the replacements above there could be more than one space next to another
# there should be a maximum of one space between two other characters hence the regex below
lcFinalFilename = re.sub(' +',' ',lcFinalFilename)

os.rename(lcFile, lcFinalFilename)

# remove temporary data
os.remove(lcTmpfile)

# end program
print('Klaar!')
lcFinalFilename = lcFinalFilename.replace('/','\\')
print('Bestand opgeslagen als: ' + lcFinalFilename)
input('Druk op een toets...')

