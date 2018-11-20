package com.phd;


import java.io.IOException;

public interface proxyCallback {

    void onSuccess() throws IOException, InterruptedException;
    void onError(String err);
}