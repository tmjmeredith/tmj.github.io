import os
import random
from datetime import datetime

# 定義文章類別對應的頁面
CATEGORY_PAGES = {
    1: "blogpage1.html",
    2: "blogpage2.html",
    3: "blogpage3.html",
    4: "blogpage4.html"
}

CATEGORY_NAMES = {
    1: "玄學",
    2: "AI產物",
    3: "大學科目",
    4: "證照"
}

# 讀取 blog1.html 作為文章模板
def load_article_template():
    with open('blog1.html', 'r', encoding='utf-8') as f:
        return f.read()

# 創建文章縮圖的 HTML 模板
THUMBNAIL_TEMPLATE = """
<article class="bg-gray-800/50 rounded-lg p-6 hover:bg-gray-800/70 transition-colors">
    <a href="https://tmjmeredith.github.io/tmj.github.io/web2/{article_filename}" class="block">
        <h3 class="text-2xl font-semibold mb-4">{title}</h3>
        <p class="text-gray-400 mb-4">{excerpt}</p>
        <div class="flex items-center text-sm text-gray-500">
            <span>{date}</span>
            <span class="mx-2">•</span>
            <span>{category}</span>
        </div>
    </a>
</article>
"""

def get_next_article_number():
    # 獲取當前目錄下所有以 blog 開頭的文件，並找出最大數字
    files = [f for f in os.listdir('.') if f.startswith('blog') and f.endswith('.html')]
    numbers = [int(f[4:-5]) for f in files if f[4:-5].isdigit()]
    return max(numbers) + 1 if numbers else 1

def create_article(title, category, date, content, excerpt):
    # 檢查類別是否有效
    if category not in CATEGORY_PAGES:
        raise ValueError("Invalid category")

    # 加載文章模板
    article_template = load_article_template()

    # 獲取下一個文章編號
    article_number = get_next_article_number()
    article_filename = f"blog{article_number}.html"

    # 創建文章 HTML 文件
    with open(article_filename, 'w', encoding='utf-8') as f:
        # 使用 HTML 格式的內容
        article_content = article_template.format(title=title, category=CATEGORY_NAMES[category], date=date, content=content)
        f.write(article_content)

    # 創建縮圖並添加到相應的分類頁面
    thumbnail_html = THUMBNAIL_TEMPLATE.format(
        title=title,
        excerpt=excerpt,
        date=date,
        category=CATEGORY_NAMES[category],
        article_filename=article_filename
    )
    category_page = CATEGORY_PAGES[category]
    with open(category_page, 'r+', encoding='utf-8') as f:
        page_content = f.read()
        # 找到文章列表的結束標記，然後插入縮圖
        insert_position = page_content.rfind('</div>\n    </div>\n</main>')
        if insert_position != -1:
            new_content = page_content[:insert_position] + thumbnail_html + page_content[insert_position:]
            f.seek(0)
            f.write(new_content)
            f.truncate()

    # 隨機插入到 blogpage.html
    insert_randomly_into_blogpage(thumbnail_html)

    # 隨機插入到 index.html
    insert_randomly_into_index(thumbnail_html)

def insert_randomly_into_blogpage(thumbnail_html):
    blogpage_file = "blogpage.html"
    with open(blogpage_file, 'r+', encoding='utf-8') as f:
        page_content = f.read()
        # 找到文章列表的結束標記
        insert_position = page_content.rfind('</div>\n    </div>\n</main>')
        if insert_position != -1:
            # 隨機選擇插入位置
            random_position = random.randint(0, insert_position)
            new_content = page_content[:random_position] + thumbnail_html + page_content[random_position:]
            f.seek(0)
            f.write(new_content)
            f.truncate()

def insert_randomly_into_index(thumbnail_html):
    index_file = "index.html"
    with open(index_file, 'r+', encoding='utf-8') as f:
        page_content = f.read()
        # 找到第一個插入位置
        first_insert_position = page_content.find('<p class="text-gray-400 mt-2">探討總體經濟理論重要概念與應用解析。</p>')
        # 找到第二個插入位置
        second_insert_position = page_content.find('<article class="hover:bg-gray-700/50 p-4 rounded-lg transition-colors duration-300">\n                                <h3 class="text-lg font-semibold text-white">簡單六爻卜卦</h3>\n                                <p class="text-gray-400 mt-2">易經六爻卜卦的基礎入門與實踐應用。</p>\n                            </article>')
        
        if first_insert_position != -1:
            # 隨機選擇一個位置插入
            if random.choice([True, False]):
                new_content = page_content[:first_insert_position] + thumbnail_html + page_content[first_insert_position:]
            else:
                new_content = page_content[:second_insert_position] + thumbnail_html + page_content[second_insert_position:]
            
            f.seek(0)
            f.write(new_content)
            f.truncate()

def main():
    # 輸入標題
    title = input("請輸入標題: ")

    # 輸入類別
    print("請輸入類別: 1代表玄學，2代表AI產物，3代表大學科目，4代表證照")
    category = int(input("請輸入類別編號: "))

    # 輸入文章內容
    content = input("請輸入文章內容: ")

    # 自動生成當前日期
    date = datetime.now().strftime("%Y-%m-%d")

    # 使用文章內容的前100個字作為摘要
    excerpt = content[:100] + "..." if len(content) > 100 else content

    # 創建文章
    create_article(title, category, date, content, excerpt)

if __name__ == "__main__":
    main()