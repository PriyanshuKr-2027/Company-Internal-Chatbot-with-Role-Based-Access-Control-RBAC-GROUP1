"""
Generate PowerPoint Presentation for Role-Based Access Chatbot
Matching the Canva template style: Tech Vibrant Trendy
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
    
    # Color scheme - Vibrant Tech Theme
    COLORS = {
        'primary': RGBColor(67, 97, 238),      # Vibrant Blue
        'secondary': RGBColor(255, 71, 133),   # Pink/Magenta
        'accent': RGBColor(58, 255, 217),      # Cyan
        'dark': RGBColor(26, 32, 44),          # Dark background
        'light': RGBColor(255, 255, 255),      # White
        'text': RGBColor(45, 55, 72),          # Dark gray text
        'success': RGBColor(72, 187, 120),     # Green
        'warning': RGBColor(237, 137, 54),     # Orange
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
        p.text = "AI-POWERED SEMANTIC SEARCH"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = COLORS['accent']
        p.alignment = PP_ALIGN.CENTER
        
        p = subtitle_frame.add_paragraph()
        p.text = "WITH RAG PIPELINE & RBAC SECURITY"
        p.font.size = Pt(24)
        p.font.color.rgb = COLORS['light']
        p.alignment = PP_ALIGN.CENTER
        
        # Tagline
        tag_box = slide.shapes.add_textbox(Inches(1), Inches(5.5), Inches(8), Inches(0.8))
        tag_frame = tag_box.text_frame
        p = tag_frame.paragraphs[0]
        p.text = "ENTERPRISE-GRADE SECURITY • INTELLIGENT RESPONSES"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['accent']
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
            ("⚡", "High Performance", "~20ms search, ~2.5s total response", COLORS['warning']),
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
        """Slide 4: System Architecture"""
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
        
        # Flow diagram
        components = [
            ("User Query", 1, COLORS['primary']),
            ("Authentication", 2.2, COLORS['secondary']),
            ("RBAC Filter", 3.4, COLORS['warning']),
            ("Semantic Search", 4.6, COLORS['success']),
            ("LLM Generation", 5.8, COLORS['primary']),
            ("Response", 7, COLORS['accent']),
        ]
        
        y_center = 3.5
        for comp_name, x_pos, color in components:
            # Component box
            box = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, 
                Inches(x_pos), Inches(y_center - 0.4), 
                Inches(1), Inches(0.8)
            )
            box.fill.solid()
            box.fill.fore_color.rgb = color
            box.line.fill.background()
            
            # Component text
            text_box = slide.shapes.add_textbox(
                Inches(x_pos), Inches(y_center - 0.4), 
                Inches(1), Inches(0.8)
            )
            text_frame = text_box.text_frame
            text_frame.word_wrap = True
            text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            
            p = text_frame.paragraphs[0]
            p.text = comp_name
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = COLORS['light']
            p.alignment = PP_ALIGN.CENTER
        
        # Sub-components
        subtext = [
            ("ChromaDB\n135 docs", 4.6, 5.3),
            ("Mistral 7B\nOpenRouter", 5.8, 5.3),
        ]
        
        for text, x, y in subtext:
            text_box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(1), Inches(0.6))
            text_frame = text_box.text_frame
            text_frame.word_wrap = True
            
            p = text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9)
            p.font.color.rgb = COLORS['text']
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
            ("Security", ["RBAC Middleware", "JWT Tokens", "Department-based Filtering"], COLORS['warning']),
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
            ("Marketing", "• Marketing Reports\n• Campaign Analytics\n• Market Research", COLORS['warning']),
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
            ("135", "Indexed Documents", COLORS['warning']),
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
            ("3. RBAC Filtering", "Results filtered based on user's department permissions", COLORS['warning']),
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
    
    def add_thank_you_slide():
        """Slide 9: Thank You / Closing"""
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
        footer_box = slide.shapes.add_textbox(Inches(1), Inches(5.5), Inches(8), Inches(1))
        footer_frame = footer_box.text_frame
        p = footer_frame.paragraphs[0]
        p.text = "Role-Based Access Chatbot with RAG Pipeline"
        p.font.size = Pt(16)
        p.font.color.rgb = COLORS['light']
        p.alignment = PP_ALIGN.CENTER
        
        p = footer_frame.add_paragraph()
        p.text = "Secure • Intelligent • Scalable"
        p.font.size = Pt(14)
        p.font.color.rgb = COLORS['accent']
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
    add_thank_you_slide()
    
    # Save presentation
    output_file = "Role_Based_Chatbot_Presentation.pptx"
    prs.save(output_file)
    print(f"\n✅ Presentation created successfully: {output_file}")
    print(f"📊 Total slides: {len(prs.slides)}")
    print("\nSlides included:")
    print("1. Title Slide")
    print("2. Problem & Solution")
    print("3. Key Features")
    print("4. System Architecture")
    print("5. Technology Stack")
    print("6. Role-Based Access Control")
    print("7. Performance Metrics")
    print("8. RAG Pipeline Workflow")
    print("9. Thank You")
    
    return output_file

if __name__ == "__main__":
    create_presentation()
