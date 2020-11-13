#ifndef uuid_guard_93abfdb6_516b349d_ec552213_792c69b8
#define uuid_guard_93abfdb6_516b349d_ec552213_792c69b8

#include <iosfwd>
#include <string>
#include <vector>

#include "partition.h"
#include "verify.h"

namespace tul{
namespace project{
namespace nngm{

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

#endif // uuid_guard_93abfdb6_516b349d_ec552213_792c69b8
