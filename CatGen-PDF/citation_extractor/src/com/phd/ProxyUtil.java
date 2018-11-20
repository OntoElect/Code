package com.phd;

import java.io.IOException;
import java.util.List;

public class ProxyUtil {

    static List<CPProxy> CPProxyList;

    public static void generateProxyList(proxyCallback callback) throws IOException, InterruptedException {

        ApiProxy apiProxy = new ApiProxy();
        List<CPProxy> res = apiProxy.getProxyList();

        CPProxyList = res;
        callback.onSuccess();
    }
}