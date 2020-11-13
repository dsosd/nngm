#include "generator.h"

#include <iostream>

namespace tul{
namespace project{
namespace nngm{

Generator::Generator(std::ostream* out_, Verify& verifier_, Partition& parter_, const std::string& seed_)
		:out(out_), verifier(verifier_), parter(parter_), seed{seed_}{
}

}
}
}
