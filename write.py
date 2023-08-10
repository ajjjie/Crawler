from genshin1 import GenshinCrawlerOfficial
from genshin2 import GenshinCrawlerWiki
import os

save_path = 'outputs'
crawler1 = GenshinCrawlerOfficial()
crawler2 = GenshinCrawlerWiki()
all_place_infos = crawler1.place_data
all_char_infos = crawler2._get_char_infos()


if not os.path.exists(save_path):
    os.makedirs(save_path)
for country, char_infos in all_char_infos.items():
    if not all_place_infos.get(country):
        continue
    char_infos.sort(key=lambda x:x.info['实装日期'])
    place_infos = all_place_infos[country]
    path = f'{save_path}/{country}.md'
    with open(path, 'w', encoding='utf-8') as f:
        # f.write(f'# 国家：{country}\n')
        f.write(f'## {country}地理介绍\n{place_infos[country]}')
        for place, info in place_infos.items():
            if place==country:
                continue
            f.write(f'### {country}地点{place}介绍：{info}\n')
        f.write(f'\n## {country}角色介绍，共有{len(char_infos)}个角色')
        for i, info in enumerate(char_infos):
            f.write(f'\n### {country}第{i+1}个角色：{info.name}')
            # f.write(f'\n#### {info.name}基本信息')
            for i in range(len(info.info)):
                f.write(f'\n#### {info.name}{info.info.index[i]}：{info.info[i]}')
            # f.write(f'#### {info.name}攻略')
            for i in range(len(info.rec)):
                if i==0:
                    f.write(f'\n##### {info.name}圣遗物')
                elif i==6:
                    f.write(f'\n##### {info.name}武器')
                f.write(f'{info.rec.index[i]}:{info.rec[i]}')
            f.write(f'\n#### {info.name}背景故事：')
            f.write(info.bg + '\n')