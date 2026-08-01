# Development Setup

## Required tools

RiftPilot currently standardizes the local environment on:

- Git
- Visual Studio Code
- Node.js 24.x
- npm
- Python 3.13.x

Exact reference versions are stored in:

- `.nvmrc`
- `.python-version`

Patch updates within the selected major and minor lines are acceptable unless a dependency requires an exact version.

## Windows installation

Open PowerShell and confirm whether the tools already exist:

```powershell
git --version
code --version
node --version
npm --version
python --version
py -3.13 --version
```

Install missing tools with Windows Package Manager:

```powershell
winget install --id Git.Git -e
winget install --id Microsoft.VisualStudioCode -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Python.Python.3.13 -e
```

Close and reopen the terminal after an installation so PATH changes are loaded.

Python 3.13 is valid when either of these commands finds it:

```powershell
python --version
py -3.13 --version
```

## VS Code extensions

Open the repository in VS Code:

```powershell
code .
```

When VS Code shows the workspace recommendations, install them.

The recommended extensions provide:

- Python language support.
- Python type analysis.
- Python linting and formatting.
- TypeScript and JavaScript linting.
- General formatting.
- EditorConfig support.

Extensions are recommendations, not application dependencies.

## Environment validation

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-environment.ps1
```

The script must finish with:

```text
Environment is ready.
```

## File standards

- Repository text files use UTF-8.
- Repository text files use LF line endings.
- Windows command scripts use CRLF line endings.
- TypeScript-related files use two spaces.
- Python files use four spaces.
- Files must end with one newline.
- Trailing whitespace is removed, except where meaningful in Markdown.

These rules are enforced by `.editorconfig`, `.gitattributes`, and the workspace settings.
