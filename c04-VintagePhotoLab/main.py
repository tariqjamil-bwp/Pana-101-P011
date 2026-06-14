# ============================================================================
# DeOldify WebApp — VintagePhotoLab
# ----------------------------------------------------------------------------
# Author : Tariq Jamil
# Version: 1.0.0
# Date   : 2025-06-14
# License: MIT
# ============================================================================

import threading

import gradio as gr
from model import PhotoProcessor, FILTER_CHOICES

processor = PhotoProcessor()


def process_image(image, filter_name, resolution, fr_weight):
    if image is None:
        return None
    result = processor.process(image, flt=filter_name, res=resolution, fr_weight=fr_weight)
    return result


css_inline = """
    footer { display: none !important; }
    .app-title { text-align: center; font-size: 2rem; margin-bottom: 0.5rem; }
    .app-subtitle { text-align: center; color: #666; margin-bottom: 1.5rem; }
"""

with gr.Blocks(title="VintagePhotoLab", css=css_inline, theme=gr.themes.Soft()) as demo:
    gr.HTML(
        '<div class="app-title">🎨 VintagePhotoLab</div>'
        '<div class="app-subtitle">Colorize old photos &amp; apply artistic filters</div>'
    )

    with gr.Row(equal_height=True):
        with gr.Column(scale=1):
            input_image = gr.Image(
                type="pil",
                label="Upload Photo",
                height=400,
            )
        with gr.Column(scale=1):
            output_image = gr.Image(
                type="pil",
                label="Result",
                height=400,
            )

    with gr.Row():
        filter_dropdown = gr.Dropdown(
            choices=FILTER_CHOICES,
            value="Colorize (DeOldify)",
            label="Filter",
            scale=2,
        )
        resolution_slider = gr.Slider(
            minimum=256,
            maximum=2048,
            value=1024,
            step=64,
            label="Max Resolution (px)",
            scale=1,
        )

    with gr.Row():
        fr_weight_slider = gr.Slider(
            minimum=0.0,
            maximum=1.0,
            value=0.5,
            step=0.05,
            label="Face Restoration Weight",
            scale=1,
        )

    with gr.Row():
        process_btn = gr.Button("Process", variant="primary", size="lg", scale=1)
        clear_btn = gr.Button("Clear", variant="secondary", size="lg", scale=1)

    process_btn.click(
        fn=process_image,
        inputs=[input_image, filter_dropdown, resolution_slider, fr_weight_slider],
        outputs=output_image,
        api_name="process",
    )
    clear_btn.click(
        fn=lambda: (None, None),
        outputs=[input_image, output_image],
    )

    gr.Examples(
        examples=[],
        inputs=[input_image],
        label="Drag & drop a photo above to get started",
    )

    gr.HTML(
        '<div style="text-align:center;padding:1rem;color:#999;font-size:0.85rem;">'
        "Built with Gradio + OpenCV + PyTorch</div>"
    )


demo.queue()
threading.Thread(target=processor.init, daemon=True).start()


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000)
