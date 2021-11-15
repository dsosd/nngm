#include "main.h"

#include <fstream>
#include <iostream>

#include "generator.h"
#include "partition.h"
#include "verify.h"

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

	//TODO maybe use json instead
	Partition_conf sentence_conf{
		Partition_t::sentence,
		2,
		40
	};
	Partition_conf chapter_conf{
		Partition_t::chapter,
		200,
		3000
	};
	Partition_conf global_conf{
		Partition_t::global,
		50000,
		//TODO replace with magic::null
		-1
	};

	Partition parter({sentence_conf, chapter_conf, global_conf});

	Verify verifier(Verify_t::none);

	Generator generator(&std::cout, verifier, parter, "seed");

	//Prng prng;
	//generator.run(prng);

	Engine engine;

	engine.init(Env{{"Sushi", "Marshmallow"}, {"Orange", "Phurr", "CCClaw"}});
	engine.run();
	engine.dump_out(std::cout);

	//dummy output
	//std::cout << "meow";
	//for (int i = 1; i < 50000; ++i){
	//	std::cout << " meow";
	//}
	//std::cout << "\n";

	return 0;
}

}
}
}
