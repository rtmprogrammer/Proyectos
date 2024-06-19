import os
import paramiko
from ftplib import FTP, FTP_TLS
import ssl
from configparser import ConfigParser

class ImplicitFTP_TLS(FTP_TLS):
    """
    FTP_TLS subclass that automatically wraps sockets in SSL to support implicit FTPS.
    Prefer explicit TLS whenever possible.
    """

    def __init__(self, *args, **kwargs):
        """Initialise self."""
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        """Return the socket."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """When modifying the socket, ensure that it is SSL wrapped."""
        if value is not None and not isinstance(value, ssl.SSLSocket):
            value = self.context.wrap_socket(value)
        self._sock = value

    def ntransfercmd(self, cmd, rest=None):
        """Override the ntransfercmd method"""
        conn, size = FTP.ntransfercmd(self, cmd, rest)
        conn = self.sock.context.wrap_socket(
            conn, server_hostname=self.host, session=self.sock.session
        )
        return conn, size


class Filezilla:
    def __init__(self, config_file):
        self.config = ConfigParser()
        self.config.read(config_file)

    def connect_and_download(self, section):
    
        if section in self.config.sections():
            
            protocol = self.config.get(section, 'protocol')
            host = self.config.get(section, 'host')
            username = self.config.get(section, 'username')
            password = self.config.get(section, 'password')
            local_dir = self.config.get(section, 'local_dir')
            remote_dir = self.config.get(section, 'remote_dir')
            #files = self.config.get(section, 'files').split(',')
            
            print(f"Server-Host: '{host}' ")
            #print(f"Port: '{port}' ")
            print(f"Usuario: '{username}' ")
            #print(f"Password: '{password}' ")
            print(f"Directorio origen: '{remote_dir}' ")
            print(f"Directorio destino: '{local_dir}' ")
            print("-----------------------------------------------------")

            if protocol.lower() == 'ftp':
                
                print("Se verifica Protocolo FTP")
                self._ftp_download(host, username, password, local_dir, remote_dir)
                
            elif protocol.lower() == 'ftp_tls':
                
                print("Se verifica Protocolo FTP con Cifrado")
                self._ftp_tls_download(host, username, password, local_dir, remote_dir)
                
            elif protocol.lower() == 'sftp':
                self._sftp_download(host, username, password, local_dir, remote_dir)
                
            else:
                print("Protocolo no soportado")
        
        else:
            print(f"No existe el nombre del servidor '{section}' en el archivo de configuracion.")
        
        

    def _ftp_download(self, host, username, password, local_dir, remote_dir):
        
        print("FTP")
        
        with FTP(host) as ftp:
            
            #ftp.set_debuglevel(2)
            
            #Se loguea a la direccion FTP
            ftp.login(user=username, passwd=password)
            
            #Ingresa al directorio para la descarga de archivos
            ftp.cwd(remote_dir)
            
            #Obtiene la lista de contenidos del directorio
            files = ftp.nlst()
            
            print("-----------------------------------------------------")
            print("ARCHIVOS DESCARGADOS")
            
            #Recorre la lista y descarga cada archivo
            for file in files:
                
                #El with trabaja con el Open(os.path.join(directorio_destino, file),modo(wb,read))
                with open(os.path.join(local_dir, file), 'wb') as f:
                    
                    
                    ftp.retrbinary(f'RETR {file}', f.write)
                print(file) 
            print("-----------------------------------------------------")      
    
    def _ftp_tls_download(self, host, username, password, local_dir, remote_dir):
        
        with ImplicitFTP_TLS() as ftp:
            
            #ftp.set_debuglevel(2)
            
            #Modo de transferencia pasivo
            #ftp.set_pasv(True)
            
            #print(ftp.connect(host,port=990))
            
            ftp.connect(host,port=990)
            
            ftp.login(user=username, passwd=password)
            
            #Configura conexion de datos segura 
            ftp.prot_p()  # Habilita el modo de protección de datos TLS
            
            #Direccion de directorio origen de descarga
            ftp.cwd(remote_dir)
            ftp.set_pasv(True)
            
            
            files = ftp.nlst()
            
            print("-----------------------------------------------------")
            print("ARCHIVOS DESCARGADOS")
            print("-----------------------------------------------------")
            
            for file in files:
                local_filename = os.path.join(local_dir, file)
                
                with open(local_filename, 'wb') as f:
                    
                    ftp.retrbinary(f'RETR {file}', f.write)
                    
                print(file)
            print("-----------------------------------------------------")
            
            ftp.quit()

    def _sftp_download(self, host, username, password, local_dir, remote_dir):
        
        #Se crea el objeto transport de paramiko, establece conexion al servidor SFTP en el puerto 22
        transport = paramiko.Transport((host, 22))
        
        #Establece la conexion
        transport.connect(username=username, password=password)
        
        #Se crea un objeto SFTPCliente a partir del objeto Transport, este objeto se utiliza para realizar operaciones SFTP
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        #Cambia el directorio remoto actual al directorio especificado
        sftp.chdir(remote_dir)
        
        #Obtiene una lista de todos lo archivos y directorios en el directorio remoto actual
        files = sftp.listdir()
        
        print("-----------------------------------------------------")
        print("ARCHIVOS DESCARGADOS")
        print("-----------------------------------------------------")
        
        #Itera sobre cada archivo en la lista de archivos
        for file in files:

            #Descarga el archivo del servidor SFTP y lo guarda en el directorio local especificado
            #utilizando os.path.join para construir al archivo local
            sftp.get(file, os.path.join(local_dir, file))
            print(file)
        print("-----------------------------------------------------")
            
        #Cierra la conexion al servidor SFTP, liberando los recursos utilizados porla conexion
        transport.close()
        

'''
        import os
import paramiko

host = "sftp.host.com"
port = 8022
transport = paramiko.Transport((host, port))
username = "sftplogin"
mykey = paramiko.RSAKey.from_private_key_file("private_export.pem", password="XXX")
print "Connecting..."
transport.connect(username = username, pkey = mykey)
sftp = paramiko.SFTPClient.from_transport(transport)
print "Connected."
print sftp.listdir()
sftp.close()
transport.close()
print "Closed connection."
    
    '''
