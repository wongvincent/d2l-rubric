import requests, json, pprint, os, shutil, argparse

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--url', dest='base_url', action='store',
                    help='specify the QA site url to get data from. For example https://qa123g.bspc.com')

    parser.add_argument('--pwd', dest='daily_pwd', action='store',
                    help='specify the password for today')

    parser.add_argument('--copy_files', dest='copy_files', action='store_true', default = False,
                    help='specify True to automatically copy generated files into the demo and test folders')
    
    return parser.parse_args()

args = get_args()
#the url and password will have to be updated based on 
#the latest available QA site and quad password
base_url = args.base_url
pwd = args.daily_pwd

support_user_name = 'd2lsupport'
rubrics_course_id = '131646'
#defined the rubrics we want to use by id and 'identifier'
rubric_ids = ['197','198','199','203']
rubric_titles = ['default-rubric','custom-points','text-only','multiple-groups']

#create local base paths for each rubric
base_paths = ['data/rubrics/organizations/%s'%title for title in rubric_titles]
#where the data will get written to
demo_data_path = os.path.join(os.getcwd(),'..','..','demo','data')
test_data_path = os.path.join(os.getcwd(),'..','components','data')

class Role():
    def __init__(self,user_name,password):
        self.user_name = user_name
        self.pwd = password

class apiRequests():
    def __init__(self,baseUrl,role):
        self.baseUrl = baseUrl
        self.api_session = requests.Session()
        #authenticate
        response = self.api_session.post('%s/d2l/lp/auth/login/login.d2l'%base_url,headers= {'content-type': 'application/x-www-form-urlencoded'},
        data = {'userName':role.user_name, 'password':role.pwd})
        response = self.api_session.get('%s/d2l/lp/auth/login/ProcessLoginActions.d2l'%base_url)

    def issueGetRequest(self,requestString,query={}):
        url = '%s/%s'%(self.baseUrl,requestString)

        if query:
            response = self.api_session.get(url,json=query)
        else:
            response = self.api_session.get(url)
        return response

def get_endpoint(rubricId):
    return 'd2l/api/hm/rubrics/organizations/%s/%s'%(rubrics_course_id,rubricId)

role = Role(support_user_name,pwd)
my_api_requests = apiRequests(base_url,role)

def get_rubric(rubric_href):
    response = my_api_requests.issueGetRequest(rubric_href)
    if not response.status_code==200:
        print ("Something went wrong. Couldn't find this rubric: %s"%rubric_href)
    default_rubric_response = response.json()
    return default_rubric_response

def replace_links(links,base_path):
    new_links = []
    for link in links:
        split_href = link['href'].split(rubrics_course_id)
        my_href = '%s%s.json'%(base_path,split_href[1])
        link['href'] = my_href
        new_links.append(link)
    return new_links

def replace_all_links_in_json(json_data,base_path):
    def replace_links_callback(input):
        if type(input) is dict:
            for k,v in input.items():
                if k == 'links':
                    new_links = replace_links(v,base_path)
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

def get_all_links_from_json(full_json):
    links_list = []
    def is_links_callback(input):
        if type(input) is dict:
            for k,v in input.items():
                if k == 'links':
                    links_list.append(v)
        return input
    traverse_object(full_json,callback = is_links_callback)
    return links_list

def create_link_path(link,rubric_id):
    link_path = os.getcwd()
    original_path = os.getcwd()
    relative_href = link['href'].split(rubric_id)[1]
    rel_paths = relative_href.split('/')
    for p in rel_paths[1:]:
        if not p == rel_paths[-1]:
            if not os.path.exists(p):
                os.mkdir(p)
            os.chdir(p)
            link_path = os.path.join(link_path,p)
    os.chdir(original_path)
    return os.path.join(link_path,rel_paths[-1])

def write_json_file(json_file_path,new_response):
    with open(json_file_path,'w') as f:
        json.dump(new_response,f,indent=4)

def create_files(original_json,rubric_id,base_path):
    all_links = get_all_links_from_json(original_json)
    for links in all_links:
        for link in links:
            if 'up' in link['rel']:
                continue    
            link_path = create_link_path(link,rubric_id)
            json_file_path = link_path
            if not os.path.exists(json_file_path):
                relative_href_no_dot_json = link['href'].split(rubric_id)[1][:-5]
                rubric_api_path = '%s%s'%(get_endpoint(rubric_id),relative_href_no_dot_json)
                new_response = get_rubric(rubric_api_path)
                new_response = replace_all_links_in_json(new_response,base_path)
                write_json_file(json_file_path,new_response)
                create_files(new_response,rubric_id,base_path)

first_dir = os.getcwd()
for base_path,rubric_id in zip(base_paths,rubric_ids):
    #make sure old data is removed first
    file_save_location = os.path.join(os.getcwd(),base_path)
    if os.path.exists(file_save_location):
        shutil.rmtree(file_save_location)
    os.makedirs(file_save_location)
    os.chdir(file_save_location)

    #write original starting point
    rub_href = get_endpoint(rubric_id)
    initial_rubric_response = get_rubric(rub_href)
    initial_rubric_response['links'] = replace_links(initial_rubric_response['links'],base_path)
    write_json_file('%s.json'%rubric_id,initial_rubric_response)

    #write groups to file
    rub_groups_href = '%s/groups'%get_endpoint(rubric_id)
    rub_groups_response = get_rubric(rub_groups_href)
    rub_groups_response = replace_all_links_in_json(rub_groups_response,base_path)

    if not os.path.exists(rubric_id):
        os.mkdir(rubric_id)
    os.chdir(rubric_id)
    
    write_json_file('groups.json',rub_groups_response)

    #create all remaining files
    create_files(rub_groups_response,rubric_id,base_path)
    os.chdir(first_dir)


if args.copy_files:
    #move the files to demo/data
    shutil.rmtree(demo_data_path)
    shutil.copytree('data',demo_data_path)

    #move the files to test/component/data
    shutil.rmtree(test_data_path)
    shutil.move('data',test_data_path)

