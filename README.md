<<<<<<< Test-Branch
# Insurance Policy Generation Chatbot

This is a full-stack application that uses a Retrieval-Augmented Generation (RAG) pipeline to generate insurance policies based on user queries. This project is built with a modern Python stack and is fully containerized for easy deployment.

## Technology Stack

-   **Backend:** FastAPI
-   **Frontend:** Streamlit
-   **RAG Pipeline:** Haystack
-   **Vector Store:** ChromaDB
-   **Containerization:** Docker & Docker Compose

## Getting Started

### Prerequisites

-   Docker and Docker Compose must be installed on your system.

### Installation & Running the Application

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <repository-name>
    ```

2.  **(Optional) Configure the LLM for Generation**

    This project can optionally use a self-hosted Large Language Model (e.g., Llama 3) for the final policy generation step. If you skip this, the application will only retrieve relevant documents from the knowledge base without generating a cohesive policy.

    -   Download a GGUF-compatible model file (e.g., from Hugging Face).
    -   Create a `.env` file in the project root directory.
    -   Add the following line to the `.env` file, replacing the example path with the actual path to your model file:
        ```env
        LLM_MODEL_PATH=/path/to/your/model.gguf
        ```

3.  **Build and Run the Application with Docker Compose**

    From the root directory of the project, run the following command. You may need to use `sudo` depending on your Docker installation.

    ```bash
    sudo docker compose up --build
    ```

    This command will:
    -   Build the Docker images for the frontend and backend services.
    -   Run an `indexer` service to create a vector database from the documents in the `/data` directory.
    -   Start the backend and frontend services once the indexing is complete.

4.  **Access the Application**
    -   **Frontend UI:** Open your browser and navigate to `http://localhost:8501`.
    -   **Backend API Docs:** The API is available at `http://localhost:8000`. You can access the OpenAPI (Swagger) documentation at `http://localhost:8000/docs`.

## Project Structure

```
.
├── backend/            # Contains the FastAPI application and Haystack pipelines
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── data/               # Sample documents for the knowledge base
│   ├── legal_clauses.txt
│   ├── policy_template.txt
│   └── underwriting_guidelines.txt
├── frontend/           # Contains the Streamlit UI application
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── docker-compose.yml  # Orchestrates all the services
```
=======

>>>>>>> main
