import ftplib
import os
import ssl

class ImplicitFTP_TLS(ftplib.FTP_TLS):
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
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        conn = self.sock.context.wrap_socket(
            conn, server_hostname=self.host, session=self.sock.session
        )
        return conn, size

def download_files_implicit_tls(host, port, username, password, remote_dir, local_dir):
    with ImplicitFTP_TLS() as ftps:
        ftps.connect(host, port)
        ftps.login(username, password)
        ftps.prot_p()  # Habilita el modo de protección de datos TLS
        ftps.cwd(remote_dir)
        ftps.set_pasv(True)

        files = ftps.nlst()  # Obtiene una lista de nombres de archivos en el directorio remoto

        for file in files:
            local_filename = os.path.join(local_dir, file)
            with open(local_filename, 'wb') as f:
                ftps.retrbinary('RETR ' + file, f.write)

        ftps.quit()

# Configuración
host = '192.168.109.1'
port = 990
username = 'BCOPFTP'
password = 'ducati12'
local_dir = 'E:/Users/ruthm/Escritorio/CierreTC_NUEVO'
remote_dir = '/trndatoent/p43'


# Descarga de archivos
download_files_implicit_tls(host, port, username, password, remote_dir, local_dir)
