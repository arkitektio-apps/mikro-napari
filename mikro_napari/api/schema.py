from mikro.funcs import asubscribe, execute, subscribe, aexecute
from typing import Iterator, Literal, AsyncIterator, Dict, Optional, List
from mikro.traits import Representation, Vectorizable, ROI
from pydantic import Field, BaseModel
from rath.scalars import ID
from mikro.scalars import ArrayInput, Store
from enum import Enum
from mikro.rath import MikroRath


class AvailableModels(str, Enum):
    GRUNNLAG_ANIMAL = "GRUNNLAG_ANIMAL"
    GRUNNLAG_EXPERIMENT = "GRUNNLAG_EXPERIMENT"
    GRUNNLAG_EXPERIMENTALGROUP = "GRUNNLAG_EXPERIMENTALGROUP"
    GRUNNLAG_REPRESENTATION = "GRUNNLAG_REPRESENTATION"
    GRUNNLAG_THUMBNAIL = "GRUNNLAG_THUMBNAIL"
    GRUNNLAG_SAMPLE = "GRUNNLAG_SAMPLE"
    GRUNNLAG_ROI = "GRUNNLAG_ROI"
    GRUNNLAG_OMEROFILE = "GRUNNLAG_OMEROFILE"
    GRUNNLAG_METRIC = "GRUNNLAG_METRIC"
    GRUNNLAG_ANTIBODY = "GRUNNLAG_ANTIBODY"
    GRUNNLAG_USERMETA = "GRUNNLAG_USERMETA"
    GRUNNLAG_LABEL = "GRUNNLAG_LABEL"
    GRUNNLAG_SIZEFEATURE = "GRUNNLAG_SIZEFEATURE"
    GRUNNLAG_COMMENT = "GRUNNLAG_COMMENT"
    BORD_TABLE = "BORD_TABLE"


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
    c: Optional[float]
    "C-coordinate"
    t: Optional[float]
    "T-coordinate"


class GroupAssignmentInput(BaseModel):
    permissions: List[Optional[str]]
    group: ID


class UserAssignmentInput(BaseModel):
    permissions: List[Optional[str]]
    user: str
    "The user email"


class DescendendInput(BaseModel):
    children: Optional[List[Optional["DescendendInput"]]]
    typename: Optional[str]
    "The type of the descendent"
    user: Optional[str]
    "The user that is mentioned"
    bold: Optional[bool]
    "Is this a bold leaf?"
    italic: Optional[bool]
    "Is this a italic leaf?"
    code: Optional[bool]
    "Is this a code leaf?"
    text: Optional[str]
    "The text of the leaf"


class DetailLabelFragmentFeatures(BaseModel):
    typename: Optional[Literal["SizeFeature"]] = Field(alias="__typename")
    id: ID
    size: float


class DetailLabelFragment(BaseModel):
    typename: Optional[Literal["Label"]] = Field(alias="__typename")
    id: ID
    instance: int
    name: Optional[str]
    features: List[DetailLabelFragmentFeatures]


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


class MultiScaleRepresentationFragment(Representation, BaseModel):
    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    derived: Optional[List[Optional[MultiScaleRepresentationFragmentDerived]]]
    "Derived Images from this Image"


