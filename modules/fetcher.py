import os
import tempfile
import shutil
import git
import errno
import stat

class Fetcher:
    @staticmethod
    def handle_zip_upload(zip_path: str) -> str:
        temp_dir = tempfile.mkdtemp()
        shutil.unpack_archive(zip_path, temp_dir)
        return temp_dir

    @staticmethod
    def handle_github_clone(git_url: str) -> str:
        temp_dir = tempfile.mkdtemp()
        git.Repo.clone_from(git_url, temp_dir)
        return temp_dir

    @staticmethod
    def _handle_remove_readonly(func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        else:
            raise excvalue

    @staticmethod
    def cleanup_temp_dir(path: str):
        if os.path.exists(path):
            shutil.rmtree(path, onerror=Fetcher._handle_remove_readonly)
