# pylint: disable=invalid-name
"""Infrastructure layer for the LambdaORM REST API."""
from typing import List, Any, Optional
import subprocess
import json
import requests
from lambdaorm.domain import (CliCommandArgs, DomainSchema, Entity, EntityMapping, Metadata,
MetadataConstraint, MetadataModel, MetadataParameter, MethodOptions, QueryOptions,
QueryPlan, Schema, SchemaConfig, Source, Stage, Version, Ping, Health, EnumDomain, Mapping)
from lambdaorm.application import ( ExpressionService, GeneralService, IOrm,
SchemaService, StageService)

class RestHelper:
    """Helper class for Client REST API."""
    def __init__(self, url: str):
        self.url = url

    def solve_method_options(self, options: MethodOptions) -> MethodOptions:
        """Solves the method options."""
        if options is None:
            options = MethodOptions(10)
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
        response =  self.rest.get('/schema/version')
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
        response =  self.rest.post('/stages/'+stage+'/import',data)
        return QueryPlan.from_dict(response)

class RestClientOrm(IOrm):
    """Client for the ORM REST API."""
    def __init__(self, url: str):
        self.expression = ExpressionRestService(url)
        self.general = GeneralRestService(url)
        self.schema = SchemaRestService(url)
        self.stage = StageRestService(url)

    @property
    def get_general(self) -> GeneralService:
        return self.general
    
    @property
    def get_schema(self) -> SchemaService:
        return self.schema
    
    @property
    def get_stage(self) -> StageService:
        return self.stage
    
    async def model(self, expression: str) -> List[MetadataModel]:
        return self.expression.model(expression)

    async def parameters(self, expression: str) -> List[MetadataParameter]:
        return self.expression.parameters(expression)

    async def constraints(self, expression: str) -> MetadataConstraint:
        return self.expression.constraints(expression)

    async def metadata(self, expression: str) -> Metadata:
        return self.expression.metadata(expression)

    async def plan(self, expression: str, options: QueryOptions, method_options: MethodOptions = None) -> QueryPlan:
        return self.expression.plan(expression, options, method_options)

    async def execute(self, expression: str, data: dict = None, options: QueryOptions = None, method_options: MethodOptions = None) -> dict:
        return self.expression.execute(expression, data, options, method_options)

    async def execute_queued(self, expression: str, topic: str, data: dict = None, options: QueryOptions = None, method_options: MethodOptions = None) -> dict:
        return self.expression.execute_queued(expression, topic, data, options, method_options)




class CliCLientHelper:
    """Helper class for Client CLI"""
    def __init__(self, workspace: str):
        self.workspace = workspace

    def solve_method_options(self, options: MethodOptions) -> MethodOptions:
        """Solves the method options."""
        if options is None:
            options = MethodOptions(10)
        if options.timeout is None:
            options.timeout = 10
        return options
    
    def command(self, command: str,args:CliCommandArgs=None,options: MethodOptions = None) -> dict:
        """Executes a command."""        
        cmd = f"lambdaorm {command} -w {self.workspace}"
        if args is not None:
            cmd += f" -q {args.expression}"
            if args.data is not None:
                cmd += f" -d {args.data}"
            if args.options is not None:
                if args.options.stage is not None:
                    cmd += f" -s {args.options.stage}"
        options = self.solve_method_options(options)
        if options.environmentFile is not None:
            cmd += f" -e {options.environmentFile}"            
        result = subprocess.check_output(cmd, shell=True, cwd=self.workspace).decode('utf-8')
        if result is None:
            return None
        return json.loads(result)

class ExpressionCliService(ExpressionService):
    """Client for the ORM CLI API."""
    def __init__(self, workspace: str):
        self.cli = CliCLientHelper(workspace)
        
    async def model(self, expression: str) -> List[MetadataModel]:
        response = self.cli.command('model',CliCommandArgs(expression))
        return MetadataModel.from_dict(response)
    
    async def parameters(self, expression: str) -> List[MetadataParameter]:
        response = self.cli.command('parameters',CliCommandArgs(expression))
        return MetadataParameter.from_dict(response)

    async def constraints(self, expression: str) -> MetadataConstraint:
        response = self.cli.command('constraints',CliCommandArgs(expression))
        return MetadataParameter.from_dict(response)

    async def metadata(self, expression: str) -> Metadata:
        response = self.cli.command('metadata',CliCommandArgs(expression))
        return MetadataParameter.from_dict(response)

    async def plan(self,expression:str, options:QueryOptions,method_options: MethodOptions=None) -> QueryPlan:
        response = self.cli.command('plan',CliCommandArgs(expression,options=options),method_options)
        return QueryPlan.from_dict(response)
    
    async def execute(self,expression:str,data:dict=None, options:QueryOptions=None,method_options: MethodOptions=None) -> dict:
        response = self.cli.command('execute',CliCommandArgs(expression, data=data, options=options),method_options)
        return QueryPlan.from_dict(response)
    
    async def execute_queued(self,expression:str,topic:str,data:dict=None, options:QueryOptions=None,method_options: MethodOptions=None) -> dict:
        raise NotImplementedError
    
class GeneralCliService(GeneralService):
    """Interface for General Service."""
    def __init__(self, workspace: str):
        self.cli = CliCLientHelper(workspace)
     
    async def version(self) -> Version:
        raise NotImplementedError

    async def ping(self) -> Ping:
        raise NotImplementedError

    async def health(self) -> Health:
        raise NotImplementedError

    async def metrics(self) -> Any:
        raise NotImplementedError
    
