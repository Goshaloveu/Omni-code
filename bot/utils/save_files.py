import os
from asyncio import get_running_loop
from functools import partial
import subprocess
import shutil

from bot import LOGGER
from pathlib import Path


space = '        '
apeak = '│     '
sprig = ['├──']
later = ['└──']


# Get struct of direct
def struct(current_folder: Path, only_dir: bool = False, prefix: str = ''):

    if only_dir:
        scope = [x for x in current_folder.iterdir() if x.is_dir()]
    else:
        scope = list(current_folder.iterdir())
    scope.sort()
    building = list(zip(sprig * (len(scope) - 1) + later, scope))
    for pointer, path in building:
        if path.is_dir():
            yield prefix + pointer + path.name
            extension = apeak if pointer == sprig[0] else space
            yield from struct(path, prefix=prefix + extension)
        elif not only_dir:
            yield prefix + pointer + path.name


# Get packages in directory as a list
async def get_packages(path):
    packages = [
        val 
        for sublist in [[j for j in i[1]] for i in os.walk(path)]
        for val in sublist
    ]   # skipcq: FLK-E501
    return sorted(packages)


# Get files in directory as a list
async def get_files_names(path):
    path_list = [
        val
        for sublist in [[j.split(".")[0] for j in i[2]] for i in os.walk(path)]
        for val in sublist
    ]  # skipcq: FLK-E501
    return sorted(path_list)


# Get files in directory as a list
async def get_files(path):
    path_list = [
        val
        for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)]
        for val in sublist
    ]  # skipcq: FLK-E501
    return sorted(path_list)


def __run_cmds_unzipper(command):
    ext_cmd = subprocess.Popen(
        command["cmd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    ext_out = ext_cmd.stdout.read()[:-1].decode("cp866").rstrip("\n")
    ext_err = ext_cmd.stderr.read()[:-1].decode("cp866").rstrip("\n")
    LOGGER.info("ext_out : " + ext_out)
    LOGGER.info("ext_err : " + ext_err)
    if ext_cmd.stderr:
        ext_cmd.stderr.close()
    if ext_cmd.stdout:
        ext_cmd.stdout.close()
    return ext_out + ext_err


async def run_cmds_on_cr(func, **kwargs):
    loop = get_running_loop()
    return await loop.run_in_executor(None, partial(func, kwargs))


# Extract with 7z
async def _extract_with_7z_helper(path, archive_path, password=None):
    LOGGER.info("7z : " + archive_path + " : " + path)
    if password:
        command = f'7z x -o"{path}" -p"{password}" "{archive_path}" -y'
    else:
        command = f'7z x -o"{path}" "{archive_path}" -y'
    return await run_cmds_on_cr(__run_cmds_unzipper, cmd=command)


# Extract with zstd (for .tar.zst files)
async def _extract_with_zstd(path, archive_path):
    command = f'zstd -f --output-dir-flat "{path}" -d "{archive_path}"'
    return await run_cmds_on_cr(__run_cmds_unzipper, cmd=command)


async def extr_files(path, archive_path, password=None):
    os.makedirs(path, exist_ok=True)
    tarball_extensions = (
        ".tar.gz",
        ".gz",
        ".tgz",
        ".taz",
        ".tar.bz2",
        ".bz2",
        ".tb2",
        ".tbz",
        ".tbz2",
        ".tz2",
        ".tar.lz",
        ".lz",
        ".tar.lzma",
        ".lzma",
        ".tlz",
        ".tar.lzo",
        ".lzo",
        ".tar.xz",
        ".xz",
        ".txz",
        ".tar.z",
        ".z",
        ".tz",
        ".taz",
    )
    if archive_path.endswith(tarball_extensions):
        LOGGER.info("tar")
        temp_path = path.rsplit("/", 1)[0] + "/tar_temp"
        os.makedirs(temp_path, exist_ok=True)
        result = await _extract_with_7z_helper(temp_path, archive_path)
        filename = await get_files(temp_path)
        filename = filename[0]
        command = f'tar -xvf "{filename}" -C "{path}"'
        result += await run_cmds_on_cr(__run_cmds_unzipper, cmd=command)
        shutil.rmtree(temp_path)
    elif archive_path.endswith((".tar.zst", ".zst", ".tzst")):
        LOGGER.info("zstd")
        os.mkdir(path)
        result = await _extract_with_zstd(path, archive_path)
    else:
        LOGGER.info("normal archive")
        result = await _extract_with_7z_helper(path, archive_path, password)
    LOGGER.info(await get_files(path))
    return result