from transformers import AutoTokenizer, AutoModelForCausalLM
import torch #type:ignore

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Set padding token as eos token (required for DialoGPT)
tokenizer.pad_token = tokenizer.eos_token

chat_history_ids = None

def generate_response(user_input, chat_round, chat_history_ids=None):
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Print shapes for debugging
    print(f"New input shape: {new_input_ids.shape}")
    if chat_history_ids is not None:
        print(f"Chat history shape: {chat_history_ids.shape}")

    # Handle chat history
    if chat_round > 0 and chat_history_ids is not None:
        try:
            chat_history_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
        except RuntimeError as e:
            print(f"Error during concatenation: {e}")
            chat_history_ids = new_input_ids
    else:
        chat_history_ids = new_input_ids

    # Create attention mask
    attention_mask = torch.ones_like(chat_history_ids)

    # Generate response
    output_ids = model.generate(
        chat_history_ids,
        attention_mask=attention_mask,
        do_sample=True,
        max_length=1000,
        top_k=50,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode the generated response
    bot_response = tokenizer.decode(output_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
    return bot_response, output_ids

# Example usage
def chater(text, chid):
    global chat_history_ids
    chat_history_ids = chid
    user_input = text
    if user_input.lower() == 'exit':
        return "Chat ended."
    
    # Increment chat_round if necessary
    chat_round = 1 if chat_history_ids is None else chat_history_ids.size(1)

    response, chat_history_ids = generate_response(user_input, chat_round, chat_history_ids)
    return response, chat_history_ids
