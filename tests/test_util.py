# -*- coding: utf-8 -*-
def test_logfmt():
    from tap.util import logfmt
    props = {
        'body': '{"id":"cus_l4YZ3720191021y7Q42002681","object":"customer","live_mode":true,"created":"1550658097743","first_name":"Ø¥Ø´ØªÙØ§Ù","last_name":"Ø¥Ø´ØªÙØ§Ù","email":"bshoor.rose@gmail.com"}',
        'message': 'API response body'
    }
    logged = logfmt(props)
    "Ø¥Ø´ØªÙØ§Ù".decode('utf-8') in logged
