from typing import Literal, AsyncIterator, Iterator, Dict, Optional, List
from pydantic import Field, BaseModel
from mikro.funcs import asubscribe, execute, aexecute, subscribe
from mikro.scalars import XArray, Store
from mikro.traits import ROI, Vectorizable, Representation, Sample
from rath.scalars import ID
from enum import Enum
from mikro.rath import MikroRath


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
    RGB = "RGB"
    "RGB (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class RepresentationVarietyInput(str, Enum):
    """Variety expresses the Type of Representation we are dealing with"""

    MASK = "MASK"
    "Mask (Value represent Labels)"
    VOXEL = "VOXEL"
    "Voxel (Value represent Intensity)"
    RGB = "RGB"
    "RGB (First three channel represent RGB)"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class ROIType(str, Enum):
    """An enumeration."""

    ELLIPSE = "ELLIPSE"
    "Ellipse"
    POLYGON = "POLYGON"
    "POLYGON"
    LINE = "LINE"
    "Line"
    RECTANGLE = "RECTANGLE"
    "Rectangle"
    PATH = "PATH"
    "Path"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class RoiTypeInput(str, Enum):
    """An enumeration."""

    ELLIPSIS = "ELLIPSIS"
    "Ellipse"
    POLYGON = "POLYGON"
    "POLYGON"
    LINE = "LINE"
    "Line"
    RECTANGLE = "RECTANGLE"
    "Rectangle"
    PATH = "PATH"
    "Path"
    UNKNOWN = "UNKNOWN"
    "Unknown"


class OmeroRepresentationInput(BaseModel):
    planes: Optional[List[Optional["PlaneInput"]]]
    channels: Optional[List[Optional["ChannelInput"]]]
    physical_size: Optional["PhysicalSizeInput"] = Field(alias="physicalSize")
    scale: Optional[List[Optional[float]]]


class PlaneInput(BaseModel):
    z_index: Optional[int] = Field(alias="zIndex")
    y_index: Optional[int] = Field(alias="yIndex")
    x_index: Optional[int] = Field(alias="xIndex")
    c_index: Optional[int] = Field(alias="cIndex")
    t_index: Optional[int] = Field(alias="tIndex")
    exposure_time: Optional[float] = Field(alias="exposureTime")
    delta_t: Optional[float] = Field(alias="deltaT")


class ChannelInput(BaseModel):
    name: Optional[str]
    emmission_wavelength: Optional[float] = Field(alias="emmissionWavelength")
    excitation_wavelength: Optional[float] = Field(alias="excitationWavelength")
    acquisition_mode: Optional[str] = Field(alias="acquisitionMode")
    color: Optional[str]


class PhysicalSizeInput(BaseModel):
    x: Optional[int]
    y: Optional[int]
    z: Optional[int]
    t: Optional[int]
    c: Optional[int]


class InputVector(BaseModel, Vectorizable):
    x: Optional[float]
    "X-coordinate"
    y: Optional[float]
    "Y-coordinate"
    z: Optional[float]
    "Z-coordinate"


OmeroRepresentationInput.update_forward_refs()


class DetailLabelFragmentFeatures(BaseModel):
    typename: Optional[Literal["SizeFeature"]] = Field(alias="__typename")
    id: ID
    size: float

    class Config:
        frozen = True


class DetailLabelFragment(BaseModel):
    typename: Optional[Literal["Label"]] = Field(alias="__typename")
    id: ID
    instance: int
    name: Optional[str]
    features: List[DetailLabelFragmentFeatures]

    class Config:
        frozen = True


