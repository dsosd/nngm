#include "generator.h"

#include <iostream>

namespace tul{
namespace project{
namespace nngm{

bool Engine::init(const Env& env_){
	env = Env_node{env_};
	env.children.push_back({Theme{"happy"}});

	auto& theme = env.children[0];
	theme.children.push_back({Clause{{"'pc", "'npc"}, {"'pc", "talk", "'npc"}}});

	auto& clause = theme.children[0];
	clause.children.push_back(Word_node{""});
	return true;
}

bool Engine::run(int steps){
	for (int i = 0; i < steps; ++i){
		for (int j = 0; j < 5; ++j){
			env.children.push_back(
				std::vector<Theme_node>{{Theme{"sad"}}, {Theme{"mad"}}, {Theme{"happy"}}}[((i + 1) * (j + 2)) % 3]
			);

			auto& theme = env.children[env.children.size() - 1];
			for (int k = 0; k < 20; ++k){
				theme.children.push_back(
					env.children[0].children[0]
				);

				auto& clause = theme.children[theme.children.size() - 1];
				for (auto tmpl_word: clause.data.template_){
					std::string word;
					if (clause.data.variables.count(tmpl_word)){
						if (tmpl_word == "'pc"){
							word = env.data.pcs[(i * 11 + j * 7 + k * 5 + 3) % env.data.pcs.size()];
						}
						else if (tmpl_word == "'npc"){
							word = env.data.npcs[(i * 11 + j * 7 + k * 5 + 3) % env.data.npcs.size()];
						}
						else{
							throw std::exception();
						}
					}
					else{
						word = tmpl_word;
					}

					clause.children.push_back(Word_node{word});
					out << word << " ";
				}
			}
		}
	}
	return true;
}

std::size_t Engine::dump_out(std::ostream& out_stream){
	auto temp = out.str();

	out_stream << temp;

	return temp.size();
}

Generator::Generator(std::ostream* out_, Verify& verifier_, Partition& parter_, const std::string& seed_)
		:out(out_), verifier(verifier_), parter(parter_), seed{seed_}{
}

}
}
}
