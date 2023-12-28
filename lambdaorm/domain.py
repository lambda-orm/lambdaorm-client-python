# pylint: disable=invalid-name
"""Domain classes for the lambdaorm package."""
from typing import List, Optional, Any, Tuple, Union
from dataclasses import dataclass
from enum import Enum

class RelationType(Enum):
    """Relation type for a property."""
    oneToMany = "oneToMany"
    manyToOne = "manyToOne"
    oneToOne = "oneToOne"

@dataclass
class MetadataParameter:
    """Metadata parameter for a property."""
    name: str
    type: str
    children: Optional[List["MetadataParameter"]] = None

    @classmethod
    def from_dict(cls, data: Union[dict, List[dict]]) -> Union["MetadataParameter", List["MetadataParameter"]]:
        """Creates a MetadataParameter instance from a dictionary or a list of dictionaries."""
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        elif isinstance(data, dict):
            name = data.get("name", "")
            type_ = data.get("type", "")
            children = cls.from_dict(data.get("children", []))
            return cls(name=name, type=type_, children=children)
        else:
            raise ValueError("Input must be a dictionary or a list of dictionaries")


@dataclass
class MetadataModel:
    """Metadata model for a property."""
    name: str
    type: str
    children: Optional[List["MetadataModel"]] = None

    def __init__(self, name: str, model_type: str, children: Optional[List["MetadataModel"]] = None):
        self.name = name
        self.type = model_type
        self.children = children

    @classmethod
    def from_dict(cls, data: Union[dict, List[dict]]) -> Union["MetadataModel", List["MetadataModel"]]:
        """Creates a MetadataModel instance from a dictionary or a list of dictionaries."""
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        elif isinstance(data, dict):
            name = data.get("name", "")
            model_type = data.get("type", "")
            children = cls.from_dict(data.get("children", []))
            return cls(name=name, model_type=model_type, children=children)
        else:
            raise ValueError("Input must be a dictionary or a list of dictionaries")

@dataclass
class Constraint:
    """Constraint for a property."""
    message: str
    condition: str

@dataclass
class MetadataConstraint:
    """Metadata constraint for a property."""
    entity: str
    constraints: List[Constraint]
    children: Optional[List["MetadataConstraint"]] = None

    @classmethod
    def from_dict(cls, data: Union[dict, List[dict]]) -> Union["MetadataConstraint", List["MetadataConstraint"]]:
        """Creates a MetadataConstraint instance from a dictionary or a list of dictionaries."""
        if isinstance(data, list):
            return [cls.from_dict(item) for item in data]
        elif isinstance(data, dict):
            entity = data.get("entity", "")
            constraints_data = data.get("constraints", [])
            constraints = [Constraint(**constraint_data) for constraint_data in constraints_data]
            children = cls.from_dict(data.get("children", []))
            return cls(entity=entity, constraints=constraints, children=children)
        else:
            raise ValueError("Input must be a dictionary or a list of dictionaries")

@dataclass
class Property:
    """Property for an entity."""
    name: str
    property_type: str
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

@dataclass
class EnumValue:
    """Enum value for an entity."""
    name: str
    value: Any

    @classmethod
    def from_dict(cls, data: dict) -> "EnumValue":
        """Create an instance of EnumValue from a dictionary."""
        return cls(
            name=data.get("name"),
            value=data.get("value")
        )

@dataclass
class EnumDomain:
    """Enum value for an entity."""
    name: str
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

@dataclass
class Relation:
    """Relation for an entity."""
    name: str
    type: RelationType
    from_: str
    entity: str
    to: str
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

@dataclass
class Dependent:
    """Dependent for an entity."""
    entity: str
    relation: Relation

    @classmethod
    def from_dict(cls, data: dict) -> "Dependent":
        """Create an instance of Dependent from a dictionary."""
        return cls(
            entity=data.get("entity", ""),
            relation=Relation.from_dict(data.get("relation", {}))
        )

@dataclass
class Index:
    """Index for an entity."""
    name: str
    fields: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Index":
        """Create an instance of Index from a dictionary."""
        return cls(
            name=data.get("name", ""),
            fields=data.get("fields", [])
        )

@dataclass
class Entity:
    """Entity for the domain model."""
    name: str
    primaryKey: List[str]
    uniqueKey: List[str]
    required: List[str]
    indexes: List[Index]
    properties: List[Any]
    relations: List[Relation]
    dependents: List[Dependent]
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

