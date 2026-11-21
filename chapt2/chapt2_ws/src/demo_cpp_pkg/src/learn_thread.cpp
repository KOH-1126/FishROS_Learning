#include <iostream>
#include <thread>
#include <chrono>
#include <functional>
#include "cpp-httplib/httplib.h"
using namespace std;

class Download
{
    public:
        void download(const string& host, const string& path, const function<void(const string&, const string&)>& callback) {
            cout << "Thread No.=" << this_thread::get_id() << endl;
            httplib::Client client(host);
            auto response = client.Get(path);
            if(response && response->status == 200){
                callback(path, response->body);
            } else {
                cout << "Download failed: " << path << endl;
            }
        };
        void startDownload(const string& host, const string& path, const function<void(const string&, const string&)>& callback) {
            auto download_fun = bind(&Download::download, this, placeholders::_1, placeholders::_2, placeholders::_3);
            thread t(download_fun, host, path, callback);
            t.detach();
        };
};

int main(){
    auto d = Download();
    auto word_count = [](const string& path, const string& content) -> void {
        cout << "Downloaded " << path << ", size: " << content.size() << "->" << content.substr(0,5) << endl;
    };
    d.startDownload("http://localhost:8000", "/novel1.txt", word_count);
    d.startDownload("http://localhost:8000", "/novel2.txt", word_count);
    d.startDownload("http://localhost:8000", "/novel3.txt", word_count);

    std::this_thread::sleep_for(std::chrono::seconds(10));
    return 0;
}