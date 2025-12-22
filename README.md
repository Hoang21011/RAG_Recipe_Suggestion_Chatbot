# 🍽️ RAG Recipe Suggestion Chatbot

A **Recipe Recommendation Chatbot** built using **Retrieval-Augmented Generation (RAG)**.
The system retrieves relevant recipes from a vector database and generates natural language responses using an LLM, enabling users to get personalized recipe suggestions based on ingredients, preferences, or questions.

---

## 🚀 Features

* 🔍 **Semantic Recipe Retrieval** using vector embeddings
* 🧠 **Retrieval-Augmented Generation (RAG)** pipeline
* 🥗 Ingredient-based recipe suggestions
* 📄 CSV-based recipe dataset
* 💬 Conversational chatbot interface
* 👤 User memory & history support
* 🔐 Basic authentication and user database

---

## 📂 Project Structure

```text
.
├── app.py                     # Main application entry point
├── RAG_O.py                   # High-level RAG orchestration logic
├── buiding_vector_database.py # Script to build vector database
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys, configs)
├── .gitignore
├── .gitattributes
│
├── backend/
│   ├── auth.py                # Authentication logic
│   ├── user_database.py       # User database handling
│   └── __init__.py
│
├── rag/
│   ├── embedder.py            # Text embedding logic
│   ├── retriever.py           # Vector search & retrieval
│   ├── generator.py           # LLM-based response generation
│   ├── memory.py              # Conversation memory handling
│   ├── test.py                # RAG testing script
│   └── __init__.py
│
├── data/
│   ├── cleaned_recipes.csv    # Cleaned recipe dataset
│   ├── shortcut.csv           # Additional mapping / shortcut data
│   └── rag_users.db           # SQLite database for users
│
├── __pycache__/
└── .DS_Store
```

---

## 📂 Retrieval-Augmented Generation (RAG) Pipeline Structure

                            +-------------------+
                            |       User        |
                            |  (Chat Interface) |
                            +---------+---------+
                                      |
                                      v
                            +-------------------+
                            |   app.py / API    |
                            |  (User Request)  |
                            +---------+---------+
                                      |
                                      v
                            +-------------------+
                            |  Query Embedder   |
                            |  rag/embedder.py  |
                            +---------+---------+
                                      |
                                      v
                            +-------------------------------+
                            |   Vector Database (FAISS)     |
                            |  - Recipe Embeddings          |
                            |  - built by                   |
                            |    buiding_vector_database.py |
                            +---------+---------------------+
                                      |
                                      v
                            +-------------------+
                            |   Retriever       |
                            |  rag/retriever.py|
                            |  (Top-k Recipes) |
                            +---------+---------+
                                      |
                                      v
                            +-------------------------------+
                            |     Prompt Construction       |
                            |  - Retrieved Recipes          |
                            |  - User Query                 |
                            |  - Conversation Memory        |
                            +---------+---------------------+
                                      |
                                      v
                            +-------------------+
                            |    Generator      |
                            |  rag/generator.py|
                            |  (LLM Response)  |
                            +---------+---------+
                                      |
                                      v
                            +-------------------+
                            |     Memory        |
                            |   rag/memory.py  |
                            | (Chat History)   |
                            +---------+---------+
                                      |
                                      v
                            +-------------------+
                            |   Final Response  |
                            |  Recipe Suggestion|
                            +-------------------+

---

## 🧠 System Architecture (RAG Pipeline)

1. **User Query**
2. **Embedding**

   * Query converted into vector representation
3. **Retriever**

   * Finds top-k relevant recipes from vector database
4. **Generator**

   * LLM generates response using retrieved context
5. **Memory**

   * Conversation history stored for continuity

---

## 📊 Dataset

* **`cleaned_recipes.csv`**

  * Contains recipe names, ingredients, instructions, and metadata
* Data is preprocessed and embedded for efficient semantic search

---

## 🛠️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set environment variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## 🧱 Build Vector Database

Before running the chatbot, build the vector database:

```bash
python buiding_vector_database.py
```

This will:

* Load recipe data
* Generate embeddings
* Store them for retrieval

---

## ▶️ Run the Application

```bash
python app.py
```

Or if using Streamlit / other UI:

```bash
streamlit run app.py
```

---

## 💬 Example Queries

* *"Suggest a chicken recipe with garlic and onions"*
* *"What can I cook with eggs and tomatoes?"*
* *"Give me a healthy vegetarian dinner idea"*

---

## 🧪 Testing

```bash
python rag/test.py
```

---

## 🧩 Technologies Used

* **Python**
* **LLMs (OpenAI / compatible models)**
* **Vector Search (FAISS / similar)**
* **Pandas & NumPy**
* **SQLite**
* **dotenv**

---

## 🔮 Future Improvements

* Add nutrition-based filtering
* Improve user preference learning
* Support multilingual recipes
* Web UI with chat history
* Recommendation ranking & feedback loop

---

## 👨‍💻 Author

**Nghĩa Hoàng**
Recipe Recommendation System using RAG