class SchemaCliService(SchemaService):
    """Service for interacting with schema-related operations."""
    def __init__(self, workspace: str):
        self.cli = CliCLientHelper(workspace)

    async def version(self) -> Version:
        raise NotImplementedError

    async def schema(self) -> Schema:
        raise NotImplementedError

    async def domain(self) -> DomainSchema:
        raise NotImplementedError

    async def sources(self) -> List[Source]:
        raise NotImplementedError

    async def source(self, source: str) -> Optional[Source]:
        raise NotImplementedError

    async def entities(self) -> List[Entity]:
        raise NotImplementedError

    async def entity(self, entity: str) -> Optional[Entity]:
        raise NotImplementedError

    async def enums(self) -> List[EnumDomain]:
        raise NotImplementedError

    async def enum(self, _enum: str) -> Optional[EnumDomain]:
        raise NotImplementedError

    async def mappings(self) -> List[Mapping]:
        raise NotImplementedError

    async def mapping(self, mapping: str) -> Optional[Mapping]:
        raise NotImplementedError

    async def entityMapping(self, mapping: str, entity: str) -> Optional[EntityMapping]:
        raise NotImplementedError

    async def stages(self) -> List[Stage]:
        raise NotImplementedError

    async def stage(self, stage: str) -> Optional[Stage]:
        raise NotImplementedError

    async def views(self) -> List[str]:
        raise NotImplementedError
    
class StageCliService(StageService):
    """Service for interacting with schema-related operations."""
    def __init__(self, workspace: str):
        self.cli = CliCLientHelper(workspace)

    async def exists(self, stage: str) -> bool:
        raise NotImplementedError

    async def export(self, stage: str) -> SchemaConfig:
        response = self.cli.command('export',CliCommandArgs(options={"stage":stage} ))
        return SchemaConfig.from_dict(response)

    async def import_(self, stage: str, data: SchemaConfig) -> None:
        self.cli.command('import_',CliCommandArgs(data=data, options={"stage":stage} ))

class CliClientOrm(IOrm):
    """Client for the ORM CLI API."""
    def __init__(self, workspace: str):
        self.expression = ExpressionCliService(workspace)
        self.general = GeneralCliService(workspace)
        self.schema = SchemaCliService(workspace)
        self.stage = StageCliService(workspace)

    @property
    def get_general(self) -> GeneralService:
        return self.general
    
    @property
    def get_schema(self) -> SchemaService:
        return self.schema
    
    @property
    def get_stage(self) -> StageService:
        return self.stage
    
    async def model(self, expression: str) -> List[MetadataModel]:
        return self.expression.model(expression)

    async def parameters(self, expression: str) -> List[MetadataParameter]:
        return self.expression.parameters(expression)

    async def constraints(self, expression: str) -> MetadataConstraint:
        return self.expression.constraints(expression)

    async def metadata(self, expression: str) -> Metadata:
        return self.expression.metadata(expression)

    async def plan(self, expression: str, options: QueryOptions, method_options: MethodOptions = None) -> QueryPlan:
        return self.expression.plan(expression, options, method_options)

    async def execute(self, expression: str, data: dict = None, options: QueryOptions = None, method_options: MethodOptions = None) -> dict:
        return self.expression.execute(expression, data, options, method_options)

    async def execute_queued(self, expression: str, topic: str, data: dict = None, options: QueryOptions = None, method_options: MethodOptions = None) -> dict:
        return self.expression.execute_queued(expression, topic, data, options, method_options)

class OrmBuilder():
    """Factory for the ORM."""

    def build(self, workspace:str=None, url:str=None) -> IOrm:
        """Builds the ORM."""
        if url is not None:
            return RestClientOrm(url)
        elif workspace is not None:
            return CliClientOrm(workspace)
        else:
            raise ValueError("Either workspace or url must be provided")

class Orm(IOrm):
    """ORM API."""
    def __init__(self):
        self._orm = None

    def init(self, workspace:str=None, url:str=None)-> None:
        """Initializes the ORM."""
        self._orm = OrmBuilder().build(workspace,url)

    @property
    def get_general(self) -> GeneralService:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.general
    
    @property
    def get_schema(self) -> SchemaService:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.schema
    
    @property
    def get_stage(self) -> StageService:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.stage
    
    async def model(self, expression: str) -> List[MetadataModel]:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.expression.model(expression)

    async def parameters(self, expression: str) -> List[MetadataParameter]:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.expression.parameters(expression)

    async def constraints(self, expression: str) -> MetadataConstraint:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.expression.constraints(expression)

    async def metadata(self, expression: str) -> Metadata:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.expression.metadata(expression)

    async def plan(self, expression: str, options: QueryOptions, method_options: MethodOptions = None) -> QueryPlan:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.expression.plan(expression, options, method_options)

    async def execute(self, expression: str, data: dict = None, options: QueryOptions = None, method_options: MethodOptions = None) -> dict:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.expression.execute(expression, data, options, method_options)

    async def execute_queued(self, expression: str, topic: str, data: dict = None, options: QueryOptions = None, method_options: MethodOptions = None) -> dict:
        if self._orm is None:
            raise ValueError("ORM is not initialized")
        return self._orm.expression.execute_queued(expression, topic, data, options, method_options)