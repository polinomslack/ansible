S = 'my.song.mp3 11b\ngreatSong.flac 1000b\nnot3.txt 5b\nvideo.mp4 200b\ngame.exe 100b\nmov!e.mkv 10000b'
def solution(S):
    music = 0
    images = 0
    movies = 0
    other = 0
    a=S.split('\n')
    for i in a:
        suba=i.split(' ')
        if (suba[0].split('.')[-1]) in ('mp3','aac','flac'):
            music+=int(suba[1][0:-1])
        elif (suba[0].split('.')[-1]) in ('jpg','bmp','gif'):
            images+=int(suba[1][0:-1])
        elif (suba[0].split('.')[-1]) in ('mp4','avi','mkv'):
            movies+=int(suba[1][0:-1])
        else:
            other+=int(suba[1][0:-1])
    result="music "+str(music)+"b\nimages "+str(images)+"b\nmovies "+str(movies)+"b\nother "+str(other)+"b"
    return result
print (solution(S))