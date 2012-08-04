#include <cstdlib>
#include <cstdio>
#include <math.h>

#include <iostream>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_sf_log.h>

#include <vector>
#include <numeric>
#include <map>

#include <string>

#define PROTOTYPING(x) x	// __ ## x
#include "Gillespie.hpp"


//============================================================
//	Debugging Utility
//============================================================
void display_vector(std::vector<double> &v)
{
	bool first = true;
	for(std::vector<double>::iterator it = v.begin(); it != v.end(); it++) {
		if (first == true) {	
			first = false;
			std::cout << "{ ";
		} else {
			std::cout << ", ";	
		}
		std::cout << *it;
	}
	std::cout << " }";
	std::cout << std::endl;
}

//============================================================
//	Math Utility Functions
//============================================================
int factorial(int n) {
	int product(1);
	for(int i(1); i <= n; i++) {
		product *= i;
	}
	return product;
}

// calcurate nPk
int permutation(int n, int k) {
	int ans(1);
	for(int i(0); i < k; i++) {
		ans *= n;
		n--;
	}
	return ans;
}

int combination(int n, int k) {
	//printf("%d C %d\n", n, k);
	int kk = k < (n - k) ? k : n-k;
	return permutation(n, kk) / factorial(kk);
}

//============================================================
//	Reaction Rules (Temporary Use)
//============================================================
ReactionRule::ReactionRule(void) {;}
ReactionRule::ReactionRule(int n1, int id1, int n2, int id2, 
			int p_n1, int p_id1, int p_n2, int p_id2, double arg_k) {
	k = arg_k;
	substitute.insert(Specie_Id_Number::value_type(id1,n1));
	if (0 < id2) {
		substitute.insert(Specie_Id_Number::value_type(id2,n2));
	}
	product.insert(Specie_Id_Number::value_type(p_id1,p_n1));
	if (0 < p_id2) {
		product.insert(Specie_Id_Number::value_type(p_id2,p_n2));
	}
}

GillespieSolver::GillespieSolver(void)
	:current_t(0.0), 
	T(gsl_rng_default)
{
	// initialize random number generator
	this->random_handle = gsl_rng_alloc(T);
	gsl_rng_set(this->random_handle, time(NULL));

}

GillespieSolver::~GillespieSolver(void)
{
	// freeing random number handle.
	gsl_rng_free(this->random_handle);
}

double GillespieSolver::random_number(bool binit = false)
{	return gsl_rng_uniform(this->random_handle);	}

// GillespieSolver::step() function returns dt.
double GillespieSolver::step(void)
{
	// XXX 
	// refactoring 
	if (models.size() == 0, current_state.size() == 0) {
		// reactions or world status not initialized.
		return 0.0;
	}

	std::vector<double>	a(this->models.size());

	for(int idx(0); idx < this->models.size(); idx++) {
		a[idx] = this->models[idx].k;

		for(Specie_Id_Number::iterator it(models[idx].substitute.begin());
				it != models[idx].substitute.end();
				it++) {
			a[idx] *= combination(this->current_state[it->chem_id], it->chem_v);
		}
	}

	double a_total( std::accumulate(a.begin(), a.end(), double(0.0) ) );
	double rnd_num(gsl_rng_uniform(this->random_handle));
	double dt = gsl_sf_log(1.0 / rnd_num) / double(a_total);

	rnd_num = gsl_rng_uniform(this->random_handle) * a_total;

	int u(-1);
	double acc(0.0);
	do {
		u++;
		acc += a[u];
	} while ( acc < rnd_num && u <= a.size() - 1 );

	this->current_t += dt;
	//	Ru(models[u]) occurs.
	for(Specie_Id_Number::iterator it(models[u].substitute.begin());
			it != models[u].substitute.end();
			it++) {
		this->current_state[it->chem_id] -= it->chem_v;
	}
	for(Specie_Id_Number::iterator it(models[u].product.begin());
			it != models[u].product.end();
			it++) {
		this->current_state[it->chem_id] += it->chem_v;
	}

	return dt;
}

#ifdef UNITTEST

int main(void)
{
	GillespieSolver gs;
	gs.current_state.insert(Specie_Id_Number::value_type('X', 1000));
	gs.current_state.insert(Specie_Id_Number::value_type('Y', 1000));
	gs.current_state.insert(Specie_Id_Number::value_type('Z', 1000));
	gs.current_state.insert(Specie_Id_Number::value_type('W', 1000));
	gs.models.push_back(ReactionRule(1, ID('X'), 0, ID(0), 1, ID('Y'), 0, ID(0), 0.5));
	gs.models.push_back(ReactionRule(1, ID('Y'), 0, ID(0), 1, ID('X'), 0, ID(0), 0.2));
	gs.models.push_back(ReactionRule(2, ID('X'), 0, ID(0), 1, ID('Z'), 0, ID(0), 0.4));
	gs.models.push_back(ReactionRule(1, ID('Z'), 0, ID(0), 2, ID('X'), 0, ID(0), 0.2));
	gs.models.push_back(ReactionRule(1, ID('X'), 1, ID('W'), 2, ID('X'), 0, ID(0), 0.3));
	gs.models.push_back(ReactionRule(2, ID('X'), 0, ID(0), 1, ID('X'), 1, ID('W'), 0.5));
	double prev_t = 0.0;
	fprintf(stderr, "Unit Test\n      t\t\tX\tY\tZ\tW\n");
	while (gs.current_t < 10) {
		gs.step();
		if (gs.current_t - prev_t > 1.0) {
			fprintf(stderr, "%f\t%d\t%d\t%d\t%d\n",
					gs.current_t, 
					gs.current_state['X'], 
					gs.current_state['Y'],
					gs.current_state['Z'], 
					gs.current_state['W'] );
			prev_t = gs.current_t;
		}
	}
	return 0;
}

#endif