class RepresentationFragmentSample(BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID
    name: str


class RepresentationFragmentOmero(BaseModel):
    typename: Optional[Literal["OmeroRepresentation"]] = Field(alias="__typename")
    scale: Optional[List[Optional[float]]]


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
    omero: Optional[RepresentationFragmentOmero]
    "Metadata in Omero-compliant format"


class ListRepresentationFragmentSample(BaseModel):
    """Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
    was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
    the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample
    """

    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID
    name: str


class ListRepresentationFragment(Representation, BaseModel):
    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    "Cleartext name"
    sample: Optional[ListRepresentationFragmentSample]
    "The Sample this representation belongs to"


class ROIFragmentVectors(BaseModel):
    typename: Optional[Literal["Vector"]] = Field(alias="__typename")
    x: Optional[float]
    "X-coordinate"
    y: Optional[float]
    "Y-coordinate"
    z: Optional[float]
    "Z-coordinate"
    t: Optional[float]
    "T-coordinate"
    c: Optional[float]
    "C-coordinate"


class ROIFragmentRepresentation(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID


class ROIFragmentCreator(BaseModel):
    """A reflection on the real User"""

    typename: Optional[Literal["User"]] = Field(alias="__typename")
    id: ID
    color: Optional[str]
    "The associated color for this user"


class ROIFragment(ROI, BaseModel):
    typename: Optional[Literal["ROI"]] = Field(alias="__typename")
    id: ID
    vectors: Optional[List[Optional[ROIFragmentVectors]]]
    type: ROIType
    "The Representation can have varying types, consult your API"
    representation: Optional[ROIFragmentRepresentation]
    creator: ROIFragmentCreator


class MultiScaleSampleFragmentRepresentationsDerived(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    store: Optional[Store]


class MultiScaleSampleFragmentRepresentations(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    store: Optional[Store]
    derived: Optional[List[Optional[MultiScaleSampleFragmentRepresentationsDerived]]]
    "Derived Images from this Image"


class MultiScaleSampleFragment(BaseModel):
    typename: Optional[Literal["Sample"]] = Field(alias="__typename")
    id: ID
    name: str
    representations: Optional[List[Optional[MultiScaleSampleFragmentRepresentations]]]


class Get_label_forQuery(BaseModel):
    label_for: Optional[DetailLabelFragment] = Field(alias="labelFor")
    "Get a label for a specific instance on a specific representation"

    class Arguments(BaseModel):
        representation: ID
        instance: int

    class Meta:
        document = "fragment DetailLabel on Label {\n  id\n  instance\n  name\n  features {\n    id\n    size\n  }\n}\n\nquery get_label_for($representation: ID!, $instance: Int!) {\n  labelFor(representation: $representation, instance: $instance) {\n    ...DetailLabel\n  }\n}"


class Get_multiscale_repQuery(BaseModel):
    representation: Optional[MultiScaleRepresentationFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = 'fragment MultiScaleRepresentation on Representation {\n  derived(tags: ["multiscale"]) {\n    name\n    tags\n    meta\n    store\n  }\n}\n\nquery get_multiscale_rep($id: ID!) {\n  representation(id: $id) {\n    ...MultiScaleRepresentation\n  }\n}'


class Get_representationQuery(BaseModel):
    representation: Optional[RepresentationFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Representation on Representation {\n  sample {\n    id\n    name\n  }\n  type\n  id\n  store\n  variety\n  name\n  omero {\n    scale\n  }\n}\n\nquery get_representation($id: ID!) {\n  representation(id: $id) {\n    ...Representation\n  }\n}"


class Get_some_representationsQuery(BaseModel):
    representations: Optional[List[Optional[ListRepresentationFragment]]]
    "All represetations"

    class Arguments(BaseModel):
        pass

    class Meta:
        document = 'fragment ListRepresentation on Representation {\n  id\n  name\n  sample {\n    id\n    name\n  }\n}\n\nquery get_some_representations {\n  representations(limit: 10, order: "-created_at") {\n    ...ListRepresentation\n  }\n}'


class Get_roisQuery(BaseModel):
    rois: Optional[List[Optional[ROIFragment]]]
    "All represetations"

    class Arguments(BaseModel):
        representation: ID
        type: Optional[List[Optional[RoiTypeInput]]] = None

    class Meta:
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n    t\n    c\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    id\n    color\n  }\n}\n\nquery get_rois($representation: ID!, $type: [RoiTypeInput]) {\n  rois(representation: $representation, type: $type) {\n    ...ROI\n  }\n}"


class Expand_multiscaleQuery(BaseModel):
    sample: Optional[MultiScaleSampleFragment]
    "Get a single representation by ID"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = 'fragment MultiScaleSample on Sample {\n  id\n  name\n  representations(tags: ["multiscale"]) {\n    id\n    store\n    derived(ordering: "-meta_multiscale_depth") {\n      store\n    }\n  }\n}\n\nquery expand_multiscale($id: ID!) {\n  sample(id: $id) {\n    ...MultiScaleSample\n  }\n}'


class Watch_roisSubscriptionRois(BaseModel):
    typename: Optional[Literal["RoiEvent"]] = Field(alias="__typename")
    update: Optional[ROIFragment]
    delete: Optional[ID]
    create: Optional[ROIFragment]


class Watch_roisSubscription(BaseModel):
    rois: Optional[Watch_roisSubscriptionRois]

    class Arguments(BaseModel):
        representation: ID

    class Meta:
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n    t\n    c\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    id\n    color\n  }\n}\n\nsubscription watch_rois($representation: ID!) {\n  rois(representation: $representation) {\n    update {\n      ...ROI\n    }\n    delete\n    create {\n      ...ROI\n    }\n  }\n}"


class Create_roiMutation(BaseModel):
    create_roi: Optional[ROIFragment] = Field(alias="createROI")
    "Creates a Sample"

    class Arguments(BaseModel):
        representation: ID
        vectors: List[Optional[InputVector]]
        creator: Optional[ID] = None
        type: RoiTypeInput

    class Meta:
        document = "fragment ROI on ROI {\n  id\n  vectors {\n    x\n    y\n    z\n    t\n    c\n  }\n  type\n  representation {\n    id\n  }\n  creator {\n    id\n    color\n  }\n}\n\nmutation create_roi($representation: ID!, $vectors: [InputVector]!, $creator: ID, $type: RoiTypeInput!) {\n  createROI(\n    representation: $representation\n    vectors: $vectors\n    type: $type\n    creator: $creator\n  ) {\n    ...ROI\n  }\n}"


class Delete_roiMutationDeleteroi(BaseModel):
    typename: Optional[Literal["DeleteROIResult"]] = Field(alias="__typename")
    id: Optional[str]


class Delete_roiMutation(BaseModel):
    delete_roi: Optional[Delete_roiMutationDeleteroi] = Field(alias="deleteROI")
    "Create an experiment (only signed in users)"

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = (
            "mutation delete_roi($id: ID!) {\n  deleteROI(id: $id) {\n    id\n  }\n}"
        )


class Create_imageMutationImage1Derived(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID


class Create_imageMutationImage1(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    "Cleartext name"
    derived: Optional[List[Optional[Create_imageMutationImage1Derived]]]
    "Derived Images from this Image"


class Create_imageMutationImage2Derived(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID


class Create_imageMutationImage2(Representation, BaseModel):
    """A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest"""

    typename: Optional[Literal["Representation"]] = Field(alias="__typename")
    id: ID
    name: Optional[str]
    "Cleartext name"
    derived: Optional[List[Optional[Create_imageMutationImage2Derived]]]
    "Derived Images from this Image"


class Create_imageMutation(BaseModel):
    image1: Optional[Create_imageMutationImage1]
    "Creates a Representation"
    image2: Optional[Create_imageMutationImage2]
    "Creates a Representation"

    class Arguments(BaseModel):
        xarray: ArrayInput

    class Meta:
        document = "mutation create_image($xarray: XArray!) {\n  image1: fromXArray(xarray: $xarray) {\n    id\n    name\n    derived {\n      id\n    }\n  }\n  image2: fromXArray(xarray: $xarray) {\n    id\n    name\n    derived {\n      id\n    }\n  }\n}"


async def aget_label_for(
    representation: ID, instance: int, rath: MikroRath = None
) -> Optional[DetailLabelFragment]:
    """get_label_for



    Arguments:
        representation (ID): representation
        instance (int): instance
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[DetailLabelFragment]"""
    return (
        await aexecute(
            Get_label_forQuery,
            {"representation": representation, "instance": instance},
            rath=rath,
        )
    ).label_for


def get_label_for(
    representation: ID, instance: int, rath: MikroRath = None
) -> Optional[DetailLabelFragment]:
    """get_label_for



    Arguments:
        representation (ID): representation
        instance (int): instance
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[DetailLabelFragment]"""
    return execute(
        Get_label_forQuery,
        {"representation": representation, "instance": instance},
        rath=rath,
    ).label_for


async def aget_multiscale_rep(
    id: ID, rath: MikroRath = None
) -> Optional[MultiScaleRepresentationFragment]:
    """get_multiscale_rep


     representation: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest


    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[MultiScaleRepresentationFragment]"""
    return (
        await aexecute(Get_multiscale_repQuery, {"id": id}, rath=rath)
    ).representation


def get_multiscale_rep(
    id: ID, rath: MikroRath = None
) -> Optional[MultiScaleRepresentationFragment]:
    """get_multiscale_rep


     representation: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest


    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[MultiScaleRepresentationFragment]"""
    return execute(Get_multiscale_repQuery, {"id": id}, rath=rath).representation


async def aget_representation(
    id: ID, rath: MikroRath = None
) -> Optional[RepresentationFragment]:
    """get_representation


     representation: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest


    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[RepresentationFragment]"""
    return (
        await aexecute(Get_representationQuery, {"id": id}, rath=rath)
    ).representation


def get_representation(
    id: ID, rath: MikroRath = None
) -> Optional[RepresentationFragment]:
    """get_representation


     representation: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest


    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[RepresentationFragment]"""
    return execute(Get_representationQuery, {"id": id}, rath=rath).representation


async def aget_some_representations(
    rath: MikroRath = None,
) -> Optional[List[Optional[ListRepresentationFragment]]]:
    """get_some_representations


     representations: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest


    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[List[Optional[ListRepresentationFragment]]]"""
    return (
        await aexecute(Get_some_representationsQuery, {}, rath=rath)
    ).representations


def get_some_representations(
    rath: MikroRath = None,
) -> Optional[List[Optional[ListRepresentationFragment]]]:
    """get_some_representations


     representations: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest


    Arguments:
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[List[Optional[ListRepresentationFragment]]]"""
    return execute(Get_some_representationsQuery, {}, rath=rath).representations


async def aget_rois(
    representation: ID,
    type: Optional[List[Optional[RoiTypeInput]]] = None,
    rath: MikroRath = None,
) -> Optional[List[Optional[ROIFragment]]]:
    """get_rois



    Arguments:
        representation (ID): representation
        type (Optional[List[Optional[RoiTypeInput]]], optional): type.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[List[Optional[ROIFragment]]]"""
    return (
        await aexecute(
            Get_roisQuery, {"representation": representation, "type": type}, rath=rath
        )
    ).rois


def get_rois(
    representation: ID,
    type: Optional[List[Optional[RoiTypeInput]]] = None,
    rath: MikroRath = None,
) -> Optional[List[Optional[ROIFragment]]]:
    """get_rois



    Arguments:
        representation (ID): representation
        type (Optional[List[Optional[RoiTypeInput]]], optional): type.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[List[Optional[ROIFragment]]]"""
    return execute(
        Get_roisQuery, {"representation": representation, "type": type}, rath=rath
    ).rois


async def aexpand_multiscale(
    id: ID, rath: MikroRath = None
) -> Optional[MultiScaleSampleFragment]:
    """expand_multiscale


     sample: Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
        was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
        the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample



    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[MultiScaleSampleFragment]"""
    return (await aexecute(Expand_multiscaleQuery, {"id": id}, rath=rath)).sample


def expand_multiscale(
    id: ID, rath: MikroRath = None
) -> Optional[MultiScaleSampleFragment]:
    """expand_multiscale


     sample: Samples are storage containers for representations. A Sample is to be understood analogous to a Biological Sample. It existed in Time (the time of acquisiton and experimental procedure),
        was measured in space (x,y,z) and in different modalities (c). Sample therefore provide a datacontainer where each Representation of
        the data shares the same dimensions. Every transaction to our image data is still part of the original acuqistion, so also filtered images are refering back to the sample



    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[MultiScaleSampleFragment]"""
    return execute(Expand_multiscaleQuery, {"id": id}, rath=rath).sample


async def awatch_rois(
    representation: ID, rath: MikroRath = None
) -> AsyncIterator[Optional[Watch_roisSubscriptionRois]]:
    """watch_rois



    Arguments:
        representation (ID): representation
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[Watch_roisSubscriptionRois]"""
    async for event in asubscribe(
        Watch_roisSubscription, {"representation": representation}, rath=rath
    ):
        yield event.rois


def watch_rois(
    representation: ID, rath: MikroRath = None
) -> Iterator[Optional[Watch_roisSubscriptionRois]]:
    """watch_rois



    Arguments:
        representation (ID): representation
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[Watch_roisSubscriptionRois]"""
    for event in subscribe(
        Watch_roisSubscription, {"representation": representation}, rath=rath
    ):
        yield event.rois


async def acreate_roi(
    representation: ID,
    vectors: List[Optional[InputVector]],
    type: RoiTypeInput,
    creator: Optional[ID] = None,
    rath: MikroRath = None,
) -> Optional[ROIFragment]:
    """create_roi



    Arguments:
        representation (ID): representation
        vectors (List[Optional[InputVector]]): vectors
        type (RoiTypeInput): type
        creator (Optional[ID], optional): creator.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[ROIFragment]"""
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
    representation: ID,
    vectors: List[Optional[InputVector]],
    type: RoiTypeInput,
    creator: Optional[ID] = None,
    rath: MikroRath = None,
) -> Optional[ROIFragment]:
    """create_roi



    Arguments:
        representation (ID): representation
        vectors (List[Optional[InputVector]]): vectors
        type (RoiTypeInput): type
        creator (Optional[ID], optional): creator.
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[ROIFragment]"""
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
    id: ID, rath: MikroRath = None
) -> Optional[Delete_roiMutationDeleteroi]:
    """delete_roi



    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[Delete_roiMutationDeleteroi]"""
    return (await aexecute(Delete_roiMutation, {"id": id}, rath=rath)).delete_roi


def delete_roi(id: ID, rath: MikroRath = None) -> Optional[Delete_roiMutationDeleteroi]:
    """delete_roi



    Arguments:
        id (ID): id
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Optional[Delete_roiMutationDeleteroi]"""
    return execute(Delete_roiMutation, {"id": id}, rath=rath).delete_roi


async def acreate_image(
    xarray: ArrayInput, rath: MikroRath = None
) -> Create_imageMutation:
    """create_image


     image1: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest

     image2: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest


    Arguments:
        xarray (ArrayInput): xarray
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_imageMutation"""
    return await aexecute(Create_imageMutation, {"xarray": xarray}, rath=rath)


def create_image(xarray: ArrayInput, rath: MikroRath = None) -> Create_imageMutation:
    """create_image


     image1: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest

     image2: A Representation is a multi-dimensional Array that can do what ever it wants


    @elements/rep:latest


    Arguments:
        xarray (ArrayInput): xarray
        rath (mikro.rath.MikroRath, optional): The mikro rath client

    Returns:
        Create_imageMutation"""
    return execute(Create_imageMutation, {"xarray": xarray}, rath=rath)


DescendendInput.update_forward_refs()
OmeroRepresentationInput.update_forward_refs()
