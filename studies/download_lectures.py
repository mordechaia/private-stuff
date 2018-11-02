import baker
import requests
import os
import commands


@baker.command
def download_files(base_url, dir_path, start, end):
    for i in range(start, end):
        with open("{}/{}.ts".format(dir_path), "w") as f:
            url = base_url.format(i)
            res = requests.get(url)
            res.raise_for_status()
            f.write(res.content)


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
