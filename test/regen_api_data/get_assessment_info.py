import json,argparse

from api_requests import api_requests
from rewrite_json import *

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--url', dest='base_url', action='store',
                    help='specify the QA site url to get data from. For example https://qa123g.bspc.com')

    parser.add_argument('--pwd', dest='daily_pwd', action='store',
                    help='specify the password for today')
    
    return parser.parse_args()

args = get_args()
#login info
qa_site_url = args.base_url
user_name = 'demo_s'
pwd = args.daily_pwd
course_id = '131646'

#assessment info
assessment_ids = [203]
rubric_titles = ['multiple-groups']
assessment_hashes = ['''sYXIWuF0ETxFZ1zN1WinLjVTh5XzJgSaSfaMEXxBuJg/UnVicmljfERyb3Bib3h8NjI2''']

def get_endpoint_assessments(assessment_id,assessment_hash):
    return 'd2l/api/hm/assessments/assessment/%s/%s'%(assessment_id,assessment_hash)

def get_assessment(assesments_rel_href):
    response = my_api_handle.issueGetRequest(assesments_rel_href)
    if not response.status_code==200:
        print ("Something went wrong. Couldn't find this assessment: %s"%assesments_rel_href)
    default_rubric_response = response.json()
    return default_rubric_response

my_api_handle = api_requests(qa_site_url,user_name,pwd)

for assessment_id,assessment_hash,rubric_title in zip(assessment_ids,assessment_hashes,rubric_titles):
    assessment_json = get_assessment(get_endpoint_assessments(assessment_id,assessment_hash))

    with open('%s_assessment.json'%rubric_title,'w') as f:
        json.dump(replace_all_links_in_json(course_id,assessment_json,rubric_title),f,indent=4)