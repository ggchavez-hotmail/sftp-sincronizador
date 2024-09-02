import paramiko
import os

class Sftp:    
    def __init__(self, hostname, username, password, port, privateKeyFilePath, blocks):
        """Constructor Method"""
        self.hostname = hostname  #
        self.username = username  #
        self.password = password  #
        self.port = port  #
        # Lugar donde se almacena clave privada
        self.privateKeyFilePath = privateKeyFilePath
        #self.blocks = int(blocks)
        self.blocks = 1024 * 1024
        # Print datos
        #print(self.hostname)
        #print(self.username)
        #print(self.password)
        #print(self.port)
        #print(self.privateKeyFilePath)

    def connect(self):
        """Connects to the sftp server and returns the sftp connection object"""

        try:
            # Connection Options
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.hostname, self.port, self.username, self.password)
            
            # Get the sftp connection object
            self.sftp = self.ssh_client.open_sftp()
            print(f"Connected to {self.hostname} as {self.username}.")
        except Exception as err:
            print(f"connect - err: {err}")
            raise Exception(err)            

    def disconnect(self):
        try:
            """Closes the sftp connection"""
            self.sftp.close()
            self.ssh_client.close()
            print(f"Disconnected from host {self.hostname}")
        except Exception as err:
            print(f"disconnect - err: {err}")
            raise Exception(err)
            
    def listdir(self, remote_path):
        """lists all the files and directories in the specified path and returns them"""
        try:
            print(f"list from {remote_path}")
            for obj in self.sftp.listdir(remote_path):
                yield obj
                
        except Exception as err:            
            print(f"listdir - err: {err}")
            raise Exception(err)

    def listdir_attr(self, remote_path):
        """lists all the files and directories (with their attributes) in the specified path and returns them"""
        try:
            print(f"list with attribute from {remote_path}")
            for attr in self.sftp.listdir_attr(remote_path):
                yield attr
                
        except Exception as err:            
            print(f"listdir_attr - err: {err}")
            raise Exception(err)

    def download(self, remote_path, target_local_path):
        """
        Downloads the file from remote sftp server to local.
        Also, by default extracts the file to the specified target_local_path
        """

        try:
            print(f"downloading from {self.hostname} as {self.username} [(remote path : {remote_path});(local path: {target_local_path})]")

            # Create the target directory if it does not exist
            path, _ = os.path.split(target_local_path)
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except Exception as err:
                    raise Exception(err)

            # Download from remote sftp server to local
            #self.sftp.get(remote_path, target_local_path)
            
            with self.sftp.open(remote_path, 'rb') as archivo_remoto:
                while True:
                    datos = archivo_remoto.read(self.blocks)
                    if not datos:
                        break
                    yield datos
            
            print("download completed")

        except Exception as err:
            print(f"download - err: {err}")
            raise Exception(err)

    def upload(self, source_local_path, remote_path):
        """
        Uploads the source files from local to the sftp server.
        """

        try:
            print(f"uploading to {self.hostname} as {self.username} [(remote path: {remote_path});(source local path: {source_local_path})]" )

            # Download file from SFTP
            #self.sftp.put(source_local_path, remote_path)
            
            with open(source_local_path, 'rb') as archivo_local:
                with self.sftp.open(remote_path, 'wb') as archivo_remoto:
                    while True:
                        datos = archivo_local.read(self.blocks)
                        if not datos:
                            break
                        archivo_remoto.write(datos)
            
            print("upload completed")

        except Exception as err:
            print(f"upload - err: {err}")
            raise Exception(err)

    def downloadDir(self, remote_path, target_local_path):
        """
        Downloads files from remote sftp server to local.
        Also, by default extracts the file to the specified target_local_path
        """

        try:
            #print(f"downloading from {self.hostname} as {self.username} 
            #      [(remote path : {remote_path});(local path: {target_local_path})]"
            #)

            # Create the target directory if it does not exist
            path, _ = os.path.split(target_local_path)
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except Exception as err:
                    raise Exception(err)

            # Download from remote sftp server to local
            self.sftp.get(remote_path, target_local_path)
            #print("download completed")

        except Exception as err:
            print(f"downloadDir - err: {err}")
            raise Exception(err)

    def uploadDir(self, source_local_path, remote_path):
        """
        Uploads source files from local to the sftp server.
        """

        try:
            #print(f"uploading to {self.hostname} as {self.username} 
            #      [(remote path: {remote_path});(source local path: {source_local_path})]"
            #)

            # Download file from SFTP
            self.sftp.put(source_local_path, remote_path)
            #print("upload completed")

        except Exception as err:
            print(f"uploadDir - err: {err}")
            raise Exception(err)

    def deleteDir(self, remote_path):
        """
        Delete the source files from remote sftp server.
        """

        try:
            #print(f"removing to {self.hostname} as {self.username}
            #      [(remote path: {remote_path})])]"
            #)

            # Download file from SFTP
            self.sftp.remove(remote_path)
            #print("delete completed")

        except Exception as err:            
            print(f"deleteDir - err: {err}")
            raise Exception(err)
