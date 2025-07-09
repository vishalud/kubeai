# Hackathon 2025 Ideas:  Features for kubeai

> **Note:** For maximum impact and inclusivity, raise a PR with your ideas and be as verbose and detailed as possible. Clear, thorough docs enable remote and asynchronous team members to participate fully, understand your design and decisions, and contribute effectively—no matter their location or time zone.

These are advanced, high-impact features for the kubeai project. Each is broken down into actionable subtasks, making them ideal for hackathon teams to tackle collaboratively.

---

## 1. Contextual Awareness for Follow-up Questions
*Enable kubeai to remember conversational context and handle multi-turn, follow-up queries.*

**Main Task:**
Implement conversational context management to allow for simple follow-up questions. The system will remember previously mentioned entities within a session.

**Subtasks:**
- **Define conversation state data structure**
  - Design and implement a data structure (e.g., ConversationState class) to hold session context, including previous queries, recognized intents, and entities.
- **Integrate state management into main application loop**
  - Modify app.py to create and maintain a ConversationState instance throughout the session. Ensure the state is updated after each user interaction.
- **Modify NLP core to use conversation state in prompts**
  - Update get_intent and related NLP functions to accept and utilize conversation state/history when constructing prompts for Gemini. Adjust prompt templates to leverage prior context for ambiguous queries.
- **Update conversation state after each interaction**
  - After each successful user interaction, update the ConversationState object with the latest query, intent, and entities. Ensure state is persisted for the session.
- **Testing and validation of multi-turn conversations**
  - Add tests and/or manual test scripts to verify that the system correctly maintains and uses context across multiple turns. Test ambiguous follow-up queries and ensure correct inference from prior state.
- **Documentation and usage examples for context management**
  - Document the conversation state management approach and provide example usage in code comments or docs. Optionally, add a script or notebook demonstrating multi-turn conversation handling.

**Example:**
```
User: Show me all pods in the kube-system namespace
kubeai: There are 5 pods in kube-system: coredns-1, coredns-2, metrics-server, ...

User: What is the status of the first one?
kubeai: Pod 'coredns-1' is Running, restarts: 0

User: And its image?
kubeai: Pod 'coredns-1' uses image: k8s.gcr.io/coredns:1.8.0
```

---

## 2. First Write Operation with User Confirmation
*Add safe, user-confirmed write operations (e.g., restarting a deployment) to kubeai.*

**Main Task:**
Introduce a controlled write operation (e.g., 'restart deployment') and implement a safety feature that requires explicit user confirmation before execution.

**Subtasks:**
- **Add 'restart_deployment' intent to NLP model and command mapping**
  - Extend the IntentModel, NLP logic, and command mapping to support a new 'restart_deployment' intent. Update prompt templates and model validation as needed.
- **Implement Kubernetes command execution for deployment restart**
  - Add a handler function in k8s_client.py to perform a rollout restart of a deployment using the Kubernetes API. Ensure it is only called for the correct intent and with required parameters.
- **Add confirmation prompt logic to CLI**
  - In app.py, implement logic to prompt the user for confirmation before executing any write operation (e.g., deployment restart). Only proceed if the user explicitly confirms.
- **Test confirmation and rejection paths for write operations**
  - Add tests or manual test scripts to verify that the confirmation prompt works as intended. Ensure the operation is only performed on explicit confirmation and is safely skipped otherwise.
- **Document the write operation and safety features**
  - Update documentation to describe the new write operation, the confirmation prompt, and any safety mechanisms. Provide usage examples and warnings as appropriate.
- **Add error handling for write operations**
  - Implement robust error handling for the restart_deployment operation, including API errors, permission issues, and invalid parameters. Ensure clear user feedback on failure.

**Example:**
```
User: Restart the deployment 'webapp' in namespace 'production'
kubeai: Are you sure you want to restart deployment 'webapp' in namespace 'production'? [y/N]

User: y
kubeai: Deployment 'webapp' has been restarted successfully.

User: n
kubeai: Operation cancelled. Deployment 'webapp' was not restarted.
```

---

*Pick a feature, form a team, and help take kubeai to the next level!* 