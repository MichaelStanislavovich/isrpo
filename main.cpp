#include <iostream>
#include <cstdlib>
#include <cctype>
#include <cstdint>


bool IsNumber(const char* str){
    /*
    Проверяет, что переданная стора является целым числом
    Параметры:
        str (const char*): строка, которую необходимо проверить.
    Возвращаемое значение:
        bool: true, если срока является целым числом,
              false, если строка является некорректным значением.
    Пример вызова:
        IsNumber("123")
    */
    if (str[0] == '\n' || str[0] == '\0'){
        return false;
    }
    for (int i = 0; str[i] != '\0'; i++){
        if (str[0] == '-' && str[1] == '\0'){
            
            return false;
        }
        if (!std::isdigit(str[i]) && !(i == 0 && str[i]== '-')){
            return false;
        }
    }
    return true;
}

bool IsNotOutOfRange(const char* str){
    /*
    Проверяет, что переданное число находится в диапазоне int32_t
    Параметры:
        str(const char*): строка, которую необходимо проверить.
    Возвращаемое значение:
        bool: true, если в пределах допустимого диапазона,
              false, если выходит за пределы допустимого диапазона.  
    Пример вызова:
        IsNotOutOfRange("123")
    */
    int32_t num = std::atol(str);
    if (num > INT32_MAX || num < INT32_MIN){
        return false;
    }
    return true;
}
void Calculate(const char* lhs, const char* op, const char* rhs) {
    /*
    Функция получает на вход два операнlа и оператор и производит указанную арифметическую операцию с двумя полученными числами и выводит результат
    Параметры:
        lhs (const char*): певый операнд
        op (const char*): арифметическая операция 
        rhs (const char*): второй операнд
    Возвращаемое значение:
        Отсутствует
    Пример вызова:
        Calculate("5" "+" "3")
    */
    if ((op[0] == '+' && op[1] == '\0') || (op[0] == '-' && op[1] == '\0') || (op[0] == '*' && op[1] == '\0') || (op[0] == '/' && op[1] == '\0')){
            
        if (!IsNumber(lhs) || !IsNumber(rhs)){
            std::cout << "Invalid number" << std::endl;
            return;
        }
        else {
            int32_t left = std::atol(lhs);
            int32_t right = std::atol(rhs);
            if (op[0] == '+' && op[1] == '\0'){
                std::cout << left + right << std::endl;
            }
            else if (op[0] == '-' && op[1] == '\0'){
                std::cout << left - right << std::endl;
            }
            else if (op[0] == '*' && op[1] == '\0'){
                std::cout << left * right << std::endl;
            }
            else if (op[0] == '/' && op[1] == '\0'){
                if (right == 0){
                    std::cout << "Division by zero" << std::endl;
                }
                else{
                    std::cout << left / right << std::endl;
                }
            }
            else{
                std::cout << "Invalid operator" << std::endl;
            }

        }
    }
    else{
        std::cout << "Invalid operator" << std::endl;
    }
}

int main(int argc, char** argv) {
    /*  
    Вход в программу
    Параметры:
        argc (int): количество аргументов командной строки,
        argv (char): сам массив аргументов командной строки
    Возвращаемо значение:
        завершение программы
    
    Пример вызова: ./build/calculator 2 + 3
    Результат: 5
    */
    if (argc != 4) {
        std::cout << "Usage: calculator <number> <operator> <number>" << std::endl;
        return 0;
    }

    Calculate(argv[1], argv[2], argv[3]);
    return 0;
}
