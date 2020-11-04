#include "main.h"

#include <fstream>
#include <iostream>

namespace tul{
namespace project{
namespace nngm{

int main(int argc, char** argv){
	//args: [config_file]
	if (argc > 2){
		std::cerr << "Incorrect argc\n";
		return 1;
	}

	if (argc >= 2){
		std::ifstream config(argv[1]);
		//TODO use config
	}

	//dummy output
	std::cout << "meow";
	for (int i = 1; i < 50000; ++i){
		std::cout << " meow";
	}
	std::cout << "\n";

	return 0;
}

}
}
}
