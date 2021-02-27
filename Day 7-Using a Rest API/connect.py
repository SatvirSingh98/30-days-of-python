from pprint import pprint

import pandas as pd
import requests

api_key_v3 = '8060352fcbb9342bcaf0f238eb099cdd'
api_key_v4 = ('eyJhbGciOiJIUzI1NiJ9.'
              'eyJhdWQiOiI4MDYwMzUyZmNiYjkzNDJiY2FmMGYyMzhlYjA5OWNkZ'
              'CIsInN1YiI6IjVmNDFmYTgwNmEzNDQ4MDAzM2IxOTc2ZCIsInNjb3B'
              'lcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.'
              'C2wkvJwKWNviiiFuVdtrxEab3tQGLu9JL_YWhRuvVNQ')


# To find results using movie_id
movie_id = 500
api_version = 3
api_base_url = f"https://api.themoviedb.org/{api_version}"
endpoint_path = f"/movie/{movie_id}"

# for version 3 api
endpoint_v3 = f"{api_base_url}{endpoint_path}?api_key={api_key_v3}"
r = requests.get(endpoint_v3)

# for version 4 api
endpoint_v4 = f"{api_base_url}{endpoint_path}"
headers = {'Authorization': f"Bearer {api_key_v4}",
           'Content-Type': 'application/json;charset=utf-8'}
# r = requests.get(endpoint_v4, headers=headers)

# print(r.status_code)
# print(r.text)


# To find results using movie_name
search_query = 'the matrix'
api_base_url = f"https://api.themoviedb.org/{api_version}"
endpoint_path = "/search/movie/"

endpoint_v3 = f"{api_base_url}{endpoint_path}?api_key={api_key_v3}\
&query={search_query}"

r = requests.get(endpoint_v3)
# pprint(r.json())  # To properly view data

if r.status_code in range(200, 300):
    data = r.json()
    # print(data.keys())
    # print(type(data['results']))

    results = data['results']
    # print(results[0].keys())

    movie_ids = set()
    for result in results:
        _id = result['id']
        movie_ids.add(_id)
    print(list(movie_ids))


output = 'movies.csv'
movie_data = []
for movie_id_ in movie_ids:
    api_version = 3
    api_base_url = f"https://api.themoviedb.org/{api_version}"
    endpoint_path = f"/movie/{movie_id_}"

    endpoint_v3 = f"{api_base_url}{endpoint_path}?api_key={api_key_v3}"
    r = requests.get(endpoint_v3)

    if r.status_code in range(200, 300):
        data = r.json()
        # pprint(r.json())
        movie_data.append(data)

df = pd.DataFrame(movie_data)
print(df.head())
df.to_csv(output, index=False)
