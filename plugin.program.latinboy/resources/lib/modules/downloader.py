import os
from urllib.request import Request, urlopen
import xbmc
import xbmcgui

class Downloader:
    def __init__(self, url):
        self.url = url
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        self.headers = {"User-Agent":self.user_agent, "Connection":'keep-alive', 'Accept':'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'}
        
    def get_urllib(self, decoding=True):
        req = Request(self.url, headers = self.headers)
        if decoding:
            return urlopen(req).read().decode('utf-8')
        else:
            return urlopen(req)
    
    def get_session(self, decoding=True, stream=False):
        import requests
        session = requests.Session()
        if decoding:
            return session.get(self.url,headers=self.headers, stream=stream).content.decode('utf-8')
        else:
            return session.get(self.url,headers=self.headers, stream=stream)
    
    def get_requests(self, decoding=True, stream=False):
        import requests
        if decoding:
            return requests.get(self.url, headers=self.headers, stream=stream).content.decode('utf-8')
        else:
            return requests.get(self.url, headers=self.headers, stream=stream)
    
    def get_length(self, response, meth = 'session'):
        try:
            if meth in ['session', 'requests']:
                return response.headers['X-Dropbox-Content-Length']
            elif meth=='urllib':
                return response.getheader('content-length')
        except KeyError:
            return None
    
    def download_build(self, name, dest, meth='requests', blocksize=1024*1024):
        try:
            if meth == 'requests':
                import requests
                r = requests.get(self.url, stream=True)
                total_size = int(r.headers.get('content-length', 0))
                
                with open(dest, 'wb') as f:
                    downloaded = 0
                    for chunk in r.iter_content(chunk_size=blocksize):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            progress = int((downloaded / total_size) * 100) if total_size > 0 else 0
                            dp.update(progress, f'Descargando {name}...')
                
            else:  # Usar urllib como fallback
                import urllib.request
                with urllib.request.urlopen(self.url) as response:
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded = 0
                    
                    with open(dest, 'wb') as f:
                        while True:
                            chunk = response.read(blocksize)
                            if not chunk:
                                break
                            f.write(chunk)
                            downloaded += len(chunk)
                            progress = int((downloaded / total_size) * 100) if total_size > 0 else 0
                            dp.update(progress, f'Descargando {name}...')
            
            return True
        
        except Exception as e:
            xbmc.log(f'[ERROR] Error en descarga: {str(e)}', xbmc.LOGINFO)
            if os.path.exists(dest):
                os.remove(dest)
            return False
    
    def download_zip(self, dest):
        r = self.get_requests(decoding=False, stream=True)
        with open(dest, "wb") as f:
              for ch in r.iter_content(chunk_size = 2391975):
                  if ch:
                      f.write(ch)
                  f.close()
