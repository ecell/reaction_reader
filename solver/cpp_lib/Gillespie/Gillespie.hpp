#include <map>
#include <vector>
#include <string>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_sf_log.h>
#define PROTOTYPING(x) x	// __ ## x

#define chem_id	first
#define chem_v	second
typedef std::map<int,int> Specie_Id_Number;

#define ID(x) x
struct ReactionRule {
	Specie_Id_Number substitute;
	Specie_Id_Number product;
	double k;
	ReactionRule(void);
	ReactionRule(int n1, int id1, int n2, int id2, 
			int p_n1, int p_id1, int p_n2, int p_id2, double arg_k);
};

//============================================================
//	Gillespie Solver Prototype Declaration.
//============================================================
class GillespieSolver {
private:
	// for random number 
	gsl_rng *random_handle;
	const gsl_rng_type *T;

public:
	GillespieSolver();
	~GillespieSolver();
	double step(void);
	void duration(float t);
	double random_number(bool);

	float current_t;

	// XXX Prototyping!!!
	Specie_Id_Number		PROTOTYPING(current_state);
	std::vector<ReactionRule> 	PROTOTYPING(models);

};
