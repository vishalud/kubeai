from src.nlp_core import get_intent, generate_response
from src.k8s_client import execute_command, KubeconfigError, CommandExecutionError

def main():
    print("Welcome to KubeAI CLI!")
    print("Type your query, or 'exit' to quit.")
    while True:
        try:
            user_input = input("kubeai> ").strip()
            if user_input.lower() in ("exit", "quit"):  # Exit commands
                print("Goodbye!")
                break
            if not user_input:
                continue
            try:
                intent = get_intent(user_input)
                print(f"Recognized intent: {intent.intent}")
                print(f"Entities: {intent.entities}")
            except Exception as e:
                print(f"[NLP Error] Could not recognize intent: {e}")
                continue
            try:
                data = execute_command(intent)
            except KubeconfigError as e:
                print(f"[Kubeconfig Error] {e}")
                continue
            except CommandExecutionError as e:
                print(f"[Command Error] {e}")
                continue
            except Exception as e:
                print(f"[Command Error] Unexpected error: {e}")
                continue
            try:
                response = generate_response(data)
                print("\n--- Response ---")
                print(response)
                print("---------------\n")
            except Exception as e:
                print(f"[Response Error] Could not generate response: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting KubeAI CLI.")
            break

if __name__ == "__main__":
    main() 