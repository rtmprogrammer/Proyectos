import sys
from filezilla import Filezilla

def main():


    if len(sys.argv) < 2:
        print("Script : python filezilla.py <section_name>")
        sys.exit(1)
    print("Ejecutanto script")
    section_name = sys.argv[1]
    downloader = Filezilla('config.ini')
    downloader.connect_and_download(section_name)
   

    
# Python boilerplate.
if __name__ == '__main__':
    main()