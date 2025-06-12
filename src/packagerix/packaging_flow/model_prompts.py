"""All model prompts for packagerix.

This module contains all functions decorated with @ask_model that interact with the AI model.
"""

from magentic import StreamedStr
from packagerix.ui.conversation import ask_model, ask_model_enum
from packagerix.errors import NixError, NixErrorKind, NixBuildErrorDiff


@ask_model("""@model You are software packaging expert who can build any project using the Nix programming language.

Your task is to read the contents of the project's GitHub page and fill out all of the sections in the code template that are marked with ... .
Do not make any other modifications or additions. Do not modify the included lib.fakeHash.

This is the code template you have to fill out:
```nix
{code_template}
```   

Here is the information form the project's GitHub page:
```text
{project_page}
```

And some relevant metadata of the latest release:
```
{release_data}
```

Note: Your reply should contain exactly one code block with the updated Nix code.
Note: Even though the provided themplate uses the mkDerivation function, this is not the appropriate way to package software for most software ecosystems (outside of C/C++).
      Make sure you base your code on an appropriate function provdied by nixpkgs instead.

"""
)
def set_up_project(code_template: str, project_page: str, release_data: dict = None) -> StreamedStr:
    """Initial setup of a Nix package from a GitHub project."""
    ...


@ask_model("""@model You are software packaging expert who can build any project using the Nix programming language.

Read the contents of the project's GitHub page and summarize it.
Include information like
    1. The build tool which should be invoked to build the project.
    2. A list of build tools and project dependencies.
    3. Other information which might be necessary for buiding the project.
    
    Do not include information which is irrelevant for building the project.
Here is the information form the project's GitHub page:

```text
{project_page}
```

{release_data}
""")
def summarize_github(project_page: str, release_data: dict = None) -> StreamedStr:
    """Summarize a GitHub project page for packaging purposes."""
    ...


@ask_model("""@model You are software packaging expert who can build any project using the Nix programming language.

Please fix the following error in the following Nix code.      

```nix
{code}
```

Error:
```
{error}
```
           
Note: Your reply should contain exactly one code block with the updated Nix code.
Note: If you need to introduce a new hash, use lib.fakeHash as a placeholder, and automated process will replace this with the actual hash.
""")
def fix_build_error(code: str, error: str) -> StreamedStr:
    """Fix a build error in Nix code."""
    ...


@ask_model_enum("""@model You are software packaging expert who can build any project using the Nix programming language.

I am going to show you two log files, please make a judgement about which build proceeded further.

Initial build:
```nix
{initial_error}
```

Attempted improvement:
```
{attempted_improvement}
```

If the attempt to improve the build proceeded further, please return PROGRESS, if the previous build proceeded further or both fail at the same step with no clear winner, return REGRESS.
""")
def evaluate_progress(initial_error: str, attempted_improvement: str) -> NixBuildErrorDiff:
    ...

@ask_model("""@model You are software packaging expert who can build any project using the Nix programming language.

Please fix the following hash mismatch error in the following Nix code by replacing the relevant intance of lib.fakeHash wiith the actual value from the error message.      

```nix
{code}
```

Error:
```
{error}
```
           
Note: Your reply should contain exactly one code block with the updated Nix code.
""")
def fix_hash_mismatch(code: str, error: str) -> StreamedStr:
    ...
