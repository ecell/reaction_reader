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

#define specie_index first
#define specie_stoichiometry second
typedef std::pair<int, int> Specie_index_number;

typedef std::vector<Specie_index_number> Species_Vector;

struct Reaction {
	Species_Vector	substances;
	Species_Vector	products;
	double k;
};

//============================================================
//	Gillespie Solver 	*Prototype Declaration.
//============================================================
class GillespieSolver {
private:
	// for random number 
	gsl_rng *random_handle;
	const gsl_rng_type *T;

	double current_t;

public:
	GillespieSolver();
	~GillespieSolver();

	// Functions about reactions.
	double step(void);
	double duration(double t);

	// Accesser
	double get_current_time(void);
	void set_current_time(double t);
	double generate_random(void) {
		return gsl_rng_uniform(this->random_handle);
	}

	std::vector<int>		current_state;
	std::vector<Reaction>		models;
};
