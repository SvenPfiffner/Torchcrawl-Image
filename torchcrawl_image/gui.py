def run(dataset):
    # Get the working directory of the dataset
    start_ui(dataset)

def start_ui(dataset):
    try:
        import gradio as gr
    except ImportError:
        print("Gradio is required to use the UI. Please install it using 'pip install gradio'")
        return

    data = dataset.get_data()
    selected_idx = 0

    def show_label(evt: gr.SelectData):
        nonlocal selected_idx
        selected_idx = evt.index
        return data[evt.index].label

    def update_label(label: str):
        data[selected_idx].label = label
        dataset.data.save_to_xml(dataset.working_dir + "/data.xml")

    with gr.Blocks() as gui:
        gr.Markdown("Start typing below and then click **Run** to see the output.")
        with gr.Row():
            gallery = gr.Gallery(show_label=True, value=[d.path + d.filename for d in data])
            with gr.Column():
                label = gr.Textbox(label="Label", interactive = True)
                btn = gr.Button("Update Label", variant='primary')
        btn.click(fn=update_label, inputs=label, outputs=None)
        gallery.select(show_label, None, label)

    gui.launch()

if __name__ == "__main__":
    # TODO: Add terminal arguments for the working directory
    start_ui()