import requests
import os
from config import tmdb_api_key, images_dir
from utils import gen_img_with_text


base_url = 'https://api.themoviedb.org/3'
img_base_url = 'https://image.tmdb.org/t/p/original'


def search_movie_maybe(query, language):
    url = base_url + '/search/movie'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': language,
        'page': 1,
        'query': query
    }
    resp = requests.get(url, params=params).json()
    if 'results' in resp.keys():
        movie_list = resp['results']
        if movie_list:
            try:
                movie = max(movie_list, key=lambda x: x['popularity'])
                movie_id = movie['id']
                outcome = fetch_movie(movie_id, language)
                    
            except Exception as err:
                outcome = str(err)
        else:
            outcome = f'未找到与”{query}“相关的影片！'
    else:
        outcome = '查找出错啦！'
    
    return outcome

def fetch_movie(id, language):
    url = base_url + f'/movie/{id}?api_key={tmdb_api_key}&language={language}'
    resp = requests.get(url).json()
    movie_info = '片名: {}\n原产地片名: {}\n时长: {}h{}min\n评分: {}\n类型: {}\n简介: {}\n上映日期: {}\nimdb_id: {}\n预算: ${}\n票房: ${}'.format(
        resp.get('title'),
        resp.get('original_title'),
        resp.get('runtime', 0)//60, resp.get('runtime', 0)%60,
        resp.get('vote_average', '无'),
        ' '.join(genre.get('name', '') for genre in resp.get('genres')),
        resp.get('overview', '无'),
        resp.get('release_date'),
        resp.get('imdb_id'),
        resp.get('budget', 0),
        resp.get('revenue', 0)
    )
    poster_path = resp.get('poster_path')

    # generate image with informations of a movie
    target_folder = f"{images_dir}/movies/{id}"
    movie_info_img_save_path = f"{target_folder}/movie_info"
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    gen_imgs = gen_img_with_text( 
        movie_info, 
        'plugins/moviedb/fonts/wqy-microhei.ttc', 
        movie_info_img_save_path,
        bg_folder = 'plugins/moviedb/bg'
    )

    # retrive and save movie's poster
    movie_poster_save_path = f"{target_folder}/{poster_path}"
    if not os.path.exists(movie_poster_save_path):
        poster_data = requests.get(img_base_url + poster_path).content
        with open(movie_poster_save_path, 'wb') as fp:
            fp.write(poster_data)

    # generate CQ code
    gen_imgs.append(movie_poster_save_path)
    outcome = ''
    for gen_img in gen_imgs:
        outcome = outcome + '[CQ:image,file={}]'.format(
            gen_img.replace(f'{images_dir}/', '')
        )

    return outcome

def search_movie(query, page, language):
    url = base_url + '/search/movie'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': language,
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
                    unspec = '暂无'
                    movie_info = '影名: {} 原名: {} 评分: {}分 id:{} 上映日期:{}'.format(
                        movie.get('title', unspec),
                        movie.get('original_title', unspec),
                        movie.get('vote_average', unspec),
                        movie.get('id', unspec),
                        movie.get('release_date', unspec)
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

def search_tv_maybe(query, language):
    url = base_url + '/search/tv'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': language,
        'page': 1,
        'query': query
    }
    resp = requests.get(url, params=params).json()
    if 'results' in resp.keys():
        tv_list = resp['results']
        if tv_list:
            try:    
                tv = max(tv_list, key=lambda x: x['popularity'])
                tv_id = tv['id']
                outcome = fetch_tv(tv_id, language)
                
            except Exception as err:
                outcome = str(err)
        else:
            outcome = f'未找到与”{query}“相关的电视剧！'
    else:
        outcome = '查找出错啦！'

    return outcome

def fetch_tv(id, language):
    url = base_url + f'/tv/{id}?api_key={tmdb_api_key}&language={language}'
    resp = requests.get(url).json()
    tv_info = '剧名: {}\n原产地剧名: {}\n评分: {}/10\n已播季数: {}季\n已播集数: {}集\n简介: {}\n首播日期: {}\n最近播出日期: {}\n'\
              '类型: {}\n播放平台: {}\n状态: {}\n创作者: {}\n{}'.format(
        resp.get('name'),
        resp.get('original_name'),
        resp.get('vote_average'),
        resp.get('number_of_seasons'),
        resp.get('number_of_episodes'),
        resp.get('overview'),
        resp.get('first_air_date'),
        resp.get('last_air_date'),
        ' '.join(genre.get('name', '') for genre in resp.get('genres')),
        ' '.join(network.get('name', '') for network in resp.get('networks')),
        resp.get('status'),
        ' & '.join(creator.get('name', '') for creator in resp.get('created_by')),
        '\n'.join( f"({season['season_number']}) {season['name']} {season['air_date']} 共{season['episode_count']}集 {season['overview']}" 
                    for season in resp.get('seasons') )
    )
    poster_path = resp.get('poster_path')

    # generate image with informations of a tv
    target_folder = f"{images_dir}/tvs/{id}"
    tv_info_img_save_path = f"{target_folder}/tv_info"
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    gen_imgs = gen_img_with_text( 
        tv_info, 
        'plugins/moviedb/fonts/wqy-microhei.ttc', 
        tv_info_img_save_path,
        bg_folder = 'plugins/moviedb/bg'
    )

    # retrive and save tv's poster
    tv_poster_save_path = f"{target_folder}/{poster_path}"
    if not os.path.exists(tv_poster_save_path):
        poster_data = requests.get(img_base_url + poster_path).content
        with open(tv_poster_save_path, 'wb') as fp:
            fp.write(poster_data)

    # generate CQ code
    gen_imgs.append(tv_poster_save_path)
    outcome = ''
    for gen_img in gen_imgs:
        outcome = outcome + '[CQ:image,file={}]'.format(
            gen_img.replace(f'{images_dir}/', '')
        )

    return outcome

