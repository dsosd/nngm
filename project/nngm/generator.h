#ifndef uuid_guard_93abfdb6_516b349d_ec552213_792c69b8
#define uuid_guard_93abfdb6_516b349d_ec552213_792c69b8

#include <iosfwd>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>

#include "partition.h"
#include "verify.h"

namespace tul{
namespace project{
namespace nngm{

template<typename T, typename U>
struct Node{
	T data;
	std::vector<U> children;
};

template<typename T>
struct Node<T, void>{
	T data;
};

enum class Node_t{
	env,
	theme,
	idea,
	clause,
	aesthetic,
	word
};

struct Env_rule{
	Node_t type;

	double activation_prob;
	std::map<std::string, std::vector<std::string>> propagation;
};

struct Env{
	//player and non-player characters
	std::vector<std::string> pcs;
	std::vector<std::string> npcs;

	std::vector<Env_rule> rules;
};

struct Theme{
	std::string id;
};

struct Clause{
	std::set<std::string> variables;
	std::vector<std::string> template_;
};

//TODO fill in intermediary nodes as we flesh this out
typedef Node<std::string, void> Word_node;
typedef Node<Clause, Word_node> Clause_node;
typedef Node<Theme, Clause_node> Theme_node;
typedef Node<Env, Theme_node> Env_node;

class Engine{
public:
	bool init(const Env& env_);

	bool run(int steps = 1);
	std::size_t dump_out(std::ostream& out_stream);
private:
	Env_node env;

	std::stringstream out;
};

class Generator{
public:
	Generator(std::ostream* out_, Verify& verifier_, Partition& parter_, const std::string& seed_);
private:
	std::ostream* out;

	Verify& verifier;
	Partition& parter;

	std::vector<std::string> seed;
};

}
}
}

#include "generator.ipp"

#endif // uuid_guard_93abfdb6_516b349d_ec552213_792c69b8
