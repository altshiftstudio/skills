
import json
import os
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

NODE_TYPE_TEXT = "text"
NODE_TYPE_FILE = "file"
NODE_TYPE_GROUP = "group"

EDGE_SIDES = {"top", "bottom", "left", "right"}

TEXT_BASE_HEIGHT = 50
TEXT_LINE_HEIGHT = 25
TEXT_CHAR_WIDTH = 6
DEFAULT_TEXT_WIDTH = 250

DEFAULT_FILE_WIDTH = 400
DEFAULT_FILE_HEIGHT = 400

DEFAULT_GROUP_WIDTH = 200
DEFAULT_GROUP_HEIGHT = 200

GROUP_PADDING = 30
GROUP_HEADER_HEIGHT = 60
GROUP_BOTTOM_BUFFER = 20
GROUP_HEADER_OVERLAP_BUFFER = 40
GROUP_HEADER_PUSH_GAP = 60
GROUP_GAP_BETWEEN = 60


@dataclass
class Rect:
    x: int
    y: int
    width: int
    height: int

    @property
    def left(self) -> int:
        return self.x

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def top(self) -> int:
        return self.y

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @property
    def center_x(self) -> float:
        return self.x + (self.width / 2)

    @property
    def center_y(self) -> float:
        return self.y + (self.height / 2)

    def overlaps_x(self, other: "Rect") -> bool:
        return not (self.right < other.left or self.left > other.right)

    def overlaps_y(self, other: "Rect") -> bool:
        return not (self.bottom < other.top or self.top > other.bottom)


@dataclass
class BaseNode:
    id: str
    node_type: str
    x: int
    y: int
    width: int
    height: int
    color: Optional[str] = None

    @property
    def rect(self) -> Rect:
        return Rect(self.x, self.y, self.width, self.height)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "id": self.id,
            "type": self.node_type,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }
        if self.color:
            data["color"] = self.color
        return data


@dataclass
class TextNode(BaseNode):
    text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["text"] = self.text
        return data


@dataclass
class FileNode(BaseNode):
    file_path: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["file"] = self.file_path
        return data


@dataclass
class GroupNode(BaseNode):
    label: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["label"] = self.label
        return data


@dataclass
class Edge:
    id: str
    from_node: str
    to_node: str
    from_side: str
    to_side: str
    label: Optional[str] = None
    color: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "id": self.id,
            "fromNode": self.from_node,
            "fromSide": self.from_side,
            "toNode": self.to_node,
            "toSide": self.to_side,
        }
        if self.label:
            data["label"] = self.label
        if self.color:
            data["color"] = self.color
        return data


