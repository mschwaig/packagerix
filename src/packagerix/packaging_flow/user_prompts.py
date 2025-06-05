"""All user prompts for packagerix.

This module contains all functions decorated with @ask_user that interact with the user.
"""

from packagerix.ui.conversation import ask_user, coordinator_error


@ask_user("""@user Welcome to Packagerix! 🚀

I'm your friendly Nix packaging assistant. I can help you:
• Package projects from GitHub
• Build derivations with mkDerivation
• Identify and resolve dependencies
• Iteratively fix build errors

To get started, please provide the GitHub URL of the project you'd like to package.

💡 Tip: Press Ctrl+L to toggle the log window and see application output.""")
def get_project_url(user_input: str) -> str:
    """Get and validate the project URL from user."""
    if not user_input.startswith("https://github.com/"):
        coordinator_error("URL must start with https://github.com/")
        return get_project_url()  # Ask again
    return user_input


def evaluate_build_progress(prev_error: str, new_error: str) -> str:
    """Get user evaluation of build progress."""
    from packagerix.ui.conversation import get_ui_adapter
    
    # Create the formatted prompt with actual error content
    prompt = f"""@user Please evaluate the build progress by comparing the errors:

Previous error:
{prev_error}

New error:
{new_error}

Please choose:
1. error not resolved - build fails earlier (REGRESS)
2. code failed to evaluate (EVAL_ERROR) 
3. error resolved - build fails later (PROGRESS)
4. hash mismatch - needs correct hash to be filled in (HASH_MISMATCH)

Enter your choice (1-4):"""
    
    # Get the UI adapter and ask for input
    adapter = get_ui_adapter()
    response = adapter.ask_user(prompt)
    
    # Validate the response
    try:
        choice = int(response.strip())
        if 1 <= choice <= 4:
            return str(choice)
        else:
            coordinator_error("Please enter a number between 1 and 4")
            return evaluate_build_progress(prev_error, new_error)  # Ask again
    except ValueError:
        coordinator_error("Please enter a valid number")
        return evaluate_build_progress(prev_error, new_error)  # Ask again