
import json
import uuid
import os

class Canvas:
    def __init__(self):
        self.nodes = []
        self.edges = []
        # Maps group_id -> list of node_ids belonging to it
        self.group_map = {} 
        
    def _get_id(self):
        return uuid.uuid4().hex[:16]

    def add_node(self, text, x, y, width=250, height=None, color=None, type="text", node_id=None):
        """
        Adds a node to the canvas.
        - Calculates dynamic height if not provided to prevent scrollbars.
        """
        if height is None:
            # Calibrated Simplification: Base 50px + 25px per line
            lines = text.count('\n') + 1
            height = 50 + (lines * 25)
            
            # Wrap check: 6px per character approx
            if len(text) > (width / 6):
                 height += (len(text) // (width / 6)) * 20
            
        nid = node_id if node_id else self._get_id()
        n = {
            "id": nid,
            "type": type,
            "text": text,
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height)
        }
        if color:
            n["color"] = color
        self.nodes.append(n)
        return nid

    def add_file(self, file_path, x, y, width=400, height=400, color=None, node_id=None):
        nid = node_id if node_id else self._get_id()
        n = {
            "id": nid,
            "type": "file",
            "file": file_path,
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height)
        }
        if color:
            n["color"] = color
        self.nodes.append(n)
        return nid

    def add_group(self, label, nodes_in_group=None, x=None, y=None, width=None, height=None, color=None, node_id=None):
        """
        Adds a group.
        - If 'nodes_in_group' (list of IDs) is provided, calculates bounds automatically.
        - Otherwise, requires x, y, width, height.
        """
        padding = 30
        header_height = 60
        
        if nodes_in_group:
            # Auto-calculate bounds
            group_nodes = [n for n in self.nodes if n['id'] in nodes_in_group]
            if not group_nodes:
                 # Fallback if no nodes found
                 return None
            
            min_x = min(n['x'] for n in group_nodes)
            min_y = min(n['y'] for n in group_nodes)
            max_x = max(n['x'] + n['width'] for n in group_nodes)
            max_y = max(n['y'] + n['height'] for n in group_nodes)
            
            x = min_x - padding
            y = min_y - padding - header_height # Extra space for label
            width = (max_x - x) + padding
            height = (max_y - y) + padding + 20 # Bottom buffer
            
        gid = node_id if node_id else self._get_id()
        g = {
            "id": gid,
            "type": "group",
            "label": label,
            "x": int(x or 0),
            "y": int(y or 0),
            "width": int(width or 200),
            "height": int(height or 200)
        }
        if color:
            g["color"] = color
        self.nodes.append(g)
        
        # Track membership for collision resolution
        if nodes_in_group:
            self.group_map[gid] = nodes_in_group
            
        return gid

    def add_edge(self, from_node, to_node, label=None, color=None, from_side=None, to_side=None):
        """
        Adds a connection. 
        - Uses Smart Routing if sides are not manually provided.
        """
        # Find nodes to determine relative positions
        fn = next((n for n in self.nodes if n['id'] == from_node), None)
        tn = next((n for n in self.nodes if n['id'] == to_node), None)
        
        if not from_side or not to_side:
            if fn and tn:
                dx = tn['x'] - fn['x']
                dy = tn['y'] - fn['y']
                
                # Thresholds
                h_dist = abs(dx)
                v_dist = abs(dy)
                
                # If further apart horizontally than vertically, use left/right
                if h_dist > v_dist:
                    if dx > 0:
                        f_s, t_s = "right", "left"
                    else:
                        f_s, t_s = "left", "right"
                else:
                    if dy > 0:
                        f_s, t_s = "bottom", "top"
                    else:
                        f_s, t_s = "top", "bottom"
                
                # Apply defaults if not provided
                if not from_side: from_side = f_s
                if not to_side: to_side = t_s
            else:
                # Fallback
                if not from_side: from_side = "bottom"
                if not to_side: to_side = "top"
        
        eid = self._get_id()
        e = {
            "id": eid,
            "fromNode": from_node,
            "fromSide": from_side,
            "toNode": to_node,
            "toSide": to_side
        }
        if label:
            e["label"] = label
        if color:
            e["color"] = color
            
        self.edges.append(e)
        return eid

    def _resolve_collisions(self):
        """
        Smart Layout:
        Identifies groups and shifts them right if they overlap horizontally
        WITHIN the same vertical band (y-axis overlap).
        Allows for both horizontal rows and vertical columns.
        """
        groups = [n for n in self.nodes if n['type'] == 'group']
        standard_nodes = [n for n in self.nodes if n['type'] != 'group']
        
        if not groups:
            return
            
        # 1. Resolve overlaps between standard nodes (like Titles) and Groups
        # Only push down if the group's HEADER area overlaps a standard node.
        for g in groups:
            g_top = g['y']
            g_left = g['x']
            g_right = g['x'] + g['width']
            
            max_push_down = 0
            for sn in standard_nodes:
                # CRITICAL: A group should never be pushed down by its OWN members
                if g['id'] in self.group_map and sn['id'] in self.group_map[g['id']]:
                    continue
                    
                sn_bottom = sn['y'] + sn['height']
                sn_left = sn['x']
                sn_right = sn['x'] + sn['width']
                
                # Check intersection (Horizontal AND Vertical)
                if not (g_right < sn_left or g_left > sn_right):
                    # Check if group is actually "under" or "overlapping" the node
                    if g_top < sn_bottom + 40:
                        push = (sn_bottom + 60) - g_top
                        if push > max_push_down:
                            max_push_down = push
            
            if max_push_down > 0:
                g['y'] += max_push_down
                if g['id'] in self.group_map:
                    for nid in self.group_map[g['id']]:
                        n = next((node for node in self.nodes if node['id'] == nid), None)
                        if n: n['y'] += max_push_down

        # 2. Resolve horizontal overlaps between groups
        groups.sort(key=lambda g: g['x'])
        GAP_BETWEEN_GROUPS = 60
        
        for i in range(1, len(groups)):
            g_current = groups[i]
            max_prev_x_edge = None
            
            curr_y_start = g_current['y']
            curr_y_end = g_current['y'] + g_current['height']
            
            for j in range(i):
                g_prev = groups[j]
                prev_y_start = g_prev['y']
                prev_y_end = g_prev['y'] + g_prev['height']
                
                if (curr_y_start < prev_y_end) and (prev_y_start < curr_y_end):
                    prev_edge = g_prev['x'] + g_prev['width']
                    if max_prev_x_edge is None or prev_edge > max_prev_x_edge:
                        max_prev_x_edge = prev_edge
            
            if max_prev_x_edge is not None:
                needed_x = max_prev_x_edge + GAP_BETWEEN_GROUPS
                if g_current['x'] < needed_x:
                    shift = needed_x - g_current['x']
                    g_current['x'] += shift
                    if g_current['id'] in self.group_map:
                        for nid in self.group_map[g_current['id']]:
                            node = next((n for n in self.nodes if n['id'] == nid), None)
                            if node: node['x'] += shift

    def save(self, filepath):
        # Auto-fix layout before saving
        self._resolve_collisions()
        
        # Proper Z-indexing: Groups must be first in the array to render behind nodes
        sorted_nodes = [n for n in self.nodes if n['type'] == 'group'] + \
                       [n for n in self.nodes if n['type'] != 'group']
        
        data = {
            "nodes": sorted_nodes,
            "edges": self.edges
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Canvas saved to {os.path.abspath(filepath)}")

if __name__ == "__main__":
    # CLI Mode: Read commands from JSON on stdin
    import sys
    
    input_data = sys.stdin.read()
    if not input_data.strip():
        print("Usage: echo 'JSON_DATA' | python3 canvas_lib.py")
        sys.exit(1)
        
    try:
        data = json.loads(input_data)
        
        c = Canvas()
        
        # Process Nodes
        for n in data.get("nodes", []):
            mapped_args = {k: v for k, v in n.items() if k != "kind"}
            if "file" in mapped_args:
                c.add_file(file_path=mapped_args.pop("file"), **mapped_args)
            else:
                c.add_node(**mapped_args)

        # Process Groups
        # (Must be after nodes exist, to calculate bounds)
        for g in data.get("groups", []):
            mapped_args = {k: v for k, v in g.items() if k != "kind"}
            c.add_group(**mapped_args)

        # Process Edges
        for e in data.get("edges", []):
            mapped_args = {k: v for k, v in e.items() if k != "kind"}
            c.add_edge(**mapped_args)
            
        # Save
        if "output" in data:
            c.save(data["output"])
        else:
            print("Error: No 'output' filename specified in JSON.")
            
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing canvas data: {e}")
        sys.exit(1)