@dataclass
class RelationInfo:
    """Relation info for an entity."""
    previousRelation: str
    previousEntity: Entity
    entity: Entity
    relation: Relation

@dataclass
class PropertyMapping:
    """Property mapping for an entity."""
    mapping: str
    readMappingExp: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "PropertyMapping":
        """Create an instance of PropertyMapping from a dictionary."""
        return cls(
            mapping=data.get("mapping"),
            readMappingExp=data.get("readMappingExp")
        )

@dataclass
class EntityMapping(Entity):
    """Entity mapping for the domain model."""
    mapping: str
    sequence: str
    properties: List[PropertyMapping]

@dataclass
class FormatMapping(Entity):
    """Format mapping for an entity."""
    dateTime: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

@dataclass
class Mapping:
    """Mapping for the domain model."""
    name: str
    entities: List[EntityMapping]
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

@dataclass
class PropertyView:
    """Property view for an entity."""
    name: str
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

@dataclass
class EntityView:
    """Entity view for the domain model."""
    name: str
    properties: List[PropertyView]

    @classmethod
    def from_dict(cls, data: dict) -> "EntityView":
        """Create an instance of EntityView from a dictionary."""
        properties_data = data.get("properties", [])
        properties = [PropertyView.from_dict(prop) for prop in properties_data]
        return cls(
            name=data.get("name"),
            properties=properties
        )

@dataclass
class View:
    """View for the domain model."""
    name: str
    entities: List[EntityView]

    @classmethod
    def from_dict(cls, data: dict) -> "View":
        """Create an instance of View from a dictionary."""
        return cls(
            name=data.get("name", ""),
            entities=[EntityView.from_dict(entity_view) for entity_view in data.get("entities", [])]
        )

@dataclass
class Source:
    """Source for the domain model."""
    name: str
    dialect: str
    mapping: str
    connection: Any

    @classmethod
    def from_dict(cls, data: dict) -> "Source":
        """Create an instance of Source from a dictionary."""
        return cls(
            name=data.get("name", ""),
            dialect=data.get("dialect", ""),
            mapping=data.get("mapping", ""),
            connection=data.get("connection")
        )

@dataclass
class SourceRule:
    """Source rule for a stage."""
    name: str
    condition: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "SourceRule":
        """Create an instance of SourceRule from a dictionary."""
        return cls(
            name=data.get("name", ""),
            condition=data.get("condition")
        )

@dataclass
class Stage:
    """Stage for the domain model."""
    name: str
    sources: List[SourceRule]

    @classmethod
    def from_dict(cls, data: dict) -> "Stage":
        """Create an instance of Stage from a dictionary."""
        return cls(
            name=data.get("name", ""),
            sources=[SourceRule.from_dict(source_rule) for source_rule in data.get("sources", [])]
        )

@dataclass
class ListenerConfig:
    """Listener configuration for the domain model."""
    name: str
    on: List[str]
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

@dataclass
class TaskConfig:
    """Task configuration for the domain model."""
    name: str
    expression: str
    condition: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "TaskConfig":
        """Create an instance of TaskConfig from a dictionary."""
        return cls(
            name=data.get("name", ""),
            expression=data.get("expression"),
            condition=data.get("condition")
        )

@dataclass
class AppPathsConfig:
    """Application paths configuration for the domain model."""
    src: str
    data: str
    domain: str

    @classmethod
    def from_dict(cls, data: dict) -> "AppPathsConfig":
        """Create an instance of AppPathsConfig from a dictionary."""
        return cls(
            src=data.get("src", ""),
            data=data.get("data", ""),
            domain=data.get("domain", "")
        )

@dataclass
class DomainSchema:
    """Domain schema for the domain model."""
    version: str
    entities: List[Entity]
    enums: List[Any]

    @classmethod
    def from_dict(cls, data: dict) -> "DomainSchema":
        """Create an instance of DomainSchema from a dictionary."""
        return cls(
            version=data.get("version", ""),
            entities=[Entity.from_dict(entity_data) for entity_data in data.get("entities", [])],
            enums=data.get("enums", [])
        )

@dataclass
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

