from PIL import Image
import requests
from io import BytesIO
from math import floor, ceil
from obs import ObsClient
from datetime import datetime

MAX_WIDTH = 1500
MAX_HEIGHT = 1500
TARGET_WIDTH = 800
OBS_ACCESS_KEY_ID = 'EULIXLKJQLUS62GPNIAX'
OBS_SECRET_ACCESS_KEY = 'vmoTDJVUOXVtwt8pwh5LQ6LnE2bJPDtxid7biimK'
OBS_SERVER = 'https://obs.cn-south-1.myhuaweicloud.com'


def make_a_poster(image_urls):
    # 获取合并后的图片
    image_url = get_merge_photo(image_urls)

    # 提示词
    prompt_text = f"""
    你是一个UI设计师，现在给你一张图，请你根据图片的信息，生成一个AI改成海报图的提示语，原图人物保持不变，在人物基础上加上边框，文字，图案，元素等海报,只需返回json格式数据{{"prompt":"提示语"}}
    """

    # 获取海报提示词
    poster_content = convert_to_fashion_image(image_url, prompt_text)

    # 生成海报图
    return get_poster(image_url, poster_content)


def generate_unique_file_name(current_date):
    """
    生成唯一的图片文件名后缀
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    return f"{current_date}_{timestamp}.png"


def upload_to_oss_sync(image) -> str:
    """
    上传图片到华为云
    """
    obsClient = ObsClient(
        access_key_id=OBS_ACCESS_KEY_ID,
        secret_access_key=OBS_SECRET_ACCESS_KEY,
        server=OBS_SERVER
    )
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)

    bucket_name = "yishou-img"
    current_date = datetime.now().strftime("%Y%m%d")
    object_key = f"yishou_tqsx_img/new_goods_monitor/picture/gce/{current_date}/{generate_unique_file_name(current_date)}"

    resp = obsClient.putContent(bucket_name, object_key, buffer)
    if resp.status < 300:
        image_url = f'https://yishou-img.obs.cn-south-1.myhuaweicloud.com/{object_key}'
        return image_url
    else:
        raise Exception(f"上传失败，状态码: {resp.status}")


def get_merge_photo(image_urls):
    """
    获取合并后的图片
    """
    images_cut = []

    # 裁剪图片
    for url in image_urls:
        data = {
            "image_url": url,
            "threshold": 0.3,
            "classes": ["person", "clothes"]
        }
        try:
            ret = requests.post("http://14.103.147.199:5156/detect", json=data, timeout=10)
            result = ret.json()
        except Exception as e:
            print(f"人体和服装区域识别失败: {e}")
            continue

        try:
            response = requests.get(url, timeout=10)
            img = Image.open(BytesIO(response.content)).convert("RGB")
        except Exception as e:
            print(f"图片下载失败: {e}")
            continue

        if result.get("status") == "success" and result.get("detections"):
            box = result["detections"][0]["bbox"]
        else:
            box = [0.0, 0.0, float(img.width), float(img.height)]

        x1 = max(0, floor(box[0]))
        y1 = max(0, floor(box[1]))
        x2 = min(img.width, ceil(box[2]))
        y2 = min(img.height, ceil(box[3]))

        cropped = img.crop((x1, y1, x2, y2))

        # 等比缩放
        width, height = cropped.size
        if width > MAX_WIDTH or height > MAX_HEIGHT:
            scale_w = TARGET_WIDTH / width
            scale_h = MAX_HEIGHT / height
            scale = min(scale_w, scale_h)
            new_w = int(width * scale)
            new_h = int(height * scale)
            cropped = cropped.resize((new_w, new_h), Image.ANTIALIAS)

        images_cut.append(cropped)

    # 拼接图片
    total_width = sum(img.width for img in images_cut)
    max_height = max(img.height for img in images_cut)

    merged_img = Image.new("RGB", (total_width, max_height))

    x_offset = 0
    for img in images_cut:
        merged_img.paste(img, (x_offset, 0))
        x_offset += img.width

    return upload_to_oss_sync(merged_img)


def convert_to_fashion_image(image_url, prompt_text):
    headers = {
        "Authorization": f"Bearer yishouai-etkwNXgrCSe2vUopO7bT1PzalwuJceSN2MomBoeKF6xfGxBYKlUdWRT",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-image-1",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant specialized in image processing."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt_text},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ]
    }
    response = requests.post("https://aipre.yishouapp.com/api/v1/chat/completions", headers=headers, json=data)
    ret = response.json()
    return ret['choices'][0]['message']['content']


def get_poster(image_url, prompt_text):
    """
    最终的生成海报图
    """
    try:
        data = {
            "image_url": image_url,
            "prompt_text": prompt_text,
            "use_image_size_1": True,
            "use_image_size_2": True,
            "width": 800,
            "height": 800
        }
        response = requests.post("http://14.103.147.199:5128/process", json=data, timeout=600)

        if response.status_code == 200:
            result = response.json()
            return result['result_url']
        else:
            raise Exception(f"生成海报图失败，状态码: {response.status_code}")

    except requests.exceptions.ConnectionError:
        raise Exception("最终的生成海报图连接失败!")
    except Exception as e:
        raise Exception(f"最终的生成海报图请求出错: {str(e)}")


if __name__ == '__main__':
    test_image_urls = [
        "https://img4.yishouapp.com/obs/baob/75f3f3e8a4a0bf3ca551e88933e88bdc.jpeg",
        "https://img4.yishouapp.com/obs/baob/f6f6c6ccad9743814968e47bd0b64065.jpeg",
        "https://img4.yishouapp.com/obs/baob/01970aca1095d6d0528102f580bd6bca.jpeg"
    ]

    url = make_a_poster(test_image_urls)
    print(url)
