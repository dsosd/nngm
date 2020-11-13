#ifndef uuid_guard_bf0f90b6_dc7825ad_983761f9_f77884f0
#define uuid_guard_bf0f90b6_dc7825ad_983761f9_f77884f0

#include <vector>

namespace tul{
namespace project{
namespace nngm{

enum class Partition_t{
	chapter,
	global,
	sentence
};

struct Partition_conf{
	Partition_t type;
	int min;
	int max;
};

class Partition{
public:
	Partition(const std::vector<Partition_conf>& conf_);
};

}
}
}

#endif // uuid_guard_bf0f90b6_dc7825ad_983761f9_f77884f0