class ApplicationSchema:
    """Application schema for the domain model."""
    start: List[TaskConfig]
    listeners: List[ListenerConfig]
    end: List[TaskConfig]

    @classmethod
    def from_dict(cls, data: dict) -> "ApplicationSchema":
        """Create an instance of ApplicationSchema from a dictionary."""
        return cls(
            start=[TaskConfig.from_dict(item) for item in data.get("start", [])],
            listeners=[ListenerConfig.from_dict(item) for item in data.get("listeners", [])],
            end=[TaskConfig.from_dict(item) for item in data.get("end", [])]
        )

@dataclass
class Schema:
    """Schema for the domain model."""
    version: str
    domain: DomainSchema
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

# @dataclass
# class ModelConfig:
#     """Model configuration for the domain model."""
#     mappings: List[Mapping]

@dataclass
class MappingConfig:
    """Mapping configuration for the domain model."""
    mapping: Any
    pending: List[Any]
    inconsistency: List[Any]

    @classmethod
    def from_dict(cls, data: dict) -> "MappingConfig":
        """Create an instance of MappingConfig from a dictionary."""
        return cls(
            mapping=data.get("mapping"),
            pending=data.get("pending", []),
            inconsistency=data.get("inconsistency", [])
        )

@dataclass
class SchemaConfigEntity:
    """Schema configuration entity for the domain model."""
    entity: str
    rows: List[Any]

    @classmethod
    def from_dict(cls, data: dict) -> "SchemaConfigEntity":
        """Create an instance of SchemaConfigEntity from a dictionary."""
        return cls(
            entity=data.get("entity"),
            rows=data.get("rows", [])
        )

@dataclass
class SchemaConfig:
    """Schema configuration for the domain model."""
    entities: List[SchemaConfigEntity]

    @classmethod
    def from_dict(cls, data: dict) -> "SchemaConfig":
        """Create an instance of SchemaConfig from a dictionary."""
        return cls(
            entities=[SchemaConfigEntity.from_dict(entity_data) for entity_data in data.get("entities", [])]
        )

@dataclass
class Behavior:
    """Behavior for the domain model."""
    alias: Optional[str] = None
    property: str
    expression: str

    @classmethod
    def from_dict(cls, data: dict) -> "Behavior":
        """Create an instance of Behavior from a dictionary."""
        return cls(
            alias=data.get("alias"),
            property=data.get("property"),
            expression=data.get("expression")
        )

@dataclass
class Position:
    """Position for the domain model."""
    ln: int
    col: int

    @classmethod
    def from_dict(cls, data: dict) -> "Position":
        """Create an instance of Position from a dictionary."""
        return cls(
            ln=data.get("ln"),
            col=data.get("col")
        )

@dataclass
class Parameter:
    """Parameter for the domain model."""
    name: str
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

@dataclass
class Metadata:
    """Metadata for the domain model."""
    classtype: str
    pos: Position
    name: str
    children: Optional[List["Metadata"]] = None
    type: str
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


@dataclass
class QueryPlan:
    """Query plan for the domain model."""
    entity: str
    dialect: str
    source: str
    sentence: str
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

@dataclass
class QueryOptions:
    """Parameters for a query."""
    stage: Optional[str] = None
    view: Optional[str] = None
    chunkSize: Optional[int] = None
    tryAllCan: Optional[bool] = None
    headers: Optional[List[Tuple[str, Any]]] = None

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

class Format(Enum):
    """Result format for a query."""
    DEFAULT = "default"
    BEAUTIFUL = "beautiful"
    LIGHT = "light"

@dataclass
class MethodOptions:
    """Parameters for a method."""
    format: Format = Format.DEFAULT
    timeout: int = 10
    chunk: int = None

@dataclass
class Version:
    """Version for the domain model."""
    version: str

    @classmethod
    def from_dict(cls, data: dict) -> "Version":
        """Create an instance of Version from a dictionary."""
        return cls(
            version=data.get("version", "")
        )

@dataclass
class Ping:
    """Ping for the domain model."""
    message: str
    time: str

    @classmethod
    def from_dict(cls, data: dict) -> "Ping":
        """Create an instance of Ping from a dictionary."""
        return cls(
            message=data.get("message", ""),
            time=data.get("time", "")
        )

@dataclass
class Health:
    """Health for the domain model."""
    message: str
    time: str
    uptime: int

    @classmethod
    def from_dict(cls, data: dict) -> "Health":
        """Create an instance of Health from a dictionary."""
        return cls(
            message=data.get("message", ""),
            time=data.get("time", ""),
            uptime=data.get("uptime", 0)
        )
