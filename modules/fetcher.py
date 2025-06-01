import os  # Provides functions to interact with the operating system (like file paths, deletion)
import tempfile  # Used to create temporary files and directories
import shutil  # High-level file operations like copying and unpacking archives
import git  # GitPython: Used to clone GitHub repositories
import errno  # Provides standard error codes (e.g., for file permission errors)
import stat  # Used to modify file permissions (like read/write access)


class Fetcher:
    def __init__(self):
        """
        Initializes the Fetcher object with a unique temporary directory.
        """
        self.temp_dir = tempfile.mkdtemp()

    def handle_zip_upload(self, zip_path: str) -> str:
        """
        Unpacks a zip archive into the object's temporary directory.
        Returns the path to that directory.
        """
        shutil.unpack_archive(zip_path, self.temp_dir)
        return self.temp_dir

    def handle_github_clone(self, git_url: str) -> str:
        """
        Clones a GitHub repository into the object's temporary directory.
        Returns the path to that directory.
        """
        git.Repo.clone_from(git_url, self.temp_dir)
        return self.temp_dir

    def _handle_remove_readonly(self, func, path, exc):
        """
        Makes read-only files writable during cleanup.
        """

        # exc is a tuple. The second value (exc[1]) is the actual exception object.
        excvalue = exc[1]

        # This checks if the error is because of access denied (read-only file) when trying to delete.
        if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        else:
            raise excvalue

    def cleanup(self):
        """
        Deletes the temporary folder managed by this object.
        """
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, onerror=self._handle_remove_readonly)
