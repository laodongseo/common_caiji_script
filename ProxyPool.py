class ProxyPool():

    def __init__(self, orderid, proxy_count,sleep_seconds=40):
        self.orderid = orderid
        self.proxy_count = proxy_count if proxy_count < 50 else 50 # 池子维护的ip总数
        self.alive_proxy_list = self._fetch_proxy_list(self.proxy_count)  # 初始化ip列表
        self.sleep_seconds = sleep_seconds # 请求接口ip的时间间隔


    def _fetch_proxy_list(self, count):
        """调用接口获取代理ip列表"""
        try:
            res = requests.get("http://dps.kdlapi.com/api/getdps/?orderid=%s&num=%s&pt=1&sep=1&f_et=1&format=json" % (self.orderid, count))
            return [proxy.split(',') for proxy in res.json().get('data').get('proxy_list')]
        except:
            print("API获取ip异常，请检查订单")
        return []


    def _update_proxy(self,proxy_list):
        """对比现有ip池和新请求的ip,更新ip池"""
        invalid_proxy_list = set(self.alive_proxy_list) - set(proxy_list)
        add_proxy_list = list(set(proxy_list) - set(alive_proxy_list))
        self.alive_proxy_list.remove(invalid_proxy_list)
        self.alive_proxy_list.extend(add_proxy_list)
        if len(self.alive_proxy_list) > 50:
                self.alive_proxy_list = self.alive_proxy_list[0:50]


    def get_proxy(self):
        """从ip池中获取ip"""
        return random.choice(self.alive_proxy_list) if self.alive_proxy_list else ""


    def run(self):
        while True:
            proxy_list = self._fetch_proxy_list(self.proxy_count)
            self._update_proxy(proxy_list)
            time.sleep(self.sleep_seconds)


    def start(self):
        """开启子线程更新ip池"""
        t = threading.Thread(target=self.run)
        t.setDaemon(True)  # 设为守护进程，
        t.start()


if __name__ == '__main__':
    proxy_pool = ProxyPool('9266892014xxxxx',30,40) # 订单号, 池子中维护的ip数,接口请求间隔
    proxy_pool.start()
    time.sleep(1)  # 等待ip池初始化

    proxy = proxy_pool.get_proxy() # 从ip池中提取ip
    if proxy:
        get_html(proxy)
