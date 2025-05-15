import requests
from typing import Tuple, Union
from requests.exceptions import RequestException, JSONDecodeError

def fofa_search_resource(api_key: str) -> Union[str, Tuple[str, int]]:
    """查询FOFA账户资源信息
    
    Args:
        api_key: FOFA API密钥
        
    Returns:
        Union[str, Tuple[str, int]]: 成功返回格式化字符串，失败返回错误信息和状态码
        
    Raises:
        RequestException: 网络请求相关异常
    """
    base_url = "https://fofa.info/api/v1/info/my"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        # 更安全的参数传递方式
        resp = requests.get(
            url=base_url,
            params={"key": api_key},
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()  # 自动处理4xx/5xx错误
        
        data = resp.json()
        
        # 更准确的错误判断
        if data.get("error", False):
            error_msg = data.get("errmsg", "Unknown error")
            return (f"[!] API Error: {error_msg}", resp.status_code)
            
        # 更安全的键值获取
        vip_level = data.get("vip_level", "N/A")
        is_vip = "Yes" if data.get("isvip", False) else "No"
        is_verified = "Yes" if data.get("is_verified", False) else "No"
        
        # 更易读的格式化输出
        result = f"""
        ======== FOFA 账户信息 ========
        [*] Email:     {data.get('email', 'N/A')}
        [*] Username: {data.get('username', 'N/A')}
        [*] Fcoin:    {data.get('fcoin', 0)}
        [*] VIP:      {is_vip}
        [*] VIP等级:   {vip_level}
        [*] 已验证:    {is_verified}
        [*] 头像地址:  {data.get('avatar', 'N/A')}
        ==============================
        """
        return result
        
    except RequestException as e:
        return (f"[!] 网络请求失败: {str(e)}", getattr(e.response, 'status_code', 500))
    except JSONDecodeError:
        return ("[!] 无效的API响应格式", 500)
    except KeyError as e:
        return (f"[!] 缺失关键响应字段: {str(e)}", 500)
    except Exception as e:
        return (f"[!] 未知错误: {str(e)}", 500)