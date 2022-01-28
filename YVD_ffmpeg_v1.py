from pytube import Playlist
from pytube import Channel
from pytube import YouTube
from tqdm import tqdm
import subprocess
import requests
import codecs
import glob
import os
import re

print("DISCLAIMER:")
print("This is the first version of this program.")
print("There may be bugs and issues, which if you do experience please report it on the Github project page ")
print("Thank you for your understanding.","\n")

print("Welcome to YouTube Video Downloader!")
print("The easiest YouTube downnloading tool created by Shadow Walker (https://github.com/SHADOW-13-WALKER)","\n")

continu = "y"
while continu != "n":
    print("Menu :","\n")
    print("Videos :")
    print("1. Download a youtube video")
    print("2. Download only music from a video (mp3 format)")
    print("")
    print("Playlists :")
    print("3. Download all the videos in a playlist")
    print("")
    print("Channels :")
    print("4. Get the list of videos from a Youtube channel")
    print("5. Download all the videos from a Youtube channel")
    print("")
    choice = int(input("Please enter the number of the option you want to select (number between 1-5): "))
    print("")
    if choice == 1:
        print("Downloading a youtube video :","\n")

        link = input('Paste the link of the video : ')

        yt = YouTube(link)
        ## Video details
        dirname = "Youtube/"
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        else:
            dirname

        print("The video title is :",yt.title)
        print("The length of the video is :",yt.length,"s")
        print("This video was published on :",yt.publish_date)
        print("The video author is :",yt.author)
        print("This video have :",yt.views,"views")
        print("")
        resol = yt.streams.order_by('resolution').filter(only_video=True)
        print('******************************VIDEO******************************')
        for res in resol:
            print("itag = ",str(res.itag)," : ",res.resolution," ",str(res.fps),"fps")
        print('*****************************************************************')
        print('\n')
        print('******************************AUDIO******************************')
        audio_video = yt.streams.filter(only_audio=True)
        for audio_tag in audio_video:
            print("itag = ",str(audio_tag.itag)," : abr=",audio_tag.abr)
        print('*****************************************************************')
        print('\n')

        itag_v = input('itag video = ')
        itag_a = input('itag audio = ')
        ## Downloading the video
        yt.streams.get_by_itag(itag_v).download(dirname,filename_prefix = "video_")
        print("The video has been downloaded")
        ## Downloading the audio
        yt.streams.get_by_itag(itag_a).download(dirname,filename_prefix = "audio_")
        print("The audio has been downloaded")

        ## Downloading the thumbnail
        r0 = requests.get("https://img.youtube.com/vi/"+yt.video_id+"/maxresdefault.jpg")
        r1 = requests.get("https://i.ytimg.com/vi/"+yt.video_id+"/hqdefault.jpg")
        r2 = requests.get("https://i.ytimg.com/vi/"+yt.video_id+"/hq720.jpg")

        if len(r0.content) >= len(r1.content) and len(r0.content) >= len(r2.content):
            rb = r0
        elif len(r1.content) >= len(r0.content) and len(r1.content) >= len(r2.content):
            rb = r1
        elif len(r2.content) >= len(r0.content) and len(r2.content) >= len(r1.content):
            rb = r2
        open(dirname+yt.video_id+".jpg", 'wb').write(rb.content)

        print("The thumbnail has been downloaded")

        ## Downloading the description
        f = codecs.open(dirname+yt.video_id+".txt","w", "utf-8")
        f.write(yt.description)
        f.close()

        print("The description has been downloaded")

        directv = glob.glob(dirname+'video_'+"*.*m*")
        video_file = directv[0]
        directa = glob.glob(dirname+'audio_'+"*")
        audio_file = directa[0]

        file_name = video_file[len(dirname)+6:len(video_file)-4]

        ## load the video
        video = video_file
        video_output_mp3 = dirname+file_name + "_final_mp3.mp4"
        ## load the audio
        audio = audio_file
        audio_mp3 = dirname+file_name + ".mp3"
        ## convert the audio into mp3
        cmd = f'ffmpeg_v5.0.exe -i "{audio}" -vn -ab 128k -ar 44100 -y "{audio_mp3}"'
        print(cmd)
        subprocess.check_output(cmd, shell=True)
        ## add the audio to the video
        cmd = f'ffmpeg_v5.0.exe -i "{video}" -i "{audio_mp3}" -c copy "{video_output_mp3}"'
        print(cmd)
        subprocess.check_output(cmd, shell=True)

        os.remove(video_file)
        os.remove(audio_file)
        os.remove(dirname+file_name+".mp3")

        os.rename(dirname+file_name+"_final_mp3.mp4",dirname+file_name+".mp4")
        os.rename(dirname+yt.video_id+".jpg",dirname+file_name+".jpg")
        os.rename(dirname+yt.video_id+".txt",dirname+file_name+".txt")

    if choice == 2:
        print("Downloading a music video :","\n")

        link = input('Paste the link of the video : ')

        yt = YouTube(link)
        ## Video details
        dirname = "Youtube/"
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        else:
            dirname

        print("The video title is :",yt.title)
        print("The length of the video is :",yt.length,"s")
        print("This video was published on :",yt.publish_date)
        print("The video author is :",yt.author)
        print("This video have :",yt.views,"views")
        print("")
        print('******************************AUDIO******************************')
        audio_video = yt.streams.filter(only_audio=True)
        for audio_tag in audio_video:
            print("itag = ",str(audio_tag.itag)," : abr=",audio_tag.abr)
        print('*****************************************************************')
        print('\n')

        itag_a = input('itag audio = ')
        ## Downloading the audio
        yt.streams.get_by_itag(itag_a).download(dirname,filename_prefix = "audio_")
        print("The audio has been downloaded")

        directa = glob.glob(dirname+'audio_'+"*")
        audio_file = directa[0]

        file_name = audio_file[len(dirname)+6:len(audio_file)-4]

        ## load the audio
        audio = audio_file
        audio_mp3 = dirname+file_name + ".mp3"
        ## convert the audio into mp3
        cmd = f'ffmpeg_v5.0.exe -i "{audio}" -vn -ab 128k -ar 44100 -y "{audio_mp3}"'
        print(cmd)
        subprocess.check_output(cmd, shell=True)

        os.remove(audio_file)

    if choice == 3:
        print("Downloading all the videos from the playlist","\n")

        playlist_link = str(input("The link of the Playlist : "))
        p = Playlist(playlist_link)
        print(p.title," contain : ",str(len(p))," videos !")
        print("Please note that this may take a long time if the Playlist have a lot of videos (the current version will download all videos at the highest resolution! I'm working on including other options)","\n")
        choice_x = str(input("Would you like to continue ? (y/n) "))
        if choice_x != "y":
            continue

        dirname_play = "Playlist/"+p.title+"/"
        if not os.path.exists(dirname_play):
            os.makedirs(dirname_play)
        else:
            dirname_play
        for url in tqdm(p):
            yt = YouTube(url)
            resol = yt.streams.order_by('resolution').filter(only_video=True)
