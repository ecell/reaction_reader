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

#include "Gillespie.hpp"


//============================================================
//	Debugging Utility
//============================================================
void display_vector_double(std::vector<double> &v)
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
void display_vector_int(std::vector<int> &v)
{
	bool first = true;
	for(std::vector<int>::iterator it = v.begin(); it != v.end(); it++) {
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
//	 Reaction Class Support Routines
//============================================================
Reaction::Reaction(void)
	: validp(false)
{;}

void Reaction::check(void) {
	if (0 < substances.size() && 0 < products.size() && k != -1) {
		this->validp = true;
	} else {
		this->validp = false;
	}
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
	int kk = k < (n - k) ? k : n-k;
	return permutation(n, kk) / factorial(kk);
}


//============================================================
//	GillespieSolver 	*Definitions
//============================================================
GillespieSolver::GillespieSolver(void)
{
	current_t = 0.0;

	// initialize random number generator
	T = gsl_rng_default;
	this->random_handle = gsl_rng_alloc(T);
	gsl_rng_set(this->random_handle, time(NULL));
}

GillespieSolver::~GillespieSolver(void)
{
	// freeing random number handle.
	gsl_rng_free(this->random_handle);
}

// GillespieSolver
//  	*about reactions
int GillespieSolver::reaction_add(void)
{
	int retval = this->models.size();
	Reaction new_react;
	new_react.validp = false;
	this->models.push_back(new_react);
	return retval;
}

void GillespieSolver::reaction_add_substance(
		int reaction_num,
		int specie_id,
		int stoichiometry )
{
	Reaction *r = &(this->models[reaction_num]);
	if (r == NULL)
		return;
	r->substances.push_back( Specie_index_number(specie_id, stoichiometry) );
	r->check();
}

void GillespieSolver::reaction_add_product(
		int reaction_num,
		int specie_id,
		double stoichiometry )
{
	Reaction *r = &(this->models[reaction_num]);
	if (r == NULL)
		return;
	r->products.push_back( Specie_index_number(specie_id, stoichiometry) );
	r->check();
}

void GillespieSolver::reaction_set_kinetic_parameter(int reaction_num, double k)
{
	Reaction *r = &(this->models[reaction_num]);
	if (r == NULL) 
		return;
	r->k = k;
	r->check();
}

// GillespieSolver
//  	*Properties.
void GillespieSolver::set_current_time(double new_t) 
{	this->current_t = new_t;	}

double GillespieSolver::get_current_time(void) 
{	return this->current_t;		}

int GillespieSolver::get_current_state(int *array, int len)
{
	if (array == NULL)
		return -1;

	int idx = 0;
	std::vector<int>::iterator it = this->current_state.begin();
	while( it != this->current_state.end() && idx < len ) {
		*(array + idx) = *it;
		idx++;
		it++;
	}
	return idx;
}

void GillespieSolver::set_current_state(int *array, int len) {
	this->current_state.clear();
	for(int i = 0; i < len; i++) {
		this->current_state.push_back(*(array + i));
	}
}

// GillespieSolver::step() function returns dt.
double GillespieSolver::step(void)
{
	if (models.size() == 0 || current_state.size() == 0) {
		// reactions or world status not initialized.
		return 0.0;
	}

	std::vector<double>	a(this->models.size() );

	for(int idx(0); idx < this->models.size(); idx++) {
		a[idx] = this->models[idx].k;
		for(Species_Vector::iterator it(models[idx].substances.begin());
				it != models[idx].substances.end();
				it++) {
			a[idx] *= combination(
					this->current_state[it->specie_index],
					it->specie_stoichiometry
				);
		}
	}

	double a_total = std::accumulate(a.begin(), a.end(), double(0.0) );
	double rnd_num1 = gsl_rng_uniform(this->random_handle);
	double dt = gsl_sf_log(1.0 / rnd_num1) / double(a_total);
	double rnd_num2 = gsl_rng_uniform(this->random_handle) * a_total;

	int u(-1);
	double acc(0.0);
	int len = a.size();
	do {
		u++;
		acc += a[u];
	} while ( acc < rnd_num2 && u < len - 1);

	this->current_t += dt;
	//	Ru(models[u]) occurs.
	for(Species_Vector::iterator it(models[u].substances.begin());
			it != models[u].substances.end();
			it++) {
		this->current_state[it->specie_index] -= it->specie_stoichiometry;
	}
	for(Species_Vector::iterator it(models[u].products.begin());
			it != models[u].products.end();
			it++) {
		this->current_state[it->specie_index] += it->specie_stoichiometry;
		}
	return dt;
}

double GillespieSolver::duration(double t) {
	double t_advanced(0.0);
	double dt(0.0);
	do {
		dt += this->step();
		if (dt == 0.0000) {
			break;
		}
		t_advanced += dt;
	} while (dt < t);
	return dt;
}

#ifdef UNITTEST
#define TEMP_ID(x)	x-'W'
int main(void)
{
	GillespieSolver gs;
	int world[] = {1000, 1000, 1000, 1000};
	gs.set_current_state(world, sizeof(world)/sizeof(int));
	/*
	Reaction r1;
	r1.substances.push_back( Specie_index_number (TEMP_ID('X'), 1) );
	r1.products.push_back( Specie_index_number( TEMP_ID('Y'), 1) );
	r1.k = 0.5;
	Reaction r2;
	r2.substances.push_back( Specie_index_number (TEMP_ID('Y'), 1) );
	r2.products.push_back( Specie_index_number (TEMP_ID('X'), 1) );
	r2.k = 0.2;
	Reaction r3;
	r3.substances.push_back( Specie_index_number (TEMP_ID('X'), 2) );
	r3.products.push_back( Specie_index_number (TEMP_ID('Z'), 1) );
	r3.k = 0.4;
	Reaction r4;
	r4.substances.push_back( Specie_index_number (TEMP_ID('Z'), 1) );
	r4.products.push_back( Specie_index_number (TEMP_ID('X'), 2) );
	r4.k = 0.2;
	Reaction r5;
	r5.substances.push_back( Specie_index_number (TEMP_ID('X'), 1) );
	r5.substances.push_back( Specie_index_number (TEMP_ID('W'), 1) );
	r5.products.push_back( Specie_index_number (TEMP_ID('X'), 2) );
	r5.k = 0.3;
	Reaction r6;
	r6.substances.push_back( Specie_index_number (TEMP_ID('X'), 2) );
	r6.products.push_back( Specie_index_number (TEMP_ID('X'), 1) );
	r6.products.push_back( Specie_index_number (TEMP_ID('W'), 1) );
	r6.k = 0.5;
	gs.models.push_back(r1);
	gs.models.push_back(r2);
	gs.models.push_back(r3);
	gs.models.push_back(r4);
	gs.models.push_back(r5);
	gs.models.push_back(r6);
	*/
	int ri1 = gs.reaction_add();
	gs.reaction_add_substance(ri1, TEMP_ID('X'), 1);
	gs.reaction_add_product(ri1, TEMP_ID('Y'), 1);
	gs.reaction_set_kinetic_parameter(ri1, 0.5);

	int ri2 = gs.reaction_add();
	gs.reaction_add_substance(ri2, TEMP_ID('Y'), 1);
	gs.reaction_add_product(ri2, TEMP_ID('X'), 1);
	gs.reaction_set_kinetic_parameter(ri2, 0.2);

	int ri3 = gs.reaction_add();
	gs.reaction_add_substance(ri3, TEMP_ID('X'), 2);
	gs.reaction_add_product(ri3, TEMP_ID('Z'), 1);
	gs.reaction_set_kinetic_parameter(ri3, 0.4);

	int ri4 = gs.reaction_add();
	gs.reaction_add_substance(ri4, TEMP_ID('Z'), 1);
	gs.reaction_add_product(ri4, TEMP_ID('X'), 2);
	gs.reaction_set_kinetic_parameter(ri4, 0.2);

	int ri5 = gs.reaction_add();
	gs.reaction_add_substance(ri5, TEMP_ID('X'), 1);
	gs.reaction_add_substance(ri5, TEMP_ID('W'), 1);
	gs.reaction_add_product(ri5, TEMP_ID('X'), 2);
	gs.reaction_set_kinetic_parameter(ri5, 0.3);

	int ri6 = gs.reaction_add();
	gs.reaction_add_substance(ri6, TEMP_ID('X'), 2);
	gs.reaction_add_product(ri6, TEMP_ID('X'), 1);
	gs.reaction_add_product(ri6, TEMP_ID('W'), 1);
	gs.reaction_set_kinetic_parameter(ri6, 0.5);

	double prev_t(0.0);
	while (gs.get_current_time() < 10.0) {
		gs.step();
		if (gs.get_current_time() - prev_t > 1.0) {
			prev_t = gs.get_current_time();
			fprintf(stderr,
					"%f, %d, %d, %d, %d\n",
					gs.get_current_time(),
					gs.current_state[0],
					gs.current_state[1],
					gs.current_state[2],
					gs.current_state[3]
			       );
		}
	}
	return 0;
}
#endif
