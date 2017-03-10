class AliPay:
    """
    alipay的Python sdk
    主要做统一收单方面的sdk
    第一步完成统一收单预创建
    """
    def __init__(self, timestamp, notify_url, biz_content, sign_type='RSA2'):
        """
        有三个参数是必须的 timestamp  notify_url biz_content
        """

        #### -------start-------- 必须需要传入的参数 ------start-------- ####
        self.timestamp = timestamp
        self.notify_url = notify_url
        self.biz_content = biz_content
        #### -------end-------- 必须需要传入的参数 ------end-------- ####

        #### -------start-------- 配置参数 -------start-------- ####
        # 支付宝分配给开发者的应用ID
        self._APP_ID = ''
        # 应用公钥路径, 暂未用到
        self._APP_PUBLIC = ''
        # 应用私钥路径
        self._APP_PRIVATE = ''
        # 支付宝公钥路径
        self._ALI_PUBLIC = ''
        #### -------end-------- 配置参数 ------end-------- ####

        #### -------start-------- 固定参数 -------start-------- ####
        # 支付宝网关接口
        self.AliGateway = 'https://openapi.alipay.com/gateway.do'
        # 格式化字符串方式 官方只支持json
        self.format = 'json'
        # 编码方式，官方支持gbk utf8  本sdk使用utf-8
        self.charset = 'utf-8'
        # 版本号  官方只有1.0
        self.version = '1.0'
        #### -------end-------- 固定参数 -------end-------- ####

        # 签名方式 可选RSA2和RSA，官方推荐RSA2
        self.sign_type = sign_type
        # 请求方式, 比如统一收单预创建接口就是 alipay.trade.precreate
        self.method = ''

    ### -------start--------以下的参数涉及到安全，通过@property设置为只读属性-------start-------- ####
    @property
    def APP_ID(self):
        return self._APP_ID

    @property
    def APP_PUBLIC(self):
        return self._APP_PUBLIC

    @property
    def APP_PRIVATE(self):
        return self._APP_PRIVATE

    @property
    def ALI_PUBLIC(self):
        return self._ALI_PUBLIC
    ### -------end-------- 参数涉及到安全，通过@property设置为只读属性 -------end-------- ####

    ### -------start-------- 提供返回配置文件信息的方法，自行继承实现配置文件还是数据库存 -------start-------- ####
    def SET_APP_ID(self):
        pass

    def SET_APP_PUBLIC(self):
        pass

    def SET_APP_PRIVATE(self):
        pass

    def SET_ALI_PUBLIC(self):
        pass
    ### -------end-------- 提供返回配置文件信息的方法，自行继承实现配置文件还是数据库存 -------end-------- ####


    def creart_trade_precreate(self, out_trade_no, seller_id='', total_amount, subject, body, timeout_express):
        pass