##            print('******************************VIDEO******************************')
            for res in resol:
##                print("itag =",str(res.itag)," : ",res.resolution," ",str(res.fps),"fps")
                max_res = res.itag
##            print('*****************************************************************')
##            print('\n')
##            print('******************************AUDIO******************************')
            audio_video = yt.streams.filter(only_audio=True)
            for audio_tag in audio_video:
##                print("itag =",str(audio_tag.itag)," : abr=",audio_tag.abr)
                max_aud = audio_tag.itag
##            print('*****************************************************************')
##            print('\n')

            itag_v = max_res
##            input('itag video = ')

            itag_a = max_aud
##            input('itag audio = ')

            yt.streams.get_by_itag(itag_v).download(dirname_play,filename_prefix = "video_")
##            print("The video has been downloaded")

            yt.streams.get_by_itag(itag_a).download(dirname_play,filename_prefix = "audio_")
##            print("The audio has been downloaded")


            directv = glob.glob(dirname_play+'video_'+"*.*m*")
            video_file = directv[0]
            directa = glob.glob(dirname_play+'audio_'+"*")
            audio_file = directa[0]

            file_name = video_file[len(dirname_play)+6:len(video_file)-4]

            video = video_file
            video_output_mp3 = dirname_play+ file_name + "_final_mp3.mp4"
            audio = audio_file
            audio_mp3 = dirname_play+ file_name + ".mp3"


            cmd = f'ffmpeg -i "{audio}" -vn -ab 128k -ar 44100 -y "{audio_mp3}"'
##            print(cmd)
            subprocess.check_output(cmd, shell=True)


            cmd = f'ffmpeg -i "{video}" -i "{audio_mp3}" -c copy "{video_output_mp3}"'
##            print(cmd)
            subprocess.check_output(cmd, shell=True)


            os.remove(video_file)
            os.remove(audio_file)