class MultiScaleRepresentationFragmentDerived(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    name: Optional[str]
    "Cleartext name"
    tags: Optional[List[Optional[str]]]
    "A comma-separated list of tags."
    meta: Optional[Dict]
    store: Optional[Store]

    class Config:
        frozen = True


class MultiScaleRepresentationFragment(Representation, BaseModel):
    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    derived: Optional[List[Optional[MultiScaleRepresentationFragmentDerived]]]
    "Derived Images from this Image"

    class Config:
        frozen = True


class RepresentationFragmentSample(Sample, BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID
    name: str

    class Config:
        frozen = True


class RepresentationFragment(Representation, BaseModel):
    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    sample: Optional[RepresentationFragmentSample]
    "The Sample this representation belongs to"
    type: Optional[str]
    "The Representation can have varying types, consult your API"
    id: ID
    store: Optional[Store]
    variety: RepresentationVariety
    "The Representation can have varying types, consult your API"
    name: Optional[str]
    "Cleartext name"

    class Config:
        frozen = True


class ListRepresentationFragmentSample(Sample, BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID
    name: str

    class Config:
        frozen = True


class ListRepresentationFragment(Representation, BaseModel):
    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    "Cleartext name"
    sample: Optional[ListRepresentationFragmentSample]
    "The Sample this representation belongs to"

    class Config:
        frozen = True


class ROIFragmentVectors(BaseModel):
    typename: Optional[Literal["Vector"]] = Field(alias="__typename")
    x: Optional[float]
    "X-coordinate"
    y: Optional[float]
    "Y-coordinate"
    z: Optional[float]
    "Z-coordinate"

    class Config:
        frozen = True


class ROIFragmentRepresentation(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class ROIFragmentCreator(BaseModel):
    """A reflection on the real User"""

    typename: Optional[Literal["User"]] = Field(alias="__typename")
    id: ID
    color: Optional[str]
    "The associated color for this user"

    class Config:
        frozen = True


class ROIFragment(ROI, BaseModel):
    typename: Optional[Literal["ROI"]] = Field(alias="__typename")
    id: ID
    vectors: Optional[List[Optional[ROIFragmentVectors]]]
    type: ROIType
    "The Representation can have varying types, consult your API"
    representation: Optional[ROIFragmentRepresentation]
    creator: ROIFragmentCreator

    class Config:
        frozen = True


class MultiScaleSampleFragmentRepresentationsDerived(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    store: Optional[Store]

    class Config:
        frozen = True


class MultiScaleSampleFragmentRepresentations(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    store: Optional[Store]
    derived: Optional[List[Optional[MultiScaleSampleFragmentRepresentationsDerived]]]
    "Derived Images from this Image"

    class Config:
        frozen = True


class MultiScaleSampleFragment(Sample, BaseModel):
    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID
    name: str
    representations: Optional[List[Optional[MultiScaleSampleFragmentRepresentations]]]

    class Config:
        frozen = True


class Get_label_forQuery(BaseModel):
    label_for: Optional[DetailLabelFragment] = Field(alias="labelFor")
    "Get a label for a specific instance on a specific representation"

    class Arguments(BaseModel):
        representation: ID
        instance: int

    class Meta:
        document = "fragment DetailLabel on Label {\n  id\n  instance\n  name\n  features {\n    id\n    size\n  }\n}\n\nquery get_label_for($representation: ID!, $instance: Int!) {\n  labelFor(representation: $representation, instance: $instance) {\n    ...DetailLabel\n  }\n}"

    class Config:
        frozen = True


class Get_multiscale_repQuery(BaseModel):
    representation: Optional[MultiScaleRepresentationFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = 'fragment MultiScaleRepresentation on Representation {\n  derived(tags: ["multiscale"]) {\n    name\n    tags\n    meta\n    store\n  }\n}\n\nquery get_multiscale_rep($id: ID!) {\n  representation(id: $id) {\n    ...MultiScaleRepresentation\n  }\n}'

    class Config:
        frozen = True


class Get_representationQuery(BaseModel):
    representation: Optional[RepresentationFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Representation on Representation {\n  sample {\n    id\n    name\n  }\n  type\n  id\n  store\n  variety\n  name\n}\n\nquery get_representation($id: ID!) {\n  representation(id: $id) {\n    ...Representation\n  }\n}"

    class Config:
        frozen = True


class Get_some_representationsQuery(BaseModel):
    representations: Optional[List[Optional[ListRepresentationFragment]]]
    "All represetations"

    class Arguments(BaseModel):
        pass

    class Meta:
        document = 'fragment ListRepresentation on Representation {\n  id\n  name\n  sample {\n    id\n    name\n  }\n}\n\nquery get_some_representations {\n  representations(limit: 10, order: "-created_at") {\n    ...ListRepresentation\n  }\n}'

    class Config:
        frozen = True


class Get_roisQuery(BaseModel):
    rois: Optional[List[Optional[ROIFragment]]]
    "All represetations"

    class Arguments(BaseModel):
        representation: ID
        type: Optional[List[Optional[RoiTypeInput]]] = None

    class Meta:
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    id\n    color\n  }\n}\n\nquery get_rois($representation: ID!, $type: [RoiTypeInput]) {\n  rois(representation: $representation, type: $type) {\n    ...ROI\n  }\n}"

    class Config:
        frozen = True


class Expand_multiscaleQuery(BaseModel):
    sample: Optional[MultiScaleSampleFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = 'fragment MultiScaleSample on Sample {\n  id\n  name\n  representations(tags: ["multiscale"]) {\n    id\n    store\n    derived(ordering: "-meta_multiscale_depth") {\n      store\n    }\n  }\n}\n\nquery expand_multiscale($id: ID!) {\n  sample(id: $id) {\n    ...MultiScaleSample\n  }\n}'

    class Config:
        frozen = True


class Watch_roisSubscriptionRois(BaseModel):
    typename: Optional[Literal["RoiEvent"]] = Field(alias="__typename")
    update: Optional[ROIFragment]
    delete: Optional[ID]
    create: Optional[ROIFragment]

    class Config:
        frozen = True


class Watch_roisSubscription(BaseModel):
    rois: Optional[Watch_roisSubscriptionRois]

    class Arguments(BaseModel):
        representation: ID

    class Meta:
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    id\n    color\n  }\n}\n\nsubscription watch_rois($representation: ID!) {\n  rois(representation: $representation) {\n    update {\n      ...ROI\n    }\n    delete\n    create {\n      ...ROI\n    }\n  }\n}"

    class Config:
        frozen = True


class Create_roiMutation(BaseModel):
    create_roi: Optional[ROIFragment] = Field(alias="createROI")
    "Creates a Sample"

    class Arguments(BaseModel):
        representation: ID
        vectors: List[Optional[InputVector]]
        creator: Optional[ID] = None
        type: RoiTypeInput

    class Meta:
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    id\n    color\n  }\n}\n\nmutation create_roi($representation: ID!, $vectors: [InputVector]!, $creator: ID, $type: RoiTypeInput!) {\n  createROI(\n    representation: $representation\n    vectors: $vectors\n    type: $type\n    creator: $creator\n  ) {\n    ...ROI\n  }\n}"

    class Config:
        frozen = True


class Delete_roiMutationDeleteroi(BaseModel):
    typename: Optional[Literal["DeleteROIResult"]] = Field(alias="__typename")
    id: Optional[str]

    class Config:
        frozen = True


class Delete_roiMutation(BaseModel):
    delete_roi: Optional[Delete_roiMutationDeleteroi] = Field(alias="deleteROI")
    "Create an experiment (only signed in users)"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = (
            "mutation delete_roi($id: ID!) {\n  deleteROI(id: $id) {\n    id\n  }\n}"
        )

    class Config:
        frozen = True


class Create_imageMutationImage1Derived(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class Create_imageMutationImage1(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    "Cleartext name"
    derived: Optional[List[Optional[Create_imageMutationImage1Derived]]]
    "Derived Images from this Image"

    class Config:
        frozen = True


class Create_imageMutationImage2Derived(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID

    class Config:
        frozen = True


class Create_imageMutationImage2(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    "Cleartext name"
    derived: Optional[List[Optional[Create_imageMutationImage2Derived]]]
    "Derived Images from this Image"

    class Config:
        frozen = True


class Create_imageMutation(BaseModel):
    image1: Optional[Create_imageMutationImage1]
    "Creates a Representation"
    image2: Optional[Create_imageMutationImage2]
    "Creates a Representation"

    class Arguments(BaseModel):
        xarray: XArray

    class Meta:
        document = "mutation create_image($xarray: XArray!) {\n  image1: fromXArray(xarray: $xarray) {\n    id\n    name\n    derived {\n      id\n    }\n  }\n  image2: fromXArray(xarray: $xarray) {\n    id\n    name\n    derived {\n      id\n    }\n  }\n}"

    class Config:
        frozen = True


async def aget_label_for(
    representation: Optional[ID], instance: Optional[int], rath: MikroRath = None
) -> DetailLabelFragment:
    """get_label_for

    Get a label for a specific instance on a specific representation

    Arguments:
        representation (ID): representation
        instance (int): instance
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        DetailLabelFragment"""
    return (
        await aexecute(
            Get_label_forQuery,
            {"representation": representation, "instance": instance},
            rath=rath,
        )
    ).label_for


def get_label_for(
    representation: Optional[ID], instance: Optional[int], rath: MikroRath = None
) -> DetailLabelFragment:
    """get_label_for

    Get a label for a specific instance on a specific representation

    Arguments:
        representation (ID): representation
        instance (int): instance
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        DetailLabelFragment"""
    return execute(
        Get_label_forQuery,
        {"representation": representation, "instance": instance},
        rath=rath,
    ).label_for


async def aget_multiscale_rep(
    id: Optional[ID], rath: MikroRath = None
) -> MultiScaleRepresentationFragment:
    """get_multiscale_rep

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        MultiScaleRepresentationFragment"""
    return (
        await aexecute(Get_multiscale_repQuery, {"id": id}, rath=rath)
    ).representation


def get_multiscale_rep(
    id: Optional[ID], rath: MikroRath = None
) -> MultiScaleRepresentationFragment:
    """get_multiscale_rep

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        MultiScaleRepresentationFragment"""
    return execute(Get_multiscale_repQuery, {"id": id}, rath=rath).representation


async def aget_representation(
    id: Optional[ID], rath: MikroRath = None
) -> RepresentationFragment:
    """get_representation

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return (
        await aexecute(Get_representationQuery, {"id": id}, rath=rath)
    ).representation


def get_representation(
    id: Optional[ID], rath: MikroRath = None
) -> RepresentationFragment:
    """get_representation

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        RepresentationFragment"""
    return execute(Get_representationQuery, {"id": id}, rath=rath).representation


async def aget_some_representations(
    rath: MikroRath = None,
) -> ListRepresentationFragment:
    """get_some_representations

    All represetations

    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ListRepresentationFragment"""
    return (
        await aexecute(Get_some_representationsQuery, {}, rath=rath)
    ).representations


def get_some_representations(rath: MikroRath = None) -> ListRepresentationFragment:
    """get_some_representations

    All represetations

    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ListRepresentationFragment"""
    return execute(Get_some_representationsQuery, {}, rath=rath).representations


async def aget_rois(
    representation: Optional[ID],
    type: Optional[List[Optional[RoiTypeInput]]] = None,
    rath: MikroRath = None,
) -> ROIFragment:
    """get_rois

    All represetations

    Arguments:
        representation (ID): representation
        type (Optional[List[Optional[RoiTypeInput]]], optional): type.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ROIFragment"""
    return (
        await aexecute(
            Get_roisQuery, {"representation": representation, "type": type}, rath=rath
        )
    ).rois


def get_rois(
    representation: Optional[ID],
    type: Optional[List[Optional[RoiTypeInput]]] = None,
    rath: MikroRath = None,
) -> ROIFragment:
    """get_rois

    All represetations

    Arguments:
        representation (ID): representation
        type (Optional[List[Optional[RoiTypeInput]]], optional): type.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ROIFragment"""
    return execute(
        Get_roisQuery, {"representation": representation, "type": type}, rath=rath
    ).rois


async def aexpand_multiscale(
    id: Optional[ID], rath: MikroRath = None
) -> MultiScaleSampleFragment:
    """expand_multiscale

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        MultiScaleSampleFragment"""
    return (await aexecute(Expand_multiscaleQuery, {"id": id}, rath=rath)).sample


def expand_multiscale(
    id: Optional[ID], rath: MikroRath = None
) -> MultiScaleSampleFragment:
    """expand_multiscale

    Get a single representation by ID

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        MultiScaleSampleFragment"""
    return execute(Expand_multiscaleQuery, {"id": id}, rath=rath).sample


async def awatch_rois(
    representation: Optional[ID], rath: MikroRath = None
) -> AsyncIterator[Optional[Watch_roisSubscriptionRois]]:
    """watch_rois



    Arguments:
        representation (ID): representation
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Watch_roisSubscription"""
    async for event in asubscribe(
        Watch_roisSubscription, {"representation": representation}, rath=rath
    ):
        yield event.rois


def watch_rois(
    representation: Optional[ID], rath: MikroRath = None
) -> Iterator[Optional[Watch_roisSubscriptionRois]]:
    """watch_rois



    Arguments:
        representation (ID): representation
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Watch_roisSubscription"""
    for event in subscribe(
        Watch_roisSubscription, {"representation": representation}, rath=rath
    ):
        yield event.rois


async def acreate_roi(
    representation: Optional[ID],
    vectors: Optional[List[Optional[InputVector]]],
    type: Optional[RoiTypeInput],
    creator: Optional[ID] = None,
    rath: MikroRath = None,
) -> ROIFragment:
    """create_roi

    Creates a Sample

    Arguments:
        representation (ID): representation
        vectors (List[Optional[InputVector]]): vectors
        type (RoiTypeInput): type
        creator (Optional[ID], optional): creator.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ROIFragment"""
    return (
        await aexecute(
            Create_roiMutation,
            {
                "representation": representation,
                "vectors": vectors,
                "creator": creator,
                "type": type,
            },
            rath=rath,
        )
    ).create_roi


def create_roi(
    representation: Optional[ID],
    vectors: Optional[List[Optional[InputVector]]],
    type: Optional[RoiTypeInput],
    creator: Optional[ID] = None,
    rath: MikroRath = None,
) -> ROIFragment:
    """create_roi

    Creates a Sample

    Arguments:
        representation (ID): representation
        vectors (List[Optional[InputVector]]): vectors
        type (RoiTypeInput): type
        creator (Optional[ID], optional): creator.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        ROIFragment"""
    return execute(
        Create_roiMutation,
        {
            "representation": representation,
            "vectors": vectors,
            "creator": creator,
            "type": type,
        },
        rath=rath,
    ).create_roi


async def adelete_roi(
    id: Optional[ID], rath: MikroRath = None
) -> Optional[Delete_roiMutationDeleteroi]:
    """delete_roi

    Create an experiment (only signed in users)

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[Delete_roiMutationDeleteroi]"""
    return (await aexecute(Delete_roiMutation, {"id": id}, rath=rath)).delete_roi


def delete_roi(
    id: Optional[ID], rath: MikroRath = None
) -> Optional[Delete_roiMutationDeleteroi]:
    """delete_roi

    Create an experiment (only signed in users)

    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[Delete_roiMutationDeleteroi]"""
    return execute(Delete_roiMutation, {"id": id}, rath=rath).delete_roi


async def acreate_image(
    xarray: Optional[XArray], rath: MikroRath = None
) -> Create_imageMutation:
    """create_image


     image1: Creates a Representation
     image2: Creates a Representation

    Arguments:
        xarray (XArray): xarray
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_imageMutation"""
    return (
        await aexecute(Create_imageMutation, {"xarray": xarray}, rath=rath)
    ).from_x_array


def create_image(
    xarray: Optional[XArray], rath: MikroRath = None
) -> Create_imageMutation:
    """create_image


     image1: Creates a Representation
     image2: Creates a Representation

    Arguments:
        xarray (XArray): xarray
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_imageMutation"""
    return execute(Create_imageMutation, {"xarray": xarray}, rath=rath).from_x_array
