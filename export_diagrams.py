"""
Export Draw.io diagrams to PNG for PowerPoint integration
This script requires Draw.io desktop app or drawio CLI
"""
import subprocess
import os
from pathlib import Path

def export_diagram(drawio_file, output_png):
    """Export Draw.io diagram to PNG"""
    try:
        # Try using draw.io CLI if available
        cmd = [
            "drawio",
            "--export",
            "--format", "png",
            "--output", output_png,
            drawio_file
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ Exported: {output_png}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"⚠️  Could not auto-export {drawio_file}")
        print(f"   Please open {drawio_file} in Draw.io and export manually to: {output_png}")
        return False

if __name__ == "__main__":
    project_root = Path(__file__).parent
    diagrams_dir = project_root / "diagrams"
    
    # Create diagrams directory if not exists
    diagrams_dir.mkdir(exist_ok=True)
    
    # List of diagrams to export
    diagrams = [
        ("chatbot-flow-diagram.drawio", "chatbot-flow.png"),
        ("diagrams/rag-pipeline-diagram.drawio", "diagrams/rag-pipeline.png"),
        ("diagrams/rbac-architecture-diagram.drawio", "diagrams/rbac-architecture.png"),
    ]
    
    print("🎨 Exporting Draw.io diagrams to PNG...\n")
    
    exported_count = 0
    for drawio_file, png_file in diagrams:
        drawio_path = str(project_root / drawio_file)
        png_path = str(project_root / png_file)
        
        if os.path.exists(drawio_path):
            if export_diagram(drawio_path, png_path):
                exported_count += 1
        else:
            print(f"⚠️  File not found: {drawio_path}")
    
    print(f"\n📊 Exported {exported_count}/{len(diagrams)} diagrams")
    
    if exported_count < len(diagrams):
        print("\n📝 Manual Export Instructions:")
        print("1. Open each .drawio file in VS Code")
        print("2. Click File > Export as > PNG...")
        print("3. Save with the corresponding filename in diagrams/ folder")
        print("\nOr use Draw.io desktop app with CLI for automated export")
