import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List

import attr
from attr.validators import instance_of

from drawio_xml_generator.config import (
    Config,
    get_dir_path,
    get_logger,
    setup_logger,
)
from drawio_xml_generator.constants import SHAPE_ICONS

Config().set_filepath(get_dir_path(__file__, 2, "configs/example_config.yaml"))
setup_logger(__file__, 2)
logger = get_logger(__name__)


@attr.define
class NetworkNode:
    name: str = attr.ib(validator=[instance_of(str)])
    ip: str = attr.ib(validator=[instance_of(str)])
    node_type: str = attr.ib(validator=[instance_of(str)])
    x: int = attr.ib(default=0, validator=[instance_of(int)], converter=int)
    y: int = attr.ib(default=0, validator=[instance_of(int)], converter=int)
    display_name: str = attr.ib(validator=[instance_of(str)], init=False)

    
    def __attrs_post_init__(self):
        self.generate_display_name()

    def generate_display_name(self):
        self.display_name = self.name.replace("_", " ") + "\n" + self.ip


@attr.define
class NetworkLink:
    src_node: NetworkNode = attr.ib(validator=[instance_of(NetworkNode)])
    dst_node: NetworkNode = attr.ib(validator=[instance_of(NetworkNode)])


@attr.define
class DrawioXMLGenerator:
    mxfile: ET.Element = attr.ib(
        validator=[instance_of(ET.Element)], init=False
    )
    diagram: ET.Element = attr.ib(
        validator=[instance_of(ET.Element)], init=False
    )
    mxGraphModel: ET.Element = attr.ib(
        validator=[instance_of(ET.Element)], init=False
    )
    root: ET.Element = attr.ib(validator=[instance_of(ET.Element)], init=False)
    mxCellID0: ET.Element = attr.ib(
        validator=[instance_of(ET.Element)], init=False
    )
    mxCellID1: ET.Element = attr.ib(
        validator=[instance_of(ET.Element)], init=False
    )
    ids: dict = attr.ib(default={}, validator=[instance_of(dict)])
    nodes: list = attr.ib(default=[], validator=[instance_of(list)])
    links: list = attr.ib(default=[], validator=[instance_of(list)])

    def __attrs_post_init__(self) -> None:
        self.xml_init()

    def xml_init(self) -> None:
        # initiating the blocks needed for the DrawIO XML template , standard in every plot
        self.mxfile = ET.Element(
            "mxfile",
            host="Electron",
            agent=(
                "5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "draw.io/19.0.0 Chrome/100.0.4896.160 Electron/18.3.2 Safari/537.36"
            ),
            type="device",
        )
        self.diagram = ET.SubElement(
            self.mxfile, "diagram", id="diagram_1", name="Page-1"
        )
        self.mxGraphModel = ET.SubElement(
            self.diagram,
            "mxGraphModel",
            grid="1",
            gridSize="10",
            guides="1",
            tooltips="1",
            connect="1",
            arrows="1",
            fold="1",
            page="1",
            pageScale="1",
            pageWidth="850",
            pageHeight="1100",
            math="0",
            shadow="0",
        )
        self.root = ET.SubElement(self.mxGraphModel, "root")
        self.mxCellID0 = ET.SubElement(self.root, "mxCell", id="0")
        # Each Node and Edge are a child to the Parent id "1"
        self.mxCellID1 = ET.SubElement(
            self.root, "mxCell", id="1", parent="0", style=";html=1;"
        )
        logger.info("xml initialised")

    def add_node(self, node: NetworkNode) -> bool:
        if node.node_type not in SHAPE_ICONS:
            logger.error(f"node_type: {node.node_type} not implemented")

        try:
            mxCell = ET.SubElement(
                self.root,
                "mxCell",
                id=node.display_name,
                value=node.display_name,
                style=(
                    "verticalLabelPosition=bottom;"
                    "html=1;"
                    "verticalAlign=top;"
                    "aspect=fixed;align=center;"
                    "pointerEvents=1;"
                    f'shape={SHAPE_ICONS[node.node_type]["shape"]}'
                    ""
                ),
                parent="1",
                vertex="1",
            )
            mxGeometry = ET.SubElement(
                mxCell,
                "mxGeometry",
                width=SHAPE_ICONS[node.node_type]["width"],
                height=SHAPE_ICONS[node.node_type]["height"],
            )
            mxGeometry.set("as", "geometry")
            mxGeometry.set("x", str(node.x))
            mxGeometry.set("y", str(node.y))
            self.ids[node.display_name] = node
            logger.debug(f"added node: {node}")
            self.nodes.append(f"    {node.name}")
            return True
        except Exception as e:
            logger.error(e)
            return False

    def add_list_nodes(self, nodes: List[NetworkNode]):
        responses = []
        for node in nodes:
            responses.append(self.add_node(node))

        return all(responses)

    def add_link(self, link: NetworkLink):
        try:
            mxCell = ET.SubElement(
                self.root,
                "mxCell",
                id=link.src_node.display_name+ link.dst_node.display_name,
                style="endFill=0;endArrow=none;",
                parent="1",
                source=link.src_node.display_name,
                target=link.dst_node.display_name,
                edge="1",
            )
            mxGeometry = ET.SubElement(mxCell, "mxGeometry")
            mxGeometry.set("as", "geometry")
            logger.debug(f"added link: {link}")
            self.links.append(
                f"    {link.src_node.name} - {link.dst_node.name}"
            )
            return True
        except Exception as e:
            logger.error(e)
            return False

    def add_list_links(self, links: List[NetworkLink]) -> bool:
        responses = []
        for link in links:
            responses.append(self.add_link(link))

        return all(responses)

    def display_xml(self) -> bytes:
        return ET.tostring(self.mxfile)

    def export(self) -> bool:
        output_folder = "./outputs"
        now = datetime.now()
        date_time = now.strftime("%Y%m%d_%H%M%S")
        os.makedirs(output_folder, exist_ok=True)
        tree = ET.ElementTree(self.mxfile)
        tree.write(f"{output_folder}/{date_time}.xml")
        return True

    def __repr__(self) -> str:
        return str(self.display_xml())

    def get_sketch(self) -> str:
        result = "nodes:\n"
        result += "\n".join(self.nodes) + "\n\n"
        result += "links:\n" + "\n".join(self.links)
        return result
