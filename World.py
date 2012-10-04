import numpy
import copy


class CompartmentSpace(object):
    def __init__(self, volume=1.0):
        self.__species_list = []
        self.__data = numpy.array([volume], numpy.float64)

    def add_species(self, species):
        num_of_species = len(self.__species_list)
        offset = self.species_offset + num_of_species

        if type(species) is list:
            for elem in species:
                if not elem in self.__species_list:
                    self.__species_list.append(elem)
            num_of_new_species = len(self.__species_list) - num_of_species

            self.__data = numpy.concatenate((
                    self.__data[: offset],
                    numpy.zeros(num_of_new_species, dtype=self.__data.dtype),
                    self.__data[offset: ]))
        else:
            if not species in self.__species_list:
                self.__species_list.append(species)
                self.__data = numpy.insert(self.__data, offset, 0.0)

    def get_species(self):
        return copy.copy(self.__species_list)

    def __get_index(self, species):
        if species in self.__species_list:
            return self.__species_list.index(species) + self.species_offset
        else:
            return None

    def set_value(self, species, value):
        idx = self.__get_index(species)
        if idx is not None:
            self.__data[idx] = value

    def get_value(self, species):
        idx = self.__get_index(species)
        if idx is not None:
            return self.__data[idx]

    def set_volume(self, value):
        if value > 0.0:
            self.__data[self.compartment_offset] = value

    def get_volume(self):
        return self.__data[self.compartment_offset]

    volume = property(get_volume, set_volume)

    def size(self):
        return self.__data.size

    def get_data(self):
        return self.__data.copy()

    def set_data(self, value):
        if (len(value) == self.size() and type(value) is numpy.ndarray and
            all(value[self.compartment_offset: ] > 0)):
            self.__data = value.copy()
        else:
            # raise an error for safety
            pass

    data = property(get_data, set_data)

    def get_species_offset(self):
        return 0

    species_offset = property(get_species_offset)

    def get_compartment_offset(self):
        return len(self.__species_list)

    compartment_offset = property(get_compartment_offset)

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
