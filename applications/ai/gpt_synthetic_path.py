import ast

import openai
import pandas as pd
import tiktoken
from sklearn.metrics.pairwise import cosine_similarity


def count_tokens(text):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    return num_tokens


def add_emb(df):
    """
    用 OpenAI API 做 embedding.
    """
    openai.organization = "org-NfM9mwOPTEnzhQCiwAT50o0D"
    openai.api_key = "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"

    if 'embedding' in df.columns:
        return df

    embed_msgs = []
    for _, row in df.iterrows():
        context = row['content']
        context_emb = openai.Embedding.create(model="text-embedding-ada-002", input=context)
        embed_msgs.append(context_emb['data'][0]['embedding'])

    df = df.copy()
    df.loc[:, 'embedding'] = embed_msgs

    return df


def df_to_csv(df, file_name):
    """
    DataFrame 转 CSV.
    """
    df.to_csv(file_name, index=False, escapechar='\\')


def load_paper_emb(filename):
    """Crate a dataframe that includes embedding information"""
    paper_df_emb = pd.read_csv(filename)
    paper_df_emb['embedding'] = paper_df_emb['embedding'].apply(ast.literal_eval)
    paper_df_emb


# embedding，制作Synthesis_Embedding.csv
paper_df_emb = load_paper_emb("./data/doi_329Synthesis_Embedding.csv")  # embedding耗时 9min


## gpt-4.0 
def add_similarity(df, given_embedding):
    def calculate_similarity(embedding):
        if isinstance(embedding, str):
            embedding = [float(x) for x in embedding.strip('[]').split(',')]
        return cosine_similarity([embedding], [given_embedding])[0][0]

    df['similarity'] = df['embedding'].apply(calculate_similarity)
    return df


def top_similar_entries(df, x=3):
    sorted_df = df.sort_values(by="similarity", ascending=False)
    top_x_entries = sorted_df["content"].head(x).tolist()

    if x >= 2:
        for i, entry in enumerate(top_x_entries):
            separator = f"\n--- SECTION {i + 1} ---"
            top_x_entries[i] = separator + "\n" + entry

    joined_entries = "\n".join(top_x_entries)

    return joined_entries


def chatbot(question, past_user_messages=None, initial_context=None):
    if past_user_messages is None:
        past_user_messages = []

    past_user_messages.append(question)

    file_name = "./data/doi_329Synthesis_Embedding.csv"
    df_with_emb = pd.read_csv(file_name)

    if initial_context is None:
        first_question = past_user_messages[0]
        question_return = openai.Embedding.create(model="text-embedding-ada-002", input=first_question)
        question_emb = question_return['data'][0]['embedding']

        df_with_emb_sim = add_similarity(df_with_emb, question_emb)
        num_paper = 1
        top_n_synthesis_str = top_similar_entries(df_with_emb_sim, num_paper)

        initial_context = top_n_synthesis_str

    message_history = [
        {
            "role": "system",
            "content": "You are an expert in nanozyme research and have specifically addressed questions related to nanozyme synthesis conditions based on the paper you reviewed. "
                       "Answer the question in as much detail as possible using the context provided, paying special attention to the concentration and dosage of the solvent in your answer. "
                       "Context:" + initial_context
        },
    ]

    for user_question in past_user_messages:
        message_history.append({"role": "user", "content": user_question})

    response = openai.ChatCompletion.create(
        model='gpt-4-1106-preview',
        # model='gpt-4',
        temperature=0.8,
        max_tokens=2000,
        messages=message_history
    )

    answer = response.choices[0].message["content"]

    return answer, initial_context, past_user_messages


# first_question = "how to synthesize Pd@Pt NPS?"

openai.api_key = "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"
