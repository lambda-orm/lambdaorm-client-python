# pylint: disable=invalid-name
"""Infrastructure layer for the LambdaORM REST API."""
from typing import List, Any, Optional
import requests
from lambdaorm.domain import (DomainSchema, Entity, EntityMapping, Format, Metadata,
MetadataConstraint, MetadataModel, MetadataParameter, MethodOptions, QueryOptions,
QueryPlan, Schema, SchemaConfig, Source, Stage, Version, Ping, Health, EnumDomain, Mapping)
from lambdaorm.application import ExpressionService, GeneralService, SchemaService, StageService

class RestHelper:
    """Helper class for REST API."""
    def __init__(self, url: str):
        self.url = url

    def solve_method_options(self, options: MethodOptions) -> MethodOptions:
        """Solves the method options."""
        if options is None:
            options = MethodOptions(Format.DEFAULT, 10)
        if options.format is None:
            options.format = Format.DEFAULT
        if options.timeout is None:
            options.timeout = 10
        return options
   
    def post(self, path: str, body: dict, options: MethodOptions=None)-> dict:
        """POST request to the REST API."""
        options = self.solve_method_options(options)
        params = { format: options.format.value }
        return requests.post(self.url + path, params= params, json=body, timeout= options.timeout).json()
    
    def get(self, path: str,options: MethodOptions=None)-> dict:
        """GET request to the REST API."""
        options = self.solve_method_options(options)
        params = { format: options.format.value }
        return requests.get(self.url + path,params= params, timeout= options.timeout).json()


class ExpressionRestService(ExpressionService):
    """Client for the ORM REST API."""
    def __init__(self, url: str):
        self.rest = RestHelper(url)
        
    async def model(self, expression: str) -> List[MetadataModel]:
        body = {'expression': expression}
        response = self.rest.post('/model',body)
        return MetadataModel.from_dict(response)
    
    async def parameters(self, expression: str) -> List[MetadataParameter]:
        body = {'expression': expression}
        response = self.rest.post('/parameters',body)
        return MetadataParameter.from_dict(response)

    async def constraints(self, expression: str) -> MetadataConstraint:
        body = {'expression': expression}
        response = self.rest.post('/constraints',body)
        return MetadataConstraint.from_dict(response)

    async def metadata(self, expression: str) -> Metadata:
        body = {'expression': expression}
        response = self.rest.post('/metadata',body)
        return Metadata.from_dict(response)

    async def plan(self,expression:str, options:QueryOptions,method_options: MethodOptions=None) -> QueryPlan:
        body = {'expression': expression, 'options': options.to_dict()}
        response =  self.rest.post('/plan',body,method_options)
        return QueryPlan.from_dict(response)
    
    async def execute(self,expression:str,data:dict=None, options:QueryOptions=None,method_options: MethodOptions=None) -> dict:
        body = {'expression': expression, 'data': data, 'options': options.to_dict()}
        return self.rest.post('/execute',body,method_options)
    
    async def execute_queued(self,expression:str,topic:str,data:dict=None, options:QueryOptions=None,method_options: MethodOptions=None) -> dict:
        body = {'expression': expression,'topic':topic, 'data': data, 'options': options.to_dict()}
        return self.rest.post('/execute-queued',body,method_options)

class GeneralRestService(GeneralService):
    """Interface for General Service."""
    def __init__(self, url: str):
        self.rest = RestHelper(url)
     
    async def version(self) -> Version:
        response =  self.rest.get('/version')
        return Version.from_dict(response)

    async def ping(self) -> Ping:
        response =  self.rest.get('/ping')
        return Ping.from_dict(response)

    async def health(self) -> Health:
        response =  self.rest.get('/health')
        return Health.from_dict(response)

    async def metrics(self) -> Any:
        return self.rest.get('/metrics')    

class SchemaRestService(SchemaService):
    """Service for interacting with schema-related operations."""
    def __init__(self, url: str):
        self.rest = RestHelper(url)

    async def version(self) -> Version:
        response =  self.rest.get('/version')
        return Version.from_dict(response)

    async def schema(self) -> Schema:
        response =  self.rest.get('/schema')
        return Schema.from_dict(response)

    async def domain(self) -> DomainSchema:
        response =  self.rest.get('/domain')
        return DomainSchema.from_dict(response)

    async def sources(self) -> List[Source]:
        response =  self.rest.get('/sources')
        return Source.from_dict(response)

    async def source(self, source: str) -> Optional[Source]:
        response =  self.rest.get('/sources/'+source)
        return Source.from_dict(response)

    async def entities(self) -> List[Entity]:
        response =  self.rest.get('/entities')
        return Entity.from_dict(response)

    async def entity(self, entity: str) -> Optional[Entity]:
        response =  self.rest.get('/entities/'+entity)
        return Entity.from_dict(response)

    async def enums(self) -> List[EnumDomain]:
        response =  self.rest.get('/enums')
        return EnumDomain.from_dict(response)

    async def enum(self, _enum: str) -> Optional[EnumDomain]:
        response =  self.rest.get('/enums/'+_enum)
        return EnumDomain.from_dict(response)

    async def mappings(self) -> List[Mapping]:
        response =  self.rest.get('/mappings')
        return Mapping.from_dict(response)

    async def mapping(self, mapping: str) -> Optional[Mapping]:
        response =  self.rest.get('/mappings/'+mapping)
        return Mapping.from_dict(response)

    async def entityMapping(self, mapping: str, entity: str) -> Optional[EntityMapping]:
        response =  self.rest.get('/mappings/'+mapping+'/'+entity)
        return EntityMapping.from_dict(response)

    async def stages(self) -> List[Stage]:
        response =  self.rest.get('/stages/')
        return Stage.from_dict(response)

    async def stage(self, stage: str) -> Optional[Stage]:
        response =  self.rest.get('/stages/'+stage)
        return Stage.from_dict(response)

    async def views(self) -> List[str]:
        response =  self.rest.get('/views')
        return response

class StageRestService(StageService):
    """Service for interacting with schema-related operations."""
    def __init__(self, url: str):
        self.rest = RestHelper(url)

    async def exists(self, stage: str) -> bool:
        return self.rest.get('/stages/'+stage+'/exists')

    async def export(self, stage: str) -> SchemaConfig:
        """Export the configuration of a stage."""
        response = self.rest.get('/stages/'+stage+'/export')
        return SchemaConfig.from_dict(response)

    async def import_(self, stage: str, data: SchemaConfig) -> None:
        response =  self.rest.post('//stages/'+stage+'/import',data)
        return QueryPlan.from_dict(response)


class RestOrm:
    """Client for the ORM REST API."""
    def __init__(self, url: str):
        self.expression = ExpressionRestService(url+'/expression')
        self.general = GeneralRestService(url)
        self.schema = SchemaRestService(url)
        self.stage = StageRestService(url)