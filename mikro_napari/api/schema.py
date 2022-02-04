from mikro.structure import Thumbnail
from mikro.structure import Table
from mikro.mixins import Array
from mikro.structure import Representation
from mikro.structure import Experiment
from mikro.structure import OmeroFile
from mikro.structure import Sample
from mikro.scalars import XArray
from mikro.scalars import File
from mikro.scalars import File
from mikro.scalars import Upload
from mikro.scalars import DataFrame
from mikro.scalars import Store
from turms.types.object import GraphQLObject
from turms.types.object import GraphQLObject
from pydantic.fields import Field
from typing import Optional, List, Dict, Union, Literal
from enum import Enum
from turms.types.object import GraphQLInputObject
from turms.types.object import GraphQLObject
from turms.types.herre import GraphQLQuery
from turms.types.herre import GraphQLMutation
from turms.types.herre import GraphQLSubscription


class OmeroFileType(str, Enum):
    """An enumeration."""

    TIFF = "TIFF"
    "Tiff"
    JPEG = "JPEG"
    "Jpeg"
    MSR = "MSR"
    "MSR File"
    CZI = "CZI"
    "Zeiss Microscopy File"
    UNKNOWN = "UNKNOWN"
    "Unwknon File Format"


class RepresentationVariety(str, Enum):
    """An enumeration."""

    MASK = "MASK"
    "Mask (Value represent Labels)"
    VOXEL = "VOXEL"
    "Voxel (Value represent Intensity)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class RepresentationVarietyInput(str, Enum):
    """Variety expresses the Type of Representation we are dealing with"""

    MASK = "MASK"
    "Mask (Value represent Labels)"
    VOXEL = "VOXEL"
    "Voxel (Value represent Intensity)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class OmeroRepresentationInput(GraphQLInputObject):
    None
    planes: Optional[List[Optional["PlaneInput"]]]
    channels: Optional[List[Optional["ChannelInput"]]]
    physicalSize: Optional["PhysicalSizeInput"]
    scale: Optional[List[Optional[float]]]


class PlaneInput(GraphQLInputObject):
    None
    zIndex: Optional[int]
    yIndex: Optional[int]
    xIndex: Optional[int]
    cIndex: Optional[int]
    tIndex: Optional[int]
    exposureTime: Optional[float]
    deltaT: Optional[float]


class ChannelInput(GraphQLInputObject):
    None
    name: Optional[str]
    emmissionWavelength: Optional[float]
    excitationWavelength: Optional[float]
    acquisitionMode: Optional[str]
    color: Optional[str]


class PhysicalSizeInput(GraphQLInputObject):
    None
    x: Optional[int]
    y: Optional[int]
    z: Optional[int]
    t: Optional[int]
    c: Optional[int]


OmeroRepresentationInput.update_forward_refs()


class MultiScaleSampleFragmentRepresentationsDerived(
    Array, Representation, GraphQLObject
):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    store: Optional[Store]


class MultiScaleSampleFragmentRepresentations(Array, Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str
    store: Optional[Store]
    derived: Optional[List[Optional[MultiScaleSampleFragmentRepresentationsDerived]]]
    "Derived Images from this Image"


class MultiScaleSampleFragment(Sample, GraphQLObject):
    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: str
    name: str
    representations: Optional[List[Optional[MultiScaleSampleFragmentRepresentations]]]


class Expand_multiscaleQuery(GraphQLQuery):
    sample: Optional[MultiScaleSampleFragment]

    class Meta:
        domain = "mikro"
        document = 'fragment MultiScaleSample on Sample {\n  id\n  name\n  representations(tags: ["multiscale"]) {\n    id\n    store\n    derived(ordering: "-meta_multiscale_depth") {\n      store\n    }\n  }\n}\n\nquery expand_multiscale($id: ID!) {\n  sample(id: $id) {\n    ...MultiScaleSample\n  }\n}'


class Create_imageMutationImage1Derived(Array, Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str


class Create_imageMutationImage1(Array, Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str
    name: Optional[str]
    "Cleartext name"
    derived: Optional[List[Optional[Create_imageMutationImage1Derived]]]
    "Derived Images from this Image"


class Create_imageMutationImage2Derived(Array, Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str


class Create_imageMutationImage2(Array, Representation, GraphQLObject):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: str
    name: Optional[str]
    "Cleartext name"
    derived: Optional[List[Optional[Create_imageMutationImage2Derived]]]
    "Derived Images from this Image"


class Create_imageMutation(GraphQLMutation):
    image1: Optional[Create_imageMutationImage1]
    image2: Optional[Create_imageMutationImage2]

    class Meta:
        domain = "mikro"
        document = "mutation create_image($xarray: XArray!) {\n  image1: fromXArray(xarray: $xarray) {\n    id\n    name\n    derived {\n      id\n    }\n  }\n  image2: fromXArray(xarray: $xarray) {\n    id\n    name\n    derived {\n      id\n    }\n  }\n}"


async def aexpand_multiscale(id: str) -> MultiScaleSampleFragment:
    """expand_multiscale

    Get a single representation by ID

    Arguments:
        id (ID): ID

    Returns:
        MultiScaleSampleFragment: The returned Mutation"""
    return (await Expand_multiscaleQuery.aexecute({"id": id})).sample


def expand_multiscale(id: str) -> MultiScaleSampleFragment:
    """expand_multiscale

    Get a single representation by ID

    Arguments:
        id (ID): ID

    Returns:
        MultiScaleSampleFragment: The returned Mutation"""
    return Expand_multiscaleQuery.execute({"id": id}).sample


async def acreate_image(xarray: XArray) -> List[Create_imageMutation]:
    """create_image


     image1: Creates a Representation
     image2: Creates a Representation

    Arguments:
        xarray (XArray): XArray

    Returns:
        Create_imageMutation: The returned Mutation"""
    return await Create_imageMutation.aexecute({"xarray": xarray})


def create_image(xarray: XArray) -> List[Create_imageMutation]:
    """create_image


     image1: Creates a Representation
     image2: Creates a Representation

    Arguments:
        xarray (XArray): XArray

    Returns:
        Create_imageMutation: The returned Mutation"""
    return Create_imageMutation.execute({"xarray": xarray})