class Canvas:
    def __init__(self):
        self.nodes: List[BaseNode] = []
        self.edges: List[Edge] = []
        self.group_map: Dict[str, List[str]] = {}
        self._nodes_by_id: Dict[str, BaseNode] = {}
        self._node_ids: Set[str] = set()
        self._edge_ids: Set[str] = set()

    def _new_id(self) -> str:
        while True:
            candidate = uuid.uuid4().hex[:16]
            if candidate not in self._node_ids and candidate not in self._edge_ids:
                return candidate

    def _register_node(self, node: BaseNode) -> None:
        if node.id in self._node_ids or node.id in self._edge_ids:
            raise ValueError(f"Duplicate id detected: {node.id}")
        self.nodes.append(node)
        self._nodes_by_id[node.id] = node
        self._node_ids.add(node.id)

    def _register_edge(self, edge: Edge) -> None:
        if edge.id in self._edge_ids or edge.id in self._node_ids:
            raise ValueError(f"Duplicate id detected: {edge.id}")
        self.edges.append(edge)
        self._edge_ids.add(edge.id)

    def _get_node(self, node_id: str) -> Optional[BaseNode]:
        return self._nodes_by_id.get(node_id)

    def _coerce_int(self, value: Optional[Any], default: int) -> int:
        if value is None:
            return default
        return int(value)

    def _maybe_int(self, value: Optional[Any]) -> Optional[int]:
        if value is None:
            return None
        return int(value)

    def _estimate_text_height(self, text: str, width: int) -> int:
        lines = text.splitlines() or [""]
        max_chars = max(int(width / TEXT_CHAR_WIDTH), 1)
        wrapped_lines = 0
        for line in lines:
            wrap_count = (len(line) + max_chars - 1) // max_chars
            wrapped_lines += max(1, wrap_count)
        return TEXT_BASE_HEIGHT + (wrapped_lines * TEXT_LINE_HEIGHT)

    def _normalize_side(self, side: Optional[str]) -> Optional[str]:
        if not side:
            return None
        if side not in EDGE_SIDES:
            raise ValueError(f"Invalid edge side: {side}")
        return side

    def add_node(self, text, x, y, width=DEFAULT_TEXT_WIDTH, height=None, color=None, type=NODE_TYPE_TEXT, node_id=None):
        width = self._coerce_int(width, DEFAULT_TEXT_WIDTH)
        height = self._maybe_int(height)
        if height is None:
            height = self._estimate_text_height(text, width)

        node_id = node_id or self._new_id()
        node = TextNode(
            id=node_id,
            node_type=type,
            text=text,
            x=int(x),
            y=int(y),
            width=width,
            height=height,
            color=color,
        )
        self._register_node(node)
        return node_id

    def add_file(self, file_path, x, y, width=DEFAULT_FILE_WIDTH, height=DEFAULT_FILE_HEIGHT, color=None, node_id=None):
        width = self._coerce_int(width, DEFAULT_FILE_WIDTH)
        height = self._coerce_int(height, DEFAULT_FILE_HEIGHT)

        node_id = node_id or self._new_id()
        node = FileNode(
            id=node_id,
            node_type=NODE_TYPE_FILE,
            file_path=file_path,
            x=int(x),
            y=int(y),
            width=width,
            height=height,
            color=color,
        )
        self._register_node(node)
        return node_id

    def add_group(self, label, nodes_in_group=None, x=None, y=None, width=None, height=None, color=None, node_id=None):
        group_nodes: List[BaseNode] = []
        if nodes_in_group:
            for nid in nodes_in_group:
                node = self._get_node(nid)
                if node:
                    group_nodes.append(node)
            if not group_nodes:
                return None

            min_x = min(n.x for n in group_nodes)
            min_y = min(n.y for n in group_nodes)
            max_x = max(n.x + n.width for n in group_nodes)
            max_y = max(n.y + n.height for n in group_nodes)

            x = min_x - GROUP_PADDING
            y = min_y - GROUP_PADDING - GROUP_HEADER_HEIGHT
            width = (max_x - x) + GROUP_PADDING
            height = (max_y - y) + GROUP_PADDING + GROUP_BOTTOM_BUFFER

        node_id = node_id or self._new_id()
        group = GroupNode(
            id=node_id,
            node_type=NODE_TYPE_GROUP,
            label=label,
            x=self._coerce_int(x, 0),
            y=self._coerce_int(y, 0),
            width=self._coerce_int(width, DEFAULT_GROUP_WIDTH),
            height=self._coerce_int(height, DEFAULT_GROUP_HEIGHT),
            color=color,
        )
        self._register_node(group)

        if nodes_in_group:
            self.group_map[node_id] = [n.id for n in group_nodes]

        return node_id

    def _auto_edge_sides(self, from_node: BaseNode, to_node: BaseNode) -> Tuple[str, str]:
        dx = to_node.rect.center_x - from_node.rect.center_x
        dy = to_node.rect.center_y - from_node.rect.center_y
        if abs(dx) > abs(dy):
            return ("right", "left") if dx > 0 else ("left", "right")
        return ("bottom", "top") if dy > 0 else ("top", "bottom")

    def add_edge(self, from_node, to_node, label=None, color=None, from_side=None, to_side=None):
        from_side = self._normalize_side(from_side)
        to_side = self._normalize_side(to_side)

        fn = self._get_node(from_node)
        tn = self._get_node(to_node)

        if not from_side or not to_side:
            if fn and tn:
                auto_from, auto_to = self._auto_edge_sides(fn, tn)
                if not from_side:
                    from_side = auto_from
                if not to_side:
                    to_side = auto_to
            else:
                from_side = from_side or "bottom"
                to_side = to_side or "top"

        edge_id = self._new_id()
        edge = Edge(
            id=edge_id,
            from_node=from_node,
            to_node=to_node,
            from_side=from_side,
            to_side=to_side,
            label=label,
            color=color,
        )
        self._register_edge(edge)
        return edge_id

    def _is_group_member(self, group_id: str, node_id: str) -> bool:
        return node_id in self.group_map.get(group_id, [])

    def _shift_group_and_members(self, group_id: str, dx: int, dy: int) -> None:
        group_node = self._get_node(group_id)
        if group_node:
            group_node.x += dx
            group_node.y += dy
        for nid in self.group_map.get(group_id, []):
            node = self._get_node(nid)
            if node:
                node.x += dx
                node.y += dy

    def _resolve_group_header_collisions(self, groups: List[BaseNode], standard_nodes: List[BaseNode]) -> None:
        for group in groups:
            max_push_down = 0
            header_rect = Rect(
                group.x,
                group.y,
                group.width,
                GROUP_HEADER_HEIGHT + GROUP_HEADER_OVERLAP_BUFFER,
            )
            for node in standard_nodes:
                if self._is_group_member(group.id, node.id):
                    continue
                if not header_rect.overlaps_x(node.rect):
                    continue
                if not header_rect.overlaps_y(node.rect):
                    continue
                node_bottom = node.y + node.height
                push = (node_bottom + GROUP_HEADER_PUSH_GAP) - group.y
                if push > max_push_down:
                    max_push_down = push
            if max_push_down > 0:
                self._shift_group_and_members(group.id, 0, max_push_down)

    def _resolve_group_horizontal_overlaps(self, groups: List[BaseNode]) -> None:
        groups_sorted = sorted(groups, key=lambda g: g.x)
        for i in range(1, len(groups_sorted)):
            g_current = groups_sorted[i]
            max_prev_x_edge = None

            curr_y_start = g_current.y
            curr_y_end = g_current.y + g_current.height

            for j in range(i):
                g_prev = groups_sorted[j]
                prev_y_start = g_prev.y
                prev_y_end = g_prev.y + g_prev.height

                if (curr_y_start < prev_y_end) and (prev_y_start < curr_y_end):
                    prev_edge = g_prev.x + g_prev.width
                    if max_prev_x_edge is None or prev_edge > max_prev_x_edge:
                        max_prev_x_edge = prev_edge

            if max_prev_x_edge is not None:
                needed_x = max_prev_x_edge + GROUP_GAP_BETWEEN
                if g_current.x < needed_x:
                    shift = needed_x - g_current.x
                    self._shift_group_and_members(g_current.id, shift, 0)

    def _resolve_collisions(self) -> None:
        groups = [n for n in self.nodes if n.node_type == NODE_TYPE_GROUP]
        if not groups:
            return
        standard_nodes = [n for n in self.nodes if n.node_type != NODE_TYPE_GROUP]
        self._resolve_group_header_collisions(groups, standard_nodes)
        self._resolve_group_horizontal_overlaps(groups)

    def layout(self) -> None:
        self._resolve_collisions()

    def _sorted_nodes_for_zindex(self) -> List[BaseNode]:
        groups = [n for n in self.nodes if n.node_type == NODE_TYPE_GROUP]
        others = [n for n in self.nodes if n.node_type != NODE_TYPE_GROUP]
        return groups + others

    def to_dict(self) -> Dict[str, Any]:
        sorted_nodes = self._sorted_nodes_for_zindex()
        return {
            "nodes": [n.to_dict() for n in sorted_nodes],
            "edges": [e.to_dict() for e in self.edges],
        }

    def save(self, filepath: str) -> None:
        self.layout()
        data = self.to_dict()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Canvas saved to {os.path.abspath(filepath)}")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Canvas":
        canvas = cls()

        for n in data.get("nodes", []):
            mapped_args = {k: v for k, v in n.items() if k != "kind"}
            if "file" in mapped_args:
                canvas.add_file(file_path=mapped_args.pop("file"), **mapped_args)
            else:
                canvas.add_node(**mapped_args)

        for g in data.get("groups", []):
            mapped_args = {k: v for k, v in g.items() if k != "kind"}
            canvas.add_group(**mapped_args)

        for e in data.get("edges", []):
            mapped_args = {k: v for k, v in e.items() if k != "kind"}
            canvas.add_edge(**mapped_args)

        return canvas


if __name__ == "__main__":
    import sys

    input_data = sys.stdin.read()
    if not input_data.strip():
        print("Usage: echo 'JSON_DATA' | python3 canvas_lib.py")
        sys.exit(1)

    try:
        data = json.loads(input_data)
        canvas = Canvas.from_dict(data)

        if "output" in data:
            canvas.save(data["output"])
        else:
            print("Error: No 'output' filename specified in JSON.")

    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing canvas data: {e}")
        sys.exit(1)
