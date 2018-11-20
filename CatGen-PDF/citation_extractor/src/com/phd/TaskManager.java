package com.phd;

import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;

public class TaskManager {

    private static final TaskManager instance = new TaskManager();
    public static TaskManager getInstance() {
        return instance;
    }

    private Timer timer = new Timer();

    private void reGenerateProxyList() throws IOException, InterruptedException {

        ProxyUtil.generateProxyList(new proxyCallback(){
            @Override
            public void onSuccess() throws IOException, InterruptedException {
                //System.out.println("re-generating of ProxyList is done");

                //clear all existed random numbers
                RandomUtil.getInstance().clearExistedRandomList();
            }

            @Override
            public void onError(String err) {
                // error happen
                System.out.println(err);
            }
        });
    }

    void start() {

        int MINUTES = 2;

        timer.schedule(new TimerTask() {
            @Override
            public void run() { // Function runs every MINUTES minutes.
                try {
                    reGenerateProxyList();
                } catch (IOException e) {
                    e.printStackTrace();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, 0, 1000 * 60 * MINUTES);
    }

    void stop() {
      //  timer.cancel();
      //  timer.purge();
    }

}
