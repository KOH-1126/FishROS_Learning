import threading
import requests
def word_count(url, result):
    """
    普通函数 用于回调
    """
    print(f"{url}:{len(result)}->{result[:5]}")

class Downloader:
    def download(self, url, callback):
        print(f"线程:{threading.get_ident()} 开始下载:{url}")
        response = requests.get(url)
        response.encoding = 'utf-8'
        callback(url, response.text)

    def startDownload(self, url, callback):
        thread = threading.Thread(target=self.download, args=(url, callback))
        thread.start()


def main():
    download = Downloader()
    download.startDownload(r'http://localhost:8000/novel1.txt', word_count)
    download.startDownload(r'http://localhost:8000/novel2.txt', word_count)
    download.startDownload(r'http://localhost:8000/novel3.txt', word_count)
