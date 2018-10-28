import re
from collections import defaultdict


def read_data():
    '''
    read playlist data.
    '''
    user_playlist = defaultdict(set)
    playlist_dict = defaultdict(list)
    song_count = defaultdict(int)
    song_set = set()
    song_id_dict = dict()
    error = []
    reg0 = re.compile(r'(\\)*\"')
    reg1 = re.compile(r'\)|\(|’|(\\)*\'|\?')
    reg2 = re.compile(",")
    reg3 = re.compile(r"(\\)+\,")
    reg4 = re.compile(r"(\\)+")
    with open("playlist_ds.csv","rt") as f:
        for line in f:
            line = line.lower()
            cur = reg0.subn("",line.rstrip())[0]
            cur = reg1.subn("",cur)[0]
            cur = reg3.subn(" ",cur)[0]
            cur = reg2.split(cur)
            cur = [reg4.subn("",item)[0] for item in cur]
            try:
                user,artist,song,plist = cur
            except Exception as e:
                print(e)
                print("fail at unzip line at: \n  {}".format(line))
                break
            u_plist = ">>".join([user,plist])
            a_song = ">>".join([artist,song])
            user_playlist[user].add(u_plist)
            playlist_dict[u_plist].append(a_song)
            if a_song not in song_set:
                song_id_dict[a_song] = len(song_set)
                song_set.add(a_song)
            song_count[a_song] = song_count[a_song]  +1
    return user_playlist,playlist_dict,song_count,song_id_dict,song_set


def searchsong(song_count=None,keyword=None,reg = None,title=True,artist=True,n=None):
    '''
    find songs by a keyword or a compiled reg exp.
    you can specify either to search by artist or song title, or both.
    the song is ordered by counts and show n results.
    '''
    if reg is None:        
        reg = re.compile(keyword,flags=re.IGNORECASE)
    res =[]
    if title and artist:
        for item,count in song_count.items():
                if reg.findall(item):
                    res.append([item,count])
    elif title and not artist:
        for item,count in song_count.items():
                *_,cur = item.split(">>")
                if reg.findall(cur):
                    res.append([item,count])
    elif artist and not title:
        for item,count in song_count.items():
                cur,*_ = item.split(">>")
                if reg.findall(cur):
                    res.append([item,count])
    res = sorted(res,key=lambda x:x[1],reverse=True)
    if n:
        res = res[0:n]
    return res     

          