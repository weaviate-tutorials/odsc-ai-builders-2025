# Database Design Patterns

# Step 1: Preparation & Setup

Clone this repo and navigate into it. This will be your working directory for the workshop.

```shell
git clone git@github.com:weaviate-tutorials/odsc-ai-builders-2025.git
cd odsc-ai-builders-2025
```

## 1.1 Install Python & set up a virtual environment

> [!NOTE]
> If you have a preferred setup (e.g. Conda/Poetry), please feel free to use that. Otherwise, we recommend following these steps.

Install `Python 3.9` or higher (e.g. from the [Python website](https://python.org/), or `pyenv`).

Then, create & activate a virtual environment:

```shell
python -m venv .venv  # Or use `python3` if `python` is Python 2
source .venv/bin/activate
```

Check that you are using the correct Python:

```shell
which python
```

This should point to the Python binary in the `.venv` directory.

Install the required Python packages:

```shell
pip install -r requirements.txt
```

> [!TIP]
> If you have network connectivity issues, the installation may time out part way through. If this happens, just try running the command again. It will re-used cached data, so you will make further

> [!TIP]
> If you open new terminal or shell window, you will need to activate the virtual environment again. Navigate to the project directory and run `source .venv/bin/activate`.

## 1.2 Choose your embedding & LLM provider

The workshop is set up for two different embeddings & LLM providers options ([Cohere](#121-option-1-cohere) or [Ollama](#122-option-2-ollama)).

### 1.2.1 Option 1: Cohere

> [!NOTE]
> - Recommended if you want to use an API-based solution
>     - We will use pre-embedded data for this workshop, so the expense will be for queries only & minimal
>     - Still, please set a budget limit in your account for extra safety

No additional setup is required for using Cohere.

You can use your own Cohere API key in the notebook.

However, if you don't have one - you can use a shared key, as shown in the notebooks.

### 1.2.2 Option 2: Ollama

> [!NOTE]
> - Recommended if you have 16+ GB of RAM and a modern computer
> - We will use pre-embedded data for this workshop, so Ollama will be used for vectorizing queries & LLM use
> - No account or API key required

Download & install Ollama from the [Ollama website](https://ollama.com/). Make sure Ollama is running, by:

```shell
ollama -v
```

You should see something like:
```shell
❯ ollama -v
ollama version is 0.5.7
```

Then, run the following command:

```shell
> ollama pull nomic-embed-text && ollama pull gemma2:2b
```

This will download the required models for the workshop.

## 1.3 Install Docker

Install Docker Desktop: https://www.docker.com/products/docker-desktop/

Start up a Weaviate cluster with the following command:

```shell
docker compose up -d
```

This will start a single-node Weaviate cluster.

Check an Weaviate endpoint:

```shell
curl http://localhost:8080/v1/meta | jq
```

You should see a response - this means Weaviate is running!

You should be able to see the memory usage of the Weaviate pod by running:

```shell
go tool pprof -top http://localhost:6060/debug/pprof/heap
```

# Step 3: Work with Weaviate

## 3.1 Work through the notebooks

See: `1_single_collection.ipynb` and `2_multi_tenancy.ipynb` notebooks and work through them during the workshop.

> [!TIP]
> Hint: The `finished_notebooks` branch contains pre-populated versions of the notebooks!

## 3.2 Run the demo Streamlit app

We have a Streamlit app that will help you to visualise basic cluster statistics, and to make use of the data. (Remember to navigate to the project directory and activate the virtual environment.) Run it with:

```shell
streamlit run app.py
```

This will throw an error, but that's OK. We'll fix that along the way.

## Finish up

### Docker

When finished with the workshop, you can stop the cluster with:

```shell
docker compose -f docker-compose.yml down
```
