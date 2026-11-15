#include <iostream>
#include <fstream>
#include <cstring>
void Parce(int argc, char** argv, bool& lines, bool& words, bool& bytes, bool& alnum){
    //checking options
    if (argc<2){
        std::cout<<"No file.";
        return;
    }
    //arguments checking 
   for (int i = 0; i<argc; i++){
        if (std::strcmp(argv[i], "--lines")==0){
            lines = true;
        }
        if (std::strcmp(argv[i], "--bytes")==0){
            bytes = true;
        }
        if (std::strcmp(argv[i], "--words")==0){
            words = true;
        }
        if (std::strcmp(argv[i], "--alnum")==0){
            alnum = true;
        } 
    }

    for (int i = 0; i<argc; i++){
        if ((argv[i][0]=='-') && (argv[i][1]!='-')){
            for (int j =0; argv[i][j]!='\0'; j++){
                if (argv[i][j] == 'l'){
                    lines = true;
                }
                if (argv[i][j] == 'w'){
                    words = true;
                }
                if (argv[i][j] == 'c'){
                    bytes = true;
                }
                if (argv[i][j] == 'a'){
                    alnum = true;
                }
            }
        }
    }

    
}

void Counter(char* filename, int& lines_count, int& words_count, int& bytes_count, int& alnum_count){
    std::ifstream file(filename);

    //lines/bytesalnims/words counting
    char ch, last_symbol;
    bool in_word = false;
    bool is_space_symbol; 
    bool last_s = false;
    while (file.get(ch))
    {
        //lines counting
        last_s = true;
        if (ch == '\n'){
            lines_count++;
        }
        //words counting
        if (ch == ' ' || ch == '\n' || ch == '\t' || ch == '\r' || ch == '\v' || ch == '\f'){
            is_space_symbol = true;
        }
        else{
            is_space_symbol = false;
        }

        if (is_space_symbol){
            in_word = false;
        }
        else if (!in_word)
        {
            words_count+=1;
            in_word = true;
        }
        //alnum counting
        if (('A'<=ch && ch<='Z') || 
            ('a'<=ch && ch<='z') ||
            ('0'<=ch && ch<='9')){
        alnum_count++;
        }
        //bytes counting
        bytes_count+=1;
        last_symbol = ch;
    }

    //last line check
    if (last_symbol!='\n' && last_s)
    {
        lines_count+=1;
    }
}


void Output(int argc, char** argv, int lines_count, int words_count, int bytes_count, int alnum_count, bool lines, bool words, bool bytes, bool alnum, char*filename){
    int a[] = {lines_count, words_count, alnum_count, bytes_count};
    if (!lines){
        a[0] = -1;
    }
    if (!words){
        a[1] = -1;
    }
    if (!bytes){
        a[3] = -1;
    }
    if (!alnum){
        a[2] = -1;
    }
    for (int i = 0; i<4; i++){
        if (a[i]!=-1){
            std::cout<<a[i]<<" ";
        }
    
    }   
    if (!lines && !words && !bytes && !alnum){
        std::cout<<lines_count<<" "<<words_count<<" "<<bytes_count<<" ";
    }
    std::cout<<filename<<'\n';
}
// ./build/WordCount test123.txt

int main(int argc, char** argv) {
    bool lines = false;
    bool words = false;
    bool bytes = false;
    bool alnum = false;
    

    Parce(argc, argv, lines, words, bytes, alnum);
    for (int i = 1; i<argc; i++){
        if (argv[i][0] != '-'){
            int  lines_count = 0, words_count = 0, bytes_count = 0, alnum_count = 0;
            char* filename = argv[i];
            Counter(filename, lines_count, words_count, bytes_count, alnum_count);
            Output(argc, argv,lines_count, words_count, bytes_count, alnum_count, lines, words, bytes, alnum, filename);
            
        }
    }
    
    return 0;
}