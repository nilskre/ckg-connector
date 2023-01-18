class MapperInterface:
    def create_mapping(self):
        """Create mapping between ontologies."""
        pass


def create_mappings(mappers):
    for mapper in mappers:
        mapper.create_mapping()
