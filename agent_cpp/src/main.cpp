// agent_cpp/src/main.cpp
#include <iostream>
#include "monitor.hpp"

int main() {
    std::cout << "C++ Agent started..." << std::endl;
    
    Monitor monitor;
    monitor.start();

    std::cout << "Agent stopped." << std::endl;
    return 0;
}
