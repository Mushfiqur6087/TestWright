from typing import List, Optional
import os

from autospectest.framework.agents.base import BaseAgent
from autospectest.framework.schemas.schemas import (
    ParsedFunctionalDescription,
    ParsedModule,
    NavigationGraph,
    NavigationNode
)

# Import graph visualization libraries
try:
    import networkx as nx # type: ignore
    import matplotlib.pyplot as plt # type: ignore
    GRAPH_LIBS_AVAILABLE = True
except ImportError:
    GRAPH_LIBS_AVAILABLE = False


class NavigationAgent(BaseAgent):
    """Agent responsible for building navigation graph of the website"""

    @property
    def name(self) -> str:
        return "Navigation Agent"

    @property
    def system_prompt(self) -> str:
        return """You are an expert in web application navigation and site mapping.

Your task is to analyze the navigation structure of a web application and build a navigation graph.

You understand:
- How sidebar menus typically work
- Page relationships and navigation paths

Provide accurate navigation information based on the description provided."""

    def run(self, parsed_desc: ParsedFunctionalDescription) -> NavigationGraph:
        """Build navigation graph from parsed functional description"""

        nav_graph = NavigationGraph()

        # Use LLM to analyze navigation structure
        nav_structure = self._analyze_navigation(
            parsed_desc.navigation_overview,
            parsed_desc.modules
        )

        # Build navigation nodes
        for module in parsed_desc.modules:
            module_nav = nav_structure.get(module.id, {})

            node = NavigationNode(
                module_id=module.id,
                title=module.title,
                url_path=module_nav.get("url_path"),
                connected_to=module_nav.get("connected_to", []),
                test_case_ids=[]  # Will be populated by AssemblerAgent
            )
            nav_graph.nodes[module.id] = node

        return nav_graph

    def _analyze_navigation(
        self,
        navigation_overview: str,
        modules: List[ParsedModule]
    ) -> dict:
        """Use LLM to analyze navigation structure"""

        modules_list = "\n".join([
            f"- ID: {m.id}, Title: {m.title}"
            for m in modules
        ])

        prompt = f"""Analyze this navigation structure and determine page relationships.

Navigation Overview:
{navigation_overview}

Modules:
{modules_list}

For each module, determine:
1. connected_to: List of module IDs that can be reached FROM this module
2. url_path: The likely URL path (if inferable from context)

Return a JSON object where keys are module IDs (as strings) and values contain:
{{
    "1": {{
        "connected_to": [2, 3, 4],
        "url_path": "/login"
    }},
    "2": {{
        "connected_to": [1],
        "url_path": "/forgot-password"
    }}
}}

Navigation Rules:
- Use the navigation overview to understand the menu structure
"""

        try:
            result = self.call_llm_json(prompt, max_tokens=16000)
            # Convert string keys to int and validate connected_to
            parsed = {}
            for k, v in result.items():
                module_id = int(k)
                connected = v.get("connected_to", [])
                # Ensure connected_to is a list of ints
                if isinstance(connected, list):
                    connected = [int(c) for c in connected if isinstance(c, (int, str))]
                else:
                    connected = []

                parsed[module_id] = {
                    "connected_to": connected,
                    "url_path": v.get("url_path")
                }
            return parsed
        except Exception as e:
            print(f"Warning: Navigation analysis failed: {e}")
            # Return default structure - all pages connect to each other.
            return self._default_navigation(modules)

    def _default_navigation(self, modules: List[ParsedModule]) -> dict:
        """Generate default navigation when LLM fails"""
        result = {}

        for module in modules:
            connected = [m.id for m in modules if m.id != module.id]

            result[module.id] = {
                "connected_to": connected,
                "url_path": None
            }

        return result

    def link_test_cases(self, nav_graph: NavigationGraph, test_cases: list) -> NavigationGraph:
        """Link test case IDs to their corresponding navigation nodes"""
        for tc in test_cases:
            if tc.module_id in nav_graph.nodes:
                if tc.id not in nav_graph.nodes[tc.module_id].test_case_ids:
                    nav_graph.nodes[tc.module_id].test_case_ids.append(tc.id)

        return nav_graph

    def generate_graph_image(
        self,
        nav_graph: NavigationGraph,
        output_path: str,
        title: str = "Navigation Graph"
    ) -> Optional[str]:
        """
        Generate a visual graph image from the navigation graph.

        Args:
            nav_graph: The navigation graph to visualize
            output_path: Path to save the image (e.g., 'output/navigation_graph.png')
            title: Title for the graph

        Returns:
            The path to the generated image, or None if generation failed
        """
        if not GRAPH_LIBS_AVAILABLE:
            print("Warning: networkx/matplotlib not installed. Skipping graph image generation.")
            return None

        if not nav_graph.nodes:
            print("Warning: Navigation graph is empty. Skipping graph image generation.")
            return None

        # Create directed graph
        G = nx.DiGraph()

        # Add nodes with attributes
        for module_id, node in nav_graph.nodes.items():
            G.add_node(
                module_id,
                label=node.title,
                test_count=len(node.test_case_ids)
            )

        # Add edges (connections)
        for module_id, node in nav_graph.nodes.items():
            for target_id in node.connected_to:
                if target_id in nav_graph.nodes:
                    G.add_edge(module_id, target_id)

        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))

        # Choose layout based on graph size
        num_nodes = len(G.nodes())
        if num_nodes <= 5:
            pos = nx.circular_layout(G)
        elif num_nodes <= 10:
            pos = nx.spring_layout(G, k=2.5, iterations=50, seed=42)
        else:
            # NetworkX's kamada_kawai_layout imports scipy internally.
            # Fall back to spring_layout when scipy isn't available.
            try:
                pos = nx.kamada_kawai_layout(G)
            except ModuleNotFoundError as e:
                if getattr(e, "name", "") == "scipy":
                    print("Warning: scipy not installed. Falling back to spring layout.")
                    pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42)
                else:
                    raise
            except Exception as e:
                print(f"Warning: kamada_kawai_layout failed ({e}). Falling back to spring layout.")
                pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42)

        # Use a single visual style for all pages.
        node_colors = ['#1E88E5' for _ in G.nodes()]

        # Node sizes based on test count
        node_sizes = []
        for node_id in G.nodes():
            test_count = G.nodes[node_id].get('test_count', 0)
            base_size = 2000
            node_sizes.append(base_size + (test_count * 100))

        # Draw edges with arrows
        nx.draw_networkx_edges(
            G, pos,
            edge_color='#757575',
            arrows=True,
            arrowsize=20,
            arrowstyle='-|>',
            connectionstyle='arc3,rad=0.1',
            alpha=0.7,
            width=1.5,
            ax=ax
        )

        # Draw nodes
        nx.draw_networkx_nodes(
            G, pos,
            node_color=node_colors,
            node_size=node_sizes,
            alpha=0.9,
            ax=ax
        )

        # Create labels with module title and test count
        labels = {}
        for node_id in G.nodes():
            node_data = G.nodes[node_id]
            label = node_data.get('label', str(node_id))
            test_count = node_data.get('test_count', 0)
            if test_count > 0:
                labels[node_id] = f"{label}\n({test_count} tests)"
            else:
                labels[node_id] = label

        # Draw labels
        nx.draw_networkx_labels(
            G, pos,
            labels=labels,
            font_size=9,
            font_weight='bold',
            ax=ax
        )

        # Set title and styling
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')

        # Add subtitle with stats
        total_nodes = len(nav_graph.nodes)
        total_edges = sum(len(node.connected_to) for node in nav_graph.nodes.values())

        subtitle = f"Nodes: {total_nodes} | Connections: {total_edges}"
        fig.text(0.5, 0.02, subtitle, ha='center', fontsize=10, color='#666666')

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Save figure
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close(fig)

        return output_path
