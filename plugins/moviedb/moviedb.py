import requests
import os
from config import tmdb_api_key, images_dir
from utils import gen_img_with_text


base_url = 'https://api.themoviedb.org/3'
img_base_url = 'https://image.tmdb.org/t/p/original'


def search_movie_proper(query):
    url = base_url + '/search/movie'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': 'zh',
        'page': 1,
        'query': query
    }
    resp = requests.get(url, params=params).json()
    if 'results' in resp.keys():
        if resp['results']:
            movie = resp['results'][0]
            try:
                movie_info = '影名: {}\n原名: {}\n评分: {}分\n简介:{}\n上映日期: {}'.format(
                    movie['title'],
                    movie['original_title'],
                    movie['vote_average'],
                    movie['overview'],
                    movie['release_date'],
                )

                # generate image with informations of a movie
                target_folder = f"{images_dir}/movies/{movie['id']}"
                movie_info_img_save_path = f"{target_folder}/{movie['title']}_info"
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                gen_imgs = gen_img_with_text( 
                    movie_info, 
                    'plugins/moviedb/fonts/wqy-microhei.ttc', 
                    movie_info_img_save_path,
                    bg_folder = 'plugins/moviedb/bg'
                )

                # retrive and save tvshow's poster
                movie_poster_save_path = f"{target_folder}{movie['poster_path']}"
                if not os.path.exists(movie_poster_save_path):
                    poster_data = requests.get(img_base_url + movie['poster_path']).content
                    with open(movie_poster_save_path, 'wb') as fp:
                        fp.write(poster_data)
                
                outcome = ''
                for gen_img in gen_imgs:
                    outcome = outcome + '[CQ:image,file={}]'.format(
                        gen_img.replace(f'{images_dir}/', '')
                    )
                outcome = '{}\n[CQ:image,file={}]'.format(
                    outcome,
                    f"movies/{movie['id']}{movie['poster_path']}"
                )
                
            except Exception as err:
                outcome = str(err)
        else:
            outcome = f'未找到与”{query}“相关的影片！'
    else:
        outcome = '查找出错啦！'
    
    return outcome

def search_movie_implicit(query, page):
    url = base_url + '/search/movie'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': 'zh',
        'page': page,
        'query': query
    }
    resp = requests.get(url, params=params).json()
    if 'results' in resp.keys():
        movies = resp['results']
        if movies:
            try:
                movies_info = []
                for movie in movies:
                    movie_info = '影名: {} 原名: {} 评分: {}分 id:{} 上映日期:{}'.format(
                        movie['title'],
                        movie['original_title'],
                        movie['vote_average'] if 'vote_average' in movie.keys() else '暂无',
                        movie['id'],
                        movie['release_date']
                    )
                    movies_info.append(movie_info)

                target_folder = f"{images_dir}/tmdb_movies"
                results_info_img_save_path = f"{target_folder}/outcome"
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                gen_imgs = gen_img_with_text(
                    '\n'.join(movies_info),
                    'plugins/moviedb/fonts/wqy-microhei.ttc',
                    results_info_img_save_path,
                    bg_folder = 'plugins/moviedb/bg'
                )

                outcome = ''
                for gen_img in gen_imgs:
                    outcome = outcome + '[CQ:image,file={}]'.format(
                        gen_img.replace(f'{images_dir}/', '')
                    )
                
            except Exception as err:
                outcome = str(err)
        else:
            outcome = f'未找到第{page}页与”{query}“相关的电影！'
    else:
        outcome = '查找出错啦！'

    return outcome

