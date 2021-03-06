# coding=utf-8
import unittest
import requests
from time import time
import hashlib


class AddEventTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_add_event/"
        # app_key
        self.api_key = "&Guest-Bugmaster"
        # 当前时间
        now_time = time()
        self.client_time = str(now_time).split('.')[0]
        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def test_add_event_sign_null(self):
        ''' sign=null 签名参数为空 '''
        now_time = str(int(self.client_time))
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'','time':now_time,'sign':''}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10012)
        self.assertEqual(result['message'], 'user sign null')

    def test_add_event_sign_error(self):
        ''' sign='error' 签名参数错误 '''
        now_time = str(int(self.client_time))
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'','time':now_time,'sign':'error'}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10014)
        self.assertEqual(result['message'], 'user sign error')

    def test_add_event_sign_timeout(self):
        ''' 签名参数超时 '''
        now_time = str(int(self.client_time) - 61)
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'','time':now_time,'sign':'error'}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10013)
        self.assertEqual(result['message'], 'user sign timeout')

    def test_add_event_sign_ok(self):
        ''' 签名参数正确 '''
        now_time = str(int(self.client_time))
        payload = {'eid':1,'':'','limit':'','address':'','start_time':'','time':now_time,'sign':self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

if __name__ == '__main__':
    unittest.main()
