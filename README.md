# AIForTesters

This repository includes a Flask web app, test automation with SeleniumBase, and machine learning notebooks.

## Run With GitHub Codespaces

The repository includes a dev container in `.devcontainer/`.

1. In GitHub, open the repository.
2. Select **Code** > **Codespaces** > **Create codespace on main**.
3. Wait for container build and post-create setup to complete.

The setup will automatically:

- Install Python dependencies from `requirements.txt`
- Install a Jupyter kernel named `Python (AIForTesters)`
- Forward app and notebook ports

## Start The Flask App

```bash
python wine.py
```

Open the forwarded port `5000` when prompted.

## Run UI Tests

Run tests in headless mode (recommended in Codespaces):

```bash
pytest tests --headless
```

## Use Jupyter Notebooks

Open any `.ipynb` file in VS Code.

Select kernel:

- `Python (AIForTesters)`

If you want to run Jupyter in the terminal:

```bash
jupyter lab --ip 0.0.0.0 --port 8888 --no-browser
```