from nicegui import ui
from PIL import Image
from colorthief import ColorThief
import io
import base64

PORT = 8081  # or any other port number you prefer

def extract_colors(image_bytes):
    """Extracts dominant colors from an image."""
    try:
        color_thief = ColorThief(image_bytes)
        palette = color_thief.get_palette(color_count=5)
        hex_colors = ['#%02x%02x%02x' % color for color in palette]
        return hex_colors
    except Exception as e:
        print(f"Error extracting colors: {e}")
        return []

def copy_to_clipboard(color):
    """Copies the color code to clipboard and shows a confirmation."""
    try:
        ui.notify(f'Copied {color} to clipboard!', position='top', type='positive')
        return ui.run_javascript(f'navigator.clipboard.writeText("{color}")')
    except Exception as e:
        ui.notify(f'Failed to copy: {str(e)}', type='negative')

def on_upload(file):
    """Handles image upload and extracts colors."""
    if file:
        try:
            # Read the file content
            content = file.content.read()
            
            # Show image preview
            with image_container:
                image_container.clear()
                # Convert bytes to base64 for image display
                image_data = base64.b64encode(content).decode()
                ui.image(f'data:image/jpeg;base64,{image_data}').classes('w-full rounded-lg mt-4')
            
            # Create new BytesIO for color extraction
            img_bytes = io.BytesIO(content)
            colors = extract_colors(img_bytes)

            with result_container:
                result_container.clear()
                ui.label("Picked palettes").classes("text-md font-semibold text-[#1995AD]")
                
                with ui.row().classes("mt-2"):
                    for hex_color in colors:
                        with ui.card().style(
                            f"""
                            background-color: {hex_color}; 
                            width: 50px; 
                            height: 50px; 
                            border-radius: 8px;
                            cursor: pointer;
                            transition: transform 0.2s ease;
                            """
                        ).classes('color-card').on('click', lambda c=hex_color: copy_to_clipboard(c)):
                            ui.tooltip(f'Click to copy {hex_color}')
        except Exception as e:
            ui.notify(f'Error processing image: {str(e)}', type='negative')

# 🎨 UI Setup with Paper Style
ui.html('''
<style>
body { 
    background-color: #1995AD !important; 
    background-image: url("data:image/png;base64,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");
    font-family: 'Comic Sans MS', cursive, sans-serif;
}
.nicegui-content { background: transparent !important; }
button { 
    background-color: #A1D6E2 !important; 
    color: #1995AD !important; 
    border: 2px solid #F1F1F2 !important;
    padding: 10px 20px;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    transition: all 0.3s ease;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
button:hover { 
    background-color: #F1F1F2 !important;
    color: #1995AD !important;
    transform: translateY(-2px);
}
.card {
    background: rgba(161, 214, 226, 0.9) !important;
    border: 2px solid #F1F1F2;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(25, 149, 173, 0.2);
}

/* Modified upload container styles */
.upload-container {
    background: rgba(161, 214, 226, 0.9) !important;
    border: 2px dashed #F1F1F2 !important;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.upload-container:hover {
    background: rgba(241, 241, 242, 0.95) !important;
    border-color: #1995AD !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(25, 149, 173, 0.2);
}

/* Hide default uploader styling */
.q-uploader {
    width: 100% !important;
    height: 100% !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    opacity: 0 !important;
    cursor: pointer !important;
}

.q-uploader__header,
.q-uploader__list {
    display: none !important;
}

.q-uploader__input {
    cursor: pointer !important;
    height: 100% !important;
    width: 100% !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
}

/* Style the upload icon and text */
.upload-icon {
    font-size: 48px;
    color: #1995AD;
    margin-bottom: 10px;
    pointer-events: none;
    z-index: 0;
}

.upload-text {
    color: #1995AD;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-size: 1.1em;
    pointer-events: none;
    z-index: 0;
}

/* Add hover effect for color cards */
.color-card:hover {
    transform: scale(1.1) !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
''')

with ui.column().classes('w-full items-center gap-4 p-8'):
    ui.label('Color Palette Extractor').classes('text-3xl font-bold text-[#F1F1F2]')
    ui.label('Extract beautiful palettes from your photos').classes('text-lg text-[#F1F1F2] mb-4')
    
    with ui.card().classes('w-full max-w-2xl p-6'):
        with ui.column().classes('w-full items-center gap-4'):
            # Upload container
            with ui.element('div').classes('upload-container w-full'):
                with ui.element('label').classes('w-full h-full cursor-pointer flex flex-col items-center justify-center'):
                    ui.icon('upload').classes('upload-icon')
                    ui.label('Upload Image').classes('text-xl font-bold text-[#1995AD] mb-2')
                    ui.label('Drag and drop your image here or click to browse').classes('upload-text mb-4')
                    ui.upload(
                        on_upload=on_upload,
                        auto_upload=True,
                    ).props('flat bordered hide-upload-btn accept="image/*"').classes('absolute inset-0 opacity-0')
            
            # Image preview container
            image_container = ui.column().classes('w-full items-center')
            # Color results container
            result_container = ui.column().classes('w-full items-center gap-4')

try:
    ui.run(port=PORT)
except OSError as e:
    if "Address already in use" in str(e):
        print(f"Port {PORT} is in use. Trying automatic port selection...")
        try:
            ui.run(port=0)  # This will automatically find an available port
        except Exception as e2:
            print(f"Failed to start server: {e2}")
    else:
        print(f"Error starting server: {e}")