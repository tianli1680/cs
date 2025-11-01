import requests
import re
import os
import sys

def extract_m3u_groups():
    # 从环境变量获取URL
    m3u_url = os.getenv('M3U_URL')
    if not m3u_url:
        print("Error: M3U_URL environment variable not set")
        sys.exit(1)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"Fetching URL: {m3u_url}")
        response = requests.get(m3u_url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        content = response.text
        
        if not content:
            print('Error: Empty response')
            sys.exit(1)
            
        print(f'Downloaded content length: {len(content)}')
        
        # 简单的分组检测 - 根据实际M3U格式调整
        lines = content.split('\n')
        groups = []
        current_group = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF'):
                # 如果当前组不为空，保存前一个组
                if current_group:
                    groups.append('\n'.join(current_group))
                    current_group = []
                current_group.append(line)
            elif line and not line.startswith('#EXTM3U'):
                current_group.append(line)
        
        # 添加最后一个分组
        if current_group:
            groups.append('\n'.join(current_group))
        
        print(f'Found {len(groups)} channel groups')
        
        # 为每个分组创建文件
        for i, group_content in enumerate(groups, 1):
            filename = f'live{i}.m3u'
            full_content = '#EXTM3U\n' + group_content
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            print(f'Created {filename}')
            
        return len(groups)
        
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    extract_m3u_groups()
