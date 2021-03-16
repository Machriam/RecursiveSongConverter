# Only runs under Linux with mplayer, ffmpeg and lame installed!
# Traverses recursively all folders and converts flac and wma files to mp3.
# Filenames with " ' ´ ` are replaced with names without those.
import os
import shlex


class Metadata:
    album = ""
    albumArtist = ""
    track = ""
    artist = ""
    title = ""
    year = ""
    genre = ""

    def readMetadata(self, metadata, file):
        fout = os.popen("ffprobe "+shlex.quote(file) +
                        " 2>&1 | grep -w -m 1 "+metadata)
        res = fout.read().split(":")
        res = res[-1].strip()
        return shlex.quote(res)

    def __init__(self, file, name):
        if (file.endswith(".wma")):
            self.album = self.readMetadata("album", file)
            self.albumArtist = self.readMetadata("album_artist", file)
            self.track = self.readMetadata("track", file)
            self.artist = self.readMetadata("artist", file)
            self.title = self.readMetadata("title", file)
            self.year = self.readMetadata("WM/Year", file)
            self.genre = self.readMetadata("genre", file)
        elif (file.endswith(".flac")):
            self.album = self.readMetadata("ALBUM", file)
            self.albumArtist = self.readMetadata("album_artist", file)
            self.track = self.readMetadata("track", file)
            self.artist = self.readMetadata("ARTIST", file)
            self.title = self.readMetadata("TITLE", file)
            self.year = self.readMetadata("DATE", file)
            self.genre = self.readMetadata("GENRE", file)
        elif (file.endswith(".ogg")):
            self.title = name
            self.album = ""
            self.albumArtist = ""
            self.track = ""
            self.artist = ""
            self.year = ""
            self.genre = ""
        elif (file.endswith(".m4a")):
            self.album = self.readMetadata("album", file)
            self.albumArtist = self.readMetadata("album_artist", file)
            self.track = self.readMetadata("track", file)
            self.artist = self.readMetadata("artist", file)
            self.title = self.readMetadata("title", file)
            self.year = self.readMetadata("date", file)
            self.genre = self.readMetadata("genre", file)
        self.album = shlex.quote(self.album)
        self.albumArtist = shlex.quote(self.albumArtist)
        self.track = shlex.quote(self.track)
        self.artist = shlex.quote(self.artist)
        self.title = shlex.quote(self.title)
        self.year = shlex.quote(self.year)
        self.genre = shlex.quote(self.genre)


def convertFileName(file):
    oldFileName = file
    file = file.replace("'", "")
    file = file.replace('"', "")
    file = file.replace('`', "")
    file = file.replace('´', "")
    command = "mv {} {}".format(shlex.quote(oldFileName), shlex.quote(file))
    os.system(command)
    return file


def isValidFileType(type):
    if (file.endswith(".wma") or file.endswith(".flac") or file.endswith(".ogg") or file.endswith(".m4a")):
        return True


for root, dirs, files in os.walk("."):
    for name in files:
        file = os.path.join(root, name)
        if (isValidFileType(file)):
            print("converting", file)
            file = convertFileName(file)
            metadata = Metadata(file, name)
            print(metadata.album, metadata.albumArtist,
                  metadata.track, metadata.artist, metadata.title)
            new_file = file[:-len(file.split(".")[-1])] + "mp3"
            command = "mplayer -ao pcm \"" + file + "\""
            os.system(command)
            command = "lame --tt {} --ta {} --tl {} --tn {} --ty {} --tg {} -b 320 audiodump.wav {}".format(
                metadata.title, metadata.artist, metadata.album, metadata.track, metadata.year, metadata.genre, shlex.quote(new_file))
            print("#"*200)
            print(command)
            print("#"*200)
            os.system(command)
            command = "rm audiodump.wav"
            os.system(command)
            if (os.path.isfile(new_file)):
                command = "rm "+shlex.quote(file)
                os.system(command)
print("Finished. Bye, Bye")
