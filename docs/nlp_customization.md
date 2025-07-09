# Advanced Extensibility: NLP Customization Guide

> This guide is for contributors who want to extend or tune kubeai's NLP/LLM layer—adding new intents, entities, or advanced conversational features using Google Gemini and prompt engineering.

---

## 1. Adding New Intents and Entities
- **Update the Gemini Prompt:**
  - In `nlp_core.py`, locate the prompt template sent to Gemini for intent recognition.
  - Add new few-shot examples for your intent, using the exact intent name and entity structure you want Gemini to return.
  - Example:
    ```
    User: Show me all nodes
    Intent: get_node_status
    Entities: []
    ```
- **Define Entities:**
  - If your new intent requires new entity types (e.g., `role`, `label`), add them to the prompt examples and update the `EntityModel` if needed.

## 2. Tuning Prompt Strictness and Flexibility
- **Strict Intent Matching:**
  - Use explicit instructions in the prompt: "Only use the following intent names: ..."
  - Add negative examples to discourage unwanted outputs.
- **Flexible Recognition:**
  - Add more varied phrasings to the few-shot examples.
  - Allow for synonyms or alternate entity names, and handle mapping in your code.

## 3. Handling Ambiguous or Multi-Turn Queries
- **Conversation State:**
  - Use the `ConversationState` model to track previous queries, intents, and entities.
  - Pass conversation history to Gemini in the prompt to provide context for follow-up questions.
- **Prompt Engineering:**
  - Instruct Gemini to "use previous context if the current query is ambiguous."
  - Example:
    ```
    User: What about their CPU usage?
    (Previous context: nodes listed above)
    Intent: get_node_cpu_usage
    Entities: [ ... ]
    ```

## 4. Custom Summarization for New Models
- **Update Response Generation:**
  - In `nlp_core.py`, adjust the prompt for the summarization step to include new model fields or custom formatting.
  - For complex resources, provide Gemini with a table or structured JSON for better summaries.
- **Special Cases:**
  - If a resource needs a unique summary style, add conditional logic to format the prompt or post-process Gemini's output.

## 5. Testing and Validation Best Practices
- **Unit Tests:**
  - Mock Gemini responses for new intents/entities and verify correct parsing into models.
- **Prompt Validation:**
  - Test with a variety of user queries, including edge cases and ambiguous phrasings.
- **Manual Review:**
  - Run the CLI and try new/modified queries to ensure Gemini returns the expected structure and summaries.
- **Regression Testing:**
  - Ensure changes to the prompt or NLP logic do not break existing intents or entity extraction.

---

**Tip:** Keep prompt examples up to date as you add new features. Regularly review Gemini's outputs for accuracy and consistency. 