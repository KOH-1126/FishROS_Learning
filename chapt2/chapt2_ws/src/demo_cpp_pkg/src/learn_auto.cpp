#include <iostream>
#include <functional>
using namespace std;

void save_with_free_func(const string& filename){
    cout << "save_with_free_func: " << filename << endl;
}

class FileSaver{
    public:
        FileSaver()=default;
        void save_with_member_func(const string& filename)
        {
            cout << "save_with_member_func" << filename << endl;
        }

};


int main(){
    
    FileSaver fs;
    auto save_with_lambda = [](const string& filename){
        cout << "save_with_lambda: " << filename << endl;
    };

    // save_with_free_func("file1.txt");
    // fs.save_with_member_func("file2.txt");
    // save_with_lambda("file3.txt"); 

    function<void(const string&)> save1 = save_with_free_func;
    function<void(const string&)> save2 = save_with_lambda;

    function<void(const string&)> save3 = bind(&FileSaver::save_with_member_func, &fs, placeholders::_1);

    save1("file1.txt");
    save2("file2.txt");
    save3("file3.txt");

    return 0;
}

