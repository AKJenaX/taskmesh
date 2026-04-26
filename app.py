import gradio as gr
import json

def schedule_tasks(tasks_json, algorithm):
    try:
        tasks = json.loads(tasks_json)
    except Exception as e:
        return f"Error parsing JSON: {e}"
        
    payload = {
        "tasks": tasks,
        "algorithm": algorithm.lower()
    }
    
    from backend.routes import get_scheduler_func, validate_and_normalize
    
    algo = payload["algorithm"]
    func = get_scheduler_func(algo)
    if func is None:
        return "Algorithm not found."
        
    try:
        result = func(payload["tasks"])
        validated = validate_and_normalize(result)
        
        if validated is None:
            return "Failed to validate schedule."
            
        return json.dumps(validated, indent=2)
    except Exception as e:
        return f"Error executing scheduler: {e}"

# Gradio Interface
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# TaskMesh")
    gr.Markdown("An RL-optimized task scheduling engine trained with PyTorch Policy Gradients over our custom `OpenEnv` wrapper.")
    
    with gr.Row():
        with gr.Column():
            tasks_input = gr.Code(
                label="Tasks Queue (JSON)",
                language="json",
                value='[\n  {"id": 1, "priority": 5, "duration": 15},\n  {"id": 2, "priority": 1, "duration": 45},\n  {"id": 3, "priority": 3, "duration": 30}\n]'
            )
            algorithm_dropdown = gr.Dropdown(
                choices=["Baseline", "RL"],
                value="RL",
                label="Algorithm"
            )
            submit_btn = gr.Button("Run Scheduler", variant="primary")
            
        with gr.Column():
            output_json = gr.Code(label="Schedule Output", language="json")
            
    submit_btn.click(
        fn=schedule_tasks,
        inputs=[tasks_input, algorithm_dropdown],
        outputs=output_json
    )

if __name__ == "__main__":
    demo.launch()