def search_tv_proper(query):
    url = base_url + '/search/tv'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': 'zh',
        'page': 1,
        'query': query
    }
    resp = requests.get(url, params=params).json()
    if 'results' in resp.keys():
        tvs = resp['results']
        if tvs:
            try:    
                tv = tvs[0]
                tv_info = '剧名: {}\n原名: {}\n评分: {}分 \n简介:{}\n上映日期:{}'.format(
                    tv['name'],
                    tv['original_name'],
                    tv['vote_average'] if 'vote_average' in tv.keys() else '暂无',
                    tv['overview'],
                    tv['first_air_date']
                )
                
                # generate image with informations of a tvshow
                target_folder = f"{images_dir}/tvs"
                results_info_img_save_path = f"{target_folder}/outcome"
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                gen_imgs = gen_img_with_text(
                    tv_info,
                    'plugins/moviedb/fonts/wqy-microhei.ttc',
                    results_info_img_save_path,
                    bg_folder = 'plugins/moviedb/bg'
                )

                # retrive and save tvshow's poster
                tv_poster_save_path = f"{target_folder}{tv['poster_path']}"
                if not os.path.exists(tv_poster_save_path):
                    poster_data = requests.get(img_base_url + tv['poster_path']).content
                    with open(tv_poster_save_path, 'wb') as fp:
                        fp.write(poster_data)
                
                outcome = ''
                for gen_img in gen_imgs:
                    outcome = outcome + '[CQ:image,file={}]'.format(
                        gen_img.replace(f'{images_dir}/', '')
                    )
                outcome = '{}\n[CQ:image,file={}]'.format(
                    outcome,
                    f"movies/{tv['id']}{tv['poster_path']}"
                )
                
            except Exception as err:
                outcome = str(err)
        else:
            outcome = f'未找到与”{query}“相关的电视剧！'
    else:
        outcome = '查找出错啦！'

    return outcome

def search_tv_implicit(query, page):
    url = base_url + '/search/tv'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': 'zh',
        'page': page,
        'query': query
    }
    resp = requests.get(url, params=params).json()
    if 'results' in resp.keys():
        tvs = resp['results']
        if tvs:
            try:
                tvs_info = []
                for tv in tvs:
                    tv_info = '剧名: {} 原名: {} 评分: {}分 id:{} 上映日期:{}'.format(
                        tv['name'],
                        tv['original_name'],
                        tv['vote_average'] if 'vote_average' in tv.keys() else '暂无',
                        tv['id'],
                        tv['first_air_date']
                    )
                    tvs_info.append(tv_info)

                target_folder = f"{images_dir}/tmdb_tvs"
                results_info_img_save_path = f"{target_folder}/outcome"
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                gen_imgs = gen_img_with_text(
                    '\n'.join(tvs_info),
                    'plugins/moviedb/fonts/wqy-microhei.ttc',
                    results_info_img_save_path,
                    bg_folder = 'plugins/moviedb/bg'
                )

                outcome = ''
                for gen_img in gen_imgs:
                    outcome = outcome + '[CQ:image,file={}]'.format(
                        gen_img.replace(f'{images_dir}/', '')
                    )
                
            except Exception as err:
                outcome = str(err)
        else:
            outcome = f'未找到第{page}页与”{query}“相关的电视剧！'
    else:
        outcome = '查找出错啦！'

    return outcome

def search_multi(query, page):
    url = base_url + '/search/multi'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': 'zh',
        'page': page,
        'query': query
    }
    resp = requests.get(url, params=params).json()
    if 'results' in resp.keys():
        results = resp['results']
        if results:
            try:
                results_info = []
                for result in results:
                    media_type_map = {
                        'movie': '电影',
                        'tv': '电视剧',
                        'person': '个人'
                    }
                    if 'release_date' in result.keys():
                        release_date = result['release_date']
                    elif 'first_air_date' in result.keys():
                        release_date =  result['first_air_date']
                    else:
                        release_date = '无'
                    result_info = '{} {} {}分 id:{} 上映日期:{}'.format(
                        result['title'] if result['media_type'] == 'movie' else result['name'],
                        media_type_map[result['media_type']],
                        result['vote_average'] if 'vote_average' in result.keys() else '暂无',
                        result['id'],
                        release_date
                    )
                    results_info.append(result_info)

                target_folder = f"{images_dir}/tmdb_multi"
                results_info_img_save_path = f"{target_folder}/outcome"
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                gen_imgs = gen_img_with_text(
                    '\n'.join(results_info),
                    'plugins/moviedb/fonts/wqy-microhei.ttc',
                    results_info_img_save_path,
                    bg_folder = 'plugins/moviedb/bg'
                )

                outcome = ''
                for gen_img in gen_imgs:
                    outcome = outcome + '[CQ:image,file={}]'.format(
                        gen_img.replace(f'{images_dir}/', '')
                    )
                
            except Exception as err:
                outcome = str(err)
        else:
            outcome = f'未找到第{page}页与”{query}“相关的电视剧或电影！'
    else:
        outcome = '查找出错啦！'

    return outcome


if __name__ == '__main__':
    pass