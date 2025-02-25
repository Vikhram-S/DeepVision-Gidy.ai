import gradio as gr
from deepventure_backend import DeepVentureBackend

# hugging face api token is confidential so iam not updated in github (Replace with actual token)
HF_API_TOKEN = "huggingface_token"
backend = DeepVentureBackend(HF_API_TOKEN)

# Function to evaluate and simulate the idea
def evaluate_and_simulate(title, description, session_state):
    score = backend.evaluate_idea(description)
    simulation = backend.run_simulation(title, description, score)
    mentor = backend.match_mentor(description)
    microlearning = backend.get_microlearning("business")
    
    # Format as a list of two-element lists for Chatbot
    user_message = f"**Title:** {title}\n**Description:** {description}"
    assistant_response = f"### Evaluation Score: {score}/100\n\n" \
                        f"#### Simulation Results:\n" \
                        f"- **Success Rate:** {simulation['success_rate']}%\n" \
                        f"- **Market Potential:** {simulation['market_potential']}%\n" \
                        f"- **Risk Factor:** {simulation['risk_factor']}%\n\n" \
                        f"**Recommended Mentor:** {mentor}\n\n" \
                        f"**Suggested Learning Modules:** {', '.join(microlearning)}"
    
    # Use list of lists instead of list of tuples
    result_message = [[user_message, assistant_response]]
    
    # Debug print to verify format
    print("Result message:", result_message)
    
    # Update session state with history
    session_state["history"].append({"title": title, "description": description, "result": result_message})
    return result_message, session_state

# Function to clear all inputs and reset state
def clear_inputs():
    return "", "", {"history": []}, [], "No evaluations yet. Submit an idea to see your history!"

# Initialize Blocks with a custom theme
demo = gr.Blocks(
    theme=gr.themes.Default(
        primary_hue="blue",
        secondary_hue="green",
        neutral_hue="gray",
        radius_size="lg",
        font=["Roboto", "sans-serif"]
    ),
    title="DeepVenture Hub - Idea Evaluator"
)

with demo:
    # Session state to track evaluation history
    state = gr.State(value={"history": []})
    
    gr.Markdown("# DeepVenture Hub - Idea Evaluator", elem_classes="header")
    gr.Markdown("Submit your business idea and get AI-powered insights!", elem_classes="subheader")
    
    # Tabbed interface
    with gr.Tabs():
        # Input Tab
        with gr.TabItem("Submit Idea"):
            with gr.Row():
                with gr.Column(scale=2):
                    title = gr.Textbox(
                        label="Idea Title",
                        placeholder="Enter your idea's name",
                        lines=1,
                        show_copy_button=True
                    )
                    description = gr.Textbox(
                        label="Idea Description",
                        placeholder="Describe your business idea in detail",
                        lines=5,
                        show_copy_button=True
                    )
                    submit = gr.Button("Evaluate Idea", variant="primary", size="lg")
                with gr.Column(scale=1):
                    gr.Markdown("### Tips\n- Be specific in your description\n- Use keywords for better mentor matching")

        # Results Tab
        with gr.TabItem("Results"):
            chatbot = gr.Chatbot(
                label="Evaluation Results",
                height=400,
                bubble_full_width=False,
                avatar_images=(None, "https://cdn-icons-png.flaticon.com/512/4303/4303316.png")  # AI avatar
            )
        
        # History Tab
        with gr.TabItem("History"):
            with gr.Accordion("Past Evaluations", open=False):
                history_text = gr.Markdown("No evaluations yet. Submit an idea to see your history!")

    # Event handling for submit
    def update_history(session_state):
        if not session_state["history"]:
            return "No evaluations yet. Submit an idea to see your history!"
        history_md = ""
        for i, entry in enumerate(session_state["history"], 1):
            history_md += f"#### Evaluation {i}: {entry['title']}\n" \
                         f"**Description:** {entry['description']}\n\n" \
                         f"{entry['result'][0][1]}\n\n---\n"  # Use the assistant response from the list
        return history_md

    submit.click(
        fn=evaluate_and_simulate,
        inputs=[title, description, state],
        outputs=[chatbot, state]
    ).then(
        fn=update_history,
        inputs=[state],
        outputs=[history_text]
    )

    # Clear button with pure Python reset
    with gr.Row():
        clear = gr.Button("Clear Inputs", variant="secondary")
        clear.click(
            fn=clear_inputs,
            inputs=None,
            outputs=[title, description, state, chatbot, history_text]
        )

if __name__ == "__main__":
    demo.launch()
