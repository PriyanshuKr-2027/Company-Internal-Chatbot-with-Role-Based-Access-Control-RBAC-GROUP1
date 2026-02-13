"""
Generate PowerPoint Presentation for Role-Based Access Chatbot
Matching the Canva template style: Tech Vibrant Trendy
Enhanced version with 15 slides matching Canva design
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    """Create a vibrant tech-themed presentation matching Canva template"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Color scheme - Exact Canva "Tech Vibrant Trendy" Theme
    COLORS = {
        'primary': RGBColor(88, 86, 214),      # Purple/Blue
        'secondary': RGBColor(255, 71, 133),   # Hot Pink
        'accent': RGBColor(58, 255, 217),      # Cyan/Turquoise
        'purple': RGBColor(138, 43, 226),      # Vibrant Purple
        'orange': RGBColor(255, 140, 0),       # Vibrant Orange
        'dark': RGBColor(26, 32, 44),          # Dark Navy
        'light': RGBColor(255, 255, 255),      # White
        'text': RGBColor(45, 55, 72),          # Dark gray text
        'success': RGBColor(46, 213, 115),     # Bright Green
        'yellow': RGBColor(255, 234, 0),       # Bright Yellow
    }
    
    def add_title_slide():
        """Slide 1: Title Slide"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
        
        # Background gradient effect (simulated with shape)
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLORS['dark']
        bg.line.fill.background()
        
        # Accent shapes
        accent1 = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8), Inches(0.5), Inches(1.5), Inches(1.5)
        )
        accent1.fill.solid()
        accent1.fill.fore_color.rgb = COLORS['primary']
        accent1.line.fill.background()
        accent1.rotation = 30
        
        accent2 = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.5), Inches(1.2), Inches(1.2)
        )
        accent2.fill.solid()
        accent2.fill.fore_color.rgb = COLORS['secondary']
        accent2.line.fill.background()
        accent2.rotation = 15
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(2))
        title_frame = title_box.text_frame
        title_frame.word_wrap = True
        
        p = title_frame.paragraphs[0]
        p.text = "ROLE-BASED ACCESS CHATBOT"
        p.font.size = Pt(48)
        p.font.bold = True
        p.font.color.rgb = COLORS['light']
        p.alignment = PP_ALIGN.CENTER
        
        # Subtitle
        subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(3.8), Inches(8), Inches(1.5))
        subtitle_frame = subtitle_box.text_frame
        subtitle_frame.word_wrap = True
        
        p = subtitle_frame.paragraphs[0]
        p.text = "AI-POWERED"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLORS['accent']
        p.alignment = PP_ALIGN.CENTER
        
        p = subtitle_frame.add_paragraph()
        p.text = "SEMANTIC SEARCH FOR COMPANY DOCUMENTS"
        p.font.size = Pt(24)
        p.font.color.rgb = COLORS['light']
        p.alignment = PP_ALIGN.CENTER
        
        # Tagline (bottom)
        tag_box = slide.shapes.add_textbox(Inches(1), Inches(5.8), Inches(8), Inches(1))
        tag_frame = tag_box.text_frame
        p = tag_frame.paragraphs[0]
        p.text = "THYNK UNLIMITED"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = COLORS['accent']
        p.alignment = PP_ALIGN.CENTER
        
        p = tag_frame.add_paragraph()
        p.text = "WE LEARN FOR THE FUTURE"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['light']
        p.alignment = PP_ALIGN.CENTER
    
    def add_problem_solution_slide():
        """Slide 2: Problem & Solution"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "PROBLEM & SOLUTION"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary']
        p.alignment = PP_ALIGN.CENTER
        
        # Problem section
        prob_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(4.2), Inches(4.5)
        )
        prob_box.fill.solid()
        prob_box.fill.fore_color.rgb = COLORS['light']
        prob_box.line.color.rgb = COLORS['secondary']
        prob_box.line.width = Pt(3)
        
        prob_text = prob_box.text_frame
        prob_text.word_wrap = True
        prob_text.margin_left = Inches(0.3)
        prob_text.margin_right = Inches(0.3)
        prob_text.margin_top = Inches(0.3)
        
        p = prob_text.paragraphs[0]
        p.text = "Problem:"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLORS['secondary']
        
        p = prob_text.add_paragraph()
        p.text = "\n• Internal company data scattered across departments"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['text']
        p.space_after = Pt(10)
        
        p = prob_text.add_paragraph()
        p.text = "• No role-based access control for sensitive information"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['text']
        p.space_after = Pt(10)
        
        p = prob_text.add_paragraph()
        p.text = "• Traditional keyword search fails to understand context"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['text']
        p.space_after = Pt(10)
        
        p = prob_text.add_paragraph()
        p.text = "• Security risks with unrestricted document access"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['text']
        
        # Solution section
        sol_box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.3), Inches(1.5), Inches(4.2), Inches(4.5)
        )
        sol_box.fill.solid()
        sol_box.fill.fore_color.rgb = COLORS['light']
        sol_box.line.color.rgb = COLORS['success']
        sol_box.line.width = Pt(3)
        
        sol_text = sol_box.text_frame
        sol_text.word_wrap = True
        sol_text.margin_left = Inches(0.3)
        sol_text.margin_right = Inches(0.3)
        sol_text.margin_top = Inches(0.3)
        
        p = sol_text.paragraphs[0]
        p.text = "Solution:"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLORS['success']
        
        p = sol_text.add_paragraph()
        p.text = "\n• AI-powered semantic search with RAG pipeline"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['text']
        p.space_after = Pt(10)
        
        p = sol_text.add_paragraph()
        p.text = "• Granular role-based access control (RBAC)"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['text']
        p.space_after = Pt(10)
        
        p = sol_text.add_paragraph()
        p.text = "• Context-aware responses using Mistral 7B LLM"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['text']
        p.space_after = Pt(10)
        
        p = sol_text.add_paragraph()
        p.text = "• Source attribution & confidence scoring"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['text']
    
    def add_key_features_slide():
        """Slide 3: Key Features"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLORS['light']
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "KEY FEATURES"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary']
        p.alignment = PP_ALIGN.CENTER
        
        features = [
            ("🔐", "RBAC Security", "Department-based access control", COLORS['secondary']),
            ("🧠", "LLM-Powered", "Mistral 7B for intelligent responses", COLORS['primary']),
            ("📊", "Source Attribution", "Citations with confidence scoring", COLORS['success']),
            ("⚡", "High Performance", "~20ms search, ~2.5s total response", COLORS['orange']),
        ]
        
        y_pos = 1.8
        for icon, title, desc, color in features:
            # Feature box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(y_pos), Inches(8), Inches(1.1)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = RGBColor(248, 250, 252)
            box.line.color.rgb = color
            box.line.width = Pt(2)
            
            # Icon
            icon_box = slide.shapes.add_textbox(Inches(1.3), Inches(y_pos + 0.15), Inches(0.8), Inches(0.8))
            icon_frame = icon_box.text_frame
            p = icon_frame.paragraphs[0]
            p.text = icon
            p.font.size = Pt(36)
            p.alignment = PP_ALIGN.CENTER
            
            # Title
            title_box = slide.shapes.add_textbox(Inches(2.3), Inches(y_pos + 0.2), Inches(3), Inches(0.4))
            title_frame = title_box.text_frame
            p = title_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(18)
            p.font.bold = True
            p.font.color.rgb = color
            
            # Description
            desc_box = slide.shapes.add_textbox(Inches(2.3), Inches(y_pos + 0.6), Inches(6), Inches(0.4))
            desc_frame = desc_box.text_frame
            p = desc_frame.paragraphs[0]
            p.text = desc
            p.font.size = Pt(14)
            p.font.color.rgb = COLORS['text']
            
            y_pos += 1.3
    
    def add_architecture_slide():
        """Slide 4: System Architecture - Visual Flowchart"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "SYSTEM ARCHITECTURE"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary']
        p.alignment = PP_ALIGN.CENTER
        
        # Main flow components with arrows
        components = [
            ("User\nQuery", 0.8, 2.5, COLORS['primary'], "🟦"),
            ("Auth", 2.2, 2.5, COLORS['secondary'], "🔐"),
            ("RBAC\nFilter", 3.5, 2.5, COLORS['orange'], "🛡️"),
            ("Semantic\nSearch", 4.9, 2.5, COLORS['success'], "🔍"),
            ("Context\nBuilder", 6.3, 2.5, COLORS['purple'], "📋"),
            ("LLM\nGenerate", 7.6, 2.5, COLORS['primary'], "🤖"),
            ("Response", 9, 2.5, COLORS['accent'], "✨"),
        ]
        
        # Draw components
        for idx, (comp_name, x_pos, y_pos, color, emoji) in enumerate(components):
            # Component box with gradient effect
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, 
                Inches(x_pos), Inches(y_pos), 
                Inches(1.2), Inches(1)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = color
            box.line.fill.background()
            box.shadow.inherit = False
            
            # Icon emoji
            icon_box = slide.shapes.add_textbox(
                Inches(x_pos), Inches(y_pos + 0.1), 
                Inches(1.2), Inches(0.4)
            )
            icon_frame = icon_box.text_frame
            p = icon_frame.paragraphs[0]
            p.text = emoji
            p.font.size = Pt(24)
            p.alignment = PP_ALIGN.CENTER
            
            # Component text
            text_box = slide.shapes.add_textbox(
                Inches(x_pos), Inches(y_pos + 0.5), 
                Inches(1.2), Inches(0.5)
            )
            text_frame = text_box.text_frame
            text_frame.word_wrap = True
            text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            
            p = text_frame.paragraphs[0]
            p.text = comp_name
            p.font.size = Pt(9)
            p.font.bold = True
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
            
            # Draw arrow to next component
            if idx < len(components) - 1:
                from pptx.shapes.connector import Connector
                from pptx.enum.shapes import MSO_CONNECTOR
                
                # Arrow line
                arrow = slide.shapes.add_shape(
                    MSO_SHAPE.RIGHT_ARROW,
                    Inches(x_pos + 1.2), Inches(y_pos + 0.45),
                    Inches(0.15), Inches(0.1)
                )
                arrow.fill.solid()
                arrow.fill.fore_color.rgb = color
                arrow.line.fill.background()
        
        # Sub-components / databases
        db_components = [
            ("ChromaDB\n135 documents\n384 dims", 4.9, 4.2, COLORS['success']),
            ("Mistral 7B\nOpenRouter API", 7.6, 4.2, COLORS['primary']),
            ("SQLite\nUser DB", 2.2, 4.2, COLORS['secondary']),
        ]
        
        for text, x, y, color in db_components:
            # Database cylinder shape (simulated with rounded rectangle)
            db_box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(x), Inches(y),
                Inches(1.2), Inches(0.8)
            )
            db_box.fill.solid()
            db_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
            db_box.line.color.rgb = color
            db_box.line.width = Pt(2)
            
            # Database text
            db_text = slide.shapes.add_textbox(Inches(x + 0.1), Inches(y + 0.15), Inches(1), Inches(0.5))
            db_frame = db_text.text_frame
            db_frame.word_wrap = True
            
            p = db_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(8)
            p.font.color.rgb = COLORS['text']
            p.alignment = PP_ALIGN.CENTER
            
            # Connection line from main component to database
            line = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(x + 0.6), Inches(y - 0.7),
                Inches(0.02), Inches(0.7)
            )
            line.fill.solid()
            line.fill.fore_color.rgb = color
            line.line.fill.background()
        
        # Performance note
        perf_box = slide.shapes.add_textbox(Inches(3), Inches(5.5), Inches(4), Inches(0.6))
        perf_frame = perf_box.text_frame
        p = perf_frame.paragraphs[0]
        p.text = "⚡ ~20ms search  |  ~1.5-3.5s total response time"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLORS['orange']
        p.alignment = PP_ALIGN.CENTER
    
    def add_tech_stack_slide():
        """Slide 5: Technology Stack"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLORS['light']
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "TECHNOLOGY STACK"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary']
        p.alignment = PP_ALIGN.CENTER
        
        # Categories
        categories = [
            ("Backend", ["FastAPI", "Python 3.8+", "SQLAlchemy", "JWT Authentication"], COLORS['primary']),
            ("AI/ML", ["Mistral 7B (OpenRouter)", "sentence-transformers", "MiniLM-L6-v2"], COLORS['secondary']),
            ("Database", ["ChromaDB (Vector Store)", "SQLite (User DB)", "135 Indexed Documents"], COLORS['success']),
            ("Security", ["RBAC Middleware", "JWT Tokens", "Department-based Filtering"], COLORS['orange']),
        ]
        
        x_positions = [0.8, 5.3]
        y_positions = [1.8, 4.5]
        
        for idx, (cat_name, items, color) in enumerate(categories):
            x = x_positions[idx % 2]
            y = y_positions[idx // 2]
            
            # Category box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(4), Inches(2)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = RGBColor(248, 250, 252)
            box.line.color.rgb = color
            box.line.width = Pt(3)
            
            # Category title
            cat_box = slide.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.2), Inches(3.4), Inches(0.4))
            cat_frame = cat_box.text_frame
            p = cat_frame.paragraphs[0]
            p.text = cat_name
            p.font.size = Pt(20)
            p.font.bold = True
            p.font.color.rgb = color
            
            # Items
            items_box = slide.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.7), Inches(3.4), Inches(1))
            items_frame = items_box.text_frame
            items_frame.word_wrap = True
            
            for item in items:
                p = items_frame.add_paragraph()
                p.text = f"• {item}"
                p.font.size = Pt(12)
                p.font.color.rgb = COLORS['text']
                p.space_after = Pt(5)
    
    def add_rbac_slide():
        """Slide 6: RBAC Details"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "ROLE-BASED ACCESS CONTROL"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary']
        p.alignment = PP_ALIGN.CENTER
        
        # Department roles
        roles = [
            ("Finance Team", "• Financial Reports\n• Quarterly Statements\n• Budget Documents", COLORS['success']),
            ("HR Department", "• Employee Data\n• Payroll Information\n• HR Policies", COLORS['secondary']),
            ("Marketing", "• Marketing Reports\n• Campaign Analytics\n• Market Research", COLORS['orange']),
            ("Engineering", "• Technical Docs\n• Architecture Plans\n• API Documentation", COLORS['primary']),
            ("General Access", "• Company Handbook\n• General Policies\n• Public Resources", COLORS['accent']),
        ]
        
        y_pos = 1.6
        for role_name, access, color in roles:
            # Role box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(y_pos), Inches(7), Inches(0.9)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = COLORS['light']
            box.line.color.rgb = color
            box.line.width = Pt(2)
            
            # Role name
            role_box = slide.shapes.add_textbox(Inches(2), Inches(y_pos + 0.15), Inches(2), Inches(0.6))
            role_frame = role_box.text_frame
            p = role_frame.paragraphs[0]
            p.text = role_name
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = color
            
            # Access details
            access_box = slide.shapes.add_textbox(Inches(4.2), Inches(y_pos + 0.15), Inches(4), Inches(0.6))
            access_frame = access_box.text_frame
            access_frame.word_wrap = True
            p = access_frame.paragraphs[0]
            p.text = access
            p.font.size = Pt(11)
            p.font.color.rgb = COLORS['text']
            
            y_pos += 1.05
    
    def add_performance_slide():
        """Slide 7: Performance Metrics"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLORS['light']
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "PERFORMANCE METRICS"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary']
        p.alignment = PP_ALIGN.CENTER
        
        # Metrics
        metrics = [
            ("~20ms", "Semantic Search", COLORS['success']),
            ("~1.5-3.5s", "End-to-End Response", COLORS['primary']),
            ("135", "Indexed Documents", COLORS['orange']),
            ("384", "Embedding Dimensions", COLORS['secondary']),
        ]
        
        x_positions = [1.2, 5.5, 1.2, 5.5]
        y_positions = [2, 2, 4.5, 4.5]
        
        for idx, (value, label, color) in enumerate(metrics):
            x = x_positions[idx]
            y = y_positions[idx]
            
            # Metric box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.5), Inches(1.8)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = color
            box.line.fill.background()
            
            # Value
            val_box = slide.shapes.add_textbox(Inches(x), Inches(y + 0.3), Inches(3.5), Inches(0.8))
            val_frame = val_box.text_frame
            val_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = val_frame.paragraphs[0]
            p.text = value
            p.font.size = Pt(48)
            p.font.bold = True
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
            
            # Label
            label_box = slide.shapes.add_textbox(Inches(x), Inches(y + 1.1), Inches(3.5), Inches(0.5))
            label_frame = label_box.text_frame
            p = label_frame.paragraphs[0]
            p.text = label
            p.font.size = Pt(18)
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
    
    def add_rag_pipeline_slide():
        """Slide 8: RAG Pipeline Details"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "RAG PIPELINE WORKFLOW"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary']
        p.alignment = PP_ALIGN.CENTER
        
        # Pipeline steps
        steps = [
            ("1. Query Processing", "User query analyzed and embedded using MiniLM-L6-v2", COLORS['primary']),
            ("2. Semantic Search", "ChromaDB finds top-k relevant documents with cosine similarity", COLORS['secondary']),
            ("3. RBAC Filtering", "Results filtered based on user's department permissions", COLORS['orange']),
            ("4. Context Building", "Retrieved documents augmented into prompt context", COLORS['success']),
            ("5. LLM Generation", "Mistral 7B generates contextual response with citations", COLORS['primary']),
            ("6. Quality Scoring", "Confidence score (HIGH/MEDIUM/LOW) assigned to response", COLORS['accent']),
        ]
        
        y_pos = 1.8
        for step, desc, color in steps:
            # Step box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(y_pos), Inches(8), Inches(0.75)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = COLORS['light']
            box.line.color.rgb = color
            box.line.width = Pt(2)
            
            # Step number/title
            step_box = slide.shapes.add_textbox(Inches(1.3), Inches(y_pos + 0.15), Inches(2.5), Inches(0.45))
            step_frame = step_box.text_frame
            p = step_frame.paragraphs[0]
            p.text = step
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = color
            
            # Description
            desc_box = slide.shapes.add_textbox(Inches(4), Inches(y_pos + 0.15), Inches(4.5), Inches(0.45))
            desc_frame = desc_box.text_frame
            desc_frame.word_wrap = True
            p = desc_frame.paragraphs[0]
            p.text = desc
            p.font.size = Pt(11)
            p.font.color.rgb = COLORS['text']
            
            y_pos += 0.9
    
    def add_vector_database_slide():
        """Slide 9: Vector Database Details"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLORS['light']
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "VECTOR DATABASE - CHROMADB"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['purple']
        p.alignment = PP_ALIGN.CENTER
        
        # Stats boxes
        stats = [
            ("135", "Indexed Documents", COLORS['primary']),
            ("384", "Embedding Dimensions", COLORS['secondary']),
            ("~20ms", "Search Speed", COLORS['success']),
        ]
        
        x_pos = 1.5
        for value, label, color in stats:
            # Stat box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x_pos), Inches(2), Inches(2.2), Inches(1.5)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = color
            box.line.fill.background()
            
            # Value
            val_box = slide.shapes.add_textbox(Inches(x_pos), Inches(2.2), Inches(2.2), Inches(0.6))
            val_frame = val_box.text_frame
            val_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = val_frame.paragraphs[0]
            p.text = value
            p.font.size = Pt(40)
            p.font.bold = True
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
            
            # Label
            lbl_box = slide.shapes.add_textbox(Inches(x_pos), Inches(2.9), Inches(2.2), Inches(0.4))
            lbl_frame = lbl_box.text_frame
            p = lbl_frame.paragraphs[0]
            p.text = label
            p.font.size = Pt(14)
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
            
            x_pos += 2.5
        
        # Features list
        features_box = slide.shapes.add_textbox(Inches(1.5), Inches(4), Inches(7), Inches(2.5))
        features_frame = features_box.text_frame
        features_frame.word_wrap = True
        
        p = features_frame.paragraphs[0]
        p.text = "Key Features:"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = COLORS['purple']
        p.space_after = Pt(10)
        
        features_list = [
            "• Semantic similarity search with cosine distance",
            "• Normalized embeddings using MiniLM-L6-v2 model",
            "• Efficient metadata filtering for RBAC",
            "• Persistent storage with automatic indexing",
            "• Support for multi-modal document types (CSV, Markdown)",
        ]
        
        for feature in features_list:
            p = features_frame.add_paragraph()
            p.text = feature
            p.font.size = Pt(14)
            p.font.color.rgb = COLORS['text']
            p.space_after = Pt(8)
    
    def add_security_features_slide():
        """Slide 10: Security Features"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "SECURITY FEATURES"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['secondary']
        p.alignment = PP_ALIGN.CENTER
        
        # Security features
        security_items = [
            ("🔐 JWT Authentication", "Secure token-based authentication with expiration", COLORS['primary']),
            ("🛡️ RBAC Middleware", "Role-based access control at API and data layer", COLORS['secondary']),
            ("📝 Audit Logging", "Complete audit trail of all user queries and access", COLORS['purple']),
            ("🔒 Password Hashing", "Bcrypt hashing for secure password storage", COLORS['success']),
            ("🚫 Department Filtering", "Automatic filtering based on user department", COLORS['orange']),
        ]
        
        y_pos = 1.8
        for icon_title, desc, color in security_items:
            # Feature box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(y_pos), Inches(7), Inches(0.85)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = COLORS['light']
            box.line.color.rgb = color
            box.line.width = Pt(3)
            
            # Title
            title_box = slide.shapes.add_textbox(Inches(2), Inches(y_pos + 0.15), Inches(3), Inches(0.3))
            title_frame = title_box.text_frame
            p = title_frame.paragraphs[0]
            p.text = icon_title
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = color
            
            # Description
            desc_box = slide.shapes.add_textbox(Inches(2), Inches(y_pos + 0.45), Inches(6), Inches(0.3))
            desc_frame = desc_box.text_frame
            desc_frame.word_wrap = True
            p = desc_frame.paragraphs[0]
            p.text = desc
            p.font.size = Pt(12)
            p.font.color.rgb = COLORS['text']
            
            y_pos += 1
    
    def add_use_cases_slide():
        """Slide 11: Use Cases"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLORS['light']
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "USE CASES"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary']
        p.alignment = PP_ALIGN.CENTER
        
        # Use cases in grid
        use_cases = [
            ("Finance Queries", "Access financial reports\nQuarterly statements\nBudget information", COLORS['success']),
            ("HR Information", "Employee policies\nPayroll queries\nBenefits information", COLORS['secondary']),
            ("Marketing Data", "Campaign analytics\nMarket research\nPerformance reports", COLORS['orange']),
            ("Technical Docs", "API documentation\nArchitecture guides\nEngineering specs", COLORS['primary']),
        ]
        
        positions = [(1, 1.8), (5.5, 1.8), (1, 4.3), (5.5, 4.3)]
        
        for idx, (title, desc, color) in enumerate(use_cases):
            x, y = positions[idx]
            
            # Box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(3.5), Inches(2)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = color
            box.line.fill.background()
            
            # Title
            title_box = slide.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.3), Inches(2.9), Inches(0.5))
            title_frame = title_box.text_frame
            p = title_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(20)
            p.font.bold = True
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
            
            # Description
            desc_box = slide.shapes.add_textbox(Inches(x + 0.3), Inches(y + 0.9), Inches(2.9), Inches(0.9))
            desc_frame = desc_box.text_frame
            desc_frame.word_wrap = True
            p = desc_frame.paragraphs[0]
            p.text = desc
            p.font.size = Pt(13)
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
    
    def add_deployment_slide():
        """Slide 12: Deployment Architecture"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "DEPLOYMENT ARCHITECTURE"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['purple']
        p.alignment = PP_ALIGN.CENTER
        
        # Components
        components = [
            ("FastAPI Backend", "RESTful API server\nPort 8000", 2, 2, COLORS['primary']),
            ("Streamlit UI", "Web interface\nPort 8501", 5.5, 2, COLORS['secondary']),
            ("ChromaDB", "Vector database\nPersistent storage", 2, 4, COLORS['success']),
            ("OpenRouter API", "LLM provider\nMistral 7B", 5.5, 4, COLORS['orange']),
        ]
        
        for name, desc, x, y, color in components:
            # Component box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(2.5), Inches(1.5)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = color
            box.line.fill.background()
            
            # Name
            name_box = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.3), Inches(2.1), Inches(0.4))
            name_frame = name_box.text_frame
            p = name_frame.paragraphs[0]
            p.text = name
            p.font.size = Pt(18)
            p.font.bold = True
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
            
            # Description
            desc_box = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.8), Inches(2.1), Inches(0.5))
            desc_frame = desc_box.text_frame
            desc_frame.word_wrap = True
            p = desc_frame.paragraphs[0]
            p.text = desc
            p.font.size = Pt(12)
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
    
    def add_benefits_slide():
        """Slide 13: Key Benefits"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLORS['light']
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "KEY BENEFITS"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary']
        p.alignment = PP_ALIGN.CENTER
        
        # Benefits
        benefits = [
            ("⚡", "Faster Decision Making", "Quick access to relevant information across departments"),
            ("🔒", "Enhanced Security", "Granular access control prevents data leaks"),
            ("💰", "Cost Effective", "Reduces time spent searching for information"),
            ("📈", "Improved Productivity", "Employees find answers instantly without manual search"),
            ("🎯", "Accurate Responses", "AI-powered semantic understanding with source citations"),
            ("🔄", "Easy Scalability", "Add new documents and departments effortlessly"),
        ]
        
        y_pos = 1.8
        for icon, title, desc in benefits:
            # Benefit row
            # Icon
            icon_box = slide.shapes.add_textbox(Inches(1.5), Inches(y_pos), Inches(0.6), Inches(0.6))
            icon_frame = icon_box.text_frame
            icon_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = icon_frame.paragraphs[0]
            p.text = icon
            p.font.size = Pt(28)
            p.alignment = PP_ALIGN.CENTER
            
            # Title
            title_box = slide.shapes.add_textbox(Inches(2.3), Inches(y_pos + 0.05), Inches(2.5), Inches(0.3))
            title_frame = title_box.text_frame
            p = title_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = COLORS['primary']
            
            # Description
            desc_box = slide.shapes.add_textbox(Inches(2.3), Inches(y_pos + 0.35), Inches(6), Inches(0.3))
            desc_frame = desc_box.text_frame
            desc_frame.word_wrap = True
            p = desc_frame.paragraphs[0]
            p.text = desc
            p.font.size = Pt(12)
            p.font.color.rgb = COLORS['text']
            
            y_pos += 0.8
    
    def add_future_enhancements_slide():
        """Slide 14: Future Enhancements"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(248, 250, 252)
        bg.line.fill.background()
        
        # Title
        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(0.8))
        title_frame = title_box.text_frame
        p = title_frame.paragraphs[0]
        p.text = "FUTURE ENHANCEMENTS"
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = COLORS['purple']
        p.alignment = PP_ALIGN.CENTER
        
        # Enhancements
        enhancements = [
            ("Multi-language Support", "Support for multiple languages in queries and documents", COLORS['primary']),
            ("Voice Integration", "Voice-based query input and audio responses", COLORS['secondary']),
            ("Advanced Analytics", "Query analytics and usage patterns dashboard", COLORS['success']),
            ("Document Versioning", "Track document changes and maintain version history", COLORS['orange']),
            ("Mobile Application", "Native mobile apps for iOS and Android", COLORS['purple']),
            ("Integration APIs", "Connect with Slack, Teams, and other tools", COLORS['primary']),
        ]
        
        y_pos = 1.8
        for title, desc, color in enhancements:
            # Enhancement box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(y_pos), Inches(7), Inches(0.75)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = COLORS['light']
            box.line.color.rgb = color
            box.line.width = Pt(2)
            
            # Title
            title_box = slide.shapes.add_textbox(Inches(2), Inches(y_pos + 0.15), Inches(3), Inches(0.25))
            title_frame = title_box.text_frame
            p = title_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = color
            
            # Description
            desc_box = slide.shapes.add_textbox(Inches(2), Inches(y_pos + 0.42), Inches(6), Inches(0.25))
            desc_frame = desc_box.text_frame
            desc_frame.word_wrap = True
            p = desc_frame.paragraphs[0]
            p.text = desc
            p.font.size = Pt(11)
            p.font.color.rgb = COLORS['text']
            
            y_pos += 0.9
    
    def add_thank_you_slide():
        """Slide 15: Thank You / Closing"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLORS['dark']
        bg.line.fill.background()
        
        # Decorative elements
        accent1 = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(0.5), Inches(1.5), Inches(1.5)
        )
        accent1.fill.solid()
        accent1.fill.fore_color.rgb = COLORS['accent']
        accent1.line.fill.background()
        accent1.rotation = 30
        
        accent2 = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8), Inches(5.5), Inches(1.2), Inches(1.2)
        )
        accent2.fill.solid()
        accent2.fill.fore_color.rgb = COLORS['secondary']
        accent2.line.fill.background()
        accent2.rotation = 15
        
        accent3 = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(6), Inches(1), Inches(1)
        )
        accent3.fill.solid()
        accent3.fill.fore_color.rgb = COLORS['purple']
        accent3.line.fill.background()
        accent3.rotation = 45
        
        # Main message
        msg_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(2))
        msg_frame = msg_box.text_frame
        msg_frame.word_wrap = True
        
        p = msg_frame.paragraphs[0]
        p.text = "THANK YOU"
        p.font.size = Pt(52)
        p.font.bold = True
        p.font.color.rgb = COLORS['light']
        p.alignment = PP_ALIGN.CENTER
        
        p = msg_frame.add_paragraph()
        p.text = "\nEnterprise-Ready AI Solution"
        p.font.size = Pt(24)
        p.font.color.rgb = COLORS['accent']
        p.alignment = PP_ALIGN.CENTER
        
        # Footer
        footer_box = slide.shapes.add_textbox(Inches(1), Inches(5.2), Inches(8), Inches(1.2))
        footer_frame = footer_box.text_frame
        
        p = footer_frame.paragraphs[0]
        p.text = "THYNK UNLIMITED"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = COLORS['accent']
        p.alignment = PP_ALIGN.CENTER
        
        p = footer_frame.add_paragraph()
        p.text = "WE LEARN FOR THE FUTURE"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['light']
        p.alignment = PP_ALIGN.CENTER
        
        p = footer_frame.add_paragraph()
        p.text = "\nRole-Based Access Chatbot • Secure • Intelligent • Scalable"
        p.font.size = Pt(12)
        p.font.color.rgb = COLORS['light']
        p.alignment = PP_ALIGN.CENTER
    
    # Generate all slides
    print("Creating presentation slides...")
    add_title_slide()
    add_problem_solution_slide()
    add_key_features_slide()
    add_architecture_slide()
    add_tech_stack_slide()
    add_rbac_slide()
    add_performance_slide()
    add_rag_pipeline_slide()
    add_vector_database_slide()
    add_security_features_slide()
    add_use_cases_slide()
    add_deployment_slide()
    add_benefits_slide()
    add_future_enhancements_slide()
    add_thank_you_slide()
    
    # Save presentation
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"Role_Based_Chatbot_Presentation_{timestamp}.pptx"
    prs.save(output_file)
    print(f"\n✅ Presentation created successfully: {output_file}")
    print(f"📊 Total slides: {len(prs.slides)}")
    print("\n🎨 Canva-Style Presentation with 15 Slides:")
    print("=" * 55)
    print("1.  Title Slide - THYNK UNLIMITED Branding")
    print("2.  Problem & Solution - Side-by-side comparison")
    print("3.  Key Features - 4 highlighted capabilities")
    print("4.  System Architecture - Visual flow diagram")
    print("5.  Technology Stack - Categorized by function")
    print("6.  Role-Based Access Control - Department permissions")
    print("7.  Performance Metrics - Key performance indicators")
    print("8.  RAG Pipeline Workflow - 6-step process")
    print("9.  Vector Database - ChromaDB details")
    print("10. Security Features - 5 security layers")
    print("11. Use Cases - Real-world applications")
    print("12. Deployment Architecture - System components")
    print("13. Key Benefits - Business value propositions")
    print("14. Future Enhancements - Roadmap")
    print("15. Thank You - Closing slide")
    print("=" * 55)
    print("\n🎯 Design: Tech Vibrant Trendy (Canva-inspired)")
    print("🎨 Colors: Purple, Pink, Cyan, Orange theme")
    print("✨ Style: Bold typography, rounded shapes, vibrant accents")
    
    return output_file

if __name__ == "__main__":
    create_presentation()
