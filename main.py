import argparse
import os
import queue
import sys
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def generate_content(client: OpenAI, messages: list, tools: list = None):
    """Sends a chat completion request with tools to the API."""
    kwargs = {
        "model": "openrouter/free",
        "messages": messages,
    }
    if tools:
        kwargs["tools"] = tools

    return client.chat.completions.create(**kwargs)


def run_agent(user_prompt: str, verbose: bool, update_queue: queue.Queue):
    """Agent logic executed in a background thread to prevent blocking the UI."""
    try:
        load_dotenv()
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            update_queue.put(("error", "Error: OPENROUTER_API_KEY environment variable is missing."))
            return

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        max_iterations = 20

        for iteration in range(max_iterations):
            response = generate_content(client, messages, tools=available_functions)

            if verbose and response.usage:
                log_msg = f"\n--- Iteration {iteration + 1} ---\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}\n"
                update_queue.put(("log", log_msg))

            message = response.choices[0].message
            messages.append(message)

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    result_message = call_function(tool_call, verbose=verbose)

                    if not result_message.get("content"):
                        update_queue.put(("error", f"Error: Tool execution for '{tool_call.function.name}' returned empty content."))
                        return

                    if verbose:
                        update_queue.put(("log", f"Tool Call Output -> {result_message['content']}\n"))

                    messages.append(result_message)
            else:
                # Final response reached
                update_queue.put(("response", message.content))
                return

        update_queue.put(("error", f"Error: Agent reached maximum loop iterations ({max_iterations}) without reaching a final response."))

    except Exception as e:
        update_queue.put(("error", f"An unexpected error occurred: {str(e)}"))


class AgentApp:
    def __init__(self, root, verbose_default=False):
        self.root = root
        self.root.title("Bloogley")
        self.root.geometry("750x600")

        self.update_queue = queue.Queue()

        # Input Frame
        input_frame = ttk.Frame(root, padding="10")
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="User Prompt:").pack(anchor=tk.W)
        
        self.prompt_entry = ttk.Entry(input_frame, width=70)
        self.prompt_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.prompt_entry.bind("<Return>", lambda event: self.send_prompt())

        self.send_btn = ttk.Button(input_frame, text="Send", command=self.send_prompt)
        self.send_btn.pack(side=tk.RIGHT)

        # Options Frame
        options_frame = ttk.Frame(root, padding="10 0 10 0")
        options_frame.pack(fill=tk.X)

        self.verbose_var = tk.BooleanVar(value=verbose_default)
        self.verbose_check = ttk.Checkbutton(options_frame, text="Verbose output", variable=self.verbose_var)
        self.verbose_check.pack(anchor=tk.W)

        # Output Text Area
        output_frame = ttk.Frame(root, padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(output_frame, text="Output Console:").pack(anchor=tk.W)
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Periodic queue checker
        self.root.after(100, self.process_queue)

    def append_output(self, text: str):
        """Helper to append text to the scrolled output box."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def send_prompt(self):
        prompt = self.prompt_entry.get().strip()
        if not prompt:
            return

        self.append_output(f"\nUser: {prompt}\n" + "-" * 50)
        self.prompt_entry.delete(0, tk.END)
        self.send_btn.config(state=tk.DISABLED)

        # Run agent task in background thread
        thread = threading.Thread(
            target=run_agent,
            args=(prompt, self.verbose_var.get(), self.update_queue),
            daemon=True
        )
        thread.start()

    def process_queue(self):
        """Checks for new UI update messages from the background thread."""
        try:
            while True:
                msg_type, content = self.update_queue.get_nowait()
                if msg_type == "log":
                    self.append_output(f"[LOG] {content}")
                elif msg_type == "response":
                    self.append_output(f"\nAssistant:\n{content}\n")
                    self.send_btn.config(state=tk.NORMAL)
                elif msg_type == "error":
                    self.append_output(f"\n{content}\n")
                    self.send_btn.config(state=tk.NORMAL)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)


def main():
    parser = argparse.ArgumentParser(description="Chatbot Agent GUI")
    parser.add_argument("user_prompt", type=str, nargs="?", default="", help="Optional initial user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output by default")
    args = parser.parse_args()

    root = tk.Tk()
    app = AgentApp(root, verbose_default=args.verbose)

    # If a prompt was passed via CLI, auto-submit it
    if args.user_prompt:
        app.prompt_entry.insert(0, args.user_prompt)
        app.send_prompt()

    root.mainloop()


if __name__ == "__main__":
    main()
