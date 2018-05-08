def replace_links(course_id,links,title):
    new_links = []
    for link in links:
        split_href = link['href'].split('dev.brightspace.com')
        if course_id in split_href[1]:
            my_href = 'data/rubrics%s.json'%split_href[1].replace(course_id,title)
        else:
            my_href = 'data/rubrics%s.json'%split_href[1]
        link['href'] = my_href
        new_links.append(link)
    return new_links

def replace_all_links_in_json(course_id,json_data,title):
    def replace_links_callback(input):
        if type(input) is dict:
            for k,v in input.items():
                if k == 'links':
                    new_links = replace_links(course_id,v,title)
                    input[k] = new_links
        return input
    return traverse_object(json_data,callback = replace_links_callback)

def traverse_object(given_object,callback = None):
    if type(given_object) is dict:
        value = {k:traverse_object(v,callback) for k,v in given_object.items()}
    elif type(given_object) is list:
        value =  [traverse_object(element,callback) for element in given_object]
    else:
        value =  given_object

    if callback is None:
        return value
    else:
        return callback(value)