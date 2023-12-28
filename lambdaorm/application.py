# pylint: disable=invalid-name
"""This module contains the main class of the library."""
from typing import List, Any, Optional
from lambdaorm.domain import (Metadata, MetadataConstraint, MetadataModel,
MetadataParameter, MethodOptions,QueryOptions, QueryPlan, SchemaConfig,Version, Ping, Health,
Schema, DomainSchema, Entity, Enum, Mapping, EntityMapping, Stage )

class ExpressionService:
    """Interface for Expression Service."""

    async def model(self, expression: str) -> List[MetadataModel]:
        """Returns the model for the given expression."""
        raise NotImplementedError

    async def parameters(self, expression: str) -> List[MetadataParameter]:
        """Returns the parameters for the given expression."""
        raise NotImplementedError

    async def constraints(self, expression: str) -> MetadataConstraint:
        """Returns the constraints for the given expression."""
        raise NotImplementedError

    async def metadata(self, expression: str) -> Metadata:
        """Returns the metadata for the given expression."""
        raise NotImplementedError

    async def plan(self, expression: str, options: QueryOptions, method_options: MethodOptions = None) -> QueryPlan:
        """Returns the query plan for the given expression."""
        raise NotImplementedError

    async def execute(self, expression: str, data: dict = None, options: QueryOptions = None, method_options: MethodOptions = None) -> dict:
        """Execute query for the given expression."""
        raise NotImplementedError

    async def execute_queued(self, expression: str, topic: str, data: dict = None, options: QueryOptions = None, method_options: MethodOptions = None) -> dict:
        """Queue execute query for the given expression."""
        raise NotImplementedError

class GeneralService:
    """Interface for General Service."""
    async def version(self) -> Version:
        """Returns the version of the service."""
        raise NotImplementedError

    async def ping(self) -> Ping:
        """Returns the ping of the service."""
        raise NotImplementedError

    async def health(self) -> Health:
        """Returns the health of the service."""
        raise NotImplementedError

    async def metrics(self) -> Any:
        """Returns the metrics of the service.s"""
        raise NotImplementedError

class SchemaService:
    """Service for interacting with schema-related operations."""

    async def version(self) -> dict:
        """Get the version information."""
        raise NotImplementedError

    async def schema(self) -> Schema:
        """Get the full schema."""
        raise NotImplementedError

    async def domain(self) -> DomainSchema:
        """Get the domain schema."""
        raise NotImplementedError

    async def sources(self) -> List[dict]:
        """Get a list of sources."""
        raise NotImplementedError

    async def source(self, source: str) -> Optional[dict]:
        """Get information about a specific source."""
        raise NotImplementedError

    async def entities(self) -> List[Entity]:
        """Get a list of entities."""
        raise NotImplementedError

    async def entity(self, entity: str) -> Optional[Entity]:
        """Get information about a specific entity."""
        raise NotImplementedError

    async def enums(self) -> List[Enum]:
        """Get a list of enums."""
        raise NotImplementedError

    async def enum(self, _enum: str) -> Optional[Enum]:
        """Get information about a specific enum."""
        raise NotImplementedError

    async def mappings(self) -> List[Mapping]:
        """Get a list of mappings."""
        raise NotImplementedError

    async def mapping(self, mapping: str) -> Optional[Mapping]:
        """Get information about a specific mapping."""
        raise NotImplementedError

    async def entityMapping(self, mapping: str, entity: str) -> Optional[EntityMapping]:
        """Get information about a specific entity mapping."""
        raise NotImplementedError

    async def stages(self) -> List[Stage]:
        """Get a list of stages."""
        raise NotImplementedError

    async def stage(self, stage: str) -> Optional[Stage]:
        """Get information about a specific stage."""
        raise NotImplementedError

    async def views(self) -> List[str]:
        """Get a list of views."""
        raise NotImplementedError

class StageService:
    """Service for interacting with stage-related operations."""

    async def exists(self, stage: str) -> bool:
        """
        Check if a stage exists.

        Args:
            stage (str): The name of the stage.

        Returns:
            bool: True if the stage exists, False otherwise.
        """
        raise NotImplementedError

    async def export(self, stage: str) -> SchemaConfig:
        """
        Export the configuration of a stage.

        Args:
            stage (str): The name of the stage.

        Returns:
            SchemaConfig: The configuration of the stage.
        """
        raise NotImplementedError

    async def import_(self, stage: str, data: SchemaConfig) -> None:
        """
        Import the configuration into a stage.

        Args:
            stage (str): The name of the stage.
            data (SchemaConfig): The configuration to import.
        """
        raise NotImplementedError

class IOrm(ExpressionService):
    """Interface for Orm."""

    @property
    def get_general(self) -> GeneralService:
        """Get the general service."""
        raise NotImplementedError
    
    @property
    def get_schema(self) -> SchemaService:
        """Get the schema service."""
        raise NotImplementedError
    
    @property
    def get_stage(self) -> StageService:
        """Get the stage service."""
        raise NotImplementedError
