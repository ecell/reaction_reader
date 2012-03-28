import numpy
import copy


class CompartmentSpace(object):
    def __init__(self, volume=1.0):
        self.species_list = []
        self.values = numpy.array([])

        # self.compartment_list = []
        self.volumes = numpy.array([volume])

    def add_species(self, species):
        if type(species) is list:
            size = len(self.values)
            for elem in species:
                if not elem in self.species_list:
                    self.species_list.append(elem)
            self.values = numpy.append(self.values, numpy.zeros(
                    len(self.species_list) - size, numpy.float64))
        else:
            if not species in self.species_list:
                self.species_list.append(species)
                self.values = numpy.append(self.values, [0.0])

    def get_species(self):
        return copy.copy(self.species_list)

    def __get_index(self, species):
        if species in self.species_list:
            return self.species_list.index(species)
        else:
            return None

    def set_value(self, species, value):
        idx = self.__get_index(species)
        if idx is not None:
            self.values[idx] = value

    def get_value(self, species):
        idx = self.__get_index(species)
        if idx is not None:
            return self.values[idx]

    def set_volume(self, value):
        if value > 0.0:
            self.volumes[0] = value

    def get_volume(self):
        return self.volumes[0]

    volume = property(get_volume, set_volume)

    def size(self):
        return len(self.values) + len(self.volumes)

    def get_data(self):
        data = numpy.empty(self.size())
        data[: len(self.values)] = self.values
        data[len(self.values): ] = self.volumes
        return data

    def set_data(self, value):
        if len(value) == self.size() and type(value) is numpy.ndarray:
            self.values = value[: len(self.values)]
            self.volumes = value[len(self.values): ]

    data = property(get_data, set_data)

class World(object):
    def __init__(self, volume=1.0):
        self.__space = CompartmentSpace()
        self.__space.volume = volume

        # this will be deprecated
        self.model = None
    
    def get_volume(self):
        return self.__space.volume

    def set_volume(self, value):
        self.__space.volume = value

    volume = property(get_volume, set_volume)

    def add_species(self, species):
        self.__space.add_species(species)

    def get_species(self):
        return self.__space.get_species()

    def get_value(self, species):
        self.__space.get_value(species)

    def set_value(self, species, value):
        return self.__space.set_value(species, value)

    def add_structure(self, structure):
        pass

    def get_data(self):
        return self.__space.data

    def set_data(self, value):
        self.__space.data = value

    data = property(get_data, set_data)

    def size(self):
        return self.__space.size()


if __name__ == '__main__':
    pass
