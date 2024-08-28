import os
import json
from utils.string import write_dict_to_file
from poller.article.pipeline.data_gatherer import generate_query_string, get_articles
from poller.article.pipeline.filter_data import clean_data


def get_SPB_articles():
    print("Getting articles from SPB")
    all_articles = []
    pageSize = 2
    for page in range(1, 2):  # Loop through pages 1 to 20
        query_string = generate_query_string(page, pageSize)
        print(f"Getting articles from SPB page {page}")

        result = get_articles(query_string)

        for article in result['data']:
            # data Processing
            content = clean_data(article)
            all_articles.append(content)
            # Text Processing
            file_path = f"tmp/source/SPB-A-{article['id']}.txt"
            if os.path.exists(file_path):
                print(f"File SPB-A-{article['id']} already exists")
                continue
            with open(file_path, "w") as f:
                # f.write(compiled_content)
                write_dict_to_file(content, f)

    # write json to source_json/export.json
    with open("tmp/source_json/export.json", "w") as f:
        # f.write(str(all_articles))
        json.dump(all_articles, f)
    return all_articles