##            os.remove(dirname+file_name+".mp3")
            os.rename(dirname_play+file_name+"_final_mp3.mp4",dirname_play+file_name+".mp4")


    if choice == 4:
        print("Getting the list of videos from a Youtube channel :","\n")

        channel_link = str(input("Paste the link of the youtube channel : "))
        c = Channel(channel_link)
        ##c = Channel('https://www.youtube.com/c/'+channel_id+'/videos')
        ##c = Channel('https://www.youtube.com/user/'+channel_id+'/videos')
        ##c = Channel('https://www.youtube.com/channel/'+channel_id+'/videos')
        ##c = Channel('https://www.youtube.com/'+channel_id+'/videos')
        print(c.channel_name," have : ",str(len(c))," videos !")

        dirname_list = "Youtube/"+c.channel_name+"/"
        if not os.path.exists(dirname_list):
            os.makedirs(dirname_list)
        else:
            dirname_list

        f1 = codecs.open(dirname_list+c.channel_name+"_url.txt","w", "utf-8")
        for url in tqdm(c):
            yt = YouTube(url)
            f1.write(url+"\n")
        f1.close()

    if choice == 5:
        print("Downloading all the videos from a Youtube channel :","\n")

        channel_link = str(input("Paste the link of the youtube channel : "))
        c = Channel(channel_link)
        ##c = Channel('https://www.youtube.com/c/'+channel_id+'/videos')
        ##c = Channel('https://www.youtube.com/user/'+channel_id+'/videos')
        ##c = Channel('https://www.youtube.com/channel/'+channel_id+'/videos')
        ##c = Channel('https://www.youtube.com/'+channel_id+'/videos')
        print(c.channel_name," have : ",str(len(c))," videos !","\n")
        print("Please note that this may take a long time if the channel have a lot of videos (the current version will download all videos at the highest resolution alongside the thumbnails and videos descriptions! I'm working on including other options)","\n")
        choice_x = str(input("Would you like to continue ? (y/n) "))
        if choice_x != "y":
            continue

        dirname_list = "Youtube/"+c.channel_name+"/"
        if not os.path.exists(dirname_list):
            os.makedirs(dirname_list)
        else:
            dirname_list
        dirname_desc = "Youtube/"+c.channel_name+"/Descriptions/"
        if not os.path.exists(dirname_desc):
            os.makedirs(dirname_desc)
        else:
            dirname_desc

        dirname_thumb = "Youtube/"+c.channel_name+"/Thumbnails/"
        if not os.path.exists(dirname_thumb):
            os.makedirs(dirname_thumb)
        else:
            dirname_thumb

        dirname_vid = "YouTube/"+c.channel_name+"/Videos/"
        if not os.path.exists(dirname_vid):
            os.makedirs(dirname_vid)
        else:
            dirname_vid

        
        f1 = codecs.open(dirname_list+c.channel_name+"_url.txt","w", "utf-8")
        
        for url in tqdm(c):
            yt = YouTube(url)
            f1.write(url+"\n")

            ff = codecs.open(dirname_desc+yt.video_id+".txt","w", "utf-8")
            ff.write(yt.description)
            ff.close()

            r0 = requests.get("https://img.youtube.com/vi/"+yt.video_id+"/maxresdefault.jpg")
            r1 = requests.get("https://i.ytimg.com/vi/"+yt.video_id+"/hqdefault.jpg")
            r2 = requests.get("https://i.ytimg.com/vi/"+yt.video_id+"/hq720.jpg")

            if len(r0.content) >= len(r1.content) and len(r0.content) >= len(r2.content):
                rb = r0
            elif len(r1.content) >= len(r0.content) and len(r1.content) >= len(r2.content):
                rb = r1
            elif len(r2.content) >= len(r0.content) and len(r2.content) >= len(r1.content):
                rb = r2
            open(dirname_thumb+yt.video_id+".jpg", 'wb').write(rb.content)

            resol = yt.streams.order_by('resolution').filter(only_video=True)
##            print('******************************VIDEO******************************')
            for res in resol:
##                print("itag =",str(res.itag)," : ",res.resolution," ",str(res.fps),"fps")
                max_res = res.itag
##            print('*****************************************************************')
##            print('\n')
##            print('******************************AUDIO******************************')
            audio_video = yt.streams.filter(only_audio=True)
            for audio_tag in audio_video:
##                print("itag =",str(audio_tag.itag)," : abr=",audio_tag.abr)
                max_aud = audio_tag.itag
##            print('*****************************************************************')
##            print('\n')

            itag_v = max_res

            itag_a = max_aud

            yt.streams.get_by_itag(itag_v).download(dirname_vid,filename_prefix = "video_")
##            print("The video has been downloaded")

            yt.streams.get_by_itag(itag_a).download(dirname_vid,filename_prefix = "audio_")
##            print("The audio has been downloaded")

            directv = glob.glob(dirname_vid+'video_'+"*.*m*")
            video_file = directv[0]
            directa = glob.glob(dirname_vid+'audio_'+"*")
            audio_file = directa[0]


            file_name = video_file[len(dirname_vid)+6:len(video_file)-4]

            video = video_file
            video_output_mp3 = dirname_vid+ file_name + "_final_mp3.mp4"
            audio = audio_file
            audio_mp3 = dirname_vid+ file_name + ".mp3"

            cmd = f'ffmpeg_v5.0.exe -i "{audio}" -vn -ab 128k -ar 44100 -y "{audio_mp3}"'
##            print(cmd)
            subprocess.check_output(cmd, shell=True)


            cmd = f'ffmpeg_v5.0.exe -i "{video}" -i "{audio_mp3}" -c copy "{video_output_mp3}"'
##            print(cmd)
            subprocess.check_output(cmd, shell=True)

            os.remove(video_file)
            os.remove(audio_file)
            os.remove(dirname_vid+file_name+".mp3")
            os.rename(dirname_vid+file_name+"_final_mp3.mp4",dirname_vid+file_name+".mp4")

        f1.close()

    print("")
    continu = str(input("Would you like to download another video ? (y/n) : "))
print("")
print("Thank you for using Youtube video downloader")
