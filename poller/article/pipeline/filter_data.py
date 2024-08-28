from utils.string import unmark, strip_tags, clean_text

def clean_data(article):
    data = article['attributes']
    compiled_content = {}

    # Content Information Header
    compiled_content['id'] = article['id']
    compiled_content['createdAt'] = data['createdAt']
    compiled_content['title'] = clean_text(data['title'])
    thCategories = [category['attributes']['title'] for category in data['categories']['data']]
    # compiled_content['categoriesTH'] = thCategories
    enCategories = [category['attributes']['slug'] for category in data['categories']['data']]
    # compiled_content['categoriesEN'] = enCategories
    compiled_content['tags'] = [tag['attributes']['name'] for tag in data['tags']['data']]
    # make tag include category
    compiled_content['tags'] = thCategories + enCategories + compiled_content['tags']
    compiled_content['highlights'] = [clean_text(highlight['content']) for highlight in data["highlights"]]

    # Content Body
    compiled_content['contents'] = []
    for content in data['contents']:
        content_data = {}
        if content['__component'] == 'article.richtext':
            # content_data['type'] = 'richtext'
            content_data = clean_text(unmark(content['content']))
        elif content['__component'] == 'article.quote':
            quote = {}
            quote['content'] = clean_text(content['content'])
            if content['title'] :
                quote['title'] = clean_text(content['title'])
            if content['by']:
                quote['by'] = content['by']
            content_data['quote'] = quote
        elif content['__component'] == 'article.html':
            # content_data['type'] = 'html'
            content_data = clean_text(strip_tags(content['content']))
        compiled_content['contents'].append(content_data)

    # References
    if data["references"]:
        compiled_content['references'] = []
        for reference in data["references"]:
            compiled_content['references'].append({
                'name': clean_text(reference['name']),
                'link': reference['link']
            })

    # Credits
    compiled_content['credits'] = []
    for credit in data['credits']:
        if credit['credit']['data'] and credit['credit']['data']['attributes']['internalName']:
            compiled_content['credits'].append(credit['credit']['data']['attributes']['internalName'])

    return compiled_content