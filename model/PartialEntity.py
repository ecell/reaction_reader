class PartialEntity(object):
    def __init__(self, key, sp):
        self.__key = key
        self.__sp = sp # RuleEntitySet

    @property
    def key(self):
        return self.__key
        
    @property
    def sp(self):
        return self.__sp
        
    def __call__(self, *args, **kwargs):
        entity = RuleEntity(self.key)




        entity = EntityType(self.key)

        # adds components without states to entity.
        for i in args:
            entity.add_component(i.key)

        # adds components with states to entity.
        for key, value in kwargs.items():
            states = StateType(key, [value.key])
            entity.add_component(key, {key: states})

        target = self.sp.add_entity(entity)

        # sets species' binding_state to BINDING_NONE (to be fixed.)
        for i in target.components.values():
            i.binding_state = BINDING_NONE
        for i in args:
            if type(i) == RuleEntityComponent:
                target_comp = target.find_components(i.key)[0]
                target_comp.binding_state = BINDING_SPECIFIED
                binding = Binding(i.bind_info, self.sp, target_comp, target_comp, False)
                target_comp.setbinding(binding)
                

        # sets species' state to key
        for key, value in kwargs.items():
            target.find_components(key)[0].set_state(key, value.key)

        # sets concreteness of species
        self.sp.concrete = True

        # registers species to model
        # sefl.model.register_species(self.sp)
        # self.sp = sp

        # print "PE.__call__()  : " + self.sp.str_simple()
        return self.sp

    def __str__(self):
        return str(self.sp)