def search_tv(query, page, language):
    url = base_url + '/search/tv'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': language,
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
                    unspec = '暂无'
                    tv_info = '剧名: {} 原名: {} 评分: {}分 id:{} 首播日期:{}'.format(
                        tv.get('name', unspec),
                        tv.get('original_name', unspec),
                        tv.get('vote_average', unspec),
                        tv.get('id', unspec),
                        tv.get('first_air_date', unspec)
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

def search_person(query, page, language):
    url = base_url + '/search/person'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': language,
        'page': page,
        'query': query
    }
    resp = requests.get(url, params=params).json()
    if 'results' in resp.keys():
        persons = resp['results']
        if persons:
            try:
                persons_info = []
                for person in persons:
                    unspec = '暂无'
                    person_info = '{} id: {} 知名领域: {}'.format(
                        person.get('name', unspec),
                        person.get('id', unspec),
                        person.get('known_for_department', unspec)
                    )
                    persons_info.append(person_info)

                target_folder = f"{images_dir}/tmdb_persons"
                results_info_img_save_path = f"{target_folder}/outcome"
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                gen_imgs = gen_img_with_text(
                    '\n'.join(persons_info),
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
            outcome = f'未找到第{page}页与”{query}“相关的人物！'
    else:
        outcome = '查找出错啦！'

    return outcome

def search_multi(query, page, language):
    url = base_url + '/search/multi'
    params = {
        'api_key': tmdb_api_key,
        'include_adult': 'false',
        'language': language,
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
                    if result['media_type'] == 'movie':
                        result_info = '{} [电影] id: {} 评分: {}/10 上映日期: {}'.format(
                            result.get('title'),
                            result.get('id'),
                            result.get('vote_average', '暂无'),
                            result.get('release_date', '暂无')
                        )
                    elif result['media_type'] == 'tv':
                        result_info = '{} [剧集] id: {} 评分: {}/10 首播日期: {}'.format(
                            result.get('name'),
                            result.get('id'),
                            result.get('vote_average', '暂无'),
                            result.get('first_air_date', '暂无')
                        )
                    elif result['media_type'] == 'person':
                        result_info = '{} [人物] id: {} 知名领域: {}'.format(
                            result.get('name'),
                            result.get('id'),
                            result.get('known_for_department')
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


def trending(media_type, time_window, language):
    url = base_url + f'/trending/{media_type}/{time_window}'
    params = {
        'api_key': tmdb_api_key,
        'language': language,
        'page': 1
    }
    resp = requests.get(url, params=params).json()
    media_list = resp.get('results')
    if not media_list:
        return '出错啦~'
    media_list.sort(key=lambda x: x['popularity'], reverse=True)
    
    if media_type == 'all':
        media_map = {
            'movie': ('title', '电影'),
            'tv': ('name', '剧集'),
            'person': ('name', '人物')
        }
        medias_info = '\n'.join(f"{media[media_map[media['media_type']][0]]}  [{media_map[media['media_type']][1]}] id:{media['id']}" 
                        for media in media_list)
    elif media_type == 'movie':
        medias_info = '\n'.join(f"{media['title']} {media['vote_average']}分 {media['release_date']} id:{media['id']}"
                        for media in media_list)
    elif media_type == 'tv':
        medias_info = '\n'.join(f"{media['name']} {media['vote_average']}分 {media['first_air_date']} id:{media['id']}"
                        for media in media_list)
    elif media_type == 'person':
        medias_info = '\n'.join(f"{media['name']} {media['known_for_department']} id:{media['id']}"
                        for media in media_list)

    target_folder = f'{images_dir}/tmdb_trending'
    medias_info_img_save_path = f"{target_folder}/outcome"
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    gen_imgs = gen_img_with_text(
        medias_info,
        'plugins/moviedb/fonts/wqy-microhei.ttc',
        medias_info_img_save_path,
        bg_folder = 'plugins/moviedb/bg'
    )

    tw_map = {
        'day': '24小时内',
        'week': '一周内'
    }
    outcome = f'{tw_map[time_window]}排行榜\n'
    for gen_img in gen_imgs:
        outcome = outcome + '[CQ:image,file={}]'.format(
            gen_img.replace(f'{images_dir}/', '')
        )

    return outcome


if __name__ == '__main__':
    pass