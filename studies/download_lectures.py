import baker
import requests
import os
import commands
from time import sleep

@baker.command
def download_files(base_url, dir_path, start, end):
    start, end = int(start), int(end)
    for i in range(start, end):
        try:
            url = base_url.format(i)
            print "download {}".format(url)
            with open("{}/{}.ts".format(dir_path, i), "w") as f:
                res = requests.get(url)
                res.raise_for_status()
                f.write(res.content)
        except Exception ,e:
            print "Got exception {}".format(e)
            sleep(5)
            download_files(base_url,dir_path,i,end)


@baker.command
def _make_file_concat_string(dir_path):
    return "|".join(os.listdir(dir_path))


@baker.command
def append_videos(dir_path, path_to_video):
    file_str = _make_file_concat_string(dir_path)
    command = "ffmpeg -i concat:'{}' -acodec copy -vcodec copy {}".format(file_str, path_to_video)
    res = commands.getstatusoutput(command)
    if res[0] != 0:
        raise Exception(res[1])
    return res[1]


if __name__ == '__main__':
    baker.run()
