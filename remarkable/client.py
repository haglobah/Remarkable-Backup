import os
from contextlib import suppress
from pathlib import Path, PurePath
from zipfile import ZipFile

import paramiko
from paramiko.client import AutoAddPolicy


class Client:
    """
    Client to access remarkable over ssh.

    Use context manager syntax.

    Attributes:
        ip: The IP of the tablet.
        port: The port of the tablet.
        username: The tablet's SSH username.
        password: The SSH password to access the tablet.
    """

    base_path = Path(".local") / "share" / "remarkable" / "xochitl"

    def __init__(self, ip: str, port: str, username: str, password: str):
        self.ip = ip
        self.port = port
        self.username, self.password = username, password
        self._ssh_client = paramiko.SSHClient()
        self._sftp_client = None

    def __enter__(self):
        self._ssh_client.set_missing_host_key_policy(AutoAddPolicy)
        self._ssh_client.connect(
            self.ip,
            username=self.username,
            password=self.password,
        )
        self._sftp_client = self._ssh_client.open_sftp()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ssh_client.close()

    def list_dir(self, path: Path = "."):
        """List the files of a directory."""
        return self._sftp_client.listdir(path.as_posix())

    def download_dir(self, rm_path: Path, out_path: Path):
        """Download a directory from the tablet."""

        # Recursively download the remote directory
        def _download_dir(remote_dir: Path, local_dir: Path):
            os.makedirs(local_dir, exist_ok=True)
            for item in self._sftp_client.listdir_attr(remote_dir.as_posix()):
                remote_item = remote_dir / item.filename
                local_item = local_dir / item.filename

                # It's a subdirectory
                print(item.st_mode)
                if item.st_mode & 0o4000:
                    _download_dir(remote_item, local_item)
                # It's a file
                else:
                    print(remote_item.as_posix())
                    with self._sftp_client.file(remote_item.as_posix()) as file_reader:
                        with open(local_item, "wb") as file_writer:
                            file_writer.write(file_reader.read())

        _download_dir(rm_path, out_path)

    def notebook(self, id: str, path: Path):
        """Download a file from the tablet by id."""
        with ZipFile(path, "w") as package:
            def _dump_directory(package_dir_name: str, remarkable_path: Path):
                """Dump all files in a directory on remarkable into folder on zip."""
                package.mkdir(package_dir_name)
                for item in self.list_dir(remarkable_path):
                    with self._sftp_client.file(
                        (remarkable_path / item).as_posix()
                    ) as item_reader:
                        with package.open(
                            str(Path(package_dir_name) / item), "w"
                        ) as item_writer:
                            item_writer.write(item_reader.read())

            def _dump_file(filename: str, remarkable_path: Path):
                """Dump a specific file to the zip."""
                with self._sftp_client.file(remarkable_path.as_posix()) as item_reader:
                    with package.open(filename, "w") as item_writer:
                        item_writer.write(item_reader.read())

            _dump_directory("pages", self.base_path / id)
            _dump_directory("thumbnails", self.base_path / f"{id}.thumbnails")
            with suppress(FileNotFoundError):
                _dump_directory("highlights", self.base_path / f"{id}.highlights")
            _dump_file("local.json", self.base_path / f"{id}.local")
            _dump_file("basicMetadata.json", self.base_path / f"{id}.metadata")
            _dump_file("extendedMetadata.json", self.base_path / f"{id}.pagedata")

