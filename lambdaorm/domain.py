# pylint: disable=invalid-name
# pylint: disable=E1123
"""Domain classes for the lambdaorm package."""
from typing import List, Optional, Any, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from dataclasses_json import dataclass_json, LetterCase

class RelationType(Enum):
    """Relation type for a property."""
    oneToMany = "oneToMany"
    manyToOne = "manyToOne"
    oneToOne = "oneToOne"

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MetadataParameter:
    """Metadata parameter for a property."""
    name: Optional[str] = None
    type: Optional[str] = None
    children: Optional[List["MetadataParameter"]] = None

    def __init__(self, name: str, type: str, children: Optional[List["MetadataParameter"]] = None):
        self.name = name
        self.type = type
        self.children = children

    @staticmethod
    def from_dict(data:Any) -> Union["MetadataParameter", List["MetadataParameter"]]:
        """Creates a MetadataParameter instance from a dictionary or a list of dictionaries."""
        if isinstance(data, list):
            return [MetadataParameter.from_dict(item) for item in data]
        elif isinstance(data, dict):
            name = data.get("name", "")
            type = data.get("type", "")
            children = MetadataParameter.from_dict(data.get("children", []))
            return MetadataParameter(name=name, type=type, children=children)
        else:
            raise ValueError("Input must be a dictionary or a list of dictionaries")
    
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class MetadataModel:
    """Metadata model for a property."""
    name: Optional[str] = None
    type: Optional[str] = None
    children: Optional[List["MetadataModel"]] = None

    def __init__(self, name: str, type: str, children: Optional[List["MetadataModel"]] = None):
        self.name = name
        self.type = type
        self.children = children

    @classmethod
    def from_dict(cls, data: Union[dict, List[dict]]) -> Union["MetadataModel", List["MetadataModel"]]:
        """Creates a MetadataModel instance from a dictionary or a list of dictionaries."""
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        elif isinstance(data, dict):
            name = data.get("name", "")
            type = data.get("type", "")
            children = cls.from_dict(data.get("children", []))
            return cls(name=name, type=type, children=children)
        else:
            raise ValueError("Input must be a dictionary or a list of dictionaries")
    
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Constraint:
    """Constraint for a property."""
    message: Optional[str] = None
    condition: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Constraint":
        """Creates a Constraint instance from a dictionary."""
        return cls(
            message=data.get("message"),
            condition=data.get("condition")
        )

    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class MetadataConstraint:
    """Metadata constraint for a property."""
    entity: Optional[str] = None
    constraints: List[Constraint] = None
    children: Optional[List["MetadataConstraint"]] = None

    @staticmethod
    def from_dict(data: Union[dict, List[dict]]) -> Union["MetadataConstraint", List["MetadataConstraint"]]:
        """Creates a MetadataConstraint instance from a dictionary or a list of dictionaries."""
        if isinstance(data, list):
            return [MetadataConstraint.from_dict(item) for item in data]
        elif isinstance(data, dict):
            entity = data.get("entity", "")
            constraints_data = data.get("constraints", [])
            constraints = [Constraint(**constraint_data) for constraint_data in constraints_data]
            children = MetadataConstraint.from_dict(data.get("children", []))
            return MetadataConstraint(entity=entity, constraints=constraints, children=children)
        else:
            raise ValueError("Input must be a dictionary or a list of dictionaries")

    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Property:
    """Property for an entity."""
    name: Optional[str] = None
    property_type: Optional[str] = None
    length: Optional[int] = None
    required: Optional[bool] = None
    primaryKey: Optional[bool] = None
    autoIncrement: Optional[bool] = None
    view: Optional[bool] = None
    readExp: Optional[str] = None
    writeExp: Optional[str] = None
    default: Optional[str] = None
    readValue: Optional[str] = None
    writeValue: Optional[str] = None
    enum: Optional[str] = None
    key: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Property":
        """Creates a Property instance from a dictionary."""
        return cls(
            name=data.get("name"),
            property_type=data.get("propertyType"),
            length=data.get("length"),
            required=data.get("required"),
            primary_key=data.get("primaryKey"),
            auto_increment=data.get("autoIncrement"),
            view=data.get("view"),
            read_exp=data.get("readExp"),
            write_exp=data.get("writeExp"),
            default=data.get("default"),
            read_value=data.get("readValue"),
            write_value=data.get("writeValue"),
            enum=data.get("enum"),
            key=data.get("key")
        )

    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class EnumValue:
    """Enum value for an entity."""
    name: Optional[str] = None
    value: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict) -> "EnumValue":
        """Create an instance of EnumValue from a dictionary."""
        return cls(
            name=data.get("name"),
            value=data.get("value")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class EnumDomain:
    """Enum value for an entity."""
    name: Optional[str] = None
    extends: Optional[str] = None
    abstract: Optional[bool] = None
    values: List[EnumValue] = None

    @classmethod
    def from_dict(cls, data: dict) -> "EnumDomain":
        """Create an instance of EnumDomain from a dictionary."""
        return cls(
            name=data.get("name"),
            extends=data.get("extends"),
            abstract=data.get("abstract"),
            values=[EnumValue.from_dict(value_data) for value_data in data.get("values", [])]
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Relation:
    """Relation for an entity."""
    name: Optional[str] = None
    type: Optional[RelationType] = None
    from_: Optional[str] = None
    entity: Optional[str] = None
    to: Optional[str] = None
    composite: Optional[bool] = None
    weak: Optional[bool] = None
    target: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Relation":
        """Create an instance of Relation from a dictionary."""
        return cls(
            name=data.get("name", ""),
            type=RelationType[data.get("type", "")],
            from_=data.get("from", ""),
            entity=data.get("entity", ""),
            to=data.get("to", ""),
            composite=data.get("composite"),
            weak=data.get("weak"),
            target=data.get("target")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Dependent:
    """Dependent for an entity."""
    entity: Optional[str] = None
    relation: Optional[Relation] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Dependent":
        """Create an instance of Dependent from a dictionary."""
        return cls(
            entity=data.get("entity", ""),
            relation=Relation.from_dict(data.get("relation", {}))
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Index:
    """Index for an entity."""
    name: Optional[str] = None
    fields: List[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Index":
        """Create an instance of Index from a dictionary."""
        return cls(
            name=data.get("name", ""),
            fields=data.get("fields", [])
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Entity:
    """Entity for the domain model."""
    name: Optional[str] = None
    primaryKey: List[str] = None
    uniqueKey: List[str] = None
    required: List[str] = None
    indexes: List[Index] = None
    properties: List[Any] = None
    relations: List[Relation] = None
    dependents: List[Dependent] = None
    extends: Optional[str] = None
    abstract: Optional[bool] = None
    singular: Optional[str] = None
    view: Optional[bool] = None
    constraints: Optional[List[Any]] = None
    hadReadExps: Optional[bool] = None
    hadWriteExps: Optional[bool] = None
    hadReadValues: Optional[bool] = None
    hadWriteValues: Optional[bool] = None
    hadDefaults: Optional[bool] = None
    hadViewReadExp: Optional[bool] = None
    composite: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Entity":
        """Create an instance of Entity from a dictionary."""
        return cls(
            name=data.get("name", ""),
            primaryKey=data.get("primaryKey", []),
            uniqueKey=data.get("uniqueKey", []),
            required=data.get("required", []),
            indexes=[Index.from_dict(index_data) for index_data in data.get("indexes", [])],
            properties=data.get("properties", []),
            relations=[Relation.from_dict(relation_data) for relation_data in data.get("relations", [])],
            dependents=[Dependent.from_dict(dependent_data) for dependent_data in data.get("dependents", [])],
            extends=data.get("extends"),
            abstract=data.get("abstract"),
            singular=data.get("singular"),
            view=data.get("view"),
            constraints=data.get("constraints", []),
            hadReadExps=data.get("hadReadExps"),
            hadWriteExps=data.get("hadWriteExps"),
            hadReadValues=data.get("hadReadValues"),
            hadWriteValues=data.get("hadWriteValues"),
            hadDefaults=data.get("hadDefaults"),
            hadViewReadExp=data.get("hadViewReadExp"),
            composite=data.get("composite")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class RelationInfo:
    """Relation info for an entity."""
    previousRelation: Optional[str] = None
    previousEntity: Optional[Entity] = None
    entity: Optional[Entity] = None
    relation: Optional[Relation] = None

    @classmethod
    def from_dict(cls, data: dict) -> "RelationInfo":
        """Creates a RelationInfo instance from a dictionary."""
        return cls(
            previous_relation=data.get("previousRelation"),
            previous_entity=Entity.from_dict(data.get("previousEntity")),
            entity=Entity.from_dict(data.get("entity")),
            relation=Relation.from_dict(data.get("relation"))
        )

    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class PropertyMapping:
    """Property mapping for an entity."""
    mapping: Optional[str] = None
    readMappingExp: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "PropertyMapping":
        """Create an instance of PropertyMapping from a dictionary."""
        return cls(
            mapping=data.get("mapping"),
            readMappingExp=data.get("readMappingExp")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class EntityMapping(Entity):
    """Entity mapping for the domain model."""
    mapping: Optional[str] = None
    sequence: Optional[str] = None
    properties: List[PropertyMapping] = None

    @classmethod
    def from_dict(cls, data: dict) -> "EntityMapping":
        """Creates an EntityMapping instance from a dictionary."""
        return cls(
            name=data.get("name"),
            label=data.get("label"),
            plural_label=data.get("pluralLabel"),
            description=data.get("description"),
            mapping=data.get("mapping"),
            sequence=data.get("sequence"),
            properties=[PropertyMapping.from_dict(prop_data) for prop_data in data.get("properties", [])]
        )

    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class FormatMapping(Entity):
    """Format mapping for an entity."""
    dateTime: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "FormatMapping":
        """Creates a FormatMapping instance from a dictionary."""
        return cls(
            name=data.get("name"),
            label=data.get("label"),
            plural_label=data.get("pluralLabel"),
            description=data.get("description"),
            date_time=data.get("dateTime"),
            date=data.get("date"),
            time=data.get("time")
        )

    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Mapping:
    """Mapping for the domain model."""
    name: Optional[str] = None
    entities: List[EntityMapping]= None
    extends: Optional[str] = None
    mapping: Optional[str] = None
    format: Optional[FormatMapping] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Mapping":
        """Create an instance of Mapping from a dictionary."""
        return cls(
            name=data.get("name", ""),
            entities=[EntityMapping.from_dict(entity_mapping) for entity_mapping in data.get("entities", [])],
            extends=data.get("extends"),
            mapping=data.get("mapping"),
            format=FormatMapping.from_dict(data.get("format", {}))
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class PropertyView:
    """Property view for an entity."""
    name: Optional[str] = None
    readExp: Optional[str] = None
    exclude: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict) -> "PropertyView":
        """Create an instance of PropertyView from a dictionary."""
        return cls(
            name=data.get("name"),
            readExp=data.get("readExp"),
            exclude=data.get("exclude")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class EntityView:
    """Entity view for the domain model."""
    name: Optional[str] = None
    properties: List[PropertyView] = None

    @classmethod
    def from_dict(cls, data: dict) -> "EntityView":
        """Create an instance of EntityView from a dictionary."""
        properties_data = data.get("properties", [])
        properties = [PropertyView.from_dict(prop) for prop in properties_data]
        return cls(
            name=data.get("name"),
            properties=properties
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class View:
    """View for the domain model."""
    name: Optional[str] = None
    entities: List[EntityView] = None

    @classmethod
    def from_dict(cls, data: dict) -> "View":
        """Create an instance of View from a dictionary."""
        return cls(
            name=data.get("name", ""),
            entities=[EntityView.from_dict(entity_view) for entity_view in data.get("entities", [])]
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Source:
    """Source for the domain model."""
    name: Optional[str] = None
    dialect: Optional[str] = None
    mapping: Optional[str] = None
    connection: Optional[Any]= None

    @classmethod
    def from_dict(cls, data: dict) -> "Source":
        """Create an instance of Source from a dictionary."""
        return cls(
            name=data.get("name", ""),
            dialect=data.get("dialect", ""),
            mapping=data.get("mapping", ""),
            connection=data.get("connection")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class SourceRule:
    """Source rule for a stage."""
    name: Optional[str] = None
    condition: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "SourceRule":
        """Create an instance of SourceRule from a dictionary."""
        return cls(
            name=data.get("name", ""),
            condition=data.get("condition")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Stage:
    """Stage for the domain model."""
    name: Optional[str] = None
    sources: List[SourceRule] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Stage":
        """Create an instance of Stage from a dictionary."""
        return cls(
            name=data.get("name", ""),
            sources=[SourceRule.from_dict(source_rule) for source_rule in data.get("sources", [])]
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class ListenerConfig:
    """Listener configuration for the domain model."""
    name: Optional[str] = None
    on: List[str] = None
    condition: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None
    error: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ListenerConfig":
        """Create an instance of ListenerConfig from a dictionary."""
        return cls(
            name=data.get("name"),
            on=data.get("on", []),
            condition=data.get("condition"),
            before=data.get("before"),
            after=data.get("after"),
            error=data.get("error")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class TaskConfig:
    """Task configuration for the domain model."""
    name: Optional[str] = None
    expression: Optional[str] = None
    condition: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "TaskConfig":
        """Create an instance of TaskConfig from a dictionary."""
        return cls(
            name=data.get("name", ""),
            expression=data.get("expression"),
            condition=data.get("condition")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class AppPathsConfig:
    """Application paths configuration for the domain model."""
    src: Optional[str] = None
    data: Optional[str] = None
    domain: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "AppPathsConfig":
        """Create an instance of AppPathsConfig from a dictionary."""
        return cls(
            src=data.get("src", ""),
            data=data.get("data", ""),
            domain=data.get("domain", "")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class DomainSchema:
    """Domain schema for the domain model."""
    version: Optional[str] = None
    entities: List[Entity] = None
    enums: List[Any] = None

    @classmethod
    def from_dict(cls, data: dict) -> "DomainSchema":
        """Create an instance of DomainSchema from a dictionary."""
        return cls(
            version=data.get("version", ""),
            entities=[Entity.from_dict(entity_data) for entity_data in data.get("entities", [])],
            enums=data.get("enums", [])
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class InfrastructureSchema:
    """Infrastructure schema for the domain model."""
    paths: Optional[AppPathsConfig] = None
    mappings: Optional[List[Mapping]] = None
    views: Optional[List[View]] = None
    sources: Optional[List[Source]] = None
    stages: Optional[List[Stage]] = None

    @classmethod
    def from_dict(cls, data: dict) -> "InfrastructureSchema":
        """Create an instance of InfrastructureSchema from a dictionary."""
        return cls(
            paths=AppPathsConfig.from_dict(data.get("paths", {})),
            mappings=[Mapping.from_dict(mapping) for mapping in data.get("mappings", [])],
            views=[View.from_dict(view) for view in data.get("views", [])],
            sources=[Source.from_dict(source) for source in data.get("sources", [])],
            stages=[Stage.from_dict(stage) for stage in data.get("stages", [])]
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

class ApplicationSchema:
    """Application schema for the domain model."""
    start: List[TaskConfig] = None
    listeners: List[ListenerConfig] = None
    end: List[TaskConfig] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ApplicationSchema":
        """Create an instance of ApplicationSchema from a dictionary."""
        return cls(
            start=[TaskConfig.from_dict(item) for item in data.get("start", [])],
            listeners=[ListenerConfig.from_dict(item) for item in data.get("listeners", [])],
            end=[TaskConfig.from_dict(item) for item in data.get("end", [])]
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Schema:
    """Schema for the domain model."""
    version: Optional[str] = None
    domain: Optional[DomainSchema] = None
    infrastructure: Optional[InfrastructureSchema] = None
    application: Optional[ApplicationSchema] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Schema":
        """Create an instance of Schema from a dictionary."""
        return cls(
            version=data.get("version", ""),
            domain=DomainSchema.from_dict(data.get("domain", {})),
            infrastructure=InfrastructureSchema.from_dict(data.get("infrastructure", {})),
            application=ApplicationSchema.from_dict(data.get("application", {}))
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class MappingConfig:
    """Mapping configuration for the domain model."""
    mapping: Optional[Any] = None
    pending: List[Any] = None
    inconsistency: List[Any] = None

    @classmethod
    def from_dict(cls, data: dict) -> "MappingConfig":
        """Create an instance of MappingConfig from a dictionary."""
        return cls(
            mapping=data.get("mapping"),
            pending=data.get("pending", []),
            inconsistency=data.get("inconsistency", [])
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class SchemaConfigEntity:
    """Schema configuration entity for the domain model."""
    entity: Optional[str] = None
    rows: List[Any] = None

    @classmethod
    def from_dict(cls, data: dict) -> "SchemaConfigEntity":
        """Create an instance of SchemaConfigEntity from a dictionary."""
        return cls(
            entity=data.get("entity"),
            rows=data.get("rows", [])
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class SchemaConfig:
    """Schema configuration for the domain model."""
    entities: List[SchemaConfigEntity] = None

    @classmethod
    def from_dict(cls, data: dict) -> "SchemaConfig":
        """Create an instance of SchemaConfig from a dictionary."""
        return cls(
            entities=[SchemaConfigEntity.from_dict(entity_data) for entity_data in data.get("entities", [])]
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Behavior:
    """Behavior for the domain model."""
    alias: Optional[str] = None
    property: Optional[str] = None
    expression: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Behavior":
        """Create an instance of Behavior from a dictionary."""
        return cls(
            alias=data.get("alias"),
            property=data.get("property"),
            expression=data.get("expression")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Position:
    """Position for the domain model."""
    ln: Optional[int] = None
    col: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Position":
        """Create an instance of Position from a dictionary."""
        return cls(
            ln=data.get("ln"),
            col=data.get("col")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Parameter:
    """Parameter for the domain model."""
    name: Optional[str] = None
    type: Optional[str] = None
    default: Optional[Any] = None
    value: Optional[Any] = None
    multiple: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Parameter":
        """Create an instance of Parameter from a dictionary."""
        return cls(
            name=data.get("name"),
            type=data.get("type"),
            default=data.get("default"),
            value=data.get("value"),
            multiple=data.get("multiple")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Metadata:
    """Metadata for the domain model."""
    classtype: Optional[str] = None
    pos: Optional[Position] = None
    name: Optional[str] = None
    children: Optional[List["Metadata"]] = None
    type: Optional[str] = None
    returnType: Optional[str] = None
    entity: Optional[str] = None
    columns: Optional[List[Property]] = None
    property: Optional[str] = None
    parameters: Optional[List[Parameter]] = None
    constraints: Optional[List[Constraint]] = None
    values: Optional[List[Behavior]] = None
    defaults: Optional[List[Behavior]] = None
    relation: Optional[Relation] = None
    clause: Optional[str] = None
    alias: Optional[str] = None
    isRoot: Optional[bool] = None
    number: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Metadata":
        """Creates a Metadata instance from a dictionary."""
        pos_data = data.get("pos", {})
        pos = Position(ln=pos_data.get("ln", 0), col=pos_data.get("col", 0))
        columns_data = data.get("columns", [])
        columns = [Property(**column_data) for column_data in columns_data]
        parameters_data = data.get("parameters", [])
        parameters = [Parameter(**param_data) for param_data in parameters_data]
        constraints_data = data.get("constraints", [])
        constraints = [Constraint(**constraint_data) for constraint_data in constraints_data]
        values_data = data.get("values", [])
        values = [Behavior(**value_data) for value_data in values_data]
        defaults_data = data.get("defaults", [])
        defaults = [Behavior(**default_data) for default_data in defaults_data]
        relation_data = data.get("relation", {})
        relation = Relation(**relation_data)
        
        return cls(
            classtype=data.get("classtype", ""),
            pos=pos,
            name=data.get("name", ""),
            children=[cls.from_dict(child_data) for child_data in data.get("children", [])],
            type=data.get("type", ""),
            returnType=data.get("returnType"),
            entity=data.get("entity"),
            columns=columns,
            property=data.get("property"),
            parameters=parameters,
            constraints=constraints,
            values=values,
            defaults=defaults,
            relation=relation,
            clause=data.get("clause"),
            alias=data.get("alias"),
            isRoot=data.get("isRoot"),
            number=data.get("number")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class QueryPlan:
    """Query plan for the domain model."""
    entity: Optional[str] = None
    dialect: Optional[str] = None
    source: Optional[str] = None
    sentence: Optional[str] = None
    children: Optional[List["QueryPlan"]] = None

    @classmethod
    def from_dict(cls, data: dict) -> "QueryPlan":
        """Creates a QueryPlan instance from a dictionary."""
        return cls(
            entity=data.get("entity", ""),
            dialect=data.get("dialect", ""),
            source=data.get("source", ""),
            sentence=data.get("sentence", ""),
            children=[cls.from_dict(child_data) for child_data in data.get("children", [])] if data.get("children") else None
        )
    
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class QueryOptions:
    """Parameters for a query."""
    stage: Optional[str] = None
    view: Optional[str] = None
    chunkSize: Optional[int] = None
    tryAllCan: Optional[bool] = None
    headers: Optional[List[Tuple[str, Any]]] = None

    def __init__(
        self,
        stage: Optional[str] = None,
        view: Optional[str] = None,
        chunk_size: Optional[int] = None,
        try_all_can: Optional[bool] = None,
        headers: Optional[List[Tuple[str, Any]]] = None
    ):
        self.stage = stage
        self.view = view
        self.chunk_size = chunk_size
        self.try_all_can = try_all_can
        self.headers = headers

    @classmethod
    def from_dict(cls, data: dict) -> "QueryOptions":
        """Create an instance of QueryOptions from a dictionary."""
        return cls(
            stage=data.get("stage"),
            view=data.get("view"),
            chunkSize=data.get("chunkSize"),
            tryAllCan=data.get("tryAllCan"),
            headers=data.get("headers")
        )
    
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()


@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class MethodOptions:
    """Parameters for a method."""
    timeout: int = 10
    chunk: int = None
    environmentFile: Optional[str] = None

    def __init__(
        self,
        timeout: int = 10,
        chunk: int = None,
        environment_file: Optional[str] = None
    ):
        self.timeout = timeout
        self.chunk = chunk
        self.environment_file = environment_file

    @classmethod
    def from_dict(cls, data: dict) -> "MethodOptions":
        """Creates a MethodOptions instance from a dictionary."""
        return cls(
            timeout=data.get("timeout", 10),
            chunk=data.get("chunk"),
            environment_file=data.get("environmentFile")
        )

    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Version:
    """Version for the domain model."""
    version: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Version":
        """Create an instance of Version from a dictionary."""
        return cls(
            version=data.get("version", "")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Ping:
    """Ping for the domain model."""
    message: Optional[str] = None
    time: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Ping":
        """Create an instance of Ping from a dictionary."""
        return cls(
            message=data.get("message", ""),
            time=data.get("time", "")
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class Health:
    """Health for the domain model."""
    message: Optional[str] = None
    time: Optional[str] = None
    uptime: Optional[int]= None

    @classmethod
    def from_dict(cls, data: dict) -> "Health":
        """Create an instance of Health from a dictionary."""
        return cls(
            message=data.get("message", ""),
            time=data.get("time", ""),
            uptime=data.get("uptime", 0)
        )
    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()

@dataclass
@dataclass_json(letter_case=LetterCase.CAMEL)
class CliCommandArgs:
    """Command line arguments."""
    expression: Optional[str]=None
    data: Optional[dict] = None
    options:Optional[QueryOptions] = None
    path: Optional[str]=None

    @classmethod
    def from_dict(cls, data: dict) -> "CliCommandArgs":
        """Creates a CliCommandArgs instance from a dictionary."""
        return cls(
            expression=data.get("expression"),
            data=data.get("data"),
            options=QueryOptions.from_dict(data.get("options")),
            path=data.get("path"),
        )

    def to_dict(self) -> dict:
        """Converts instance to a dictionary."""
        return self.to_dict()
