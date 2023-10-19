from conector_sftp import Sftp
import os
from urllib.parse import urlparse

cod_status = None
msg_status = None
sftp = None


class Sftp_Options:
    def __init__(self, sftp_url, privateKeyFilePath):
        # print(f"sftp_url: {sftp_url}")
        # print(f"privateKeyFilePath: {privateKeyFilePath}")

        if sftp_url:
            parsed_url = urlparse(sftp_url)

            self.sftp = Sftp(
                hostname=parsed_url.hostname,
                username=parsed_url.username,
                password=parsed_url.password,
                port=parsed_url.port,
                privateKeyFilePath=privateKeyFilePath,
            )
        else:
            self.cod_status = 1
            self.msg_status = "First, please set environment variable sftp://user:password@host and try again."

    def listdir_attr(self, path_list):
        try:
            # Connect to SFTP
            print(f"--path_list: {path_list}")
            self.sftp.connect()

            resultado = self.sftp.listdir_attr(path_list)
            lista = []
            for file in resultado:
                # st_atime - last time the file was accessed.
                # st_mtime - last time the file's CONTENTS were changed
                # st_ctime - the last time the file's inode was changed (e.g. permissions changed, file renamed, etc..)
                elemento = [file.filename, file.st_mode, file.st_size,
                            file.st_atime, file.st_mtime]
                lista.append(elemento)
            self.cod_status = 0
            self.msg_status = "Proceso OK"

            return lista

        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error List: {err}"

        finally:
            # Disconnect from SFTP
            self.sftp.disconnect()

    def get(self, local_path, remote_path):
        try:
            # Connect to SFTP
            self.sftp.connect()

            # Download files from SFTP
            self.sftp.download(
                remote_path, os.path.join(remote_path, local_path)
            )

            self.cod_status = 0
            self.msg_status = "Proceso OK"
        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error Get: {err}"

        finally:
            # Disconnect from SFTP
            self.sftp.disconnect()

    def put(self, local_path, remote_path):
        try:
            # Connect to SFTP
            self.sftp.connect()

            # Upload files by SFTP
            self.sftp.upload(local_path, remote_path)

            self.cod_status = 0
            self.msg_status = "Proceso OK"

        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error Put: {err}"

        finally:
            # Disconnect from SFTP
            self.sftp.disconnect()

    def mget(self, local_path, remote_path):
        try:
            # Connect to SFTP
            self.sftp.connect()

            # Download files from SFTP
            self.sftp.downloadDir(
                remote_path, os.path.join(remote_path, local_path)
            )

            self.cod_status = 0
            self.msg_status = "Proceso OK"
        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error MGet: {err}"

        finally:
            # Disconnect from SFTP
            self.sftp.disconnect()

    def mput(self, local_path, remote_path):
        try:
            # Connect to SFTP
            self.sftp.connect()

            # Upload files by SFTP
            self.sftp.uploadDir(local_path, remote_path)

            self.cod_status = 0
            self.msg_status = "Proceso OK"

        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error MPut: {err}"

        finally:
            # Disconnect from SFTP
            self.sftp.disconnect()

    def mdelete(self, host_path):
        try:
            # Connect to SFTP
            self.sftp.connect()

            # Download files from SFTP
            self.sftp.deleteDir(host_path)

            self.cod_status = 0
            self.msg_status = "Proceso OK"
        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error MDelete: {err}"

        finally:
            # Disconnect from SFTP
            self.sftp.disconnect()
