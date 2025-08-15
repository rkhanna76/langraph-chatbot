"""
Graph visualization module for the LangGraph Chatbot
"""

import os
from typing import Optional
from pathlib import Path


class GraphVisualizer:
    """Handles graph visualization generation and saving"""
    
    def __init__(self, output_dir: str = ".", formats: list = None):
        self.output_dir = Path(output_dir)
        self.formats = formats or ["png", "mermaid"]
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_visualizations(self, graph) -> dict:
        """Generate visualizations in multiple formats"""
        results = {}
        
        try:
            graph_viz = graph.get_graph()
            
            for format_type in self.formats:
                try:
                    if format_type == "png":
                        results["png"] = self._save_png_visualization(graph_viz)
                    elif format_type == "mermaid":
                        results["mermaid"] = self._save_mermaid_visualization(graph_viz)
                    elif format_type == "svg":
                        results["svg"] = self._save_svg_visualization(graph_viz)
                except Exception as e:
                    print(f"Warning: Failed to generate {format_type} visualization: {e}")
                    results[format_type] = None
            
            # Try inline display for Jupyter environments
            self._try_inline_display(graph_viz)
            
        except Exception as e:
            print(f"Could not generate graph visualization: {e}")
            print("This requires graphviz to be installed")
        
        return results
    
    def _save_png_visualization(self, graph_viz) -> Optional[str]:
        """Save graph as PNG file"""
        try:
            png_data = graph_viz.draw_mermaid_png()
            output_path = self.output_dir / "langgraph_visualization.png"
            
            with open(output_path, "wb") as f:
                f.write(png_data)
            
            print(f"Graph visualization saved as '{output_path}'")
            print("Open this file to view your LangGraph structure")
            
            return str(output_path)
        except Exception as e:
            print(f"Could not save PNG visualization: {e}")
            return None
    
    def _save_mermaid_visualization(self, graph_viz) -> Optional[str]:
        """Save graph as Mermaid text file"""
        try:
            mermaid_text = graph_viz.draw_mermaid()
            output_path = self.output_dir / "langgraph_visualization.mmd"
            
            with open(output_path, "w") as f:
                f.write(mermaid_text)
            
            print(f"Mermaid code saved as '{output_path}'")
            print("Copy this to https://mermaid.live/ to view online")
            
            return str(output_path)
        except Exception as e:
            print(f"Could not save Mermaid format: {e}")
            return None
    
    def _save_svg_visualization(self, graph_viz) -> Optional[str]:
        """Save graph as SVG file"""
        try:
            svg_data = graph_viz.draw_mermaid_svg()
            output_path = self.output_dir / "langgraph_visualization.svg"
            
            with open(output_path, "w") as f:
                f.write(svg_data)
            
            print(f"SVG visualization saved as '{output_path}'")
            
            return str(output_path)
        except Exception as e:
            print(f"Could not save SVG format: {e}")
            return None
    
    def _try_inline_display(self, graph_viz):
        """Try to display the graph inline (for Jupyter/IPython environments)"""
        try:
            from IPython.display import Image, display
            png_data = graph_viz.draw_mermaid_png()
            display(Image(png_data))
        except ImportError:
            print("IPython not available - image saved to file only")
        except Exception as e:
            print(f"Could not display inline: {e}")
    
    def cleanup_old_visualizations(self):
        """Remove old visualization files"""
        for format_type in self.formats:
            if format_type == "png":
                old_file = self.output_dir / "langgraph_visualization.png"
            elif format_type == "mermaid":
                old_file = self.output_dir / "langgraph_visualization.mmd"
            elif format_type == "svg":
                old_file = self.output_dir / "langgraph_visualization.svg"
            else:
                continue
            
            if old_file.exists():
                try:
                    old_file.unlink()
                    print(f"Removed old {format_type} visualization")
                except Exception as e:
                    print(f"Could not remove old {format_type} visualization: {e}")
